package main

import (
	"encoding/json"
	"fmt"
	"log"
	"github.com/aws/aws-lambda-go/lambda"
)

type MyEvent struct {
	Body struct {
		Url string `json:"url"`
	} `json:"body"`
}

type MyResponse struct {
	Message string `json:"message"`
}

func HandleLambdaEvent(event MyEvent)(MyResponse, error){
	return MyResponse{Message: "Esto es una lambda de GO :D"}, nil
}

func main() {
	event := MyEvent{}

	event.Body.Url = "https://chapmanganelo.com/manga-aa88620"

	js, err := json.Marshal(event)
	if err != nil {
		log.Println(err)
		return
	}
	s := string(js)
	fmt.Println(s)

}
