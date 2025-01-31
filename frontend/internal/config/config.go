package config

import (
	"encoding/json"
	"os"
)

type Config struct {
	Server struct {
		Host string `json:"host"`
		Port int    `json:"port"`
	} `json:"server"`
	Database struct {
		Host     string `json:"host"`
		Port     int    `json:"port"`
		Name     string `json:"name"`
		User     string `json:"user"`
		Password string `json:"password"`
	} `json:"database"`
}

func Load(path string) (*Config, error) {
	config := &Config{}

	file, err := os.Open(path)
	if err != nil {
		return nil, err
	}
	defer file.Close()

	decoder := json.NewDecoder(file)
	if err := decoder.Decode(config); err != nil {
		return nil, err
	}

	return config, nil
}

func GetDefaultConfig() *Config {
	config := &Config{}

	// Set default server values
	config.Server.Host = "localhost"
	config.Server.Port = 8080

	// Set default database values
	config.Database.Host = "localhost"
	config.Database.Port = 5432
	config.Database.Name = "myapp"
	config.Database.User = "user"
	config.Database.Password = ""

	return config
}
