package main

import (
	"log"
	"net/http"
	"os"
	"strconv"

	"github.com/gin-gonic/gin"
	"github.com/jackc/pgx/v5/pgxpool"
)

type User struct {
	ID        string `json:"id"`
	Name      string `json:"name"`
	Email     string `json:"email"`
	City      string `json:"city"`
	Country   string `json:"country"`
	Age       string `json:"age"`
	Active    string `json:"active"`
	CreatedAt string `json:"created_at"`
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
		port = "8080"
	}

	cfg, err := pgxpool.ParseConfig(dbUrl)
	if err != nil {
		log.Fatal(err)
	}
	cfg.MaxConns = 20

	pool, err := pgxpool.NewWithConfig(nil, cfg)
	if err != nil {
		log.Fatal(err)
	}
	defer pool.Close()

	r := gin.Default()

	r.GET("/users/hello", func(c *gin.Context) {
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

		rows, err := pool.Query(c.Request.Context(),
			`SELECT id, name, email, city, country, age, active, created_at
			FROM users WHERE active = true
			ORDER BY created_at DESC
			OFFSET $1 LIMIT $2`,
			page*size, size,
		)
		if err != nil {
			c.JSON(http.StatusInternalServerError, gin.H{"error": err.Error()})
			return
		}
		defer rows.Close()

		users := []User{}
		for rows.Next() {
			var u User
			if err := rows.Scan(&u.ID, &u.Name, &u.Email, &u.City, &u.Country, &u.Age, &u.Active, &u.CreatedAt); err != nil {
				c.JSON(http.StatusInternalServerError, gin.H{"error": err.Error()})
				return
			}
			users = append(users, u)
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
		size, _ := strconv.Atoi(c.DefaultQuery("size", "0"))
		if size < 1 {
			size = 20
		}
		if size > 100 {
			size = 100
		}

		query := `
			SELECT id, name, email, city, country, age, active, created_At
			FROM users WHERE active = true
		`

		args := []interface{}{}
		argIdx := 1

		if body.Name != nil && *body.Name != "" {
			query += ` AND name ILIKE '%' || $` + strconv.Itoa(argIdx) + ` || '%'`
			args = append(args, *body.Name)
			argIdx++
		}
		if body.City != nil && *body.City != "" {
			query += ` AND city ILIKE '%' || $` + strconv.Itoa(argIdx) + ` || '%'`
			args = append(args, *body.City)
			argIdx++
		}

		query += ` ORDER BY created_at DESC OFFSET $` + strconv.Itoa(argIdx) + ` LIMIT $` + strconv.Itoa(argIdx+1)
		args = append(args, page*size, size)

		rows, err := pool.Query(c.Request.Context(), query, args...)
		if err != nil {
			c.JSON(http.StatusInternalServerError, gin.H{"error": err.Error()})
			return
		}
		defer rows.Close()

		users := []User{}
		for rows.Next() {
			var u User
			if err := rows.Scan(&u.ID, &u.Name, &u.Email, &u.City, &u.Country, &u.Age, &u.Active, &u.CreatedAt); err != nil {
				c.JSON(http.StatusInternalServerError, gin.H{"error": err.Error()})
				return
			}
			users = append(users, u)
		}

		c.JSON(http.StatusOK, users)
	})

	if err := r.Run(":" + port); err != nil {
		log.Fatal(err)
	}
}
