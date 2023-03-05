import json
import logging

import scrapy

from twitter_public_opinion import twitter_list


class TwitterSpider(scrapy.Spider):
    name = "twitter"
    allowed_domains = ["twitter.com"]
    url = "https://api.twitter.com/graphql/73BM9FU1mPITScnhs6iXug/UserTweets?variables={user_json}&features=%7B%22responsive_web_twitter_blue_verified_badge_is_enabled%22%3Atrue%2C%22responsive_web_graphql_exclude_directive_enabled%22%3Afalse%2C%22verified_phone_label_enabled%22%3Afalse%2C%22responsive_web_graphql_timeline_navigation_enabled%22%3Atrue%2C%22responsive_web_graphql_skip_user_profile_image_extensions_enabled%22%3Afalse%2C%22tweetypie_unmention_optimization_enabled%22%3Atrue%2C%22vibe_api_enabled%22%3Atrue%2C%22responsive_web_edit_tweet_api_enabled%22%3Atrue%2C%22graphql_is_translatable_rweb_tweet_is_translatable_enabled%22%3Atrue%2C%22view_counts_everywhere_api_enabled%22%3Atrue%2C%22longform_notetweets_consumption_enabled%22%3Atrue%2C%22tweet_awards_web_tipping_enabled%22%3Afalse%2C%22freedom_of_speech_not_reach_fetch_enabled%22%3Afalse%2C%22standardized_nudges_misinfo%22%3Atrue%2C%22tweet_with_visibility_results_prefer_gql_limited_actions_policy_enabled%22%3Afalse%2C%22interactive_text_enabled%22%3Atrue%2C%22responsive_web_text_conversations_enabled%22%3Afalse%2C%22longform_notetweets_richtext_consumption_enabled%22%3Afalse%2C%22responsive_web_enhance_cards_enabled%22%3Afalse%7D"
    start_urls = []
    twitter_header = {
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

    def start_requests(self):
        """
        :return:
        """
        for user in twitter_list.user_dict:
            url = self.url.format(user_json=twitter_list.user_dict[user])
            print(url)
            yield scrapy.FormRequest(url=url,
                                     method="get",
                                     headers=self.twitter_header,
                                     dont_filter=True,
                                     meta={"twitter_user": user})
            # break

    def parse(self, response):
        # twitter_user
        twitter_user = response.meta['twitter_user']
        logging.info(twitter_user)
        json_data = json.loads(response.text)
        speech_list = json_data['data']['user']['result']['timeline_v2']['timeline']['instructions'][1]['entries']

        # twitter comments
        for row in speech_list:
            created_at = row['content']['itemContent']['tweet_results']['result']['legacy']['created_at']
            try:
                if 'tweet' in row['content']['itemContent']['tweet_results']['result']:
                    twitter_comments = row['content']['itemContent']['tweet_results']['result']['tweet']['legacy']['full_text']
                else:
                    twitter_comments = row['content']['itemContent']['tweet_results']['result']['legacy']['full_text']
                print(twitter_user, created_at, twitter_comments)
            except Exception as exc:
                logging.warning(exc)
                continue


# use scrapy，local
if __name__ == '__main__':
    from scrapy import cmdline

    args = "scrapy crawl twitter".split()
    cmdline.execute(args)
