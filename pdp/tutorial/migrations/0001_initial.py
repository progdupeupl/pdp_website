# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Tutorial'
        db.create_table('tutorial_tutorial', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=80)),
            ('is_mini', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal('tutorial', ['Tutorial'])

        # Adding M2M table for field authors on 'Tutorial'
        db.create_table('tutorial_tutorial_authors', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('tutorial', models.ForeignKey(orm['tutorial.tutorial'], null=False)),
            ('user', models.ForeignKey(orm['auth.user'], null=False))
        ))
        db.create_unique('tutorial_tutorial_authors', ['tutorial_id', 'user_id'])

        # Adding model 'Part'
        db.create_table('tutorial_part', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('tutorial', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['tutorial.Tutorial'])),
            ('position_in_tutorial', self.gf('django.db.models.fields.IntegerField')()),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=80)),
            ('introduction', self.gf('django.db.models.fields.TextField')()),
            ('conclusion', self.gf('django.db.models.fields.TextField')()),
        ))
        db.send_create_signal('tutorial', ['Part'])

        # Adding model 'Chapter'
        db.create_table('tutorial_chapter', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('part', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['tutorial.Part'], null=True)),
            ('position_in_part', self.gf('django.db.models.fields.IntegerField')(null=True)),
            ('tutoriel', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['tutorial.Tutorial'], null=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=80)),
            ('introduction', self.gf('django.db.models.fields.TextField')()),
            ('text', self.gf('django.db.models.fields.TextField')()),
            ('conclusion', self.gf('django.db.models.fields.TextField')()),
        ))
        db.send_create_signal('tutorial', ['Chapter'])


    def backwards(self, orm):
        # Deleting model 'Tutorial'
        db.delete_table('tutorial_tutorial')

        # Removing M2M table for field authors on 'Tutorial'
        db.delete_table('tutorial_tutorial_authors')

        # Deleting model 'Part'
        db.delete_table('tutorial_part')

        # Deleting model 'Chapter'
        db.delete_table('tutorial_chapter')


    models = {
        'auth.group': {
            'Meta': {'object_name': 'Group'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        'auth.permission': {
            'Meta': {'ordering': "('content_type__app_label', 'content_type__model', 'codename')", 'unique_together': "(('content_type', 'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Group']", 'symmetrical': 'False', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'tutorial.chapter': {
            'Meta': {'object_name': 'Chapter'},
            'conclusion': ('django.db.models.fields.TextField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'introduction': ('django.db.models.fields.TextField', [], {}),
            'part': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['tutorial.Part']", 'null': 'True'}),
            'position_in_part': ('django.db.models.fields.IntegerField', [], {'null': 'True'}),
            'text': ('django.db.models.fields.TextField', [], {}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '80'}),
            'tutoriel': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['tutorial.Tutorial']", 'null': 'True'})
        },
        'tutorial.part': {
            'Meta': {'object_name': 'Part'},
            'conclusion': ('django.db.models.fields.TextField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'introduction': ('django.db.models.fields.TextField', [], {}),
            'position_in_tutorial': ('django.db.models.fields.IntegerField', [], {}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '80'}),
            'tutorial': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['tutorial.Tutorial']"})
        },
        'tutorial.tutorial': {
            'Meta': {'object_name': 'Tutorial'},
            'authors': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.User']", 'symmetrical': 'False'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_mini': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '80'})
        }
    }

    complete_apps = ['tutorial']