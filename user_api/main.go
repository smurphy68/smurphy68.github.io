package main

import (
	"github.com/gin-gonic/gin"
	"github.com/smurphy68/user_api/routes"
)

func main() {
	r := gin.Default()
	routes.RegisterRoutes(r)

	r.Run(":8080")
}
