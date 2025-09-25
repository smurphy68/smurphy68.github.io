package user_controller

import (
	"net/http"

	"github.com/gin-gonic/gin"
	"github.com/smurphy68/go_project/broadcaster/services"
	"github.com/smurphy68/go_project/shared/models"
)

func PublishUser(c *gin.Context) {
	var user models.User

	// TODO: make error handling reflect new const errors
	if e := c.ShouldBindJSON(&user); e != nil {
		c.JSON(http.StatusBadRequest, gin.H{"error": "Invalid request"})
		return
	}

	e := services.ValidateUser(user)
	if e != nil {
		c.JSON(http.StatusBadRequest, gin.H{"error": "User validation failed"})
		return
	}

	if e := services.PublishUser(user); e != nil {
		c.JSON(http.StatusInternalServerError, gin.H{"error": "Failed to publish user"})
		return
	}

	c.JSON(http.StatusOK, gin.H{
		"message": "User published successfully",
		"user":    user,
	})
}
