import scrapy

from scrapy.pipelines.images import ImagesPipeline


class DoubanSpider(scrapy.Spider):
    name = 'douban'
    allowed_domains = ['movie.douban.com']
    start_urls = ['https://movie.douban.com/cinema/nowplaying/beijing/']

    def start_requests(self):
        # 设置请求头
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3',
        }

        # 设置Cookie
        # cookies = {
        #     'name': 'value',
        #     'other_cookie': 'other_value',
        # }
        # 发送请求，并在请求中设置headers和cookies
        for url in self.start_urls:
            yield scrapy.Request(url, headers=headers, callback=self.parse)

    def parse(self, response, **kwargs):
        movie_list = response.css('.mod-bd .lists .list-item')
        for movie in movie_list:
            title = movie.css('li.stitle a::text').get()
            score = movie.css('li.srating .subject-rate::text').get()
            director = movie.css('li[data-director]::attr(data-director)').get()
            actors = movie.css('li[data-actors]::attr(data-actors)').get()
            poster = movie.css('li.poster a img::attr(src)').get()
            new_poster = poster.replace(".jpg", ".webp")
            movie_detail=movie.css('li.poster a::attr(href)').get()
            print(new_poster)
            # self.log(f'Title: {title}, score: {score}, Director: {director}, Actors: {actors},poster:{poster}')
            yield {
                'title': title,
                'score': score,
                'director': director,
                'actors': actors,
                'poster': new_poster,
                'movie_url':movie_detail
            }
