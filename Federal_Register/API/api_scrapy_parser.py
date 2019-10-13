import scrapy
import json
import arrow

class RegisterApiSpider(scrapy.Spider):

    name = "API"
    #API only allows 2000 results per query, date range filters are recommended
    #https://www.federalregister.gov/reader-aids/developer-resources/rest-api
    query_form ='https://www.federalregister.gov/api/v1/documents.json?'\
    'per_page=1000&order=oldest&conditions[publication_date][is]={date}'
    
    #get all the dates possible
    start_date = arrow.get('1994-01-03')
    end_date = arrow.utcnow().floor("day")
    dates = [date.format("YYYY-MM-DD") \
            for date in arrow.Arrow.range('day',start_date,end_date)]

    start_urls = [query_form.format(date=date) for date in dates]
    #e.g. www.federalregister.gov/api/v1/documents.json?per_page=1000&order=oldest&conditions[publication_date][is]=1994-01-03'
    
    def parse(self,response):
        #load the response as a json document
        j = json.loads(response.text)
        #we've included some weekends etc. where nothing is published,
        #avoid throwing an error
        if j['count']==0:
            return
        #the results are simply json, so we can yield them directly
        for result in j["results"]:
            yield result
        #probably there will never be more than 1,000 rules published on a day
        #however in case
        if j.has_key("next_page_url"):
            yield scrapy.Request(j['next_page_url'],self.parse)
        
            
        
        
        
