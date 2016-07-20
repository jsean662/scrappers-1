import scrapy
from scrapy.spiders import Spider
from scrapy.selector import Selector
from scrapy.http import Request
from scrapy.http import FormRequest
from scrapy.utils.response import open_in_browser

class Formfill(Spider):
    name = 'form'
    
    allowed_domains = ['magicbricks.com']
    start_urls = ['http://www.magicbricks.com/Real-estate-property-agents/agent-in-Mumbai?proptype=Multistorey-Apartment,Builder-Floor-Apartment,Penthouse,Studio-Apartment,Residential-House,Villa&category=R&price=Y&source=HomePage&tab1Agent=property&page=1&bar_propertyType_new=10002_10003_10021_10022_10020,10001_10017&mbTrackSrc=tabChange']
    
    def parse(self,response):
        
        
        yield FormRequest.from_response(response,
                                        formxpath=".//*[@id='viewPhoneBtn5920621']",
                                        clickdata={ 'id' : 'viewPhoneBtn5920621' },
                                        callback=self.parse1)
                                        
    def parse1(self, response):
        open_in_browser(response)                                    
