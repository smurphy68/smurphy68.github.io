package routes

import (
	"github.com/gin-gonic/gin"
	controllers "github.com/smurphy68/user_api/controllers/user_controller"
)

func RegisterRoutes(router *gin.Engine) {
	userRoutes := router.Group("/users")
	{
		userRoutes.POST("", controllers.PublishUser)
	}
}
