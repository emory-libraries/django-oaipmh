# coding: utf-8

from __future__ import unicode_literals
from datetime import datetime
from django.contrib.flatpages.models import FlatPage
from django_oaipmh import OAIProvider


class ExampleOAIProvider(OAIProvider):
    def items(self):
        return FlatPage.objects.filter()

    def last_modified(self, obj):
        return datetime.now()

    def oai_identifier(self, obj):
        return 'oai:example_project:' + obj.get_absolute_url()

    def sets(self, obj):
        return []
