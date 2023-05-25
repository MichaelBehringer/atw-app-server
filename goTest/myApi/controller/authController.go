package controller

import (
	"fmt"
	. "myApi_go/models"
	"net/http"
	"time"

	"github.com/gin-gonic/gin"
	"github.com/golang-jwt/jwt/v5"
)

func DoLogin(login Login, c *gin.Context) AcessToken {
	var (
		key []byte
		t   *jwt.Token
		s   string
	)

	var isAllowed bool
	ExecuteSQLRow("SELECT COUNT(*) FROM pers WHERE USERNAME=? AND PASSWORD=?", login.Username, login.Password).Scan(&isAllowed)
	if !isAllowed {
		c.AbortWithStatus(http.StatusUnauthorized)
	}

	key = []byte("my_secret_key")
	t = jwt.NewWithClaims(jwt.SigningMethodHS256,
		jwt.MapClaims{
			"user":         login.Username,
			"creationTime": time.Now().UnixNano(),
		})
	s, _ = t.SignedString(key)

	return AcessToken{AccessToken: s}
}

func CheckToken(tokenStr string) string {
	isValid, claims := ParseToken(tokenStr)
	if !isValid {
		return "eroor"
	} else {

	}
	// claims := jwt.MapClaims{}
	// tkn, err := jwt.ParseWithClaims(paramToken, claims, func(token *jwt.Token) (interface{}, error) {
	// 	return []byte("my_secret_key"), nil
	// })

	// if err != nil {
	// 	if err == jwt.ErrSignatureInvalid {
	// 		return "ErrSignatureInvalid"
	// 	}
	// 	fmt.Printf(err.Error())

	// 	if !tkn.Valid {
	// 		fmt.Printf("invalid")
	// 	}

	// 	return "StatusBadRequest"
	// }
	// if !tkn.Valid {
	// 	return "StatusUnauthorized"
	// }
	// ... error handling

	// do something with decoded claims
	for key, val := range claims {
		fmt.Printf("Key: %v, value: %v\n", key, val)
	}
	return "erfolg"
}

func ParseToken(tokenStr string) (bool, jwt.MapClaims) {
	claims := jwt.MapClaims{}
	tkn, err := jwt.ParseWithClaims(tokenStr, claims, func(token *jwt.Token) (interface{}, error) {
		return []byte("my_secret_key"), nil
	})
	return (err == nil && tkn.Valid), claims
}
