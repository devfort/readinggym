# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Piece'
        db.create_table(u'readfast_piece', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('slug', self.gf('django.db.models.fields.SlugField')(max_length=50)),
            ('text', self.gf('django.db.models.fields.TextField')()),
        ))
        db.send_create_signal(u'readfast', ['Piece'])

        # Adding model 'ComprehensionQuestion'
        db.create_table(u'readfast_comprehensionquestion', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('piece', self.gf('django.db.models.fields.related.ForeignKey')(related_name='questions', to=orm['readfast.Piece'])),
            ('text', self.gf('django.db.models.fields.CharField')(max_length=200)),
        ))
        db.send_create_signal(u'readfast', ['ComprehensionQuestion'])

        # Adding model 'ComprehensionAnswer'
        db.create_table(u'readfast_comprehensionanswer', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('question', self.gf('django.db.models.fields.related.ForeignKey')(related_name='answers', to=orm['readfast.ComprehensionQuestion'])),
            ('text', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('correct', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal(u'readfast', ['ComprehensionAnswer'])


    def backwards(self, orm):
        # Deleting model 'Piece'
        db.delete_table(u'readfast_piece')

        # Deleting model 'ComprehensionQuestion'
        db.delete_table(u'readfast_comprehensionquestion')

        # Deleting model 'ComprehensionAnswer'
        db.delete_table(u'readfast_comprehensionanswer')


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
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '50'}),
            'text': ('django.db.models.fields.TextField', [], {})
        }
    }

    complete_apps = ['readfast']