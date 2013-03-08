django-oaipmh
=============

OAI-PMH provider for django sites


Intended to be extended similar to django.contrib.sitemaps


How to use
----------

* Add `django_oaipmh` to your INSTALLED_APPS

* Extend OAIProvider and customize, similar to the way you would
  django.contrib.sitemaps.Sitemap  (should implement methods for
  items, last_modified, oai_identifier, sets; probably will also
  need to set values for oai identify)

* Bind your customized OAI provider to your desired url, e.g.::

  url(r'^oai/', MyCustomOaiProvider.as_view()),



Developer Notes
---------------

Use git flow and standard git flow naming conventions.

The OAI-PMH protocol is available at
http://www.openarchives.org/OAI/openarchivesprotocol.html

OAI provider implementations can be tested using the
OAI Repository Explorer (perhaps no longer available?)

Where possible, OAIprovider should be modeled on django.contrib.sitemap for
easy extensibility and familiarity to Django developers:
