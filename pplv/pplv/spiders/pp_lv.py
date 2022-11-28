import scrapy
from scrapy_splash import SplashRequest

lua_script="""
function main(splash, args)
    splash.resource_timeout = 0
    splash.private_mode_enabled = false
    assert(splash:go(args.url))
    assert(splash:wait(3))
    return {
        html = splash:html(),
    }
end
"""


class CarsSpider(scrapy.Spider):
    name = "pp_lv"
    
    def start_requests(self):
        url = 'https://pp.lv/lv/transports-un-tehnika/vieglie-auto?page=1'
        
        yield SplashRequest(
            url, 
            callback=self.parse, 
            endpoint='execute',
            args={'wait': 3, 'lua_source': lua_script,  url :'https://pp.lv/lv/transports-un-tehnika/vieglie-auto?page=1'}
            )
        
    def parse(self, response):
        for link in response.css('div.pp-list-view a::attr(href)'):
            yield response.follow(link.get(), callback=self.parse_ads)
    
    def parse_ads(self, response):
        yield {
            'title': response.css('title::text').get()
        }
            
            
        # details = response.css('div.single-pp-data.row')
        # for detail in details:
        #     yield{
        #         'year': detail.css('div.single-pp-data-value col-6 col-sm-7::text').get()
        #     }
        



# ---Data from main ads page---
# def parse(self, response):
#   cars = response.css('div.list-content')
#   for car in cars:
#       info = car.css('div.filter-list')
#       for item in info:
#           yield{
#               'name': car.css('strong.d-none.d-md-block::text').get(),
#               'link': car.css('div::text').get(),
#               }
    