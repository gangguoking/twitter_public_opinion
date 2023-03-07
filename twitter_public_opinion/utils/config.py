import configparser

from scrapy.utils import conf


# lark_url
config = conf.closest_scrapy_cfg()


def get_config(section, key):
    parser = configparser.ConfigParser()
    parser.read(config)
    return parser.get(section, key)
