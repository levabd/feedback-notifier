# coding=utf-8

from collections import namedtuple
from feedbacknotifier.src.lib import logger
import settings
import json
import datetime
import feedparser
import requests
import sys
import inspect
from requests.exceptions import *
from time import mktime
import feedback

# noinspection PyUnresolvedReferences
import apiclient
import httplib2
from oauth2client.service_account import ServiceAccountCredentials


def get_ios_feedback_messages(limit=10):
    """
    :param limit: max number of returned feedback messages
    :rtype: list[feedback.Feedback]
    """
    langs = settings.IOS_LANGUAGES.split(',')
    urls = ['https://itunes.apple.com/%(language)s/rss/customerreviews/' \
            'id=%(app_id)s/sortBy=mostRecent/xml' %
            {'language': lang, 'app_id': settings.APPSTORE_APP_ID}
            for lang in langs]
    messages = []
    try:
        responses = [requests.get(url, headers={
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1)'},
                              timeout=settings.REQUEST_TIMEOUT)
                     for url in urls]
        for response in responses:
            response.encoding = 'utf-8'  # avoid charset not guessing correctly
            feed = feedparser.parse(response.text)

            if len(feed['entries']) < 2:
                logger.warning(
                    "Something happened with iOS feedback messages. We "
                    "received 0 messages. Try to check your apple id.")

            messages.extend([feedback.Feedback(
                os='ios',
                review_id=entry.id,
                author=entry.author,
                comment=entry.title + ' ' + entry.summary,
                updated_at=mktime(entry.updated_parsed),
                rating=int(entry.im_rating),
                device=None,
                os_version=None,
                app_version=entry.im_version,
                device_metadata=None
            ) for entry in feed['entries'][1:1 + limit]])
    except (HTTPError, ConnectionError, SSLError, ConnectTimeout, Timeout,
            TooManyRedirects, ProxyError, ContentDecodingError,
            ChunkedEncodingError, RequestException, ReadTimeout):
        logger.error("Can`t get request result from itunes.apple.com. "
                     "Something happened with apple or your internet. "
                     "Contact your server administrator.")

    logger.info("Last 10 iOS Feedback Messages successfully received")
    return messages


def get_android_feedback_messages(key_file_path, limit=10):
    """
    :param key_file_path: path to JSON key Google Play Android Developer API
    :param limit: max number of returned feedback messages
    :rtype: list[feedback.Feedback]
    """
    # noinspection PyBroadException
    try:
        credentials = ServiceAccountCredentials.from_json_keyfile_name(
            key_file_path,
            scopes='https://www.googleapis.com/auth/androidpublisher')
    except:
        logger.error("Can`t load credentials. The key file is empty or "
                     "corrupted. Contact your server administrator.")
        return []

    messages = []
    logger.info("Request for {0} started".format(settings.GOOGLEPLAY_PACKAGE))

    # noinspection PyBroadException
    try:
        service = apiclient.discovery.build(
            'androidpublisher', 'v2',
            http=credentials.authorize(httplib2.Http()))
        reviews_page = service.reviews().list(
            packageName=settings.GOOGLEPLAY_PACKAGE,
            maxResults=limit
        ).execute()
        reviews_list = reviews_page["reviews"]
        infinite_loop_canary = 5
        while "tokenPagination" in reviews_page:
            reviews_page = service.reviews().list(
                packageName=settings.GOOGLEPLAY_PACKAGE,
                token=reviews_page["tokenPagination"]["nextPageToken"],
                maxResults=limit).execute()
            reviews_list.extend(reviews_page["reviews"])
            infinite_loop_canary -= 1
            if infinite_loop_canary < 0:
                break

        messages.extend([feedback.Feedback(
            os='android',
            review_id=review["reviewId"],
            author=review["authorName"],
            comment=review['comments'][0]['userComment']['text'],
            updated_at=int(review['comments'][0]['userComment']['lastModified']
                           ['seconds']),
            rating=int(review['comments'][0]['userComment']['starRating']),
            device=review['comments'][0]['userComment']['device'],
            os_version=int(review['comments'][0]['userComment'][
                'androidOsVersion']),
            app_version=review['comments'][0]['userComment'][
                'appVersionName'] if 'appVersionName' in review[
                'comments'][0]['userComment'] else None,
            device_metadata=review['comments'][0]['userComment'][
                'deviceMetadata']
        ) for review in reviews_list[0:limit]])
    except IndexError:
        logger.error(sys.exc_info()[0])
        logger.error("No one valid version for {0} was found.".format(
            settings.GOOGLEPLAY_PACKAGE))
        return []
    except apiclient.errors.HttpError:
        logger.error(sys.exc_info()[0])
        logger.error("Can`t find package " + settings.GOOGLEPLAY_PACKAGE)
        return []
    except:
        logger.error(sys.exc_info()[0])
        logger.error("Can`t get android package feedback for some reason")
        return []

    return messages
