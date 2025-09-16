#!/bin/bash

# Script para entrar nos diretórios do Sonarr, Readarr, Bazarr e Lidarr
# e executar 'docker compose pull' para atualizar

# --- Configurações ---
SONARR_DIR="/home/emanoel/sonarr"    # Substitua pelo caminho real
READARR_DIR="/home/emanoel/readarr"  # Substitua pelo caminho real
BAZARR_DIR="/home/emanoel/bazarr"    # Substitua pelo caminho real
LIDARR_DIR="/home/emanoel/lidarr"    # Substitua pelo caminho real

# --- Funções ---

atualizar_servico() {
  local diretorio="$1"
  local nome_servico="$2"

  if [ -d "$diretorio" ]; then
    echo "Entrando no diretório do $nome_servico: $diretorio"
    cd "$diretorio" || {
      echo "Erro: Não foi possível entrar no diretório do $nome_servico."
      return 1
    }

    echo "Executando 'docker compose pull' no $nome_servico..."
    docker compose pull
    STATUS=$?

    if [ $STATUS -eq 0 ]; then
      echo "'docker compose pull' executado com sucesso no $nome_servico."
    else
      echo "Erro ao executar 'docker compose pull' no $nome_servico."
      return 1
    fi

    cd - > /dev/null # Retorna ao diretório anterior silenciosamente
    return 0
  else
    echo "Aviso: O diretório do $nome_servico não foi encontrado: $diretorio"
    return 1
  fi
}

# --- Execução ---

echo "----------------------------------------"
echo "Atualizando Sonarr, Readarr, Bazarr e Lidarr via Docker Compose Pull"
echo "----------------------------------------"

atualizar_servico "$SONARR_DIR" "Sonarr"
STATUS_SONARR=$?

echo ""

atualizar_servico "$READARR_DIR" "Readarr"
STATUS_READARR=$?

echo ""

atualizar_servico "$BAZARR_DIR" "Bazarr"
STATUS_BAZARR=$?

echo ""

atualizar_servico "$LIDARR_DIR" "Lidarr"
STATUS_LIDARR=$?

echo ""

success=0
failure=0

if [ $STATUS_SONARR -eq 0 ]; then
  ((success++))
else
  ((failure++))
fi

if [ $STATUS_READARR -eq 0 ]; then
  ((success++))
else
  ((failure++))
fi

if [ $STATUS_BAZARR -eq 0 ]; then
  ((success++))
else
  ((failure++))
fi

if [ $STATUS_LIDARR -eq 0 ]; then
  ((success++))
else
  ((failure++))
fi

echo "Resumo da atualização:"
if [ $success -gt 0 ]; then
  echo "  Sucesso: $success serviço(s) atualizado(s)."
fi
if [ $failure -gt 0 ]; then
  echo "  Falha: $failure serviço(s) não pôde(m) ser atualizado(s)."
fi

echo "----------------------------------------"

exit 0
