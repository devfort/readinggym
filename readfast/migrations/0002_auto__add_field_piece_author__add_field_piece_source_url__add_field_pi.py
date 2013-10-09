# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'Piece.author'
        db.add_column(u'readfast_piece', 'author',
                      self.gf('django.db.models.fields.CharField')(default='', max_length=200),
                      keep_default=False)

        # Adding field 'Piece.source_url'
        db.add_column(u'readfast_piece', 'source_url',
                      self.gf('django.db.models.fields.URLField')(default='', max_length=200),
                      keep_default=False)

        # Adding field 'Piece.source_title'
        db.add_column(u'readfast_piece', 'source_title',
                      self.gf('django.db.models.fields.CharField')(default='', max_length=200),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting field 'Piece.author'
        db.delete_column(u'readfast_piece', 'author')

        # Deleting field 'Piece.source_url'
        db.delete_column(u'readfast_piece', 'source_url')

        # Deleting field 'Piece.source_title'
        db.delete_column(u'readfast_piece', 'source_title')


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
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '50'}),
            'source_title': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'source_url': ('django.db.models.fields.URLField', [], {'max_length': '200'}),
            'text': ('django.db.models.fields.TextField', [], {})
        }
    }

    complete_apps = ['readfast']