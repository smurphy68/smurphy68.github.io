package sharedservices

import (
	"log"
)

func HandleError(e error, errorType string) error {
	// TODO: make this not a meme
	log.Println("Ain't working bub:", e) // 🐺
	return e
}

const (
	INFO    = "Info"
	FATAL   = "Fatal"
	WARNING = "Warning"
	ERROR   = "Error"
)
