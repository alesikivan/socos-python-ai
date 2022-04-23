import scrapy

class MainSpider(scrapy.spiders.SitemapSpider):
    name = 'main'
    custom_settings = {
        "SPLASH_URL": "http://splash:8050",
        "DOWNLOADER_MIDDLEWARES": {
            'scrapy_splash.SplashCookiesMiddleware': 723,
            'scrapy_splash.SplashMiddleware': 725,
            'scrapy.downloadermiddlewares.httpcompression.HttpCompressionMiddleware': 810,
        },
        "SPIDER_MIDDLEWARES": {
            'scrapy_splash.SplashDeduplicateArgsMiddleware': 100,
        },
        "DUPEFILTER_CLASS": 'scrapy_splash.SplashAwareDupeFilter',
        "HTTPCACHE_STORAGE": 'scrapy_splash.SplashAwareFSCacheStorage',

        "FEED_EXPORT_ENCODING": 'utf-8',
        # 'USER_AGENT': ,
        # "CLOSESPIDER_PAGECOUNT": 50,
    
        "DEFAULT_REQUEST_HEADERS": {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language': 'en, ru-RU',

            'cache-control': 'max-age=0',
            'cookie': 'cookieLanguageType=en;',
            'referer': 'https://www.google.com',
        },

        "COOKIES_ENABLED": False,
    }


    handle_httpstatus_list = [301, 302]
    sitemap_urls = [
        # 'https://docs.scrapy.org/robots.txt',
        # 'https://www.youtube.com/robots.txt'
    ]
    other_urls = [
        # 'https://www.coursera.org',
        # 'https://www.youtube.com/',
        # 'http://quotes.toscrape.com/tag/humor/',
    ]
    use_js_rendering = True


    def __init__(self, *a, **kw):
        super(MainSpider, self).__init__(*a, **kw)

        use_js_rendering = kw.get('use_js_rendering')
        self.use_js_rendering = use_js_rendering

    def start_requests(self):


        requests = list(super(MainSpider, self).start_requests())

        if (self.use_js_rendering):
            other_urls_requests = [scrapy.Request(x, self.parse, meta={
                'splash': {
                    'endpoint': 'render.html',
                    'args': {'wait': 0.1}
                }
            }) for x in self.other_urls]
        else: 
            other_urls_requests = [scrapy.Request(x, self.parse) for x in self.other_urls]

        requests += other_urls_requests
        return requests


    def parse(self, response):
        meta_tags = ['meta[name*="title"]', 'meta[property*="og:title"]', 'meta[name*="keywords"]', 'meta[name*="description"]', 'meta[property*="og:description"]']
        html_tags = ['title', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'nav', 'p', 'b', 'i', 'li', 'strong', 'em', 'blockquote', 'caption', 'abbr', 'data', 'mark', 'bdi', 'address', '.keywords', '.keyword', '.robot', '.primary', '.title', '.main', '.nav', '.contentinfo', '.content', '.info', 'a[rel*=author]',]

        # yield {"_": response.css('#video-title::text').getall()}

        for meta_tag in meta_tags:
            yield {'_': response.css(meta_tag + '::attr("content")').getall()}
            
            # yield {meta_tag: response.css(meta_tag + '::attr("content")').getall()}

        for html_tag in html_tags:
            yield {'_': response.css(html_tag + '::text').getall()}
            
            # yield {html_tag: response.css(html_tag + '::text').getall()}

        
