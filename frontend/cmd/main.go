package main

import (
	"fmt"
	"log"
	"time"

	"github.com/bulletdev/sql-query-builder/internal/client"
	"github.com/bulletdev/sql-query-builder/internal/models"
)

func main() {
	// Cria cliente com timeout de 30 segundos
	c := client.NewClient("http://localhost:5000", 30*time.Second)

	// Verifica saúde da API
	if err := c.HealthCheck(); err != nil {
		log.Fatalf("API não está disponível: %v", err)
	}

	// Exemplo de configuração para consulta no Sankhya
	limit := 1000
	config := &models.QueryConfig{
		DbType:    "oracle",
		User:      "seu_usuario",
		Password:  "sua_senha",
		Host:      "localhost",
		DbName:    "sankhya",
		MainTable: "TGFCAB",
		Columns: []string{
			"TGFCAB.NUNOTA",
			"TGFCAB.DTNEG",
			"TGFPAR.NOMEPARC",
			"TGFPRO.DESCRPROD",
		},
		Joins: []models.JoinCondition{
			{
				Table:       "TGFPAR",
				LeftColumn:  "CODPARC",
				RightColumn: "CODPARC",
				JoinType:    "left",
			},
			{
				Table:       "TGFITE",
				LeftColumn:  "NUNOTA",
				RightColumn: "NUNOTA",
				JoinType:    "inner",
			},
			{
				Table:       "TGFPRO",
				LeftColumn:  "CODPROD",
				RightColumn: "CODPROD",
				JoinType:    "left",
			},
		},
		Filters: []models.QueryFilter{
			{
				Column:    "TGFCAB.DTNEG",
				Operator:  ">=",
				Value:     "2024-01-01",
				Connector: "AND",
			},
		},
		OrderBy: []string{"TGFCAB.DTNEG DESC"},
		Limit:   &limit,
	}

	// Executa a query
	response, err := c.ExecuteQuery(config)
	if err != nil {
		log.Fatalf("Erro ao executar query: %v", err)
	}

	// Imprime resultados
	fmt.Printf("Query executada: %s\n", response.Query)
	fmt.Printf("Tempo de execução: %.2fs\n", response.ExecutionTime)
	fmt.Printf("Total de registros: %d\n", response.TotalRows)

	// Imprime os primeiros 5 resultados
	for i, row := range response.Data {
		if i >= 5 {
			break
		}
		fmt.Printf("Registro %d: %+v\n", i+1, row)
	}
}
