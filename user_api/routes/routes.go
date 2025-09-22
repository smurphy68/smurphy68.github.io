package routes

import (
	"github.com/gin-gonic/gin"
	"github.com/smurphy68/user_api/consts"
	controllers "github.com/smurphy68/user_api/controllers/user_controller"
)

func RegisterRoutes(router *gin.Engine) {
	userRoutes := router.Group(consts.USERROUTE)
	{
		userRoutes.POST("", controllers.PublishUser)

		// AddMoar
	}
}
