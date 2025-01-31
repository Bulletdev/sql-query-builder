package models

import "time"

// JoinCondition representa uma condição de JOIN entre tabelas
type JoinCondition struct {
	Table       string `json:"table"`
	LeftColumn  string `json:"left_column"`
	RightColumn string `json:"right_column"`
	JoinType    string `json:"join_type"`
}

// QueryFilter representa um filtro para a cláusula WHERE
type QueryFilter struct {
	Column    string      `json:"column"`
	Operator  string      `json:"operator"`
	Value     interface{} `json:"value"`
	Connector string      `json:"connector"`
}

// QueryConfig representa a configuração completa para construção de queries
type QueryConfig struct {
	DbType    string          `json:"db_type"`
	User      string          `json:"user"`
	Password  string          `json:"password"`
	Host      string          `json:"host"`
	DbName    string          `json:"db_name"`
	MainTable string          `json:"main_table"`
	Columns   []string        `json:"columns"`
	Joins     []JoinCondition `json:"joins"`
	Filters   []QueryFilter   `json:"filters,omitempty"`
	GroupBy   []string        `json:"group_by,omitempty"`
	OrderBy   []string        `json:"order_by,omitempty"`
	Limit     *int            `json:"limit,omitempty"`
	Offset    *int            `json:"offset,omitempty"`
}

// QueryResponse representa a resposta da execução da query
type QueryResponse struct {
	Success       bool                     `json:"success"`
	Data          []map[string]interface{} `json:"data"`
	Query         string                   `json:"query"`
	ExecutionTime float64                  `json:"execution_time"`
	TotalRows     int                      `json:"total_rows"`
	Error         string                   `json:"error,omitempty"`
	Details       string                   `json:"details,omitempty"`
	CreatedAt     time.Time                `json:"created_at"`
}

// ErrorResponse representa uma resposta de erro da API
type ErrorResponse struct {
	Success bool   `json:"success"`
	Error   string `json:"error"`
	Details string `json:"details"`
}
