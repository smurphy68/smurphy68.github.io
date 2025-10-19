package main

import (
	"context"
	"encoding/json"
	"fmt"
	"time"
	
	services "github.com/smurphy68/go_project/listener/services"
	models "github.com/smurphy68/go_project/shared/models"
	errorService "github.com/smurphy68/go_project/shared/shared_services"
)

func main() {
	for {
		e := services.InitialiseDatabase()
		if e != nil {
			errorService.HandleError(e, "FATAL")
			time.Sleep(time.Second * 5)
			continue
		} else {
			break
		}
	}

	r := services.Reader()
	for {
		var user = models.User{}
		m, e := r.ReadMessage(context.Background())
		if e != nil {
			errorService.HandleError(e, "INFO")
			continue
		}

		e = json.Unmarshal(m.Value, &user)
		if e != nil {
			errorService.HandleError(e, "INFO")
			continue
		}
		result := services.Db.Create(&user)
		if result.Error != nil {
			errorService.HandleError(result.Error, "INFO")
			continue
		} else {
			fmt.Printf("User with ID %d saved to database.\n", user.Id)
		}

		fmt.Printf("Message received at offset %d: %s\n", m.Offset, string(m.Value))
	}
}
