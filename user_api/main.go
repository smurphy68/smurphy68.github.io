package main

import (
	"github.com/gin-gonic/gin"
	"github.com/smurphy68/user_api/consts"
	"github.com/smurphy68/user_api/routes"
	"github.com/smurphy68/user_api/services"
)

func main() {
	r := gin.Default()
	routes.RegisterRoutes(r)
	services.TryStartTopic(consts.KAFKAPORT, consts.USERSTOPIC)

	r.Run(":8080")
}
