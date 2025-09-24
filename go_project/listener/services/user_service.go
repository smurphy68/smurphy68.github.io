package services

import (
	"github.com/smurphy68/go_project/shared/models"
	// errorService "github.com/smurphy68/go_project/shared/shared_services"
)

func ValidateUser(user models.User) bool {
	if user.Id > 0 && user.Name != "" {
		return true
	}

	// AddMoar
	return false
}
