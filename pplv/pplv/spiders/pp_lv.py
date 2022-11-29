import scrapy
from scrapy.exceptions import CloseSpider
import json

class CarsSpider(scrapy.Spider):
    name = "pp_lv"
    start_urls = [f'https://apipub.pp.lv/lv/api_user/v1/categories/2/lots?orderColumn=publishDate&orderDirection=DESC&currentPage=1&itemsPerPage=20']
    page_number = 1
    car_names = []
    
    def parse(self, response):
        raw_data = response.body
        data = json.loads(raw_data)
        
        # loading scraped existing car names from file
        with open('scraped_names.txt', 'r', encoding='utf-8') as f:
            for line in f:
                x = line[:-1]
                self.car_names.append(x)
            
        
        # check if cars data are in response
        if data['content']['data'] == []:
            raise CloseSpider('No more cars in response')
        
        # loop through every car
        for car in data['content']['data']:
            year = ''
            mileage = ''
            vin = ''
            plate = ''
            
            # loop through car details and assign if exists
            for detail in car['adFilterValues']:
                if detail['filter']['name'] == 'Izlaiduma gads':
                    year = detail['value']['displayValue']
                if detail['filter']['name'] == 'Nobraukums, km':
                    mileage = detail['textValue']
                if detail['filter']['name'] == 'VIN kods':
                    vin = detail['textValue']
                if detail['filter']['name'] == 'Auto numurs':
                    plate = detail['textValue']    
            
            # check bad car make names, add car
            if car['category']['parent']['name'] == 'Vieglie auto':
                yield{
                'Make': car['category']['name'],
                'Model': car['category']['name'],
                'Year': year,
                'Mileage':mileage,
                'VIN': vin,
                'Plate': plate,
                }
            if car['category']['parent']['name'] != 'Vieglie auto' and car['category']['parent']['name'] not in self.car_names: 
                yield{
                'Make': car['category']['parent']['parent']['name'],
                'Model': car['category']['name'],
                'Year': year,
                'Mileage':mileage,
                'VIN': vin,
                'Plate': plate,
                }
            else:
                yield{
                'Make': car['category']['parent']['name'],
                'Model': car['category']['name'],
                'Year': year,
                'Mileage':mileage,
                'VIN': vin,
                'Plate': plate,
                }
        
        # go to next page
        self.page_number += 1
        next_page = f'https://apipub.pp.lv/lv/api_user/v1/categories/2/lots?orderColumn=publishDate&orderDirection=DESC&currentPage={self.page_number}&itemsPerPage=20'
        yield response.follow(next_page, callback=self.parse)