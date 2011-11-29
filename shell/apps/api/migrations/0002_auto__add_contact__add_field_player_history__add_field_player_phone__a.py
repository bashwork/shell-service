# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding model 'Contact'
        db.create_table('api_contact', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('player', self.gf('django.db.models.fields.related.ForeignKey')(related_name='contacts', to=orm['api.Player'])),
            ('firstname', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('lastname', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('phone', self.gf('django.db.models.fields.CharField')(max_length=20, null=True, blank=True)),
            ('altphone', self.gf('django.db.models.fields.CharField')(max_length=20, null=True, blank=True)),
            ('address', self.gf('django.db.models.fields.CharField')(max_length=100, null=True, blank=True)),
            ('relation', self.gf('django.db.models.fields.IntegerField')(max_length=1)),
        ))
        db.send_create_signal('api', ['Contact'])

        # Adding field 'Player.history'
        db.add_column('api_player', 'history', self.gf('django.db.models.fields.TextField')(null=True, blank=True), keep_default=False)

        # Adding field 'Player.phone'
        db.add_column('api_player', 'phone', self.gf('django.db.models.fields.CharField')(max_length=20, null=True, blank=True), keep_default=False)

        # Adding field 'Player.address'
        db.add_column('api_player', 'address', self.gf('django.db.models.fields.CharField')(max_length=100, null=True, blank=True), keep_default=False)


    def backwards(self, orm):
        
        # Deleting model 'Contact'
        db.delete_table('api_contact')

        # Deleting field 'Player.history'
        db.delete_column('api_player', 'history')

        # Deleting field 'Player.phone'
        db.delete_column('api_player', 'phone')

        # Deleting field 'Player.address'
        db.delete_column('api_player', 'address')


    models = {
        'api.contact': {
            'Meta': {'ordering': "('lastname', 'firstname')", 'object_name': 'Contact'},
            'address': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'altphone': ('django.db.models.fields.CharField', [], {'max_length': '20', 'null': 'True', 'blank': 'True'}),
            'firstname': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'lastname': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'phone': ('django.db.models.fields.CharField', [], {'max_length': '20', 'null': 'True', 'blank': 'True'}),
            'player': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'contacts'", 'to': "orm['api.Player']"}),
            'relation': ('django.db.models.fields.IntegerField', [], {'max_length': '1'})
        },
        'api.player': {
            'Meta': {'ordering': "('lastname', 'firstname')", 'object_name': 'Player'},
            'active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'address': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'birthday': ('django.db.models.fields.DateField', [], {}),
            'comments': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'firstname': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'height': ('django.db.models.fields.DecimalField', [], {'max_digits': '5', 'decimal_places': '2'}),
            'history': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'lastname': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'number': ('django.db.models.fields.IntegerField', [], {}),
            'phone': ('django.db.models.fields.CharField', [], {'max_length': '20', 'null': 'True', 'blank': 'True'}),
            'weight': ('django.db.models.fields.DecimalField', [], {'max_digits': '5', 'decimal_places': '2'})
        },
        'api.reading': {
            'Meta': {'ordering': "('date',)", 'object_name': 'Reading'},
            'acceleration': ('django.db.models.fields.DecimalField', [], {'max_digits': '8', 'decimal_places': '3'}),
            'date': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'hits': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'humidity': ('django.db.models.fields.DecimalField', [], {'max_digits': '6', 'decimal_places': '2'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'player': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'readings'", 'to': "orm['api.Player']"}),
            'temperature': ('django.db.models.fields.DecimalField', [], {'max_digits': '6', 'decimal_places': '2'})
        }
    }

    complete_apps = ['api']
