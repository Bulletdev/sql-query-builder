#!/bin/bash

# Cores para output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

echo -e "${YELLOW}Instalando dependências...${NC}"

# Instala dependências do sistema (exemplo para Ubuntu/Debian)
if [ -x "$(command -v apt-get)" ]; then
    echo -e "${GREEN}Instalando dependências do sistema...${NC}"
    sudo apt-get update
    sudo apt-get install -y \
        python3-dev \
        python3-pip \
        python3-venv \
        golang \
        unixodbc-dev \
        libaio1
fi

# Instala Oracle Instant Client se necessário
if [ ! -d "/opt/oracle" ]; then
    echo -e "${YELLOW}Oracle Instant Client não encontrado. Por favor, instale manualmente.${NC}"
    echo "Instruções em: https://oracle.github.io/odpi/doc/installation.html"
fi

# Instala dependências Python
echo -e "${GREEN}Instalando dependências Python...${NC}"
cd backend
python3 -m venv venv
source venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt

# Instala dependências Go
echo -e "${GREEN}Instalando dependências Go...${NC}"
cd ../frontend
go mod download

echo -e "${GREEN}Instalação de dependências concluída!${NC}"