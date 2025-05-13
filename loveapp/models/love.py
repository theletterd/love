# -*- coding: utf-8 -*-
from time import mktime

from google.appengine.ext import ndb

from loveapp.models import Employee

import loveapp.config as config


class Love(ndb.Model):
    """Models an instance of sent love."""
    message = ndb.TextProperty()
    recipient_key = ndb.KeyProperty(kind=Employee)
    secret = ndb.BooleanProperty(default=False)
    sender_key = ndb.KeyProperty(kind=Employee)
    timestamp = ndb.DateTimeProperty(auto_now_add=True)
    company_values = ndb.StringProperty(repeated=True)

    @property
    def seconds_since_epoch(self):
        return int(mktime(self.timestamp.timetuple()))

    @property
    def tags(self):
        return self._tags

    @tags.setter
    def tags(self, value):
        self._tags = value

    def __init__(self, *args, **kwargs):
        super(Love, self).__init__(*args, **kwargs)
        self._tags = []

        # Initialize tags based on message content
        self._init_tags()

    def _init_tags(self):
        """Initialize tags based on message content."""
        if self.message and self._is_work_anniversary_message(self.message):
            self._add_tag('work_anniversary')

    def _add_tag(self, tag):
        """Helper method to append a tag to the tags list."""
        if tag not in self._tags:
            self._tags.append(tag)

    def _is_work_anniversary_message(self, message: str) -> bool:
        """Helper function to check if a message contains work anniversary text."""
        work_anniversary_finder = config.MESSAGE_TAG_CONFIG.get("work_anniversary_tag_substring")
        if work_anniversary_finder is None:
            self._tags = []
            return False

        return bool(message and work_anniversary_finder in message.lower())