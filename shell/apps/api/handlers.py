from django.shortcuts import get_object_or_404
from piston.handler import BaseHandler
from shell.apps.api.models import Player, Reading, Contact

class PlayerHandler(BaseHandler):
    ''' This it the service interface to the
    player information.
    '''
    allowed_methods = ('GET', 'POST', 'PUT',)
    model = Player
    exclude = ()

    def read(self, request, player_id=None):
        ''' Returns one or more players that have been requested

        :param request: The request to process
        :param player_id: The player identifier to process
        '''
        objects = Player.objects
        if player_id:
            return get_object_or_404(Player, id=player_id)
        else: return objects.all()

class ContactHandler(BaseHandler):
    ''' This it the service interface to the
    player information.
    '''
    allowed_methods = ('GET', 'POST', 'PUT',)
    model = Contact
    exclude = ()

    def read(self, request, player_id=None):
        ''' Returns one or more players that have been requested

        :param request: The request to process
        :param player_id: The player identifier to process
        '''
        objects = Contact.objects
        if player_id:
            return objects.filter(player__id=player_id)
        else: return objects.all()

class ReadingHandler(BaseHandler):
    ''' This it the service interface to the
    player's history readings.
    '''
    allowed_methods = ('GET', 'POST',)
    model = Reading
    exclude = ('player',)

    def read(self, request, player_id=None, count=30):
        ''' Returns one or more players that have been requested

        :param request: The request to process
        :param player_id: The player identifier to process
        :param count: The number of readings to return
        '''
        readings = []
        if player_id:
            player = get_object_or_404(Player, id=player_id)
            readings = player.readings.all()[:30]
        return readings
