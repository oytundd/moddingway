package database

import (
	"context"
	"fmt"
	"log"

	"github.com/jackc/pgx/v5/pgxpool"
)

type DbInfo struct {
	Host     string
	Port     string
	User     string
	Password string
	DbName   string
}

func ConnectToDatabase(p DbInfo) *pgxpool.Pool {
	dbUrl := fmt.Sprintf("postgres://%s:%s@%s:%s/%s", p.User, p.Password, p.Host, p.Port, p.DbName)

	log.Printf("Connecting to database...\n")
	conn, err := pgxpool.New(context.Background(), dbUrl)
	if err != nil {
		tempstr := fmt.Sprintf("Unable to connect to database: %v\n", err)
		log.Panic(tempstr)
	}

	return conn
}
