import scrapy
from imaMember.items import ImamemberItem
from scrapy.spiders import Spider
from scrapy.spiders import CrawlSpider, Rule
from scrapy.selector import Selector
from scrapy.http import Request
import json

class ImaSpider(Spider):
	name = 'ima'
	allowed_domains = ['ima-india.org']
	start_urls = ['http://www.ima-india.org/demomembership/ima-member-sys-encr/server_processing.php?sEcho=1&iColumns=8&sColumns=&iDisplayStart=0&iDisplayLength=100&mDataProp_0=0&mDataProp_1=1&mDataProp_2=2&mDataProp_3=3&mDataProp_4=4&mDataProp_5=5&mDataProp_6=6&mDataProp_7=7&sSearch=mumbai&bRegex=false&sSearch_0=&bRegex_0=false&bSearchable_0=true&sSearch_1=&bRegex_1=false&bSearchable_1=true&sSearch_2=&bRegex_2=false&bSearchable_2=true&sSearch_3=&bRegex_3=false&bSearchable_3=true&sSearch_4=&bRegex_4=false&bSearchable_4=true&sSearch_5=&bRegex_5=false&bSearchable_5=true&sSearch_6=&bRegex_6=false&bSearchable_6=true&sSearch_7=&bRegex_7=false&bSearchable_7=true&iSortCol_0=0&sSortDir_0=asc&iSortingCols=1&bSortable_0=true&bSortable_1=true&bSortable_2=true&bSortable_3=true&bSortable_4=true&bSortable_5=true&bSortable_6=true&bSortable_7=true&_=1470210388768']

	custom_settings = {
		'DEPTH_LIMIT' : 2000 ,
		'DOWNLOAD_DELAY' : 4
	}

	def parse(self , response):
		hxs = response.body
		
		jsondata = json.loads(hxs)

		path = jsondata['aaData']
		no = len(path)
		total = jsondata['iTotalDisplayRecords']

		for i in range(0,no):
			item = ImamemberItem()
			if 'MUMBAI' in path[i][1]:
				item['branch'] = path[i][1]
				item['a_name'] = path[i][3] + path[i][4]
				item['postalcode'] = path[i][7]
				yield item

		pageNo = int(response.url.split('&')[3].split('=')[-1])

		if (pageNo+100) < total :
			next_url = 'http://www.ima-india.org/demomembership/ima-member-sys-encr/server_processing.php?sEcho=1&iColumns=8&sColumns=&iDisplayStart={x}&iDisplayLength=100&mDataProp_0=0&mDataProp_1=1&mDataProp_2=2&mDataProp_3=3&mDataProp_4=4&mDataProp_5=5&mDataProp_6=6&mDataProp_7=7&sSearch=mumbai&bRegex=false&sSearch_0=&bRegex_0=false&bSearchable_0=true&sSearch_1=&bRegex_1=false&bSearchable_1=true&sSearch_2=&bRegex_2=false&bSearchable_2=true&sSearch_3=&bRegex_3=false&bSearchable_3=true&sSearch_4=&bRegex_4=false&bSearchable_4=true&sSearch_5=&bRegex_5=false&bSearchable_5=true&sSearch_6=&bRegex_6=false&bSearchable_6=true&sSearch_7=&bRegex_7=false&bSearchable_7=true&iSortCol_0=0&sSortDir_0=asc&iSortingCols=1&bSortable_0=true&bSortable_1=true&bSortable_2=true&bSortable_3=true&bSortable_4=true&bSortable_5=true&bSortable_6=true&bSortable_7=true&_=1470210388768'.format(x=str(pageNo+100))
			yield Request(next_url,callback=self.parse)