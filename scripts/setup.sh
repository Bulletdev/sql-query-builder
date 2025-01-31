#!/bin/bash

# Cores para output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

echo -e "${YELLOW}Iniciando setup do SQL Query Builder...${NC}"

# Verifica Python
python3 --version >/dev/null 2>&1
if [ $? -ne 0 ]; then
    echo -e "${RED}Python 3 não encontrado. Por favor, instale o Python 3.${NC}"
    exit 1
fi

# Verifica Go
go version >/dev/null 2>&1
if [ $? -ne 0 ]; then
    echo -e "${RED}Go não encontrado. Por favor, instale o Go.${NC}"
    exit 1
fi

# Cria estrutura de diretórios
echo -e "${GREEN}Criando estrutura de diretórios...${NC}"
mkdir -p backend/src/{database,query,utils}
mkdir -p backend/tests
mkdir -p backend/logs
mkdir -p frontend/{cmd,internal/{config,models,client}}
mkdir -p examples
mkdir -p scripts

# Setup do backend
echo -e "${GREEN}Configurando backend...${NC}"
cd backend
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Setup do frontend
echo -e "${GREEN}Configurando frontend...${NC}"
cd ../frontend
go mod tidy

echo -e "${GREEN}Setup concluído com sucesso!${NC}"
echo -e "${YELLOW}Para iniciar o backend:${NC}"
echo "cd backend && source venv/bin/activate && python src/app.py"
echo -e "${YELLOW}Para iniciar o frontend:${NC}"
echo "cd frontend && go run cmd/main.go"