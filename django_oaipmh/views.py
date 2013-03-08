# file django_oaipmh/views.py
#
#   Copyright 2013 Emory University Libraries
#
#   Licensed under the Apache License, Version 2.0 (the "License");
#   you may not use this file except in compliance with the License.
#   You may obtain a copy of the License at
#
#       http://www.apache.org/licenses/LICENSE-2.0
#
#   Unless required by applicable law or agreed to in writing, software
#   distributed under the License is distributed on an "AS IS" BASIS,
#   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#   See the License for the specific language governing permissions and
#   limitations under the License.

from django.conf import settings
from django.views.generic import TemplateView


class OAIProvider(TemplateView):
    content_type = 'text/xml'  # possibly application/xml ?

    # modeling on sitemaps: these methods should be implemented
    # when extending OAIProvider

    def items(self):
        # list/generator/queryset of items to be made available via oai
        # NOTE: this will probably have other optional parameters,
        # e.g. filter by set or date modified
        # - could possibly include find by id for GetRecord here also...
        pass

    def last_modified(self, obj):
        # datetime object was last modified
        pass

    def oai_identifier(self, obj):
        # oai identifier for a given object
        pass

    def sets(self, obj):
        # list of set identifiers for a given object
        return []

    # TODO: get metadata record for a given object in a given metadata format

    def render_to_response(self, context, **response_kwargs):
        # all OAI responses should be xml
        if 'content_type' not in response_kwargs:
            response_kwargs['content_type'] = self.content_type

        # add common context data needed for all responses
        context.update({
            'verb': self.oai_verb,
            'url': self.request.build_absolute_uri(self.request.path),
        })
        return super(TemplateView, self) \
            .render_to_response(context, **response_kwargs)

    def identify(self):
        self.template_name = 'django_oaipmh/identify.xml'
        # TODO: these should probably be class variables/configurations
        # that extending classes could set
        identify_data = {
            'name': 'oai repo name',
            # perhaps an oai_admins method with default logic settings.admins?
            'admins': (email for name, email in settings.ADMINS),
            'earliest_date': '1990-02-01T12:00:00Z',   # placeholder
            # should probably be a class variable/configuration
            'deleted': 'no',  # no, transient, persistent (?)
            # class-level variable/configuration (may affect templates also)
            'granularity': 'YYYY-MM-DDThh:mm:ssZ',  # or YYYY-MM-DD
            # class-level config?
            'compression': 'deflate',  # gzip?  - optional
            # description - optional
            # (place-holder values from OAI docs example)
            'identifier_scheme': 'oai',
            'repository_identifier': 'lcoa1.loc.gov',
            'identifier_delimiter': ':',
            'sample_identifier': 'oai:lcoa1.loc.gov:loc.music/musdi.002'
        }
        return self.render_to_response(identify_data)

    def list_identifiers(self):
        self.template_name = 'django_oaipmh/list_identifiers.xml'
        items = []
        # TODO: eventually we will need pagination with oai resumption tokens
        # should be able to model similar to django.contrib.sitemap
        for i in self.items():
            item_info = {
                'identifier': self.oai_identifier(i),
                'last_modified': self.last_modified(i),
                'sets': self.sets(i)
            }
            items.append(item_info)
        return self.render_to_response({'items': items})

    def error(self, code, text):
        # TODO: HTTP error response code? maybe 400 bad request?
        # NOTE: may need to revise, could have multiple error codes/messages
        self.template_name = 'django_oaipmh/error.xml'
        return self.render_to_response({
            'error_code': code,
            'error': text,
        })

    # HTTP GET request: determine OAI verb and hand off to appropriate
    # method
    def get(self, request, *args, **kwargs):
        self.request = request   # store for access in other functions

        self.oai_verb = request.GET.get('verb', None)

        if self.oai_verb == 'Identify':
            return self.identify()

        if self.oai_verb == 'ListIdentifiers':
            return self.list_identifiers()

        # OAI verbs still TODO:
        #
        # GetRecord
        #  - will probably require an item_by_id method similar items
        # ListMetadataFormats
        # ListRecords
        #  - should have some overlap/reusability with ListIdentifiers
        # ListSets
        #  - could start with noSetHierarchy in initial implementation

        else:
            # if no verb = bad request response

            if self.oai_verb is None:
                error_msg = 'The request did not provide any verb.'
            else:
                'The verb "%s" is illegal' % self.oai_verb
            return self.error('badVerb', error_msg)
