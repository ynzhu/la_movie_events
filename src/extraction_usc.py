#coding: utf-8
import scrapy
import os

class QuotesSpider(scrapy.Spider):
    name = "quotes"

    def start_requests(self):
        with open('./data/usc_events.csv','w') as f:
            pass

        urls = [
            'https://cinema.usc.edu/events/index.cfm'
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        #print("/n")
        element = response.css('div.events h2').extract()
        #self.log("aaaa")  a::attr("href")

        title = response.css('div.events h2').extract()#[0]#.split("<")[1].split(">")[1]
        time = response.css('div.events em').extract()#[0]
        location = response.css('div.events span').extract()#[0]
        movie = response.css('h2 em strong').extract()
        movie2 = response.css('h2 strong em').extract()
        link = response.url
       
        if movie:
            pass 
        elif movie2:
            movie = movie2
        else:
            movie = ""


        if title and time and location:
            tit = title[0].split("<")[1].split(">")[1].replace(',',' ')
            tim = time[0].split("<")[1].split(">")[1].replace(',',' ')
            loc = location[0].split("<")[1].split(">")[1].replace(',',' ')
            if movie:
                mov = movie[0].split("<")[1].split(">")[1].replace(',',' ')
            else:
                mov = ""

           

            with open('./data/usc_events.csv','a') as f:
                f.write(tit + "," + mov + ","+ tim + "," + loc + "," + link + "\n")


        next_page = response.css('div.col-lg-12 h5 a::attr("href")').extract()
        if next_page is not None:
            for href in next_page:
                yield response.follow(href, self.parse)








