package main

import (
	"database/sql"
	"fmt"
	"os"

	"github.com/gin-gonic/gin"
	"github.com/smurphy68/user_api/consts"
	"github.com/smurphy68/user_api/routes"
	"github.com/smurphy68/user_api/services"
)

func main() {
	r := gin.Default()
	routes.RegisterRoutes(r)
	services.TryStartTopic(consts.KAFKAPORT, consts.USERSTOPIC)

	conn := connectToDB()
	defer conn.Close()

	r.Run(":8080")
}

func connectToDB() *sql.DB {
	user := os.Getenv("POSTGRES_USER")
	password := os.Getenv("POSTGRES_PASSWORD")
	dbName := os.Getenv("POSTGRES_DB")
	connectionString := fmt.Sprintf(
		"postgres://%s:%s@postgres:5432/%s?sslmode=disable",
		user,
		password,
		dbName,
	)

	conn, e := sql.Open("postgres", connectionString)
	if e != nil {
		services.HandleError(e)
	}
	return conn
}
