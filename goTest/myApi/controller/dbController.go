package controller

import (
	"database/sql"
	"fmt"

	_ "github.com/go-sql-driver/mysql"
)

var db *sql.DB
var err error

func InitDB() {
	db, err = sql.Open("mysql", "dbadmin:raspberry@tcp(127.0.0.1:3306)/ffw")
	if err != nil {
		panic(err.Error())
	}
}

func CloseDB() {
	db.Close()
}

func ExecuteSQL(statement string) *sql.Rows {
	results, err := db.Query(statement)
	if err != nil {
		fmt.Println("Err", err.Error())
		return nil
	}
	return results
}

func ExecuteSQLRow(statement string, params ...interface{}) *sql.Row {
	// var selectCount bool
	// err := db.QueryRow(statement, params...).Scan(&selectCount)
	// if err != nil {
	// 	fmt.Println("Err", err.Error())
	// 	return false
	// }
	// return selectCount

	return db.QueryRow(statement, params...)
}
