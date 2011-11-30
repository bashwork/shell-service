# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding field 'Reading.updated'
        db.add_column('api_reading', 'updated', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, default=datetime.date(2011, 11, 30), blank=True), keep_default=False)

        # Changing field 'Reading.date'
        db.alter_column('api_reading', 'date', self.gf('django.db.models.fields.DateTimeField')())

        # Adding field 'Trauma.updated'
        db.add_column('api_trauma', 'updated', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, default=datetime.date(2011, 11, 30), blank=True), keep_default=False)

        # Changing field 'Trauma.date'
        db.alter_column('api_trauma', 'date', self.gf('django.db.models.fields.DateTimeField')())


    def backwards(self, orm):
        
        # Deleting field 'Reading.updated'
        db.delete_column('api_reading', 'updated')

        # Changing field 'Reading.date'
        db.alter_column('api_reading', 'date', self.gf('django.db.models.fields.DateTimeField')(auto_now=True))

        # Deleting field 'Trauma.updated'
        db.delete_column('api_trauma', 'updated')

        # Changing field 'Trauma.date'
        db.alter_column('api_trauma', 'date', self.gf('django.db.models.fields.DateTimeField')(auto_now=True))


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
            'relation': ('django.db.models.fields.IntegerField', [], {'default': '0', 'max_length': '1'})
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
            'date': ('django.db.models.fields.DateTimeField', [], {}),
            'hits': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'humidity': ('django.db.models.fields.DecimalField', [], {'max_digits': '6', 'decimal_places': '2'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'player': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'readings'", 'to': "orm['api.Player']"}),
            'status': ('django.db.models.fields.IntegerField', [], {'default': '0', 'max_length': '1'}),
            'temperature': ('django.db.models.fields.DecimalField', [], {'max_digits': '6', 'decimal_places': '2'}),
            'updated': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'})
        },
        'api.trauma': {
            'Meta': {'ordering': "('date',)", 'object_name': 'Trauma'},
            'acceleration': ('django.db.models.fields.DecimalField', [], {'max_digits': '8', 'decimal_places': '3'}),
            'comments': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'conscious': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'date': ('django.db.models.fields.DateTimeField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'player': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "''", 'to': "orm['api.Player']"}),
            'updated': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'})
        }
    }

    complete_apps = ['api']
