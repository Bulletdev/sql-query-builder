# SQL Query Builder - Automatizador de Queries Multi-Database

[![Go Version](https://img.shields.io/badge/Go-1.20+-00ADD8?style=flat&logo=go)](https://golang.org/doc/go1.20)
[![Python Version](https://img.shields.io/badge/Python-3.8+-yellow?style=flat&logo=python)](https://www.python.org/downloads/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](https://opensource.org/licenses/MIT)

Um sistema robusto para automatizar a construção e execução de queries SQL em diferentes bancos de dados, com suporte especial para sistemas legados. 
O projeto utiliza Python (Flask/SQLAlchemy) no backend e Go no frontend.

## 📋 Índice

- [Características](#características)
- [Requisitos](#requisitos)
- [Instalação](#instalação)
- [Configuração](#configuração)
- [Uso](#uso)
- [Exemplos](#exemplos)
- [Contribuição](#contribuição)
- [Licença](#licença)

## ✨ Características

### Backend (Python)
- Suporte multi-database (MySQL, PostgreSQL, Oracle, SQL Server)
- Construção dinâmica de queries com múltiplos JOINs
- Pool de conexões para melhor performance
- Tratamento robusto de erros
- Logging configurável
- Validação de dados via dataclasses
- Suporte a queries complexas (WHERE, GROUP BY, ORDER BY, LIMIT)

### Frontend (Go)
- Interface tipo-segura para configuração de queries
- Timeout configurável para requisições
- Tratamento elegante de erros
- Formatação automática dos resultados

## 📦 Requisitos

### Backend
- Python 3.8+
- Flask
- SQLAlchemy
- Drivers de banco de dados específicos:
  - MySQL: `pymysql`
  - PostgreSQL: `psycopg2-binary`
  - Oracle: `cx-oracle`
  - SQL Server: `pyodbc`

### Frontend
- Go 1.20+
- Sem dependências externas além da biblioteca padrão


## 🚀 Instalação

1. Clone o repositório:
```bash
git clone https://github.com/bulletdev/sql-query-builder.git
cd sql-query-builder
```

2. Configure o ambiente virtual Python e instale as dependências:
```bash
cd backend
python -m venv venv
source venv/bin/activate  
pip install -r requirements.txt
```
>> No Windows:

```bash
cd backend
python -m venv venv
source venv\Scripts\activate  
pip install -r requirements.txt
```

3. Configure o ambiente Go:
```bash
cd ../frontend
go mod tidy
```

## ⚙️ Configuração

1. Copie o arquivo de configuração de exemplo:
```bash
cp backend/config.yml.example backend/config.yml
```

2. Edite `config.yml` com suas configurações de banco de dados:
```yaml
databases:
  mysql:
    host: localhost
    port: 3306
    pool_size: 5
    timeout: 30
  oracle:
    host: localhost
    port: 1521
    pool_size: 5
    timeout: 30
```

## 💻 Uso

1. Inicie o backend:
```bash
cd backend
python src/app.py
```

2. Em outro terminal, execute o frontend:
```bash
cd frontend
go run cmd/main.go
```

## 📝 Exemplos

### Consulta básica com JOIN (Go)
```go
config := QueryConfig{
    DbType:    "mysql",
    MainTable: "TGFCAB",
    Columns: []string{"TGFCAB.NUNOTA", "TGFPAR.NOMEPARC"},
    Joins: []JoinCondition{
        {
            Table:       "TGFPAR",
            LeftColumn:  "CODPARC",
            RightColumn: "CODPARC",
            JoinType:    "left",
        },
    },
}
```

### Consulta com condições e ordenação (Python)
```python
query_config = QueryConfig(
    db_type="oracle",
    main_table="TGFCAB",
    columns=["NUNOTA", "DTNEG"],
    conditions=[{"expression": "DTNEG >= '2024-01-01'"}],
    order_by=["DTNEG DESC"],
    limit=100
)
```

## 🤝 Contribuição

1. Faça um Fork do projeto
2. Crie sua Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit suas mudanças (`git commit -m 'Add some AmazingFeature'`)
4. Push para a Branch (`git push origin feature/AmazingFeature`)
5. Abra um Pull Request

## 📄 Licença

Este projeto está licenciado sob a Licença MIT - veja o arquivo [LICENSE](LICENSE) para detalhes.