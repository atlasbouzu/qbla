package main

import (
	// "net/http"
	"github.com/gin-gonic/gin"
	"athomaslab/qbla/handler"
)

func main() {
	router := gin.Default()
	/**
		TO DO: Add grouped routes for auth required routes.
	*/
	// router.POST("/auth", authUser)
	
	router.GET("/users/:userId/profiles", handler.GetAllProfiles)
	// router.GET("/users/:userId/profiles/:profileId", getAccountProfile)
	
	// router.GET("/users/:userId/profiles/:profileId/taxes", getTaxes)

	// router.GET("/users/:userId/profiles/:profileId/incomes", getIncomes)
	// router.POST("/users/:userId/profiles/:profileId/incomes", addIncome)
	
	// router.GET("/users/:userId/profiles/:profileId/expenditures", getExpenditures)
	// router.POST("/users/:userId/profiles/:profileId/expenditures", addExpenditures)
	
	// router.GET("/items", getExpendItems)
	// router.GET("/items/:itemId", getExpendItem)

	router.Run()
}