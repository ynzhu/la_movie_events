#coding: utf-8
import scrapy
import os

class QuotesSpider(scrapy.Spider): 
    name = "ucla_events"
    
    def start_requests(self):
        start_urls = [
        'https://www.cinema.ucla.edu/events',
        ]
        filename = './data/ucla_events.csv'
        with open(filename, 'w') as f:
            pass
        for url in start_urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        # eventname = response.css('.series-title p').extract()
        # moviename = response.css('.event-name p').extract()
        # eventtime = response.css('.event-time').extract()
        # eventdate_month = response.css('.month').extract()
        # eventdate_date = response.css('.date').extract()
        # eventdate_day = response.css('.day').extract()
        # eventdate = list(zip(eventname, moviename, eventtime))

        # output = list(zip(eventname, moviename, eventtime))
        # print(eventdate)
        # print(output)
        def clean_tag(lst):
            return lst[0].split('>')[1].split('<')[0].strip().replace(',',' ')
        if response.css('.field-name-field-event .field-item a').extract():
            moviename = response.css('.default-title p').extract()
            eventname = response.css('.field-name-field-event .field-item a').extract()
            location = response.css('.field-name-field-location .field-item a').extract()
            eventtime = response.css('.field-name-field-datetime span').extract()
            link = response.url
            moviename = clean_tag(moviename)
            eventname = clean_tag(eventname)
            location = clean_tag(location)
            eventtime = clean_tag(eventtime)
            if not os.path.exists('./data'):
                os.mkdir('data')
            filename = './data/ucla_events.csv'
            with open(filename, 'a') as f:
                f.write(eventname+','+moviename+','+eventtime+','+location+','+link+'\n')
            self.log("Saved file %s" % filename)

        next_page = response.css('.event-name a::attr("href")')
        next_page += response.css('li.pager-item a::attr("href")')
        # next_page = None
        if next_page is not None:
            for href in next_page:
                yield response.follow(href, self.parse)

