import scrapy


class WebsiteSpider(scrapy.Spider):
    name = "website"
    allowed_domains = ['google.com']
    # start_urls = ["https://www.worldometers.info/world-population/population-by-country/"]
    start_urls = ['https://www.google.com/search?q=site%3Ayoutube.com+openinapp.co&num=40000']

    def parse(self, response):
        results = response.css('div.yuRUbf')
        youtube_channels = []
        youtube_channel_name = []
        for result in results:
            link = result.css('a::attr(href)').get()
            if link.startswith('https://www.youtube.com/c/'):
                # youtube_channel_link = link.split('/url?q=')[1].split('&')[0]
                youtube_channels.append(link)
                name = link.split('/')[4]
                youtube_channel_name.append(name)
        print("Extracted YouTube Channels:", results)
        # print("Extracted Channel Names:", youtube_channel_name)

        yield {
            'youtube_channels': youtube_channels,
            'youtube_channel_name': youtube_channel_name,

        }