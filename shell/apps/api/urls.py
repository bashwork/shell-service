from django.conf.urls.defaults import *
from piston.resource import Resource
from piston.doc import documentation_view
from shell.apps.api.handlers import PlayerHandler, ReadingHandler
from shell.apps.api.handlers import ContactHandler

# ------------------------------------------------------------
# initialization
# ------------------------------------------------------------
urlpatterns = []

# ------------------------------------------------------------
# player api reference
# ------------------------------------------------------------
player_handler = Resource(PlayerHandler)
urlpatterns += patterns('',
    url(r'^$', documentation_view),
    url(r'^player/?$', player_handler),
    url(r'^player/search/(?P<name>[^/]+)/?$', player_handler),
    url(r'^player/(?P<player_id>[^/]+)/?$', player_handler),
)

# ------------------------------------------------------------
# player api reference
# ------------------------------------------------------------
contact_handler = Resource(ContactHandler)
urlpatterns += patterns('',
    url(r'^$', documentation_view),
    url(r'^contact?$', contact_handler),
    url(r'^player/(?P<player_id>[^/]+)/contacts?$', contact_handler),
)

# ------------------------------------------------------------
# reading api reference
# ------------------------------------------------------------
reading_handler = Resource(ReadingHandler)
urlpatterns += patterns('',
    url(r'^history/date/(?P<date>[^/]+)/?$', reading_handler),
    url(r'^player/(?P<player_id>[^/]+)/history/?$', reading_handler),
)

