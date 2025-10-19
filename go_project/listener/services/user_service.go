package services

import (
	"errors"

	"github.com/smurphy68/go_project/shared/consts"
	"github.com/smurphy68/go_project/shared/models"
	errorService "github.com/smurphy68/go_project/shared/shared_services"
)

var messageReader = Reader()

func SaveUser(user models.User) error {
	return errorService.HandleError(
		Db.Create(&user).Error,
		"INFO",
	)
}

func ValidateUser(user models.User) error {
	if user.Id > 0 && user.Name != "" {
		return nil
	}

	// AddMoar
	return errors.New(consts.UserValidationError)
}
