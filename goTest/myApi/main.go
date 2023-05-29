package main

import (
	"fmt"
	. "myApi_go/controller"
	"myApi_go/middleware"
	. "myApi_go/models"
	"net/http"

	"github.com/gin-contrib/cors"
	"github.com/gin-gonic/gin"
)

func main() {
	InitDB()
	defer CloseDB()

	router := gin.Default()
	// router.Use(cors.Default())
	config := cors.DefaultConfig()
	config.AllowAllOrigins = true
	config.AllowHeaders = []string{"Content-Type", "Content-Length", "Accept-Encoding", "Authorization", "Cache-Control"}
	router.Use(cors.New(config))
	router.GET("/test", middleware.AuthUser(), getProducts)
	router.POST("/login", login)
	router.GET("/file", file)
	// router.GET("/getUserToToken", getUserToToken)
	router.GET("/checkToken/:token", checkToken)
	router.Run(":8080")
}

func login(c *gin.Context) {
	var login Login
	c.BindJSON(&login)
	retJWT := DoLogin(login, c)
	c.IndentedJSON(http.StatusOK, retJWT)
}

func file(c *gin.Context) {
	fmt.Printf("wir habens")
	numbers := [4]int{1, 2, 3, 4}
	pathZip, fileZip := CreateCityPDFs(numbers[:], 2022)
	c.Writer.Header().Set("Content-Disposition", "attachment; filename="+fileZip)
	c.File(pathZip + fileZip)
}

func checkToken(c *gin.Context) {
	token := c.Param("token")
	tokenRes := CheckToken(token)
	c.IndentedJSON(http.StatusOK, tokenRes)
}

func getProducts(c *gin.Context) {
	persons := GetPersons()

	if persons == nil || len(persons) == 0 {
		c.AbortWithStatus(http.StatusNotFound)
	} else {
		c.IndentedJSON(http.StatusOK, persons)
	}
}
