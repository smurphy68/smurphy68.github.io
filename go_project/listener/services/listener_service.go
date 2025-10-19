package services

import (
	"fmt"
	"log"
	"os"

	"github.com/segmentio/kafka-go"
	consts "github.com/smurphy68/go_project/shared/consts"
	"github.com/smurphy68/go_project/shared/models"
	"gorm.io/driver/postgres"
	"gorm.io/gorm"
)

var Db *gorm.DB

func InitialiseDatabase() error {
	var e error

	user := os.Getenv("POSTGRES_USER")
	password := os.Getenv("POSTGRES_PASSWORD")
	dbname := os.Getenv("POSTGRES_DB")
	host := "postgres"

	connectionString := fmt.Sprintf(
		"host=%s user=%s password=%s database=%s port=5432 sslmode=disable",
		host, user, password, dbname,
	)

	db, e := gorm.Open(postgres.Open(connectionString), &gorm.Config{})
	if e != nil {
		log.Println(connectionString)
		return e
	}

	Db = db
	log.Println("Database connection established")

	e = Db.AutoMigrate(&models.User{})
	if e != nil {
		return e
	}
	log.Println("Migration successful")
	return nil
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
