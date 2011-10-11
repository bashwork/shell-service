from django.shortcuts import get_object_or_404
from piston.handler import BaseHandler
from shell.apps.api.models import Player, Reading, Contact

# -------------------------------------------------------- #
# class CsrfExemptBaseHandler(BaseHandler):
#     """
#     handles request that have had csrfmiddlewaretoken inserted 
#     automatically by django's CsrfViewMiddleware
#     
#     """
#     def flatten_dict(self, dct):
#         if 'csrfmiddlewaretoken' in dct:
#             # dct is a QueryDict and immutable
#             dct = dct.copy()  
#             del dct['csrfmiddlewaretoken']
#         return super(CsrfExemptBaseHandler, self).flatten_dict(dct)
# -------------------------------------------------------- #

class PlayerHandler(BaseHandler):
    ''' This it the service interface to the
    player information.
    '''
    allowed_methods = ('GET', 'POST', 'PUT',)
    model = Player

    def read(self, request, number=None):
        ''' Returns one or more players that have been requested

        :param request: The request to process
        :param number: The player number to process
        '''
        objects = Player.objects
        if number:
            return objects.filter(number=number)
        else: return objects.all()

class ContactHandler(BaseHandler):
    ''' This it the service interface to the
    player information.
    '''
    allowed_methods = ('GET', 'POST', 'PUT',)
    model = Contact
    exclude = ('player',)

    def read(self, request, id=None, number=None):
        ''' Returns one or more players that have been requested

        :param request: The request to process
        :param number: The player number to process
        '''
        objects = Contact.objects
        if number:
            return objects.filter(player__number=number)
        else: return objects.all()

class ReadingHandler(BaseHandler):
    ''' This it the service interface to the
    player's history readings.
    '''
    allowed_methods = ('GET', 'POST',)
    model = Reading
    exclude = ('player',)

    def read(self, request, number=None, count=30):
        ''' Returns one or more players that have been requested

        :param request: The request to process
        :param number: The player number to process
        :param count: The number of readings to return
        '''
        readings = []
        if number:
            player = Reading.objects.filter(player__number=number)
            readings = player[0].readings.all()[:count]
        return readings
