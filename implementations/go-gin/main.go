package main

import (
	"database/sql"
	"fmt"
	"log"
	"net/http"
	"os"
	"strconv"
	"time"

	"github.com/gin-gonic/gin"
	_ "github.com/jackc/pgx/v5/stdlib"
)

type User struct {
	ID        string    `json:"id"`
	Name      string    `json:"name"`
	Email     string    `json:"email"`
	City      string    `json:"city"`
	Country   string    `json:"country"`
	Age       int       `json:"age"`
	Active    bool      `json:"active"`
	CreatedAt time.Time `json:"created_at"`
}

type SearchRequest struct {
	Name *string `json:"name,omitempty"`
	City *string `json:"city,omitempty"`
}

func main() {
	dbUrl := os.Getenv("DATABASE_URL")
	if dbUrl == "" {
		dbUrl = "postgres://bench:bench123@localhost:5432/benchmark?sslmode=disable"
	}
	port := os.Getenv("PORT")
	if port == "" {
		port = "5000"
	}

	db, err := sql.Open("pgx", dbUrl)
	if err != nil {
		log.Fatal(err)
	}
	db.SetMaxOpenConns(30)
	db.SetMaxIdleConns(15)

	r := gin.Default()

	r.GET("/hello", func(c *gin.Context) {
		c.JSON(http.StatusOK, gin.H{"message": "ok", "stack": "go-gin"})
	})

	r.GET("/users", func(c *gin.Context) {
		page, _ := strconv.Atoi(c.DefaultQuery("page", "0"))
		size, _ := strconv.Atoi(c.DefaultQuery("size", "20"))
		if size < 1 {
			size = 20
		}
		if size > 100 {
			size = 100
		}

		rows, err := db.QueryContext(c.Request.Context(),
			`SELECT id, name, email, city, country, age, active, created_at
			 FROM users WHERE active = $1
			 ORDER BY created_at DESC LIMIT $2 OFFSET $3`,
			true, size, page*size,
		)
		if err != nil {
			c.JSON(http.StatusInternalServerError, gin.H{"error": err.Error()})
			return
		}
		defer rows.Close()

		users := make([]User, 0, size)
		for rows.Next() {
			var u User
			if err := rows.Scan(&u.ID, &u.Name, &u.Email, &u.City, &u.Country, &u.Age, &u.Active, &u.CreatedAt); err != nil {
				c.JSON(http.StatusInternalServerError, gin.H{"error": err.Error()})
				return
			}
			users = append(users, u)
		}
		if err := rows.Err(); err != nil {
			c.JSON(http.StatusInternalServerError, gin.H{"error": err.Error()})
			return
		}

		c.JSON(http.StatusOK, users)
	})

	r.POST("/users/search", func(c *gin.Context) {
		var body SearchRequest
		if err := c.ShouldBindJSON(&body); err != nil {
			c.JSON(http.StatusBadRequest, gin.H{"error": err.Error()})
			return
		}

		page, _ := strconv.Atoi(c.DefaultQuery("page", "0"))
		size, _ := strconv.Atoi(c.DefaultQuery("size", "20"))
		if size < 1 {
			size = 20
		}
		if size > 100 {
			size = 100
		}

		query := "SELECT id, name, email, city, country, age, active, created_at FROM users WHERE active = true"
		args := make([]any, 0, 4)
		idx := 1

		if body.Name != nil && *body.Name != "" {
			query += fmt.Sprintf(" AND name ILIKE $%d", idx)
			idx++
			args = append(args, "%"+*body.Name+"%")
		}
		if body.City != nil && *body.City != "" {
			query += fmt.Sprintf(" AND city ILIKE $%d", idx)
			idx++
			args = append(args, "%"+*body.City+"%")
		}

		query += fmt.Sprintf(" ORDER BY created_at DESC LIMIT $%d OFFSET $%d", idx, idx+1)
		args = append(args, size, page*size)

		rows, err := db.QueryContext(c.Request.Context(), query, args...)
		if err != nil {
			c.JSON(http.StatusInternalServerError, gin.H{"error": err.Error()})
			return
		}
		defer rows.Close()

		users := make([]User, 0, size)
		for rows.Next() {
			var u User
			if err := rows.Scan(&u.ID, &u.Name, &u.Email, &u.City, &u.Country, &u.Age, &u.Active, &u.CreatedAt); err != nil {
				c.JSON(http.StatusInternalServerError, gin.H{"error": err.Error()})
				return
			}
			users = append(users, u)
		}
		if err := rows.Err(); err != nil {
			c.JSON(http.StatusInternalServerError, gin.H{"error": err.Error()})
			return
		}

		c.JSON(http.StatusOK, users)
	})

	if err := r.Run(":" + port); err != nil {
		log.Fatal(err)
	}
}
