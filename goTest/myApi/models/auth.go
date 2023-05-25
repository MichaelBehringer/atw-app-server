package models

type Login struct {
	Username string `json:"username"`
	Password string `json:"password"`
}

type AcessToken struct {
	AccessToken string `json:"accessToken"`
}
