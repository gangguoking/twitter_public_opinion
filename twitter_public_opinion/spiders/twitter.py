# -*- coding: utf-8 -*-
"""
Created on 2023/03/03 10:14

@author: hao.hu
"""

import json
import logging

import scrapy

from twitter_public_opinion import twitter_list
from twitter_public_opinion.lark import lark_robot_monitor
from twitter_public_opinion import settings


class TwitterSpider(scrapy.Spider):
    name = "twitter"
    allowed_domains = ["twitter.com"]
    url = "https://api.twitter.com/graphql/73BM9FU1mPITScnhs6iXug/UserTweets?variables={user_json}&features=%7B%22responsive_web_twitter_blue_verified_badge_is_enabled%22%3Atrue%2C%22responsive_web_graphql_exclude_directive_enabled%22%3Afalse%2C%22verified_phone_label_enabled%22%3Afalse%2C%22responsive_web_graphql_timeline_navigation_enabled%22%3Atrue%2C%22responsive_web_graphql_skip_user_profile_image_extensions_enabled%22%3Afalse%2C%22tweetypie_unmention_optimization_enabled%22%3Atrue%2C%22vibe_api_enabled%22%3Atrue%2C%22responsive_web_edit_tweet_api_enabled%22%3Atrue%2C%22graphql_is_translatable_rweb_tweet_is_translatable_enabled%22%3Atrue%2C%22view_counts_everywhere_api_enabled%22%3Atrue%2C%22longform_notetweets_consumption_enabled%22%3Atrue%2C%22tweet_awards_web_tipping_enabled%22%3Afalse%2C%22freedom_of_speech_not_reach_fetch_enabled%22%3Afalse%2C%22standardized_nudges_misinfo%22%3Atrue%2C%22tweet_with_visibility_results_prefer_gql_limited_actions_policy_enabled%22%3Afalse%2C%22interactive_text_enabled%22%3Atrue%2C%22responsive_web_text_conversations_enabled%22%3Afalse%2C%22longform_notetweets_richtext_consumption_enabled%22%3Afalse%2C%22responsive_web_enhance_cards_enabled%22%3Afalse%7D"
    start_urls = []

    def start_requests(self):
        """
        :return:
        """
        for user in twitter_list.user_dict:
            url = self.url.format(user_json=twitter_list.user_dict[user])
            yield scrapy.FormRequest(url=url,
                                     method="get",
                                     headers=settings.DEFAULT_REQUEST_HEADERS,
                                     dont_filter=True,
                                     meta={"twitter_user": user})

    def parse(self, response):
        twitter_id_set = settings.redis_tool.get_all(key=settings.TWITTER_REDIS_KEY)
        # twitter_user
        twitter_user = response.meta['twitter_user']

        json_data = json.loads(response.text)
        speech_list = json_data['data']['user']['result']['timeline_v2']['timeline']['instructions'][1]['entries']

        # twitter comments
        for row in speech_list:
            try:
                source_twitter_user = \
                row['content']['itemContent']['tweet_results']['result']['core']['user_results']['result']['legacy'][
                    'screen_name']
                source_twitter_user = "@" + source_twitter_user
                twitter_id = row['sortIndex']
                if twitter_id in twitter_id_set:
                    continue
                settings.redis_tool.set(key=settings.TWITTER_REDIS_KEY,
                                        field=twitter_id,
                                        val=None)
                created_at = row['content']['itemContent']['tweet_results']['result']['legacy']['created_at']
                if 'tweet' in row['content']['itemContent']['tweet_results']['result']:
                    twitter_comments = row['content']['itemContent']['tweet_results']['result']['tweet']['legacy'][
                        'full_text']
                else:
                    twitter_comments = row['content']['itemContent']['tweet_results']['result']['legacy']['full_text']

                lark_content = "user_link: https://twitter.com/{twitter_user}\n\n\n{twitter_comments}".format(
                    twitter_user=twitter_user,
                    twitter_comments=twitter_comments)

                # If it is original
                if str(twitter_user) == source_twitter_user:
                    lark_robot_monitor.send_lark(twitter_user=twitter_user,
                                                 created_at=created_at,
                                                 lark_content=lark_content)
                # If it is retransfer
                else:
                    lark_twitter_user = "{twitter_user} retransfer {source_twitter_user}".format(
                        twitter_user=twitter_user, source_twitter_user=source_twitter_user)
                    lark_robot_monitor.send_lark(twitter_user=lark_twitter_user,
                                                 created_at=created_at,
                                                 lark_content=lark_content)

                # setting log_message
                log_message = "{twitter_user}\n {source_twitter_user}\n {created_at}\n {twitter_comments}\n".format(
                    twitter_user=twitter_user,
                    source_twitter_user=source_twitter_user,
                    created_at=created_at,
                    twitter_comments=twitter_comments
                )
                logging.info(log_message)
            except Exception as exc:
                logging.warning(exc)
                continue


# use scrapy，local
if __name__ == '__main__':
    from scrapy import cmdline

    args = "scrapy crawl twitter".split()
    cmdline.execute(args)
