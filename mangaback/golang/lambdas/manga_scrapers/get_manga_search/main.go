package main

import (
	//"encoding/json"
	"fmt"
	// "log"
	"github.com/aws/aws-lambda-go/lambda"
	"github.com/gocolly/colly"
)

type MangaSearchItem struct {
	Title string `json:"title"`
	Author string `json:"author"`
	LastChapter string `json:"last-chapter"`
	ImgUrl string `json:"image-url"`
}

type MyEvent struct {
	Body struct {
		Url string `json:"url"`
	} `json:"body"`
}

type MyResponse struct {
	SearchItems []MangaSearchItem `json:"search_items"`
}

func main() {
	lambda.Start(HandleLambdaEvent)
}

func HandleLambdaEvent(event MyEvent)(MyResponse, error){
	// Instantiate default collector
	c := colly.NewCollector(
		// Visit only domains: hackerspaces.org, wiki.hackerspaces.org
		colly.AllowedDomains("m.manganelo.com"),
	)

	// On every a element which has href attribute call callback
	searchItems := []MangaSearchItem{}
	c.OnHTML("div[class=search-story-item]", func(e *colly.HTMLElement) {
		item := MangaSearchItem{
			Title: e.ChildText("h3"),
			Author: e.ChildText("span.item-author"),
			LastChapter: e.ChildText("a:nth-child(2)"),
			ImgUrl: e.ChildAttr("h3 a", "href"),
		}
		//fmt.Printf("title: %q\n", e.ChildText("h3"))
		//fmt.Printf("title: %q\n", e.ChildText("h3"))

		searchItems = append(searchItems, item)
	})

	// Before making a request print "Visiting ..."
	c.OnRequest(func(r *colly.Request) {
		fmt.Println("Visiting", r.URL.String())
	})

	// Start scraping on https://hackerspaces.org
	//c.Visit("https://m.manganelo.com/search/story/dragon_ball")
	c.Visit(event.Body.Url)

	return MyResponse{
		SearchItems: searchItems,
		}, nil
}


