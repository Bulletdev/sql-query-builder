package client

import (
	"bytes"
	"encoding/json"
	"fmt"
	"io/ioutil"
	"net/http"
	"time"

	"github.com/bulletdev/sql-query-builder/internal/models"
)

// Client representa o cliente HTTP para a API do Query Builder
type Client struct {
	BaseURL    string
	HTTPClient *http.Client
}

// NewClient cria uma nova instância do cliente
func NewClient(baseURL string, timeout time.Duration) *Client {
	return &Client{
		BaseURL: baseURL,
		HTTPClient: &http.Client{
			Timeout: timeout,
		},
	}
}

// ExecuteQuery envia uma configuração de query para a API e retorna os resultados
func (c *Client) ExecuteQuery(config *models.QueryConfig) (*models.QueryResponse, error) {
	// Serializa a configuração
	jsonData, err := json.Marshal(config)
	if err != nil {
		return nil, fmt.Errorf("erro ao serializar config: %v", err)
	}

	// Cria a requisição
	req, err := http.NewRequest(
		"POST",
		fmt.Sprintf("%s/query", c.BaseURL),
		bytes.NewBuffer(jsonData),
	)
	if err != nil {
		return nil, fmt.Errorf("erro ao criar requisição: %v", err)
	}

	req.Header.Set("Content-Type", "application/json")

	// Executa a requisição
	resp, err := c.HTTPClient.Do(req)
	if err != nil {
		return nil, fmt.Errorf("erro na requisição: %v", err)
	}
	defer resp.Body.Close()

	// Lê o corpo da resposta
	body, err := ioutil.ReadAll(resp.Body)
	if err != nil {
		return nil, fmt.Errorf("erro ao ler resposta: %v", err)
	}

	// Verifica o status code
	if resp.StatusCode != http.StatusOK {
		var errorResponse models.ErrorResponse
		if err := json.Unmarshal(body, &errorResponse); err != nil {
			return nil, fmt.Errorf("erro desconhecido da API: %s", string(body))
		}
		return nil, fmt.Errorf("erro da API: %s - %s", errorResponse.Error, errorResponse.Details)
	}

	// Deserializa a resposta
	var queryResponse models.QueryResponse
	if err := json.Unmarshal(body, &queryResponse); err != nil {
		return nil, fmt.Errorf("erro ao deserializar resposta: %v", err)
	}

	return &queryResponse, nil
}

// HealthCheck verifica se a API está funcionando
func (c *Client) HealthCheck() error {
	resp, err := c.HTTPClient.Get(fmt.Sprintf("%s/health", c.BaseURL))
	if err != nil {
		return fmt.Errorf("erro ao verificar saúde da API: %v", err)
	}
	defer resp.Body.Close()

	if resp.StatusCode != http.StatusOK {
		return fmt.Errorf("API não está saudável: status code %d", resp.StatusCode)
	}

	return nil
}
