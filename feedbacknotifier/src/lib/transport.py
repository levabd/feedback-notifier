# coding=utf-8

from feedbacknotifier.src.lib import logger
import settings
import json
import datetime
import pytz
import requests
import feedback


def post_to_slack(feedback_message):
    """
    :type feedback_message: feedback.Feedback
    """

    __metadata_fields = {
        "productName": "Device model",
        "manufacturer": "Device manufacturer",
        "screenWidthPx": "Screen Width in PX",
        "screenHeightPx": "Screen Height in PX",
        "deviceClass": "Type of device",
        "screenDensityDpi": "Screen Density in DPI",
        "nativePlatform": "Hardware platform",
        "ramMb": "RAM (in MB)",
        "cpuModel": "CPU model",
        "cpuMake": "Type of CPU (Mark)",
        "glEsVersion": "OpenGL ES version"
    }

    __markets = {
        'ios':      'App Store',
        'android':  'Google Play'
    }

    __android_versions = {
        1: 'The original, first, version of Android. Yay!',
        2: 'Android 1.1',
        3: 'Android 1.5 Cupcace',
        4: 'Android 1.6 Donut',
        5: 'Android 2.0 Eclair',
        6: 'Android 2.0.1 Eclair',
        7: 'Android 2.1 Eclair',
        8: 'Android 2.2 Froyo',
        9: 'Android 2.3 Gingerbread',
        10: 'Android 2.3.3 Gingerbread',
        11: 'Android 3.0 Honeycomb',
        12: 'Android 3.1 Honeycomb',
        13: 'Android 3.2 Honeycomb',
        14: 'Android 4.0 Ice-cream sandwich',
        15: 'Android 4.0.3 Ice-cream sandwich',
        16: 'Android 4.1 Jelly Bean',
        17: 'Android 4.2 Jelly Bean',
        18: 'Android 4.3 Jelly Bean',
        19: 'Android 4.4 KitKat',
        20: 'Android 4.4W KitKat Watch',
        21: 'Android 5.0 Lollipop',
        22: 'Android 5.1 Lollipop',
        23: 'Android 6.0 Marshmallow',
        24: 'Android 7.0 Nougat',
        25: 'Android 7.1.1 Nougat',
        10000: 'Android development build o_0'
    }

    __emoji = {
        1: ':thunder_cloud_and_rain:',
        2: ':rain_cloud:',
        3: ':cloud:',
        4: ':partly_sunny:',
        5: ':sunny:',
        None: ':partly_sunny:'
    }
    __colors = {
        1: '#CC2525',
        2: '#CC2525',
        3: '#E8AD0C',
        4: '#30E80C',
        5: '#30E80C',
        None: '#E8AD0C'
    }
    __stars = {
        1: u'★☆☆☆☆',
        2: u'★★☆☆☆',
        3: u'★★★☆☆',
        4: u'★★★★☆',
        5: u'★★★★★',
        None: ''
    }

    def __convert_timezone(dt, tz_old, tz_new):
        return tz_old.localize(dt).astimezone(tz_new)

    def __get_date_string(timestamp, os):
        return str(
            __convert_timezone(
                datetime.datetime.fromtimestamp(timestamp),
                # Need to convert timezone before beatifying if `ios` OS
                pytz.timezone('GMT' if os == 'ios' else settings.NEEDED_TIMEZONE),
                pytz.timezone(settings.NEEDED_TIMEZONE)
            ).strftime('%d.%m.%Y %H:%M:%S'))

    device_and_os_version = u'[Device: %s], %s' % (
        feedback_message.device if feedback_message.device else '',
        __android_versions[feedback_message.os_version] if feedback_message.os_version else '')
    payload = {
        'attachments':
            [
                {
                    'title': 'New Feedback from ' + __markets[
                        feedback_message.os],
                    'color': __colors[feedback_message.rating],
                    'text': u'{stars}\n{summary}\n\n_*{author}*_, {date} '
                            u'v{version}\n{device_and_osv}'.format(
                      stars=__stars[feedback_message.rating],
                      summary=feedback_message.comment,
                      author=feedback_message.author or u'-',
                      date=__get_date_string(feedback_message.updated_at,
                                             feedback_message.os),
                      version=u'[%s]' % feedback_message.app_version if
                              feedback_message.app_version else '',
                      device_and_osv=device_and_os_version if
                              feedback_message.os == 'android' else ''
                    ),
                    "mrkdwn_in": ["text"],
                }
            ],
        'username': settings.SLACK_INCOMING_USER,
        "icon_emoji": __emoji[feedback_message.rating],
        "channel": settings.SLACK_INCOMING_CHANNEL
    }
    fields = []
    if feedback_message.device_metadata:
        fields.extend([
            {
                "title": __metadata_fields[key],
                "value": hex(value) if key == 'glEsVersion' else value,
                "short": True
            } for key, value in feedback_message.device_metadata.iteritems()])
        payload['attachments'][0]['fields'] = fields

    r = requests.post(settings.SLACK_INCOMING_WEB_HOOK, json.dumps(payload),
                      headers={'content-type': 'application/json'},
                      timeout=settings.REQUEST_TIMEOUT)
    if r.status_code == requests.codes.ok:
        logger.info("Message to Slack was sent")
        return True
    else:
        logger.error("Can`t send message to Slack")
        return False
