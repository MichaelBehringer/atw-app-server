package main
import (
  "database/sql"
  _"github.com/go-sql-driver/mysql"
	"log"
)
var db *sql.DB
var err error

type Tag struct {
	ID   int    `json:"id"`
	Lastname string `json:"lastname"`
}

func main() {
  db, err = sql.Open("mysql", "dbadmin:raspberry@tcp(127.0.0.1:3306)/ffw")
  if err != nil {
    panic(err.Error())
  }
	getPost()
  defer db.Close()
}

func getPost() {
  results, err := db.Query("SELECT PERS_NO , lastname from pers")
	if err != nil {
			panic(err.Error()) // proper error handling instead of panic in your app
	}

	for results.Next() {
			var tag Tag
			// for each row, scan the result into our tag composite object
			err = results.Scan(&tag.ID, &tag.Lastname)
			if err != nil {
					panic(err.Error()) // proper error handling instead of panic in your app
			}
							// and then print out the tag's Name attribute
			log.Printf(tag.Lastname)
	}
}