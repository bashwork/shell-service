from django.shortcuts import get_object_or_404
from piston.utils import rc
from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned
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
        else: return objects.filter(active=1)

    def update(self, request, *args, **kwargs):
        if not self.has_model():
            return rc.NOT_IMPLEMENTED

        pkfield = self.model._meta.pk.name

        if pkfield not in kwargs:
            # No pk was specified
            return rc.BAD_REQUEST

        try:
            inst = self.model.objects.all().get(pk=kwargs.get(pkfield))
        except ObjectDoesNotExist:
            return rc.NOT_FOUND
        except MultipleObjectsReturned: # should never happen, since we're using a PK
            return rc.BAD_REQUEST

        attrs = self.flatten_dict(request.data)
        for k,v in attrs.iteritems():
            setattr( inst, k, v )

        inst.save()
        return rc.ALL_OK

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

    def update(self, request, *args, **kwargs):
        if not self.has_model():
            return rc.NOT_IMPLEMENTED

        pkfield = self.model._meta.pk.name

        if pkfield not in kwargs:
            # No pk was specified
            return rc.BAD_REQUEST

        try:
            inst = self.model.objects.all().get(pk=kwargs.get(pkfield))
        except ObjectDoesNotExist:
            return rc.NOT_FOUND
        except MultipleObjectsReturned: # should never happen, since we're using a PK
            return rc.BAD_REQUEST

        attrs = self.flatten_dict(request.data)
        for k,v in attrs.iteritems():
            setattr( inst, k, v )

        inst.save()
        return rc.ALL_OK

class ReadingHandler(BaseHandler):
    ''' This it the service interface to the
    player's history readings.
    '''
    allowed_methods = ('GET', 'POST',)
    model = Reading
    exclude = ('player',)

    def read(self, request, id, count=30):
        ''' Returns one or more players that have been requested

        :param request: The request to process
        :param id: The player number to process
        :param count: The number of readings to return
        '''
        player = Reading.objects.filter(player__id=id)
        readings = player.order_by('-date')[:count]
        return readings
