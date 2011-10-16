from django.conf.urls.defaults import *
from shell.apps.piston.doc import documentation_view
from shell.apps.piston.resource import Resource
from shell.apps.api import handlers

# -------------------------------------------------------- #
# csrf exempt resource
# -------------------------------------------------------- #
class CsrfExemptResource(Resource):

    def __init__(self, handler, authentication=None):
        super(CsrfExemptResource, self).__init__(handler, authentication)
        self.csrf_exempt = getattr(self.handler, 'csrf_exempt', True)

# ------------------------------------------------------------
# initialization
# ------------------------------------------------------------
urlpatterns = []

# ------------------------------------------------------------
# player api reference
# ------------------------------------------------------------
player_handler = CsrfExemptResource(handlers.PlayerHandler)
urlpatterns += patterns('',
    url(r'^$', documentation_view),
    url(r'^player/?$', player_handler),
    url(r'^player/search/(?P<name>[^/]+)/?$', player_handler),
    url(r'^player/(?P<id>[^/]+)/?$', player_handler),
)

# ------------------------------------------------------------
# player api reference
# ------------------------------------------------------------
contact_handler = CsrfExemptResource(handlers.ContactHandler)
urlpatterns += patterns('',
    url(r'^$', documentation_view),
    url(r'^contact/?$', contact_handler),
    url(r'^contact/(?P<id>[^/]+)/?$', contact_handler),
    url(r'^player/(?P<pid>[^/]+)/contacts/?$', contact_handler),
)

# ------------------------------------------------------------
# reading api reference
# ------------------------------------------------------------
reading_handler = CsrfExemptResource(handlers.ReadingHandler)
urlpatterns += patterns('',
    url(r'^player/(?P<id>[^/]+)/history/?$', reading_handler),
    url(r'^player/(?P<id>[^/]+)/history/(?P<count>[^/]+)/?$', reading_handler),
)

