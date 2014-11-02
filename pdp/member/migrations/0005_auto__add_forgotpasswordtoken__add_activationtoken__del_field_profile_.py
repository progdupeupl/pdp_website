# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'ForgotPasswordToken'
        db.create_table('member_forgotpasswordtoken', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
            ('token', self.gf('django.db.models.fields.CharField')(blank=True, max_length=40)),
            ('expires', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime(2014, 11, 2, 0, 0))),
        ))
        db.send_create_signal('member', ['ForgotPasswordToken'])

        # Adding model 'ActivationToken'
        db.create_table('member_activationtoken', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
            ('token', self.gf('django.db.models.fields.CharField')(blank=True, max_length=40)),
            ('expires', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime(2014, 11, 2, 0, 0))),
        ))
        db.send_create_signal('member', ['ActivationToken'])

        # Deleting field 'Profile.key_expires'
        db.delete_column('member_profile', 'key_expires')

        # Deleting field 'Profile.activation_key'
        db.delete_column('member_profile', 'activation_key')


    def backwards(self, orm):
        # Deleting model 'ForgotPasswordToken'
        db.delete_table('member_forgotpasswordtoken')

        # Deleting model 'ActivationToken'
        db.delete_table('member_activationtoken')

        # Adding field 'Profile.key_expires'
        db.add_column('member_profile', 'key_expires',
                      self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime(2014, 6, 13, 0, 0)),
                      keep_default=False)

        # Adding field 'Profile.activation_key'
        db.add_column('member_profile', 'activation_key',
                      self.gf('django.db.models.fields.CharField')(blank=True, max_length=40, default=''),
                      keep_default=False)


    models = {
        'auth.group': {
            'Meta': {'object_name': 'Group'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'to': "orm['auth.Permission']", 'symmetrical': 'False'})
        },
        'auth.permission': {
            'Meta': {'ordering': "('content_type__app_label', 'content_type__model', 'codename')", 'object_name': 'Permission', 'unique_together': "(('content_type', 'codename'),)"},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'blank': 'True', 'max_length': '75'}),
            'first_name': ('django.db.models.fields.CharField', [], {'blank': 'True', 'max_length': '30'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "'user_set'", 'to': "orm['auth.Group']", 'symmetrical': 'False'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'blank': 'True', 'max_length': '30'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "'user_set'", 'to': "orm['auth.Permission']", 'symmetrical': 'False'}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        'contenttypes.contenttype': {
            'Meta': {'object_name': 'ContentType', 'ordering': "('name',)", 'db_table': "'django_content_type'", 'unique_together': "(('app_label', 'model'),)"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'member.activationtoken': {
            'Meta': {'object_name': 'ActivationToken'},
            'expires': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2014, 11, 2, 0, 0)'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'token': ('django.db.models.fields.CharField', [], {'blank': 'True', 'max_length': '40'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']"})
        },
        'member.forgotpasswordtoken': {
            'Meta': {'object_name': 'ForgotPasswordToken'},
            'expires': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2014, 11, 2, 0, 0)'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'token': ('django.db.models.fields.CharField', [], {'blank': 'True', 'max_length': '40'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']"})
        },
        'member.profile': {
            'Meta': {'object_name': 'Profile'},
            'avatar_url': ('django.db.models.fields.CharField', [], {'blank': 'True', 'null': 'True', 'max_length': '128'}),
            'biography': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'show_email': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'site': ('django.db.models.fields.CharField', [], {'blank': 'True', 'max_length': '128'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'unique': 'True', 'to': "orm['auth.User']"})
        }
    }

    complete_apps = ['member']