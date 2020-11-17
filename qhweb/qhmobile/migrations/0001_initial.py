# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'QuickHelpUser'
        db.create_table('qhmobile_quickhelpuser', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('lastFourDigits', self.gf('django.db.models.fields.CharField')(max_length=4)),
            ('imageUrl', self.gf('django.db.models.fields.URLField')(max_length=200)),
        ))
        db.send_create_signal('qhmobile', ['QuickHelpUser'])

        # Adding model 'String'
        db.create_table('qhmobile_string', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('en', self.gf('django.db.models.fields.TextField')()),
            ('es', self.gf('django.db.models.fields.TextField')()),
            ('needsTranslation', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal('qhmobile', ['String'])

        # Adding model 'FoodStuff'
        db.create_table('qhmobile_foodstuff', (
            ('id', self.gf('django.db.models.fields.CharField')(max_length=24, primary_key=True)),
            ('nameString', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['qhmobile.String'])),
            ('active', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal('qhmobile', ['FoodStuff'])

        # Adding model 'Attribute'
        db.create_table('qhmobile_attribute', (
            ('name', self.gf('django.db.models.fields.CharField')(max_length=24, primary_key=True)),
        ))
        db.send_create_signal('qhmobile', ['Attribute'])

        # Adding model 'OrRequirement'
        db.create_table('qhmobile_orrequirement', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
        ))
        db.send_create_signal('qhmobile', ['OrRequirement'])

        # Adding M2M table for field attributes on 'OrRequirement'
        db.create_table('qhmobile_orrequirement_attributes', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('orrequirement', models.ForeignKey(orm['qhmobile.orrequirement'], null=False)),
            ('attribute', models.ForeignKey(orm['qhmobile.attribute'], null=False))
        ))
        db.create_unique('qhmobile_orrequirement_attributes', ['orrequirement_id', 'attribute_id'])

        # Adding model 'StockPhoto'
        db.create_table('qhmobile_stockphoto', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('img', self.gf('django.db.models.fields.files.ImageField')(max_length=100)),
        ))
        db.send_create_signal('qhmobile', ['StockPhoto'])

        # Adding model 'Photo'
        db.create_table('qhmobile_photo', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('img', self.gf('django.db.models.fields.files.ImageField')(max_length=100)),
        ))
        db.send_create_signal('qhmobile', ['Photo'])

        # Adding model 'Annotation'
        db.create_table('qhmobile_annotation', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('img', self.gf('django.db.models.fields.files.ImageField')(max_length=100, null=True, blank=True)),
            ('displayedIf', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['qhmobile.OrRequirement'])),
        ))
        db.send_create_signal('qhmobile', ['Annotation'])

        # Adding model 'RecipeAnnotation'
        db.create_table('qhmobile_recipeannotation', (
            ('name', self.gf('django.db.models.fields.CharField')(max_length=24, primary_key=True)),
        ))
        db.send_create_signal('qhmobile', ['RecipeAnnotation'])

        # Adding model 'Recipe'
        db.create_table('qhmobile_recipe', (
            ('recipeId', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('title', self.gf('django.db.models.fields.related.ForeignKey')(related_name='title', to=orm['qhmobile.String'])),
            ('isActive', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('storyLine', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='storyline', null=True, to=orm['qhmobile.String'])),
            ('timeToPrepare', self.gf('django.db.models.fields.related.ForeignKey')(related_name='timeToPrepare', to=orm['qhmobile.String'])),
            ('timeToCook', self.gf('django.db.models.fields.related.ForeignKey')(related_name='timeToCook', to=orm['qhmobile.String'])),
            ('servings', self.gf('django.db.models.fields.related.ForeignKey')(related_name='servings', to=orm['qhmobile.String'])),
            ('canBeMadeAhead', self.gf('django.db.models.fields.related.ForeignKey')(related_name='canBeMadeAhead', to=orm['qhmobile.String'])),
            ('canBeFrozen', self.gf('django.db.models.fields.related.ForeignKey')(related_name='canBeFrozen', to=orm['qhmobile.String'])),
            ('goodForLeftovers', self.gf('django.db.models.fields.related.ForeignKey')(related_name='goodForLeftovers', to=orm['qhmobile.String'])),
            ('rid', self.gf('django.db.models.fields.CharField')(unique=True, max_length=6, blank=True)),
            ('foodStuff', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['qhmobile.FoodStuff'])),
        ))
        db.send_create_signal('qhmobile', ['Recipe'])

        # Adding M2M table for field requirements on 'Recipe'
        db.create_table('qhmobile_recipe_requirements', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('recipe', models.ForeignKey(orm['qhmobile.recipe'], null=False)),
            ('orrequirement', models.ForeignKey(orm['qhmobile.orrequirement'], null=False))
        ))
        db.create_unique('qhmobile_recipe_requirements', ['recipe_id', 'orrequirement_id'])

        # Adding M2M table for field photos on 'Recipe'
        db.create_table('qhmobile_recipe_photos', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('recipe', models.ForeignKey(orm['qhmobile.recipe'], null=False)),
            ('photo', models.ForeignKey(orm['qhmobile.photo'], null=False))
        ))
        db.create_unique('qhmobile_recipe_photos', ['recipe_id', 'photo_id'])

        # Adding M2M table for field annotations on 'Recipe'
        db.create_table('qhmobile_recipe_annotations', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('recipe', models.ForeignKey(orm['qhmobile.recipe'], null=False)),
            ('annotation', models.ForeignKey(orm['qhmobile.annotation'], null=False))
        ))
        db.create_unique('qhmobile_recipe_annotations', ['recipe_id', 'annotation_id'])

        # Adding model 'RecipeIngredient'
        db.create_table('qhmobile_recipeingredient', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('recipeId', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['qhmobile.Recipe'])),
            ('content', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['qhmobile.String'])),
        ))
        db.send_create_signal('qhmobile', ['RecipeIngredient'])

        # Adding model 'RecipeStep'
        db.create_table('qhmobile_recipestep', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('recipeId', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['qhmobile.Recipe'])),
            ('content', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['qhmobile.String'])),
        ))
        db.send_create_signal('qhmobile', ['RecipeStep'])

        # Adding model 'Question'
        db.create_table('qhmobile_question', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('mnemonic', self.gf('django.db.models.fields.TextField')()),
            ('phase', self.gf('django.db.models.fields.CharField')(max_length=1)),
            ('intro', self.gf('django.db.models.fields.related.ForeignKey')(related_name='intro', to=orm['qhmobile.String'])),
            ('qtype', self.gf('django.db.models.fields.CharField')(max_length=1)),
        ))
        db.send_create_signal('qhmobile', ['Question'])

        # Adding model 'ChoiceQuestion'
        db.create_table('qhmobile_choicequestion', (
            ('question_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['qhmobile.Question'], unique=True, primary_key=True)),
        ))
        db.send_create_signal('qhmobile', ['ChoiceQuestion'])

        # Adding model 'MultipleChoiceQuestion'
        db.create_table('qhmobile_multiplechoicequestion', (
            ('choicequestion_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['qhmobile.ChoiceQuestion'], unique=True, primary_key=True)),
        ))
        db.send_create_signal('qhmobile', ['MultipleChoiceQuestion'])

        # Adding model 'SingleChoiceQuestion'
        db.create_table('qhmobile_singlechoicequestion', (
            ('choicequestion_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['qhmobile.ChoiceQuestion'], unique=True, primary_key=True)),
        ))
        db.send_create_signal('qhmobile', ['SingleChoiceQuestion'])

        # Adding model 'QuestionChoice'
        db.create_table('qhmobile_questionchoice', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('questionId', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['qhmobile.Question'])),
            ('content', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['qhmobile.String'])),
            ('attribute', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['qhmobile.Attribute'])),
        ))
        db.send_create_signal('qhmobile', ['QuestionChoice'])


    def backwards(self, orm):
        # Deleting model 'QuickHelpUser'
        db.delete_table('qhmobile_quickhelpuser')

        # Deleting model 'String'
        db.delete_table('qhmobile_string')

        # Deleting model 'FoodStuff'
        db.delete_table('qhmobile_foodstuff')

        # Deleting model 'Attribute'
        db.delete_table('qhmobile_attribute')

        # Deleting model 'OrRequirement'
        db.delete_table('qhmobile_orrequirement')

        # Removing M2M table for field attributes on 'OrRequirement'
        db.delete_table('qhmobile_orrequirement_attributes')

        # Deleting model 'StockPhoto'
        db.delete_table('qhmobile_stockphoto')

        # Deleting model 'Photo'
        db.delete_table('qhmobile_photo')

        # Deleting model 'Annotation'
        db.delete_table('qhmobile_annotation')

        # Deleting model 'RecipeAnnotation'
        db.delete_table('qhmobile_recipeannotation')

        # Deleting model 'Recipe'
        db.delete_table('qhmobile_recipe')

        # Removing M2M table for field requirements on 'Recipe'
        db.delete_table('qhmobile_recipe_requirements')

        # Removing M2M table for field photos on 'Recipe'
        db.delete_table('qhmobile_recipe_photos')

        # Removing M2M table for field annotations on 'Recipe'
        db.delete_table('qhmobile_recipe_annotations')

        # Deleting model 'RecipeIngredient'
        db.delete_table('qhmobile_recipeingredient')

        # Deleting model 'RecipeStep'
        db.delete_table('qhmobile_recipestep')

        # Deleting model 'Question'
        db.delete_table('qhmobile_question')

        # Deleting model 'ChoiceQuestion'
        db.delete_table('qhmobile_choicequestion')

        # Deleting model 'MultipleChoiceQuestion'
        db.delete_table('qhmobile_multiplechoicequestion')

        # Deleting model 'SingleChoiceQuestion'
        db.delete_table('qhmobile_singlechoicequestion')

        # Deleting model 'QuestionChoice'
        db.delete_table('qhmobile_questionchoice')


    models = {
        'qhmobile.annotation': {
            'Meta': {'object_name': 'Annotation'},
            'displayedIf': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['qhmobile.OrRequirement']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'img': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'})
        },
        'qhmobile.attribute': {
            'Meta': {'object_name': 'Attribute'},
            'name': ('django.db.models.fields.CharField', [], {'max_length': '24', 'primary_key': 'True'})
        },
        'qhmobile.choicequestion': {
            'Meta': {'ordering': "['id']", 'object_name': 'ChoiceQuestion', '_ormbases': ['qhmobile.Question']},
            'question_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['qhmobile.Question']", 'unique': 'True', 'primary_key': 'True'})
        },
        'qhmobile.foodstuff': {
            'Meta': {'object_name': 'FoodStuff'},
            'active': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'id': ('django.db.models.fields.CharField', [], {'max_length': '24', 'primary_key': 'True'}),
            'nameString': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['qhmobile.String']"})
        },
        'qhmobile.multiplechoicequestion': {
            'Meta': {'ordering': "['id']", 'object_name': 'MultipleChoiceQuestion', '_ormbases': ['qhmobile.ChoiceQuestion']},
            'choicequestion_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['qhmobile.ChoiceQuestion']", 'unique': 'True', 'primary_key': 'True'})
        },
        'qhmobile.orrequirement': {
            'Meta': {'object_name': 'OrRequirement'},
            'attributes': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['qhmobile.Attribute']", 'symmetrical': 'False'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        'qhmobile.photo': {
            'Meta': {'object_name': 'Photo'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'img': ('django.db.models.fields.files.ImageField', [], {'max_length': '100'})
        },
        'qhmobile.question': {
            'Meta': {'ordering': "['id']", 'object_name': 'Question'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'intro': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'intro'", 'to': "orm['qhmobile.String']"}),
            'mnemonic': ('django.db.models.fields.TextField', [], {}),
            'phase': ('django.db.models.fields.CharField', [], {'max_length': '1'}),
            'qtype': ('django.db.models.fields.CharField', [], {'max_length': '1'})
        },
        'qhmobile.questionchoice': {
            'Meta': {'ordering': "['questionId', 'id']", 'object_name': 'QuestionChoice'},
            'attribute': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['qhmobile.Attribute']"}),
            'content': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['qhmobile.String']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'questionId': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['qhmobile.Question']"})
        },
        'qhmobile.quickhelpuser': {
            'Meta': {'object_name': 'QuickHelpUser'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'imageUrl': ('django.db.models.fields.URLField', [], {'max_length': '200'}),
            'lastFourDigits': ('django.db.models.fields.CharField', [], {'max_length': '4'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        'qhmobile.recipe': {
            'Meta': {'object_name': 'Recipe'},
            'annotations': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': "orm['qhmobile.Annotation']", 'null': 'True', 'blank': 'True'}),
            'canBeFrozen': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'canBeFrozen'", 'to': "orm['qhmobile.String']"}),
            'canBeMadeAhead': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'canBeMadeAhead'", 'to': "orm['qhmobile.String']"}),
            'foodStuff': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['qhmobile.FoodStuff']"}),
            'goodForLeftovers': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'goodForLeftovers'", 'to': "orm['qhmobile.String']"}),
            'isActive': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'photos': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': "orm['qhmobile.Photo']", 'null': 'True', 'blank': 'True'}),
            'recipeId': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'requirements': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': "orm['qhmobile.OrRequirement']", 'null': 'True', 'blank': 'True'}),
            'rid': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '6', 'blank': 'True'}),
            'servings': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'servings'", 'to': "orm['qhmobile.String']"}),
            'storyLine': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'storyline'", 'null': 'True', 'to': "orm['qhmobile.String']"}),
            'timeToCook': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'timeToCook'", 'to': "orm['qhmobile.String']"}),
            'timeToPrepare': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'timeToPrepare'", 'to': "orm['qhmobile.String']"}),
            'title': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'title'", 'to': "orm['qhmobile.String']"})
        },
        'qhmobile.recipeannotation': {
            'Meta': {'object_name': 'RecipeAnnotation'},
            'name': ('django.db.models.fields.CharField', [], {'max_length': '24', 'primary_key': 'True'})
        },
        'qhmobile.recipeingredient': {
            'Meta': {'ordering': "['recipeId', 'id']", 'object_name': 'RecipeIngredient'},
            'content': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['qhmobile.String']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'recipeId': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['qhmobile.Recipe']"})
        },
        'qhmobile.recipestep': {
            'Meta': {'ordering': "['recipeId', 'id']", 'object_name': 'RecipeStep'},
            'content': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['qhmobile.String']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'recipeId': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['qhmobile.Recipe']"})
        },
        'qhmobile.singlechoicequestion': {
            'Meta': {'ordering': "['id']", 'object_name': 'SingleChoiceQuestion', '_ormbases': ['qhmobile.ChoiceQuestion']},
            'choicequestion_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['qhmobile.ChoiceQuestion']", 'unique': 'True', 'primary_key': 'True'})
        },
        'qhmobile.stockphoto': {
            'Meta': {'object_name': 'StockPhoto'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'img': ('django.db.models.fields.files.ImageField', [], {'max_length': '100'})
        },
        'qhmobile.string': {
            'Meta': {'object_name': 'String'},
            'en': ('django.db.models.fields.TextField', [], {}),
            'es': ('django.db.models.fields.TextField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'needsTranslation': ('django.db.models.fields.BooleanField', [], {'default': 'False'})
        }
    }

    complete_apps = ['qhmobile']