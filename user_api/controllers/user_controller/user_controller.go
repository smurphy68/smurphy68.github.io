package user_controller

import (
	"net/http"

	"github.com/gin-gonic/gin"
	"github.com/smurphy68/user_api/models"
	"github.com/smurphy68/user_api/services"
)

func PublishUser(c *gin.Context) {
	var user models.User

	if err := c.ShouldBindJSON(&user); err != nil {
		c.JSON(http.StatusBadRequest, gin.H{"error": "Invalid request"})
		return
	}

	if !services.ValidateUser(user) {
		c.JSON(http.StatusBadRequest, gin.H{"error": "User validation failed"})
		return
	}

	if err := services.PublishUser(user); err != nil {
		c.JSON(http.StatusInternalServerError, gin.H{"error": "Failed to publish user"})
		return
	}

	c.JSON(http.StatusOK, gin.H{
		"message": "User published successfully",
		"user":    user,
	})
}
