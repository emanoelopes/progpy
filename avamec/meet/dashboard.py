"""
Dashboard Streamlit para monitoramento em tempo real das salas temáticas.
"""
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
import time
from typing import Optional

from config import (
    SPREADSHEET_ID, DASHBOARD_REFRESH_INTERVAL, NUM_GRUPOS, TURMAS,
    OLLAMA_BASE_URL, OLLAMA_MODEL
)
from google_integration import GoogleIntegration
from monitor import MonitorSalas
from agente_ia import AgenteIA


# Configuração da página
st.set_page_config(
    page_title="Monitor de Salas Temáticas - Google Meet",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Inicialização de sessão
if 'google_integration' not in st.session_state:
    st.session_state.google_integration = None
if 'monitor' not in st.session_state:
    st.session_state.monitor = None
if 'agente_ia' not in st.session_state:
    st.session_state.agente_ia = None
if 'dados_carregados' not in st.session_state:
    st.session_state.dados_carregados = False
if 'ultima_atualizacao' not in st.session_state:
    st.session_state.ultima_atualizacao = None


def inicializar_servicos():
    """Inicializa serviços do Google e agente IA."""
    if st.session_state.google_integration is None:
        try:
            with st.spinner("Conectando com Google APIs..."):
                st.session_state.google_integration = GoogleIntegration()
                st.session_state.agente_ia = AgenteIA(
                    base_url=OLLAMA_BASE_URL,
                    model=OLLAMA_MODEL
                )
            st.success("✅ Conectado com sucesso!")
        except FileNotFoundError as e:
            st.error(f"❌ {str(e)}")
            st.info("💡 Dica: Baixe o arquivo credentials.json do Google Cloud Console e coloque no diretório meet/")
            st.stop()
        except Exception as e:
            error_msg = str(e)
            if 'insufficient authentication scopes' in error_msg.lower() or 'scope' in error_msg.lower():
                st.error("❌ Erro de autenticação: Permissões insuficientes")
                st.warning("""
                **Solução:**
                1. Delete o arquivo `token.json` no diretório meet/
                2. Clique novamente em "Conectar Google APIs"
                3. Autorize todos os scopes solicitados no navegador
                """)
                if st.button("🗑️ Deletar token.json e reautenticar"):
                    import os
                    token_path = os.path.join(os.path.dirname(__file__), 'token.json')
                    if os.path.exists(token_path):
                        os.remove(token_path)
                        st.session_state.google_integration = None
                        st.rerun()
            else:
                st.error(f"❌ Erro ao conectar: {error_msg}")
            st.stop()


def carregar_dados_planilha(spreadsheet_id: str, worksheet_name: Optional[str] = None):
    """Carrega dados da planilha Google Sheets."""
    try:
        with st.spinner("Carregando dados da planilha..."):
            df = st.session_state.google_integration.ler_planilha_por_id(
                spreadsheet_id, worksheet_name
            )
            
            if df.empty:
                st.error("Planilha vazia ou não encontrada.")
                return False
            
            # Cria monitor
            st.session_state.monitor = MonitorSalas(df)
            st.session_state.dados_carregados = True
            st.session_state.ultima_atualizacao = datetime.now()
            
            st.success(f"✅ Dados carregados: {len(df)} registros")
            return True
            
    except Exception as e:
        error_msg = str(e)
        st.error(f"❌ Erro ao carregar planilha: {error_msg}")
        
        # Detecta erro de scope insuficiente
        if 'insufficient authentication scopes' in error_msg.lower() or 'ACCESS_TOKEN_SCOPE_INSUFFICIENT' in error_msg:
            st.warning("""
            **Erro de Permissões:**
            
            O token de autenticação não tem permissões suficientes para acessar o Google Sheets.
            
            **Solução:**
            1. Delete o arquivo `token.json` no diretório meet/
            2. Clique em "Conectar Google APIs" novamente
            3. Autorize TODOS os scopes solicitados no navegador
            
            Você pode deletar o token executando no terminal:
            ```bash
            rm /home/emanoel/progpy/avamec/meet/token.json
            ```
            """)
            if st.button("🔄 Tentar reconectar (delete token.json primeiro)"):
                import os
                token_path = os.path.join(os.path.dirname(__file__), 'token.json')
                if os.path.exists(token_path):
                    os.remove(token_path)
                    st.session_state.google_integration = None
                    st.rerun()
        
        return False


def atualizar_participantes_reais():
    """
    Atualiza lista de participantes reais.
    Nota: Em produção, isso viria da Google Meet API.
    Por enquanto, permite entrada manual ou simulação.
    """
    # TODO: Implementar integração real com Google Meet API
    # Por enquanto, retorna estrutura vazia
    participantes_por_grupo = {}
    
    # Placeholder para implementação futura
    # participantes_por_grupo = {
    #     1: [{'email': 'exemplo@email.com', 'nome': 'Exemplo'}],
    #     ...
    # }
    
    if st.session_state.monitor:
        st.session_state.monitor.atualizar_participantes_reais(participantes_por_grupo)


def exibir_metricas_gerais(turma: Optional[str] = None):
    """Exibe métricas gerais do monitoramento."""
    if not st.session_state.monitor:
        return
    
    estatisticas = st.session_state.monitor.obter_estatisticas_gerais(turma=turma)
    
    col1, col2, col3, col4, col5 = st.columns(5)
    
    with col1:
        st.metric(
            "Total Esperado",
            estatisticas['total_esperado']
        )
    
    with col2:
        st.metric(
            "Total Presente",
            estatisticas['total_presente'],
            delta=f"{estatisticas['percentual_presente']:.1f}%"
        )
    
    with col3:
        st.metric(
            "Total Ausente",
            estatisticas['total_ausente'],
            delta=f"{estatisticas['percentual_ausente']:.1f}%",
            delta_color="inverse"
        )
    
    with col4:
        st.metric(
            "Em Sala Errada",
            estatisticas['total_errados'],
            delta_color="inverse"
        )
    
    with col5:
        if st.session_state.ultima_atualizacao:
            tempo_decorrido = (datetime.now() - st.session_state.ultima_atualizacao).total_seconds()
            st.metric(
                "Última Atualização",
                f"{int(tempo_decorrido)}s atrás"
            )


def exibir_status_por_sala(turma: Optional[str] = None):
    """Exibe status detalhado de cada sala."""
    if not st.session_state.monitor:
        return
    
    status_salas = st.session_state.monitor.calcular_status(turma=turma)
    
    # Filtra salas da turma selecionada
    salas_filtradas = [
        (t, g) for t, g in status_salas.keys()
        if turma is None or t == turma
    ]
    salas_filtradas.sort()
    
    # Cria grid de cards
    num_cols = 5
    for i in range(0, len(salas_filtradas), num_cols):
        cols = st.columns(num_cols)
        for j, (t, g) in enumerate(salas_filtradas[i:i+num_cols]):
            if j < len(cols):
                status = status_salas[(t, g)]
                with cols[j]:
                    exibir_card_sala(status)


def exibir_card_sala(status):
    """Exibe card de uma sala."""
    # Determina cor baseada no status
    if status.total_ausente == 0 and len(status.participantes_errados) == 0:
        cor = "🟢"
        cor_bg = "#d4edda"
    elif status.total_ausente > 0 or len(status.participantes_errados) > 0:
        cor = "🟡"
        cor_bg = "#fff3cd"
    else:
        cor = "🔴"
        cor_bg = "#f8d7da"
    
    st.markdown(
        f"""
        <div style="
            background-color: {cor_bg};
            padding: 15px;
            border-radius: 10px;
            margin-bottom: 10px;
        ">
            <h3>{cor} Grupo {status.grupo} - Turma {status.turma}</h3>
            <p><strong>Esperado:</strong> {status.total_esperado}</p>
            <p><strong>Presente:</strong> {status.total_presente}</p>
            <p><strong>Ausente:</strong> {status.total_ausente}</p>
            <p><strong>Errados:</strong> {len(status.participantes_errados)}</p>
        </div>
        """,
        unsafe_allow_html=True
    )
    
    # Expander com detalhes
    with st.expander(f"Detalhes - Turma {status.turma}, Grupo {status.grupo}"):
        if status.participantes_ausentes:
            st.write("**Ausentes:**")
            df_ausentes = pd.DataFrame([
                {'Nome': p.nome, 'Email': p.email, 'Telefone': p.telefone or 'N/A'}
                for p in status.participantes_ausentes
            ])
            st.dataframe(df_ausentes, use_container_width=True, hide_index=True)
        
        if status.participantes_errados:
            st.write("**Em Sala Errada:**")
            df_errados = pd.DataFrame([
                {
                    'Nome': p.nome,
                    'Email': p.email,
                    'Turma Esperada': p.turma,
                    'Grupo Esperado': p.grupo_esperado if p.grupo_esperado > 0 else 'N/A',
                    'Grupo Atual': p.grupo_atual or 'N/A'
                }
                for p in status.participantes_errados
            ])
            st.dataframe(df_errados, use_container_width=True, hide_index=True)
        
        if status.participantes_presentes:
            st.write("**Presentes Corretamente:**")
            st.write(f"{len(status.participantes_presentes)} participantes")


def exibir_graficos(turma: Optional[str] = None):
    """Exibe gráficos de visualização."""
    if not st.session_state.monitor:
        return
    
    status_salas = st.session_state.monitor.calcular_status(turma=turma)
    
    # Prepara dados para gráficos
    dados_grafico = []
    for (t, g), status in status_salas.items():
        if turma is None or t == turma:
            dados_grafico.append({
                'Turma': t,
                'Grupo': g,
                'Presente': status.total_presente,
                'Ausente': status.total_ausente,
                'Errados': len(status.participantes_errados),
                'Esperado': status.total_esperado
            })
    
    if not dados_grafico:
        return
    
    df_grafico = pd.DataFrame(dados_grafico)
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Gráfico de barras - Presença por grupo
        fig = px.bar(
            df_grafico,
            x='Grupo',
            y=['Presente', 'Ausente'],
            title='Presença por Grupo',
            labels={'value': 'Quantidade', 'variable': 'Status'},
            color_discrete_map={'Presente': '#28a745', 'Ausente': '#dc3545'}
        )
        fig.update_layout(barmode='stack')
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        # Gráfico de pizza - Distribuição geral
        estatisticas = st.session_state.monitor.obter_estatisticas_gerais(turma=turma)
        fig = px.pie(
            values=[
                estatisticas['total_presente'],
                estatisticas['total_ausente']
            ],
            names=['Presente', 'Ausente'],
            title='Distribuição Geral',
            color_discrete_map={'Presente': '#28a745', 'Ausente': '#dc3545'}
        )
        st.plotly_chart(fig, use_container_width=True)


def exibir_recomendacoes_ia(turma: Optional[str] = None):
    """Exibe recomendações do agente de IA."""
    if not st.session_state.monitor or not st.session_state.agente_ia:
        return
    
    with st.spinner("Analisando com IA..."):
        try:
            analise = st.session_state.agente_ia.analisar_discrepancias(
                st.session_state.monitor, turma=turma
            )
            
            st.subheader("🤖 Análise e Recomendações da IA")
            
            # Resumo
            st.info(f"**Resumo:** {analise.get('resumo', 'N/A')}")
            
            # Problemas principais
            if analise.get('problemas_principais'):
                st.write("**Problemas Principais:**")
                for problema in analise['problemas_principais']:
                    st.write(f"- {problema}")
            
            # Recomendações
            if analise.get('recomendacoes'):
                st.write("**Recomendações:**")
                for rec in analise['recomendacoes']:
                    st.write(f"- {rec}")
            
            # Ações sugeridas
            if analise.get('acoes_sugeridas'):
                st.write("**Ações Sugeridas:**")
                for i, acao in enumerate(analise['acoes_sugeridas'], 1):
                    st.write(f"{i}. {acao}")
            
            # Prioridade
            prioridade = analise.get('prioridade', 'media')
            cor_prioridade = {
                'alta': '🔴',
                'media': '🟡',
                'baixa': '🟢'
            }.get(prioridade, '⚪')
            st.write(f"**Prioridade:** {cor_prioridade} {prioridade.upper()}")
            
        except Exception as e:
            st.error(f"Erro ao obter análise da IA: {str(e)}")


def main():
    """Função principal do dashboard."""
    st.title("📊 Monitor de Salas Temáticas - Google Meet")
    st.markdown("---")
    
    # Sidebar
    with st.sidebar:
        st.header("⚙️ Configurações")
        
        # Inicialização de serviços
        if st.button("🔌 Conectar Google APIs"):
            inicializar_servicos()
        
        if st.session_state.google_integration:
            st.success("✅ Conectado")
            
            # Configuração da planilha
            st.subheader("📋 Planilha Google Sheets")
            spreadsheet_id = st.text_input(
                "ID da Planilha",
                value=SPREADSHEET_ID,
                help="ID da planilha Google Sheets (encontrado na URL)"
            )
            worksheet_name = st.text_input(
                "Nome da Aba (opcional)",
                value="",
                help="Deixe vazio para usar a primeira aba"
            )
            
            if st.button("📥 Carregar Dados"):
                if spreadsheet_id:
                    worksheet = worksheet_name if worksheet_name else None
                    carregar_dados_planilha(spreadsheet_id, worksheet)
                else:
                    st.error("Por favor, informe o ID da planilha")
        
        # Filtro por turma
        st.subheader("🔍 Filtros")
        turma_selecionada = st.selectbox(
            "Turma",
            options=[None, 'A', 'B'],
            format_func=lambda x: "Todas" if x is None else f"Turma {x}"
        )
        
        # Atualização automática
        st.subheader("🔄 Atualização")
        auto_refresh = st.checkbox("Atualização Automática", value=False)
        if auto_refresh:
            st.info(f"Atualizando a cada {DASHBOARD_REFRESH_INTERVAL}s")
            time.sleep(DASHBOARD_REFRESH_INTERVAL)
            st.rerun()
        
        if st.button("🔄 Atualizar Agora"):
            if st.session_state.monitor:
                atualizar_participantes_reais()
                st.session_state.ultima_atualizacao = datetime.now()
                st.rerun()
    
    # Conteúdo principal
    if not st.session_state.dados_carregados:
        st.info("👆 Configure a conexão e carregue os dados na barra lateral para começar.")
        st.markdown("""
        ### 📋 Como usar:
        1. Clique em "Conectar Google APIs" na barra lateral
        2. Informe o ID da planilha Google Sheets
        3. Clique em "Carregar Dados"
        4. O dashboard será atualizado automaticamente
        """)
        return
    
    # Métricas gerais
    st.subheader("📈 Métricas Gerais")
    exibir_metricas_gerais(turma=turma_selecionada)
    
    st.markdown("---")
    
    # Gráficos
    st.subheader("📊 Visualizações")
    exibir_graficos(turma=turma_selecionada)
    
    st.markdown("---")
    
    # Status por sala
    st.subheader("🏫 Status por Sala")
    exibir_status_por_sala(turma=turma_selecionada)
    
    st.markdown("---")
    
    # Lista de problemas
    st.subheader("⚠️ Participantes com Problemas")
    problemas = st.session_state.monitor.obter_problemas(turma=turma_selecionada)
    
    if problemas:
        df_problemas = pd.DataFrame([
            {
                'Nome': p.nome,
                'Email': p.email,
                'Turma': p.turma,
                'Grupo Esperado': p.grupo_esperado,
                'Grupo Atual': p.grupo_atual or 'N/A',
                'Status': 'Ausente' if not p.presente else 'Sala Errada',
                'Telefone': p.telefone or 'N/A'
            }
            for p in problemas
        ])
        st.dataframe(df_problemas, use_container_width=True, hide_index=True)
        
        # Download CSV
        csv = df_problemas.to_csv(index=False)
        st.download_button(
            label="📥 Download CSV",
            data=csv,
            file_name=f"problemas_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
            mime="text/csv"
        )
    else:
        st.success("🎉 Nenhum problema detectado! Todos os participantes estão nas salas corretas.")
    
    st.markdown("---")
    
    # Recomendações da IA
    if st.session_state.agente_ia:
        exibir_recomendacoes_ia(turma=turma_selecionada)


if __name__ == "__main__":
    main()

