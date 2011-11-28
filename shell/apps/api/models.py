from django.db import models
from django.db.models import Q

class Player(models.Model):
    ''' Represents a player and their basic information
    '''
    firstname = models.CharField(max_length=100)
    lastname  = models.CharField(max_length=100)
    number    = models.IntegerField()
    birthday  = models.DateField()
    height    = models.DecimalField(max_digits=5, decimal_places=2)
    weight    = models.DecimalField(max_digits=5, decimal_places=2)
    active    = models.BooleanField(default=True)
    history   = models.TextField(null=True, blank=True)
    comments  = models.TextField(null=True, blank=True)
    phone     = models.CharField(max_length=20, null=True, blank=True)
    address   = models.CharField(max_length=100, null=True, blank=True)

    class Meta:
        ordering = ('lastname','firstname',)

    def __unicode__(self):
        return "[%d] %s, %s" % (self.number, self.lastname, self.firstname)

    @classmethod
    def byName(cls, name):
        ''' A helper method to search for a player by name

        :param name: The name to search with
        :returns: Any matching players
        '''
        return Player.objects.get(Q(firstname__istartswith=name)
            | Q(lastname__istartswith=name))

class Contact(models.Model):
    ''' Represents a player and their basic information
    '''
    RELATION_CHOICES = (
      (0, 'Other'),
      (1, 'Doctor'),
      (2, 'Mother'),
      (3, 'Father'),
      (4, 'Brother'),
      (5, 'Sister'),
      (6, 'Spouse'),
      (7, 'Relative'),
    )
    player    = models.ForeignKey('Player', related_name='contacts')
    firstname = models.CharField(max_length=100)
    lastname  = models.CharField(max_length=100)
    phone     = models.CharField(max_length=20,  null=True, blank=True)
    altphone  = models.CharField(max_length=20,  null=True, blank=True)
    address   = models.CharField(max_length=100, null=True, blank=True)
    relation  = models.IntegerField(max_length=1, choices=RELATION_CHOICES, default=0)

    class Meta:
        ordering = ('lastname','firstname',)

    def __unicode__(self):
        return "[%s] %s, %s" % (self.relation, self.lastname, self.firstname)

class Reading(models.Model):
    ''' Represents a single reading for a given player

    .. note:: The temperature and humidity will be the max value
              for the given session. Also, except for notable hits,
              the acceleration will be the aggregate for the session.
    '''
    STATUS_CHOICES = (
      (0, 'Inactive'),
      (1, 'Good'),
      (2, 'Warning'),
      (3, 'Emergency'),
    )
    player       = models.ForeignKey('Player', related_name='readings')
    date         = models.DateTimeField(auto_now=True)
    hits         = models.IntegerField(default=0)
    temperature  = models.DecimalField(max_digits=6, decimal_places=2)
    humidity     = models.DecimalField(max_digits=6, decimal_places=2)
    acceleration = models.DecimalField(max_digits=8, decimal_places=3)
    status       = models.IntegerField(max_length=1, choices=STATUS_CHOICES, default=0)

    class Meta:
        ordering = ('date',)

    def __unicode__(self):
        return "[%s] %s" % (self.date, self.status)

class Trauma(models.Model):
    ''' Represents a single tramatic hit for a given player
    '''
    player       = models.ForeignKey('Player', related_name='')
    date         = models.DateTimeField(auto_now=True)
    acceleration = models.DecimalField(max_digits=8, decimal_places=3)
    conscious    = models.BooleanField(default=True)
    comments     = models.TextField(null=True, blank=True)

    class Meta:
        ordering = ('date',)

    def __unicode__(self):
        return "[%s] %fg" % (self.date, self.acceleration)
