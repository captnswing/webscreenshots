# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'WebSite'
        db.create_table(u'main_website', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('url', self.gf('django.db.models.fields.CharField')(max_length=250)),
        ))
        db.send_create_signal(u'main', ['WebSite'])


    def backwards(self, orm):
        # Deleting model 'WebSite'
        db.delete_table(u'main_website')


    models = {
        u'main.website': {
            'Meta': {'ordering': "['url']", 'object_name': 'WebSite'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'url': ('django.db.models.fields.CharField', [], {'max_length': '250'})
        }
    }

    complete_apps = ['main']