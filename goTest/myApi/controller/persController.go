package controller

import (
	. "myApi_go/models"

	_ "github.com/go-sql-driver/mysql"
)

func GetPersons() []Person {
	results := ExecuteSQL("SELECT PERS_NO, LASTNAME, FIRSTNAME from pers")
	persons := []Person{}
	for results.Next() {
		var pers Person
		err = results.Scan(&pers.PersNo, &pers.Lastname, &pers.Firstname)
		if err != nil {
			panic(err.Error())
		}
		persons = append(persons, pers)
	}
	return persons
}
