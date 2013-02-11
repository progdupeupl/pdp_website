# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Category'
        db.create_table('forum_category', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=80)),
        ))
        db.send_create_signal('forum', ['Category'])

        # Adding model 'Forum'
        db.create_table('forum_forum', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=80)),
            ('subtitle', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('category', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['forum.Category'])),
        ))
        db.send_create_signal('forum', ['Forum'])

        # Adding model 'Topic'
        db.create_table('forum_topic', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=80)),
            ('subtitle', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('forum', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['forum.Forum'])),
            ('author', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
            ('last_message', self.gf('django.db.models.fields.related.ForeignKey')(related_name='last_message', null=True, to=orm['forum.Post'])),
            ('pubdate', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('is_solved', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('is_locked', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('is_sticky', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal('forum', ['Topic'])

        # Adding model 'Post'
        db.create_table('forum_post', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('topic', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['forum.Topic'])),
            ('author', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
            ('text', self.gf('django.db.models.fields.TextField')()),
            ('pubdate', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('update', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
            ('position_in_topic', self.gf('django.db.models.fields.IntegerField')()),
            ('is_useful', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal('forum', ['Post'])


    def backwards(self, orm):
        # Deleting model 'Category'
        db.delete_table('forum_category')

        # Deleting model 'Forum'
        db.delete_table('forum_forum')

        # Deleting model 'Topic'
        db.delete_table('forum_topic')

        # Deleting model 'Post'
        db.delete_table('forum_post')


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
        'forum.category': {
            'Meta': {'object_name': 'Category'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '80'})
        },
        'forum.forum': {
            'Meta': {'object_name': 'Forum'},
            'category': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['forum.Category']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'subtitle': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '80'})
        },
        'forum.post': {
            'Meta': {'object_name': 'Post'},
            'author': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_useful': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'position_in_topic': ('django.db.models.fields.IntegerField', [], {}),
            'pubdate': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'text': ('django.db.models.fields.TextField', [], {}),
            'topic': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['forum.Topic']"}),
            'update': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'})
        },
        'forum.topic': {
            'Meta': {'object_name': 'Topic'},
            'author': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']"}),
            'forum': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['forum.Forum']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_locked': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_solved': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_sticky': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_message': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'last_message'", 'null': 'True', 'to': "orm['forum.Post']"}),
            'pubdate': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'subtitle': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '80'})
        }
    }

    complete_apps = ['forum']