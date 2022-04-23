import json
import regex

from pkg.spiders.main_spider import MainSpider

from scrapy.cmdline import execute
from scrapy.crawler import CrawlerProcess

from pkg.parse_robots_files import robots_parser

desktop_agents = [
    # 'Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)'
    'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.99 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.99 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.99 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_1) AppleWebKit/602.2.14 (KHTML, like Gecko) Version/10.0.1 Safari/602.2.14',
    'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.71 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.98 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.98 Safari/537.36',
    'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.71 Safari/537.36',
    'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.99 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:50.0) Gecko/20100101 Firefox/50.0',
]

folder = 'static/'

def parse(url):
	use_js_rendering = True 
	page_limit = 50
	
	filename = generate_filename(folder)

	generate_subprocess(filename, page_limit=page_limit, other_urls=[url], use_js_rendering=use_js_rendering)
	
	robots_url = robots_parser.get_robots_url(url)
	generate_subprocess(filename, page_limit=page_limit, sitemap_urls=[robots_url], use_js_rendering=use_js_rendering)
	
	text = read_file(filename)

	# if (len(text) < 2000):
		# robots_url = robots_parser.get_robots_url(url)
		# generate_subprocess(filename, page_limit=page_limit, sitemap_urls=[robots_url], use_js_rendering=use_js_rendering)
		# text = read_file(filename)

	clear_folder(filename)
	text = regex.sub(r"\\n+", ' ', text).strip()

	return get_cyrillic_and_latin(text)
	return "text: " + text
	return get_pure_text(text)


# TEXT
def get_pure_text(text=""):
	return regex.sub(r"[^\p{L}\s]+", ' ', text).strip()

def get_cyrillic_and_latin(text=""):
	# \p{Script=Cyrillic}
	return regex.sub(r"[^A-Za-z^А-Яа-я]+", ' ', text).strip()



# PROCESSING
def generate_subprocess(filename, page_limit=5, other_urls=[], sitemap_urls=[], use_js_rendering=True):
	from multiprocessing import Process
	p = Process(target=execute_crawling, args=(filename, page_limit, other_urls, sitemap_urls, use_js_rendering))
	p.start()
	p.join() # this blocks until the process terminates

def execute_crawling(filename, page_limit, other_urls, sitemap_urls, use_js_rendering):
	from random import choice
	
	process = CrawlerProcess(settings={
    	"FEEDS": {
	    	filename: {"format": "jsonlines"},
    	},
    	'CLOSESPIDER_PAGECOUNT': page_limit,
		'USER_AGENT': choice(desktop_agents),
		'CLOSESPIDER_TIMEOUT': 60,
	}) #same way can be done for Crawlrunner
	process.crawl(MainSpider, other_urls=other_urls, sitemap_urls=sitemap_urls, use_js_rendering=use_js_rendering)
	process.start()



# FILESYSTEM
def generate_filename(folder_name=""):
	import secrets 
	hash = secrets.token_urlsafe(32)
	filename = folder + hash + '.json'
	return filename

def read_file(filename=""):
	file = open(filename, "r")
	text = file.read()
	file.close()

	return text

# def clear_folder(folder_name=""):
def clear_folder(filename=""):
	import glob, time, os, os.path
	os.remove(filename)
	
	# delete old files (> 1hour)
	now = time.time()
	for f in os.listdir(folder):
		f = os.path.join(folder, f)

		if os.stat(f).st_mtime < now - 1 * 3600:
			if os.path.isfile(f):
				os.remove(f)

	# filelist = glob.glob(os.path.join(folder, "*.json"))
	# for f in filelist:
		# os.remove(f)