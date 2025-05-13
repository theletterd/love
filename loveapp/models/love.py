# -*- coding: utf-8 -*-
from time import mktime

from google.appengine.ext import ndb

from loveapp.models import Employee


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

    def add_tag(self, tag):
        """Helper method to append a tag to the tags list."""
        if tag not in self._tags:
            self._tags.append(tag)
