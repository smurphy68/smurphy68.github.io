package sharedservices

import (
	"log"
)

func HandleError(e error) error {
	// TODO: make this not a meme
	log.Println("Ain't working bub:", e) // 🐺
	return e
}
