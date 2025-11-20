"""
Módulo de integração com APIs do Google (Sheets, Calendar, Meet).
"""
import os.path
import pandas as pd
from typing import Dict, List, Optional
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.apps import meet_v2
from googleapiclient.discovery import build
import gspread
from google.oauth2.credentials import Credentials as OAuthCredentials

from config import SCOPES, TOKEN_FILE, CREDENTIALS_FILE


class GoogleIntegration:
    """Classe para integração com APIs do Google."""
    
    def __init__(self):
        self.creds = None
        self.meet_client = None
        self.sheets_service = None
        self.calendar_service = None
        self._authenticate()
    
    def _authenticate(self):
        """Autentica com as APIs do Google usando token.json existente."""
        # Carrega credenciais existentes
        if os.path.exists(TOKEN_FILE):
            try:
                self.creds = Credentials.from_authorized_user_file(TOKEN_FILE, SCOPES)
                
                # Verifica se o token tem todos os scopes necessários
                if self.creds and self.creds.valid:
                    token_scopes = set(self.creds.scopes or [])
                    required_scopes = set(SCOPES)
                    if not required_scopes.issubset(token_scopes):
                        # Token não tem todos os scopes necessários, força reautenticação
                        print(f"⚠️ Token não tem todos os scopes necessários. Reautenticando...")
                        print(f"   Scopes necessários: {required_scopes}")
                        print(f"   Scopes no token: {token_scopes}")
                        self.creds = None
            except Exception as e:
                print(f"⚠️ Erro ao carregar token: {e}. Reautenticando...")
                self.creds = None
        
        # Se não há credenciais válidas, solicita autenticação
        if not self.creds or not self.creds.valid:
            if self.creds and self.creds.expired and self.creds.refresh_token:
                try:
                    self.creds.refresh(Request())
                except Exception as e:
                    print(f"⚠️ Erro ao renovar token: {e}. Reautenticando...")
                    self.creds = None
            
            if not self.creds or not self.creds.valid:
                if not os.path.exists(CREDENTIALS_FILE):
                    raise FileNotFoundError(
                        f"Arquivo credentials.json não encontrado em {CREDENTIALS_FILE}. "
                        "Por favor, baixe as credenciais OAuth2 do Google Cloud Console."
                    )
                print("🔐 Autenticando com Google...")
                print("   Por favor, autorize o acesso no navegador que será aberto.")
                flow = InstalledAppFlow.from_client_secrets_file(
                    CREDENTIALS_FILE, SCOPES)
                self.creds = flow.run_local_server(port=0)
            
            # Salva as credenciais atualizadas
            with open(TOKEN_FILE, 'w') as token:
                token.write(self.creds.to_json())
            print("✅ Autenticação concluída!")
        
        # Inicializa clientes das APIs
        self.meet_client = meet_v2.SpacesServiceClient(credentials=self.creds)
        self.sheets_service = build('sheets', 'v4', credentials=self.creds)
        self.calendar_service = build('calendar', 'v3', credentials=self.creds)
    
    def ler_planilha_por_id(self, spreadsheet_id: str, worksheet_name: str = None) -> pd.DataFrame:
        """
        Lê dados de uma planilha Google Sheets.
        
        Args:
            spreadsheet_id: ID da planilha Google Sheets (pode ser URL completa ou apenas o ID)
            worksheet_name: Nome da aba (None para primeira aba)
            
        Returns:
            DataFrame com os dados da planilha
        """
        try:
            # Extrai o ID da planilha se uma URL foi fornecida
            if 'docs.google.com' in spreadsheet_id or 'spreadsheets/d/' in spreadsheet_id:
                # Extrai o ID da URL
                if '/d/' in spreadsheet_id:
                    spreadsheet_id = spreadsheet_id.split('/d/')[1].split('/')[0]
                elif 'id=' in spreadsheet_id:
                    spreadsheet_id = spreadsheet_id.split('id=')[1].split('&')[0]
            
            sheet = self.sheets_service.spreadsheets()
            
            # Se não especificou aba, pega a primeira
            if worksheet_name is None:
                spreadsheet = sheet.get(spreadsheetId=spreadsheet_id).execute()
                worksheet_name = spreadsheet['sheets'][0]['properties']['title']
            
            result = sheet.values().get(
                spreadsheetId=spreadsheet_id,
                range=worksheet_name
            ).execute()
            
            values = result.get('values', [])
            
            if not values:
                return pd.DataFrame()
            
            # Primeira linha como cabeçalho
            headers = values[0]
            data = values[1:] if len(values) > 1 else []
            
            # Garante que todas as linhas tenham o mesmo número de colunas
            max_cols = len(headers)
            normalized_data = []
            for row in data:
                normalized_row = row + [''] * (max_cols - len(row))
                normalized_data.append(normalized_row[:max_cols])
            
            df = pd.DataFrame(normalized_data, columns=headers)
            
            # Normaliza nomes das colunas (lowercase, sem espaços)
            df.columns = df.columns.str.strip().str.lower()
            
            return df
            
        except Exception as e:
            error_msg = str(e)
            # Detecta erro de scope insuficiente
            if 'insufficient authentication scopes' in error_msg or 'ACCESS_TOKEN_SCOPE_INSUFFICIENT' in error_msg:
                raise Exception(
                    f"Erro de autenticação: O token não tem permissões suficientes para acessar o Google Sheets.\n"
                    f"Por favor, delete o arquivo token.json e execute o dashboard novamente para reautenticar com os scopes corretos.\n"
                    f"Erro original: {error_msg}"
                )
            raise Exception(f"Erro ao ler planilha: {error_msg}")
    
    def ler_planilha_gspread(self, spreadsheet_id: str, worksheet_index: int = 0) -> pd.DataFrame:
        """
        Lê planilha usando gspread (alternativa).
        
        Args:
            spreadsheet_id: ID da planilha Google Sheets
            worksheet_index: Índice da aba (0 para primeira)
            
        Returns:
            DataFrame com os dados da planilha
        """
        try:
            # Converte credenciais OAuth2 para formato gspread
            gc = gspread.authorize(self.creds)
            sh = gc.open_by_key(spreadsheet_id)
            worksheet = sh.get_worksheet(worksheet_index)
            
            # Pega todos os dados
            data = worksheet.get_all_records()
            df = pd.DataFrame(data)
            
            # Normaliza nomes das colunas
            df.columns = df.columns.str.strip().str.lower()
            
            return df
            
        except Exception as e:
            raise Exception(f"Erro ao ler planilha com gspread: {str(e)}")
    
    def obter_eventos_calendario(self, calendar_id: str = 'primary', max_results: int = 10) -> List[Dict]:
        """
        Obtém eventos do Google Calendar.
        
        Args:
            calendar_id: ID do calendário ('primary' para calendário principal)
            max_results: Número máximo de resultados
            
        Returns:
            Lista de eventos
        """
        try:
            from datetime import datetime, timedelta
            
            now = datetime.utcnow().isoformat() + 'Z'
            time_max = (datetime.utcnow() + timedelta(days=7)).isoformat() + 'Z'
            
            events_result = self.calendar_service.events().list(
                calendarId=calendar_id,
                timeMin=now,
                timeMax=time_max,
                maxResults=max_results,
                singleEvents=True,
                orderBy='startTime'
            ).execute()
            
            events = events_result.get('items', [])
            
            return events
            
        except Exception as e:
            raise Exception(f"Erro ao obter eventos do calendário: {str(e)}")
    
    def obter_link_meet_do_evento(self, event: Dict) -> Optional[str]:
        """
        Extrai link do Google Meet de um evento do Calendar.
        
        Args:
            event: Dicionário do evento do Calendar
            
        Returns:
            Link do Meet ou None
        """
        # Tenta obter do campo conferenceData
        if 'conferenceData' in event:
            entry_points = event['conferenceData'].get('entryPoints', [])
            for entry in entry_points:
                if entry.get('entryPointType') == 'video':
                    return entry.get('uri')
        
        # Tenta obter do campo hangoutLink (legado)
        if 'hangoutLink' in event:
            return event['hangoutLink']
        
        return None
    
    def listar_participantes_meet(self, meeting_code: str) -> List[Dict]:
        """
        Lista participantes de uma reunião do Google Meet.
        
        Args:
            meeting_code: Código ou URI da reunião Meet
            
        Returns:
            Lista de participantes com informações (nome, email, etc.)
        """
        try:
            # Nota: A API do Google Meet v2 tem limitações para listar participantes
            # Em produção, pode ser necessário usar outras abordagens
            
            # Para breakout rooms, pode ser necessário usar a API de Reports
            # ou outras APIs administrativas do Google Workspace
            
            # Por enquanto, retorna estrutura vazia - será implementado conforme
            # disponibilidade da API
            participants = []
            
            # TODO: Implementar quando a API permitir acesso a participantes
            # de breakout rooms em tempo real
            
            return participants
            
        except Exception as e:
            raise Exception(f"Erro ao listar participantes: {str(e)}")
    
    def criar_espaco_meet(self) -> str:
        """
        Cria um novo espaço (reunião) no Google Meet.
        
        Returns:
            URI da reunião criada
        """
        try:
            request = meet_v2.CreateSpaceRequest()
            response = self.meet_client.create_space(request=request)
            return response.meeting_uri
        except Exception as e:
            raise Exception(f"Erro ao criar espaço Meet: {str(e)}")

