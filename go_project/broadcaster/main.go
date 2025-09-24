package main

import (
	"github.com/gin-gonic/gin"
	"github.com/smurphy68/go_project/shared/consts"

	"github.com/smurphy68/go_project/broadcaster/routes"
	"github.com/smurphy68/go_project/broadcaster/services"
)

func main() {
	// This should have no knowledge of the DB
	r := gin.Default()
	routes.RegisterRoutes(r)
	services.TryStartTopic(consts.KAFKAPORT, consts.USERSTOPIC)

	r.Run(":8080")
}
