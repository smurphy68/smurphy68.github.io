package models

type User struct {
	Id   int    `gorm:"primaryKey"`
	Name string `gorm:"size:100;not null"`
}
