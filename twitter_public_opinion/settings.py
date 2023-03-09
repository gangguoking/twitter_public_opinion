# Scrapy settings for twitter_public_opinion project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     https://docs.scrapy.org/en/latest/topics/settings.html
#     https://docs.scrapy.org/en/latest/topics/downloader-middleware.html
#     https://docs.scrapy.org/en/latest/topics/spider-middleware.html

from twitter_public_opinion.utils.config import get_config
from twitter_public_opinion.utils import redis_set_pool

BOT_NAME = "twitter_public_opinion"

SPIDER_MODULES = ["twitter_public_opinion.spiders"]
NEWSPIDER_MODULE = "twitter_public_opinion.spiders"

# lark_url
LARKURL = get_config("lark", "lark_url")

REDIS_HOST = get_config("redis", "host")
REDIS_PORT = int(get_config("redis", "port"))
REDIS_PASSWORD = get_config("redis", "password")
REDIS_DB = get_config("redis", "db")
TWITTER_REDIS_KEY = get_config("redis", "twitter_redis_key")

redis_tool = redis_set_pool.IndexTool(host=REDIS_HOST,
                                      port=REDIS_PORT,
                                      pwd=REDIS_PASSWORD,
                                      db=REDIS_DB)

"""
redis_tool.set(key=TWITTER_REDIS_KEY,
               field="1633721674121244673",
               val=None)

tem = redis_tool.get_all(key=TWITTER_REDIS_KEY)
print(tem)
"""

# Crawl responsibly by identifying yourself (and your website) on the user-agent
# USER_AGENT = "twitter_public_opinion (+http://www.yourdomain.com)"

# Obey robots.txt rules
ROBOTSTXT_OBEY = False

# Configure maximum concurrent requests performed by Scrapy (default: 16)
# CONCURRENT_REQUESTS = 32

# Configure a delay for requests for the same website (default: 0)
# See https://docs.scrapy.org/en/latest/topics/settings.html#download-delay
# See also autothrottle settings and docs
# DOWNLOAD_DELAY = 3
# The download delay setting will honor only one of:
# CONCURRENT_REQUESTS_PER_DOMAIN = 16
# CONCURRENT_REQUESTS_PER_IP = 16

# Disable cookies (enabled by default)
COOKIES_ENABLED = False

# Disable Telnet Console (enabled by default)
# TELNETCONSOLE_ENABLED = False

# Override the default request headers:
DEFAULT_REQUEST_HEADERS = {
        'authority': 'api.twitter.com',
        'accept': '*/*',
        'accept-language': 'en,zh-CN;q=0.9,zh;q=0.8',
        'authorization': 'Bearer AAAAAAAAAAAAAAAAAAAAANRILgAAAAAAnNwIzUejRCOuH5E6I8xnZz4puTs%3D1Zv7ttfk8LF81IUq16cHjhLTvJu4FA33AGWWjCpTnA',
        'content-type': 'application/json',
        'cookie': 'kdt=HEbiZg3taUjnw3DI579KYxKt55DVIYegXnTuluQR; guest_id=v1%3A167315514058656582; auth_token=904485ed7c8003132e03807aad9f8896495fdff0; ct0=c9af3604057e3b1131cd12884730e38b92bd4559dd2dde623fd61f6810a809cdec31ab2c7dbfcf62da5ebdabe4370c80c372043483c5f08ce90349e70855641b0c186041d9d412707a98134612fae5b0; twid=u%3D1519303115178004482; _ga_BYKEBDM7DS=GS1.1.1676798152.1.1.1676798523.0.0.0; _ga_ZJQNEMXF73=GS1.1.1676798523.2.0.1676798523.0.0.0; des_opt_in=Y; _gcl_au=1.1.1296960259.1676798827; mbox=PC#096b3483342548d089910069e1420199.38_0#1740195702|session#c7fbf217572946868015a50615f70b8f#1676952762; _ga_34PHSZMC42=GS1.1.1676950218.9.1.1676950904.0.0.0; _ga=GA1.2.291429187.1673073700; guest_id_marketing=v1%3A167315514058656582; guest_id_ads=v1%3A167315514058656582; _gid=GA1.2.1507049117.1678014999; personalization_id="v1_zmyEea/Lr6EkPfDDMhbGbw=="',
        'origin': 'https://twitter.com',
        'referer': 'https://twitter.com/',
        'sec-ch-ua': '"Chromium";v="110", "Not A(Brand";v="24", "Google Chrome";v="110"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"macOS"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-site',
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36',
        'x-csrf-token': 'c9af3604057e3b1131cd12884730e38b92bd4559dd2dde623fd61f6810a809cdec31ab2c7dbfcf62da5ebdabe4370c80c372043483c5f08ce90349e70855641b0c186041d9d412707a98134612fae5b0',
        'x-twitter-active-user': 'yes',
        'x-twitter-auth-type': 'OAuth2Session',
        'x-twitter-client-language': 'en',
}

# Enable or disable spider middlewares
# See https://docs.scrapy.org/en/latest/topics/spider-middleware.html
# SPIDER_MIDDLEWARES = {
#    "twitter_public_opinion.middlewares.TwitterPublicOpinionSpiderMiddleware": 543,
# }

# Enable or disable downloader middlewares
# See https://docs.scrapy.org/en/latest/topics/downloader-middleware.html
# DOWNLOADER_MIDDLEWARES = {
#    "twitter_public_opinion.middlewares.TwitterPublicOpinionDownloaderMiddleware": 543,
# }

# Enable or disable extensions
# See https://docs.scrapy.org/en/latest/topics/extensions.html
# EXTENSIONS = {
#    "scrapy.extensions.telnet.TelnetConsole": None,
# }

# Configure item pipelines
# See https://docs.scrapy.org/en/latest/topics/item-pipeline.html
# ITEM_PIPELINES = {
#    "twitter_public_opinion.pipelines.TwitterPublicOpinionPipeline": 300,
# }

# Enable and configure the AutoThrottle extension (disabled by default)
# See https://docs.scrapy.org/en/latest/topics/autothrottle.html
# AUTOTHROTTLE_ENABLED = True
# The initial download delay
# AUTOTHROTTLE_START_DELAY = 5
# The maximum download delay to be set in case of high latencies
# AUTOTHROTTLE_MAX_DELAY = 60
# The average number of requests Scrapy should be sending in parallel to
# each remote server
# AUTOTHROTTLE_TARGET_CONCURRENCY = 1.0
# Enable showing throttling stats for every response received:
# AUTOTHROTTLE_DEBUG = False

# Enable and configure HTTP caching (disabled by default)
# See https://docs.scrapy.org/en/latest/topics/downloader-middleware.html#httpcache-middleware-settings
# HTTPCACHE_ENABLED = True
# HTTPCACHE_EXPIRATION_SECS = 0
# HTTPCACHE_DIR = "httpcache"
# HTTPCACHE_IGNORE_HTTP_CODES = []
# HTTPCACHE_STORAGE = "scrapy.extensions.httpcache.FilesystemCacheStorage"

# Set settings whose default value is deprecated to a future-proof value
REQUEST_FINGERPRINTER_IMPLEMENTATION = "2.7"
TWISTED_REACTOR = "twisted.internet.asyncioreactor.AsyncioSelectorReactor"
FEED_EXPORT_ENCODING = "utf-8"
