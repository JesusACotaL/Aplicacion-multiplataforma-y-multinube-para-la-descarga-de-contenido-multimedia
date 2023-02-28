package main

import (
	//"encoding/json"
	"fmt"
	// "log"
	"github.com/aws/aws-lambda-go/lambda"
	"github.com/gocolly/colly"
)

type ChapterSearchItem struct {
	Name string `json:"name"`
	Url string `json:"url"`
}

type MyEvent struct {
	Body struct {
		Url string `json:"url"`
	} `json:"body"`
}

type MyResponse struct {
	SearchItems []ChapterSearchItem `json:"search_items"`
}

func main() {
	lambda.Start(HandleLambdaEvent)
}

func HandleLambdaEvent(event MyEvent)(MyResponse, error){
	// Instantiate default collector
	c := colly.NewCollector(
		colly.AllowedDomains("m.manganelo.com", "chapmanganelo.com"),
	)

	// On every a element which has li[class=a-h]
	searchItems := []ChapterSearchItem{}
	c.OnHTML("li[class=a-h]", func(e *colly.HTMLElement) {
		item := ChapterSearchItem{
			Name: e.ChildText("a"),
			Url: e.ChildAttr("a", "href"),
		}

		searchItems = append(searchItems, item)
	})

	// "Visiting..."" log message
	c.OnRequest(func(r *colly.Request) {
		fmt.Println("Visiting", r.URL.String())
	})

	c.Visit(event.Body.Url)

	return MyResponse{
		SearchItems: searchItems,
		}, nil
}
