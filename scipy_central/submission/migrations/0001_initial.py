# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Module'
        db.create_table('submission_module', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(unique=True, max_length=100)),
            ('website', self.gf('django.db.models.fields.URLField')(max_length=200)),
        ))
        db.send_create_signal('submission', ['Module'])

        # Adding model 'License'
        db.create_table('submission_license', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('slug', self.gf('django.db.models.fields.SlugField')(max_length=255)),
            ('description', self.gf('django.db.models.fields.TextField')()),
            ('text_template', self.gf('django.db.models.fields.TextField')()),
        ))
        db.send_create_signal('submission', ['License'])

        # Adding model 'Submission'
        db.create_table('submission_submission', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('sub_type', self.gf('django.db.models.fields.CharField')(max_length=10)),
            ('created_by', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'], null=True, blank=True)),
            ('date_created', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('fileset', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['filestorage.FileSet'], null=True, blank=True)),
            ('frozen', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal('submission', ['Submission'])

        # Adding M2M table for field inspired_by on 'Submission'
        db.create_table('submission_submission_inspired_by', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('from_submission', models.ForeignKey(orm['submission.submission'], null=False)),
            ('to_submission', models.ForeignKey(orm['submission.submission'], null=False))
        ))
        db.create_unique('submission_submission_inspired_by', ['from_submission_id', 'to_submission_id'])

        # Adding model 'Revision'
        db.create_table('submission_revision', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('entry', self.gf('django.db.models.fields.related.ForeignKey')(related_name='revisions', to=orm['submission.Submission'])),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=150)),
            ('slug', self.gf('django.db.models.fields.SlugField')(max_length=155)),
            ('date_created', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('created_by', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'], null=True, blank=True)),
            ('sub_license', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['submission.License'], null=True, blank=True)),
            ('description', self.gf('django.db.models.fields.TextField')()),
            ('description_html', self.gf('django.db.models.fields.TextField')()),
            ('hash_id', self.gf('django.db.models.fields.CharField')(max_length=60, null=True, blank=True)),
            ('item_code', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('item_highlighted_code', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('item_url', self.gf('django.db.models.fields.URLField')(max_length=255, null=True, blank=True)),
            ('is_displayed', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('validation_hash', self.gf('django.db.models.fields.CharField')(max_length=40, null=True, blank=True)),
            ('update_reason', self.gf('django.db.models.fields.CharField')(max_length=155, null=True, blank=True)),
        ))
        db.send_create_signal('submission', ['Revision'])

        # Adding M2M table for field modules_used on 'Revision'
        db.create_table('submission_revision_modules_used', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('revision', models.ForeignKey(orm['submission.revision'], null=False)),
            ('module', models.ForeignKey(orm['submission.module'], null=False))
        ))
        db.create_unique('submission_revision_modules_used', ['revision_id', 'module_id'])

        # Adding model 'TagCreation'
        db.create_table('submission_tagcreation', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('created_by', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
            ('revision', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['submission.Revision'])),
            ('tag', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['tagging.Tag'])),
            ('date_created', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
        ))
        db.send_create_signal('submission', ['TagCreation'])

        # Adding model 'ZipFile'
        db.create_table('submission_zipfile', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('date_added', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('zip_hash', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('raw_zip_file', self.gf('django.db.models.fields.files.FileField')(max_length=1024)),
        ))
        db.send_create_signal('submission', ['ZipFile'])

        # Adding model 'DisplayFile'
        db.create_table('submission_displayfile', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('fhash', self.gf('django.db.models.fields.CharField')(max_length=32)),
            ('display_type', self.gf('django.db.models.fields.CharField')(max_length=10)),
            ('display_obj', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
        ))
        db.send_create_signal('submission', ['DisplayFile'])


    def backwards(self, orm):
        # Deleting model 'Module'
        db.delete_table('submission_module')

        # Deleting model 'License'
        db.delete_table('submission_license')

        # Deleting model 'Submission'
        db.delete_table('submission_submission')

        # Removing M2M table for field inspired_by on 'Submission'
        db.delete_table('submission_submission_inspired_by')

        # Deleting model 'Revision'
        db.delete_table('submission_revision')

        # Removing M2M table for field modules_used on 'Revision'
        db.delete_table('submission_revision_modules_used')

        # Deleting model 'TagCreation'
        db.delete_table('submission_tagcreation')

        # Deleting model 'ZipFile'
        db.delete_table('submission_zipfile')

        # Deleting model 'DisplayFile'
        db.delete_table('submission_displayfile')


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
        'filestorage.fileset': {
            'Meta': {'object_name': 'FileSet'},
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'repo_path': ('django.db.models.fields.CharField', [], {'max_length': '500'})
        },
        'submission.displayfile': {
            'Meta': {'object_name': 'DisplayFile'},
            'display_obj': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'display_type': ('django.db.models.fields.CharField', [], {'max_length': '10'}),
            'fhash': ('django.db.models.fields.CharField', [], {'max_length': '32'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        'submission.license': {
            'Meta': {'object_name': 'License'},
            'description': ('django.db.models.fields.TextField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '255'}),
            'text_template': ('django.db.models.fields.TextField', [], {})
        },
        'submission.module': {
            'Meta': {'object_name': 'Module'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '100'}),
            'website': ('django.db.models.fields.URLField', [], {'max_length': '200'})
        },
        'submission.revision': {
            'Meta': {'ordering': "['date_created']", 'object_name': 'Revision'},
            'created_by': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']", 'null': 'True', 'blank': 'True'}),
            'date_created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {}),
            'description_html': ('django.db.models.fields.TextField', [], {}),
            'entry': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'revisions'", 'to': "orm['submission.Submission']"}),
            'hash_id': ('django.db.models.fields.CharField', [], {'max_length': '60', 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_displayed': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'item_code': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'item_highlighted_code': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'item_url': ('django.db.models.fields.URLField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'modules_used': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': "orm['submission.Module']", 'null': 'True', 'blank': 'True'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '155'}),
            'sub_license': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['submission.License']", 'null': 'True', 'blank': 'True'}),
            'tags': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['tagging.Tag']", 'through': "orm['submission.TagCreation']", 'symmetrical': 'False'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '150'}),
            'update_reason': ('django.db.models.fields.CharField', [], {'max_length': '155', 'null': 'True', 'blank': 'True'}),
            'validation_hash': ('django.db.models.fields.CharField', [], {'max_length': '40', 'null': 'True', 'blank': 'True'})
        },
        'submission.submission': {
            'Meta': {'object_name': 'Submission'},
            'created_by': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']", 'null': 'True', 'blank': 'True'}),
            'date_created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'fileset': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['filestorage.FileSet']", 'null': 'True', 'blank': 'True'}),
            'frozen': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'inspired_by': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "'inspired_by_rel_+'", 'null': 'True', 'to': "orm['submission.Submission']"}),
            'sub_type': ('django.db.models.fields.CharField', [], {'max_length': '10'})
        },
        'submission.tagcreation': {
            'Meta': {'object_name': 'TagCreation'},
            'created_by': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']"}),
            'date_created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'revision': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['submission.Revision']"}),
            'tag': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['tagging.Tag']"})
        },
        'submission.zipfile': {
            'Meta': {'object_name': 'ZipFile'},
            'date_added': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'raw_zip_file': ('django.db.models.fields.files.FileField', [], {'max_length': '1024'}),
            'zip_hash': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        'tagging.tag': {
            'Meta': {'object_name': 'Tag'},
            'description': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'blank': 'True'}),
            'name': ('django.db.models.fields.TextField', [], {'max_length': '50'}),
            'slug': ('django.db.models.fields.SlugField', [], {'unique': 'True', 'max_length': '50'}),
            'tag_type': ('django.db.models.fields.TextField', [], {'default': "'regular'", 'max_length': '10'})
        }
    }

    complete_apps = ['submission']