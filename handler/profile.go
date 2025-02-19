package handler

import (
	"net/http"
	"github.com/gin-gonic/gin"
)

func GetAllProfiles(ctx *gin.Context) {
	ctx.IndentedJSON(http.StatusOK, gin.H{"message": "Success!~"})
}

func GetProfile(ctx *gin.Context) {

}

func AddProfile(ctx *gin.Context) {

}

func DeleteProfile(ctx *gin.Context) {

}

func UpdateProfile(ctx *gin.Context) {

}