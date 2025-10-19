package services

import (
	"fmt"
	"log"
	"os"

	"github.com/segmentio/kafka-go"
	consts "github.com/smurphy68/go_project/shared/consts"
	"github.com/smurphy68/go_project/shared/models"
	errorService "github.com/smurphy68/go_project/shared/shared_services"
	"gorm.io/driver/postgres"
	"gorm.io/gorm"
)

var Db *gorm.DB

func InitialiseDatabase() {
	connectionString := fmt.Sprintf(
		"host=postgres user=%s password=%s dbname=%s port=5432 sslmode=disable",
		os.Getenv("POSTGRES_USER"),
		os.Getenv("POSTGRES_PASSWORD"),
		os.Getenv("POSTGRES_DB"),
	)

	var e error
	Db, e = gorm.Open(postgres.Open(connectionString), &gorm.Config{})
	if e != nil {
		log.Fatal("failed to connect database:", e)
		errorService.HandleError(e, "FATAL")
	}

	Db.AutoMigrate(&models.User{})
}

func Reader() *kafka.Reader {
	fmt.Println("Listener started. Waiting for messages...")
	return kafka.NewReader(
		kafka.ReaderConfig{
			Brokers:  []string{consts.KAFKAPORT},
			Topic:    consts.USERSTOPIC,
			MinBytes: 10e3,
			MaxBytes: 10e6,
		})
}
