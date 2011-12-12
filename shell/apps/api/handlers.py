from django.shortcuts import get_object_or_404
from shell.apps.piston.handler import BaseHandler
from shell.apps.api.models import Player, Reading, Contact, Trauma

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
    fields = ('id', 'firstname', 'lastname', 'number', 'birthday',
      'height', 'weight', 'history', 'comments', 'phone', 'address',
      ('contacts', (),),)

    def read(self, request, id=None):
        ''' Returns one or more players that have been requested

        :param request: The request to process
        :param id: The player id to process
        '''
        objects = Player.objects
        if id:
            return objects.filter(id=id)[0]
        else: return objects.filter(active=1).order_by('number')

class ContactHandler(BaseHandler):
    ''' This it the service interface to the
    player information.
    '''
    allowed_methods = ('GET', 'POST', 'PUT',)
    model = Contact
    exclude = ('player',)

    def read(self, request, id=None, pid=None):
        ''' Returns one or more players that have been requested

        :param request: The request to process
        :param id: The contact id to process
        :param pid: The player id to process
        '''
        objects = Contact.objects
        if id:
            return objects.filter(id=id)[0]
        elif pid:
            return objects.filter(player__id=pid)
        else: return objects.all()

    def create(self, request):
        ''' Creates a new history instance

        :param request: The request to process
        '''
        request.data._mutable = True # hack
        pid = request.data.get('player', None)
        request.data['player'] = get_object_or_404(Player, id=pid)
        return super(ContactHandler, self).create(request)

class ReadingHandler(BaseHandler):
    ''' This it the service interface to the
    player's history readings.
    '''
    allowed_methods = ('GET', 'POST', 'PUT')
    model = Reading
    exclude = ('player',)

    def read(self, request, id=None, pid=None, count=30):
        ''' Returns one or more readings that have been requested

        :param request: The request to process
        :param id: The reading id to process
        :param pid: The player id to process
        :param count: The number of readings to return
        '''
        readings = []
        if id != None:
            readings = Reading.objects.filter(id=id)
        elif pid != None:
            player = Reading.objects.filter(player__id=pid)
            readings = player.order_by('-date')[:count]
        else: readings = Readings.objects.all()[:count]
        return readings

    def create(self, request):
        ''' Creates a new history instance

        :param request: The request to process
        '''
        request.data._mutable = True # hack
        pid = request.data.get('player', None)
        request.data['player'] = get_object_or_404(Player, id=pid)
        return super(ReadingHandler, self).create(request)

class TraumaHandler(BaseHandler):
    ''' This it the service interface to the
    player's tramatic readings.
    '''
    allowed_methods = ('GET', 'POST', 'PUT')
    model = Trauma
    exclude = ('player',)

    def read(self, request, id=None, pid=None, count=30):
        ''' Returns one or more tramatic hits that have been requested

        :param request: The request to process
        :param id: The trauma id to process
        :param pid: The player id to process
        :param count: The number of readings to return
        '''
        readings = []
        if id != None:
            readings = Trauma.objects.filter(id=id)
        elif pid != None:
            player = Trauma.objects.filter(player__id=pid)
            readings = player.order_by('-date')[:count]
        else: readings = Trauma.objects.all()[:count]
        return readings

    def create(self, request):
        ''' Creates a new trauma instance

        :param request: The request to process
        '''
        request.data._mutable = True # hack
        pid = request.data.get('player', None)
        request.data['player'] = get_object_or_404(Player, id=pid)
        return super(TraumaHandler, self).create(request)
