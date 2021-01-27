package main

import (
    "fmt"
    "net/http"
    "encoding/json"
    _ "github.com/go-sql-driver/mysql"
    "database/sql"
)

type Pokemon struct{
    ID int `json: ID`
	Name *string `json: Name`
	Type1 *string `json: Type_1`
    Type2 *string `json: Type_2`
}

func isEmptyStringPtr(s *string) bool{
    if s == nil {
        return true
    }
    return len(*s) <= 0
}

func enableCors(w *http.ResponseWriter) {
    (*w).Header().Set("Access-Control-Allow-Origin", "*")
}

func fetch_data(type1 *string, type2 *string)([]Pokemon){
    db, err := sql.Open("mysql", "test1:test1@tcp(localhost)/pokedex")

    if err != nil {
        panic(err.Error())
    }

    defer db.Close()

    _, _ = type1, type2

    query := "SELECT * FROM pokemon"
    if !isEmptyStringPtr(type1){
        if !isEmptyStringPtr(type2){
            query += " WHERE (Type_1 = \"" + *type1 + "\" OR Type_2 = \"" + *type1 + "\")"
            query += " AND (" + " Type_2 = \"" + *type2 + "\" OR Type_1 = \"" + *type2 + "\")"
        } else {
            query += " WHERE (Type_1 = \"" + *type1 + "\" OR Type_2 = \"" + *type1 + "\""
            query += ")"
        }
    }

    fmt.Println(query)

    results, err := db.Query(query)
    if err != nil {
        panic(err.Error())
    }

    rows := make(map[int]Pokemon)

    for results.Next() {
        var pokemon Pokemon
        err = results.Scan(&pokemon.ID, &pokemon.Name, &pokemon.Type1, &pokemon.Type2)
        if err != nil {
            panic(err.Error())
        }
        rows[pokemon.ID] = pokemon
    }

    var ret []Pokemon
    for _, val := range rows {
        ret = append(ret, val)
    }

    return ret
}

func my_server(w http.ResponseWriter, r *http.Request) {
    enableCors(&w)

    type1, ok1 := r.URL.Query()["type1"]
    type2, ok2 := r.URL.Query()["type2"]

    if !ok1 || !ok2 {
        fmt.Println("an error occurred while parsing params")
        return
    }
 
    data := fetch_data(&type1[0], &type2[0])
    response, err := json.Marshal(data)
    
    if err != nil {
    	fmt.Fprintf(w, "Error: %s", err)
    	return
    }

    w.Header().Set("Content-Type", "application/json")
  	w.Write(response)
}

func main() {
    http.HandleFunc("/pokemon", my_server)
    http.ListenAndServe(":8080", nil)
}