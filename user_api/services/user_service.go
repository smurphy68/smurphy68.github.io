package services

import (
	"context"
	"encoding/json"
	"log"

	"github.com/segmentio/kafka-go"
	"github.com/smurphy68/user_api/consts"
	"github.com/smurphy68/user_api/models"
)

var messageWriter = Writer([]string{consts.KAFKAPORT}, consts.USERSTOPIC)

func PublishUser(user models.User) error {
	json, e := json.Marshal(user)
	if e != nil {
		return HandleError(e)
	}

	message := kafka.Message{
		Value: json,
	}

	_context := context.Background()

	e = messageWriter.WriteMessages(_context, message)
	if e != nil {
		return HandleError(e)
	}
	// TODO: log something if error or success
	return nil
}

func HandleError(e error) error {
	// TODO: make this not a meme
	log.Println("Ain't working bub:", e) // 🐺
	return e
}

func ValidateUser(user models.User) bool {
	if user.Id > 0 && user.Name != "" {
		return true
	}

	// AddMoar
	return false
}
