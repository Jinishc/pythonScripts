import scrapy

from tripadvisor.items import TAitem

class ReviewSpider(scrapy.Spider):
	name = "tr"
	allowed_domains = ["http://www.tripadvisor.in/"]
	start_urls = [
"http://www.tripadvisor.in/Hotel_Review-g297600-d6476284-Reviews-The_Deltin_Hotel_Casino-Daman_Daman_and_Diu.html",
]

	def parse(self, response):

		# getting the last page number
		end_page = int(response.css("a.pageNum::text").extract()[-1])*10
        
        # breaking the url to generate page urls
		break_url_at = self.start_urls[0].index("Reviews") + 7

		url1 = self.start_urls[0][:break_url_at + 1]

		url2 = self.start_urls[0][break_url_at + 1:]
        

        #generating urls and queing it for sending GET requests
		for i in range(10,end_page,10):

			url = url1 + "or" + str(i) + "-" + url2
			yield scrapy.Request(url, callback=self.parse_dir_contents)

	def parse_dir_contents(self, response):
		for sel in response.css('div.reviewSelector'):
			item = TAitem()
			item['username'] = sel.css('div.username > span :: text').extract()
			item['user_place'] = sel.css('div.username > .location :: text').extract()
			item['date'] = sel.css('span.ratingDate::text').extract()
			item['review_title'] = sel.css('span.noQuotes::text').extract()
			item['review'] = sel.css('p.partial_entry::text').extract()
			yield item
