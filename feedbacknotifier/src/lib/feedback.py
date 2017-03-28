

class Feedback(object):
    """
    :param os: `ios` or `android`
    :type os: str
    :param id: Id of review.
    :type id: str
    :param author: The name of the user who wrote the review.
    :type author: str
    :param comment: The content of the comment, i.e. review body.
    :type comment: str
    :param updated_at: The last time at which this comment was updated in seconds
    :type updated_at: int
    :param rating: The star rating associated with the review, from 1 to 5.
    :type rating: int
    :param device: Codename for the reviewer's device, e.g. klte, flounder.
    :type device: str | None
    :param os_version: Integer Android SDK version of the user's device at the time the review was written, e.g. 23 is Marshmallow.
    :type os_version: int | None
    :param app_version: String version name of the app as installed at the time the review was written.
    :type app_version: str | None
    :param device_metadata: JSON object with full metadata of device
    :type device_metadata: str | None
    """

    def __init__(self, os, review_id, author, comment, updated_at, rating,
                 device, os_version, app_version, device_metadata):
        self.os = os
        self.id = review_id
        self.author = author
        self.comment = comment
        self.updated_at = updated_at
        self.rating = rating
        self.device = device
        self.os_version = os_version
        self.app_version = app_version
        self.device_metadata = device_metadata

    def __str__(self):
        # noinspection SpellCheckingInspection
        return (u'Feedback (%s):\nauthor=$s\ncomment=%s\nupdated_at=%s\nrating'
                u'=%s\ndevice=%ss_version=%s\napp_version=%s\n' % (
                    self.author,
                    self.comment,
                    self.updated_at,
                    self.rating,
                    self.device or '',
                    self.os_version or '',
                    self.app_version or ''
                ))
