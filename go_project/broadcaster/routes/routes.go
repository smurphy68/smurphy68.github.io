package routes

import (
	"github.com/gin-gonic/gin"
	"github.com/smurphy68/go_project/shared/consts"
	controllers "github.com/smurphy68/go_project/broadcaster/user_controller"
)

func RegisterRoutes(router *gin.Engine) {
	userRoutes := router.Group(consts.USERROUTE)
	{
		userRoutes.POST("", controllers.PublishUser)

		// AddMoar
	}
}
