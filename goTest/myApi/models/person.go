package models

type Person struct {
	PersNo int `json:"persNo"`
	Lastname string `json:"lastname"`
	Firstname string `json:"firstname"`
}