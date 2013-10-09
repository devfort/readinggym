# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding unique constraint on 'Piece', fields ['slug']
        db.create_unique(u'readfast_piece', ['slug'])


    def backwards(self, orm):
        # Removing unique constraint on 'Piece', fields ['slug']
        db.delete_unique(u'readfast_piece', ['slug'])


    models = {
        u'readfast.comprehensionanswer': {
            'Meta': {'object_name': 'ComprehensionAnswer'},
            'correct': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'question': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'answers'", 'to': u"orm['readfast.ComprehensionQuestion']"}),
            'text': ('django.db.models.fields.CharField', [], {'max_length': '200'})
        },
        u'readfast.comprehensionquestion': {
            'Meta': {'object_name': 'ComprehensionQuestion'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'piece': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'questions'", 'to': u"orm['readfast.Piece']"}),
            'text': ('django.db.models.fields.CharField', [], {'max_length': '200'})
        },
        u'readfast.piece': {
            'Meta': {'object_name': 'Piece'},
            'author': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'slug': ('django.db.models.fields.SlugField', [], {'unique': 'True', 'max_length': '50'}),
            'source_title': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'source_url': ('django.db.models.fields.URLField', [], {'max_length': '200'}),
            'text': ('django.db.models.fields.TextField', [], {})
        }
    }

    complete_apps = ['readfast']