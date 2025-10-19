package main

import (
	"context"
	"fmt"
	services "github.com/smurphy68/go_project/listener/services"
	errorService "github.com/smurphy68/go_project/shared/shared_services"
)

func main() {
	// services.InitialiseDatabase()

	r := services.Reader()
	for {
		m, e := r.ReadMessage(context.Background())
		if e != nil {
			errorService.HandleError(e, "INFO")
			continue
		}
	
		fmt.Printf("Message received at offset %d: %s\n", m.Offset, string(m.Value))
	}
}
