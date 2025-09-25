package services

import (
	"errors"
	"context"
	"encoding/json"

	"github.com/segmentio/kafka-go"
	"github.com/smurphy68/go_project/shared/consts"
	"github.com/smurphy68/go_project/shared/models"
	errorService "github.com/smurphy68/go_project/shared/shared_services"
)

var messageWriter = Writer([]string{consts.KAFKAPORT}, consts.USERSTOPIC)

func PublishUser(user models.User) error {
	json, e := json.Marshal(user)
	if e != nil {
		return errorService.HandleError(e)
	}

	message := kafka.Message{
		Value: json,
	}

	_context := context.Background()

	e = messageWriter.WriteMessages(_context, message)
	if e != nil {
		return errorService.HandleError(e)
	}
	// TODO: log something if error or success
	return nil
}

func ValidateUser(user models.User) error {
	if user.Id > 0 && user.Name != "" {
		return nil
	}

	// AddMoar
	return errors.New(consts.UserValidationError)
}
