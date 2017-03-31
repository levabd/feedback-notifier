# coding=utf-8

from lib import logger
import sqlite3
import os
import settings
import lib.transport as transport
import lib.parsers as parsers
import lib.feedback


class Notifier(object):

    def __init__(self, base_path):

        self.__base_path = base_path
        self.__googleplay_key_file = os.path.join(base_path,
                                                  settings.GOOGLEPLAY_KEY_FILE)

    def run(self):
        returned_messages = parsers.get_ios_feedback_messages(10)
        returned_messages.extend(parsers.get_android_feedback_messages(
            self.__googleplay_key_file, 10))

        db_path = os.path.join(self.__base_path, "db/feedback_messages.db")
        conn = sqlite3.connect(db_path)
        c = conn.cursor()
        for message in returned_messages:
            c.execute(
                "SELECT * FROM feedback_messages WHERE os = ? AND id = ?",
                (message.os, message.id))
            if c.fetchone() is None:
                transport.post_to_slack(message)
                c.execute(
                  "INSERT INTO feedback_messages VALUES (?,?,?,?,?,?,?,?,?,?)",
                  (message.os, message.id, message.author, message.comment,
                   message.updated_at, message.rating, message.device,
                   message.os_version, message.app_version,
                   str(message.device_metadata)))

        conn.commit()
        conn.close()
