package gorm

import (
	"fmt"
	"os"

	"github.com/smurphy68/go_project/shared/models"
	errorService "github.com/smurphy68/go_project/shared/shared_services"
	"gorm.io/driver/postgres"
	"gorm.io/gorm"
)

func ConnectToDB() (*gorm.DB, error) {
	connectionString := fmt.Sprintf(
		"host=postgres user=%s password=%s dbname=%s port=5432 sslmode=disable",
		os.Getenv("POSTGRES_USER"),
		os.Getenv("POSTGRES_PASSWORD"),
		os.Getenv("POSTGRES_DB"),
	)

	conn, e := gorm.Open(postgres.Open(connectionString), &gorm.Config{})
	if e != nil {
		errorService.HandleError(e, "INFO")
		return nil, e
	}

	conn.AutoMigrate(&models.User{})
	return conn, nil
}
