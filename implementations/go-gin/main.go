package main

import (
	"log"
	"net/http"
	"os"
	"strconv"
	"time"

	"github.com/gin-gonic/gin"
	"gorm.io/driver/postgres"
	"gorm.io/gorm"
)

type User struct {
	ID        string    `gorm:"type:uuid;primaryKey;default:gen_random_uuid()" json:"id"`
	Name      string    `gorm:"type:varchar(100)" json:"name"`
	Email     string    `gorm:"type:varchar(150)" json:"email"`
	City      string    `gorm:"type:varchar(100)" json:"city"`
	Country   string    `gorm:"type:varchar(100)" json:"country"`
	Age       int       `json:"age"`
	Active    bool      `json:"active"`
	CreatedAt time.Time `gorm:"autoCreateTime" json:"created_at"`
}

func (User) TableName() string {
	return "users"
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

	db, err := gorm.Open(postgres.Open(dbUrl), &gorm.Config{
		SkipDefaultTransaction: true,
		PrepareStmt:            true,
	})
	if err != nil {
		log.Fatal(err)
	}
	sqlDB, _ := db.DB()
	sqlDB.SetMaxOpenConns(30)
	sqlDB.SetMaxIdleConns(15)

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

		var users []User
		result := db.WithContext(c.Request.Context()).
			Where("active = ?", true).
			Order("created_at DESC").
			Offset(page * size).
			Limit(size).
			Find(&users)
		if result.Error != nil {
			c.JSON(http.StatusInternalServerError, gin.H{"error": result.Error.Error()})
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

		query := db.WithContext(c.Request.Context()).Where("active = ?", true)

		if body.Name != nil && *body.Name != "" {
			query = query.Where("name ILIKE ?", "%"+*body.Name+"%")
		}
		if body.City != nil && *body.City != "" {
			query = query.Where("city ILIKE ?", "%"+*body.City+"%")
		}

		var users []User
		result := query.
			Order("created_at DESC").
			Offset(page * size).
			Limit(size).
			Find(&users)
		if result.Error != nil {
			c.JSON(http.StatusInternalServerError, gin.H{"error": result.Error.Error()})
			return
		}

		c.JSON(http.StatusOK, users)
	})

	if err := r.Run(":" + port); err != nil {
		log.Fatal(err)
	}
}
