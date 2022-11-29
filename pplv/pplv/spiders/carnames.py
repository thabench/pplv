import scrapy
import json

class CarsNamesSpider(scrapy.Spider):
    name = "car_names"
    start_urls = ['https://apipub.pp.lv/lv/api_user/v1/slugs/categories/transports-un-tehnika/vieglie-auto/subcategories']
    
    def parse(self, response):
        raw_data = response.body
        data = json.loads(raw_data)
        
        # saving existing car names in file
        with open('scraped_names.txt', 'w', encoding='utf-8') as f:
            for carname in data['content']['children']:
                f.write("%s\n" % carname['name'])
            
            