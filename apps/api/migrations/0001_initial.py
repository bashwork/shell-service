# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding model 'Player'
        db.create_table('api_player', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('firstname', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('lastname', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('birthday', self.gf('django.db.models.fields.DateField')()),
            ('height', self.gf('django.db.models.fields.FloatField')()),
            ('weight', self.gf('django.db.models.fields.FloatField')()),
            ('active', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('comments', self.gf('django.db.models.fields.TextField')()),
        ))
        db.send_create_signal('api', ['Player'])

        # Adding model 'Reading'
        db.create_table('api_reading', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('player', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['api.Player'])),
            ('date', self.gf('django.db.models.fields.DateTimeField')()),
            ('temperature', self.gf('django.db.models.fields.DecimalField')(max_digits=6, decimal_places=2)),
            ('humidity', self.gf('django.db.models.fields.DecimalField')(max_digits=6, decimal_places=2)),
            ('acceleration', self.gf('django.db.models.fields.DecimalField')(max_digits=8, decimal_places=3)),
        ))
        db.send_create_signal('api', ['Reading'])


    def backwards(self, orm):
        
        # Deleting model 'Player'
        db.delete_table('api_player')

        # Deleting model 'Reading'
        db.delete_table('api_reading')


    models = {
        'api.player': {
            'Meta': {'object_name': 'Player'},
            'active': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'birthday': ('django.db.models.fields.DateField', [], {}),
            'comments': ('django.db.models.fields.TextField', [], {}),
            'firstname': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'height': ('django.db.models.fields.FloatField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'lastname': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'weight': ('django.db.models.fields.FloatField', [], {})
        },
        'api.reading': {
            'Meta': {'object_name': 'Reading'},
            'acceleration': ('django.db.models.fields.DecimalField', [], {'max_digits': '8', 'decimal_places': '3'}),
            'date': ('django.db.models.fields.DateTimeField', [], {}),
            'humidity': ('django.db.models.fields.DecimalField', [], {'max_digits': '6', 'decimal_places': '2'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'player': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['api.Player']"}),
            'temperature': ('django.db.models.fields.DecimalField', [], {'max_digits': '6', 'decimal_places': '2'})
        }
    }

    complete_apps = ['api']
