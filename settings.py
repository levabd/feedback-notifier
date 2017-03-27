import os
# noinspection PyPackageRequirements
from dotenv import load_dotenv


def str2bool(v):
    return v.lower() in ("yes", "true", "t", "1")

dotenv_path = os.path.join(os.path.dirname(__file__), '.env')
load_dotenv(dotenv_path)

FEEDBACK_NOTIFIER_GLOBAL_LOG = str2bool(os.environ.get(
    "FEEDBACK_NOTIFIER_GLOBAL_LOG"))
LOG_PATH = os.environ.get("LOG_PATH")
GOOGLEPLAY_KEY_FILE = os.environ.get("GOOGLEPLAY_KEY_FILE")
GOOGLEPLAY_PACKAGE = os.environ.get("GOOGLEPLAY_PACKAGE")
APPSTORE_APP_ID = os.environ.get("APPSTORE_APP_ID")
SLACK_INCOMING_WEB_HOOK = os.environ.get("SLACK_INCOMING_WEB_HOOK")
SLACK_INCOMING_USER = os.environ.get("SLACK_INCOMING_USER")
SLACK_INCOMING_CHANNEL = os.environ.get("SLACK_INCOMING_CHANNEL")
IOS_LANGUAGES = os.environ.get("IOS_LANGUAGES")
REQUEST_TIMEOUT = int(os.environ.get("REQUEST_TIMEOUT"))
NEEDED_TIMEZONE = os.environ.get("NEEDED_TIMEZONE")
