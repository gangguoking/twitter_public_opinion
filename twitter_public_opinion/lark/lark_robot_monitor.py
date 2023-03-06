# -*- coding: utf-8 -*-
"""
Created on 2022/6/13 10:14

@author: hao.hu
"""

import json
import logging

import requests

from scrapy.utils import conf


# lark_url
LARKURL = conf.closest_scrapy_cfg()


def send_lark(twitter_user, created_at, twitter_comments):
    """

    :param twitter_user:
    :param created_at:
    :param twitter_comments:
    :return:
    """
    headers = {
        'Content-Type': 'application/json'
    }

    card = {
        "msg_type": "interactive",
        "card": {
            # header
            "header": {
                "title": {
                    "tag": "plain_text",
                    "content": "{created_at}, {twitter_user}".format(created_at=created_at, twitter_user=twitter_user)
                },
                "template": "orange"
            },
            # element
            "elements": [
                #
                {
                    "tag": "hr"
                },
                # Market Share
                {
                    "tag": "div",
                    "text": {
                        "tag": "lark_md",
                        "content": twitter_comments
                    }
                },
                #
                {
                    "tag": "hr"
                }
            ]
        }
    }
    response = requests.post(LARKURL, headers=headers, data=json.dumps(card))
    logging.info(response.text)


if __name__ == '__main__':
    send_lark(twitter_user="cz_binance", created_at="2023-03-02", twitter_comments="btc fly!!!")
