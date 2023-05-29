package middleware

import (
	"fmt"
	. "myApi_go/controller"
	. "myApi_go/models"
	"net/http"
	"strings"

	"github.com/gin-gonic/gin"
)

type authHeader struct {
	IDToken string `header:"Authorization"`
}

func AuthUser() gin.HandlerFunc {
	return func(c *gin.Context) {
		h := authHeader{}
		c.ShouldBindHeader(&h)
		fmt.Printf("pre")
		fmt.Printf(h.IDToken)
		fmt.Printf("post")
		idTokenHeader := strings.Split(h.IDToken, "Bearer ")
		fmt.Printf("\n\n%v", len(idTokenHeader))

		if len(idTokenHeader) < 2 {
			fmt.Printf("drinnen")
			c.AbortWithStatusJSON(http.StatusBadRequest, ResponseText{Reason: "kein Token"})
			return
		}
		isAllowed, _ := ParseToken(idTokenHeader[1])
		if isAllowed {
			c.Next()
		} else {
			c.AbortWithStatus(http.StatusBadRequest)
			return
		}
	}
}
