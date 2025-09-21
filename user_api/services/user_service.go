package services

import (
	"context"
	"encoding/json"
	"log"

	"github.com/segmentio/kafka-go"
	"github.com/smurphy68/user_api/models"
)

var messageWriter *kafka.Writer

// Initialise KafkaWriter
func Writer(brokers []string, topic string) {
	var writerConfig = kafka.WriterConfig{
		Brokers: brokers,
		Topic:   topic,
	}
	messageWriter = kafka.NewWriter(writerConfig)
}

func PublishUser(user models.User) error {
	json, e := json.Marshal(user)
	if e != nil {
		// TODO: wrap whole logic chain to remove
		HandleError(e)
	}

	message := kafka.Message{
		Value: json,
	}

	_context := context.Background()

	e = messageWriter.WriteMessages(_context, message)
	if e != nil {
		HandleError(e)
	}
	// TODO: log something if error or success
	return nil
}

func HandleError(e error) error {
	log.Println("Ain't working bub:", e)
	return e
}

func ValidateUser(user models.User) bool {
	// TODO implement service level validation
	return true
}
