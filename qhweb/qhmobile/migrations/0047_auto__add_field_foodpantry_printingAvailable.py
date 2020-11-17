# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'FoodPantry.printingAvailable'
        db.add_column('qhmobile_foodpantry', 'printingAvailable',
                      self.gf('django.db.models.fields.BooleanField')(default=False),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting field 'FoodPantry.printingAvailable'
        db.delete_column('qhmobile_foodpantry', 'printingAvailable')


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
        'easy_maps.address': {
            'Meta': {'object_name': 'Address'},
            'address': ('django.db.models.fields.CharField', [], {'max_length': '255', 'db_index': 'True'}),
            'computed_address': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'geocode_error': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'latitude': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'longitude': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'})
        },
        'qhmobile.annotation': {
            'Meta': {'object_name': 'Annotation'},
            'color': ('django.db.models.fields.CharField', [], {'default': "'ffffff'", 'max_length': '6'}),
            'displayedIf': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['qhmobile.OrRequirement']"}),
            'en_img': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'en_img'", 'null': 'True', 'to': "orm['qhmobile.StockPhoto']"}),
            'es_img': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'es_img'", 'null': 'True', 'to': "orm['qhmobile.StockPhoto']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'text': ('django.db.models.fields.related.ForeignKey', [], {'default': '1', 'related_name': "'annotation'", 'to': "orm['qhmobile.String']"})
        },
        'qhmobile.attribute': {
            'Meta': {'object_name': 'Attribute'},
            'name': ('django.db.models.fields.CharField', [], {'max_length': '24', 'primary_key': 'True'})
        },
        'qhmobile.booktype': {
            'Meta': {'object_name': 'BookType'},
            'id': ('django.db.models.fields.CharField', [], {'max_length': '24', 'primary_key': 'True'})
        },
        'qhmobile.choicequestion': {
            'Meta': {'ordering': "['orderPriority', 'id']", 'object_name': 'ChoiceQuestion', '_ormbases': ['qhmobile.Question']},
            'question_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['qhmobile.Question']", 'unique': 'True', 'primary_key': 'True'})
        },
        'qhmobile.coverphoto': {
            'Meta': {'ordering': "('order', 'id')", 'object_name': 'CoverPhoto'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'img': ('django.db.models.fields.files.ImageField', [], {'max_length': '100'}),
            'order': ('django.db.models.fields.IntegerField', [], {'default': '1000'}),
            'owner': ('django.db.models.fields.related.ForeignKey', [], {'default': 'None', 'to': "orm['auth.User']", 'null': 'True', 'blank': 'True'}),
            'restrictTo': ('django.db.models.fields.related.ForeignKey', [], {'default': 'None', 'to': "orm['qhmobile.FoodStuff']", 'null': 'True', 'blank': 'True'})
        },
        'qhmobile.foodpantry': {
            'Meta': {'object_name': 'FoodPantry', '_ormbases': ['easy_maps.Address']},
            'address_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['easy_maps.Address']", 'unique': 'True', 'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '256'}),
            'printerEmail': ('django.db.models.fields.EmailField', [], {'default': "'tdi2048cynp656@print.epsonconnect.com'", 'max_length': '75'}),
            'printingAvailable': ('django.db.models.fields.BooleanField', [], {'default': 'False'})
        },
        'qhmobile.foodstuff': {
            'Meta': {'object_name': 'FoodStuff'},
            'active': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'id': ('django.db.models.fields.CharField', [], {'max_length': '24', 'primary_key': 'True'}),
            'image': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['qhmobile.StockPhoto']"}),
            'nameString': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['qhmobile.String']"})
        },
        'qhmobile.foodtip': {
            'Meta': {'ordering': "('foodStuff', 'fsIndex', 'id')", 'object_name': 'FoodTip'},
            'foodStuff': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['qhmobile.FoodStuff']"}),
            'fsIndex': ('django.db.models.fields.IntegerField', [], {'default': '10000'}),
            'heading': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'heading'", 'to': "orm['qhmobile.String']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'requirement': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['qhmobile.OrRequirement']"})
        },
        'qhmobile.librarydata': {
            'Meta': {'object_name': 'LibraryData'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'version': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'db_index': 'True', 'blank': 'True'})
        },
        'qhmobile.multiplechoicequestion': {
            'Meta': {'ordering': "['orderPriority', 'id']", 'object_name': 'MultipleChoiceQuestion', '_ormbases': ['qhmobile.ChoiceQuestion']},
            'choicequestion_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['qhmobile.ChoiceQuestion']", 'unique': 'True', 'primary_key': 'True'})
        },
        'qhmobile.orderabletip': {
            'Meta': {'ordering': "('position', 'id')", 'object_name': 'OrderableTip'},
            'content': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['qhmobile.String']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'photo': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['qhmobile.Photo']", 'null': 'True', 'blank': 'True'}),
            'position': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'tipId': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['qhmobile.FoodTip']"})
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
            'Meta': {'ordering': "['orderPriority', 'id']", 'object_name': 'Question'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'intro': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'intro'", 'to': "orm['qhmobile.String']"}),
            'mnemonic': ('django.db.models.fields.TextField', [], {}),
            'orderPriority': ('django.db.models.fields.IntegerField', [], {'default': '100'}),
            'phase': ('django.db.models.fields.CharField', [], {'max_length': '1'}),
            'qtype': ('django.db.models.fields.CharField', [], {'max_length': '1'}),
            'subIntro': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'subintro'", 'null': 'True', 'to': "orm['qhmobile.String']"})
        },
        'qhmobile.questionchoice': {
            'Meta': {'ordering': "['questionId', 'id']", 'object_name': 'QuestionChoice'},
            'attribute': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['qhmobile.Attribute']", 'unique': 'True'}),
            'content': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['qhmobile.String']"}),
            'firstDefault': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
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
            'recipeId': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'requirements': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': "orm['qhmobile.OrRequirement']", 'null': 'True', 'blank': 'True'}),
            'rid': ('django.db.models.fields.CharField', [], {'max_length': '6', 'null': 'True', 'blank': 'True'}),
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
        'qhmobile.recipebook': {
            'Meta': {'object_name': 'RecipeBook'},
            'attributes': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['qhmobile.Attribute']", 'symmetrical': 'False'}),
            'coverPhoto': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['qhmobile.CoverPhoto']"}),
            'createdAt': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'foodStuff': ('django.db.models.fields.related.ForeignKey', [], {'default': 'None', 'to': "orm['qhmobile.FoodStuff']", 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'pantry': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['qhmobile.FoodPantry']", 'null': 'True', 'blank': 'True'}),
            'pdf_en': ('django.db.models.fields.files.FileField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'pdf_es': ('django.db.models.fields.files.FileField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'selections': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['qhmobile.RecipeBookSelection']", 'symmetrical': 'False'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']"})
        },
        'qhmobile.recipebookselection': {
            'Meta': {'object_name': 'RecipeBookSelection'},
            'extras': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'recipe': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['qhmobile.Recipe']"}),
            'selected': ('django.db.models.fields.BooleanField', [], {'default': 'True'})
        },
        'qhmobile.recipeingredient': {
            'Meta': {'ordering': "('position', 'id')", 'object_name': 'RecipeIngredient'},
            'content': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['qhmobile.String']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'position': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'recipeId': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['qhmobile.Recipe']"})
        },
        'qhmobile.recipenote': {
            'Meta': {'ordering': "('position', 'id')", 'object_name': 'RecipeNote'},
            'content': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['qhmobile.String']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'position': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'recipeId': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['qhmobile.Recipe']"})
        },
        'qhmobile.recipephoto': {
            'Meta': {'ordering': "('position', 'id')", 'object_name': 'RecipePhoto'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'photo': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['qhmobile.Photo']"}),
            'position': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'recipeId': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['qhmobile.Recipe']"})
        },
        'qhmobile.recipestep': {
            'Meta': {'ordering': "('position', 'id')", 'object_name': 'RecipeStep'},
            'content': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['qhmobile.String']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'position': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'recipeId': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['qhmobile.Recipe']"})
        },
        'qhmobile.secret': {
            'Meta': {'object_name': 'Secret'},
            'category': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['qhmobile.SecretCategory']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'isActive': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'secret': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'secretText'", 'to': "orm['qhmobile.String']"}),
            'title': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'secretTitle'", 'to': "orm['qhmobile.String']"}),
            'whyItWorks': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'whyItWorks'", 'to': "orm['qhmobile.String']"})
        },
        'qhmobile.secretcategory': {
            'Meta': {'object_name': 'SecretCategory'},
            'color': ('django.db.models.fields.CharField', [], {'default': "'69d0ee'", 'max_length': '6'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'title': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'secretCategory'", 'to': "orm['qhmobile.String']"})
        },
        'qhmobile.singlechoicequestion': {
            'Meta': {'ordering': "['orderPriority', 'id']", 'object_name': 'SingleChoiceQuestion', '_ormbases': ['qhmobile.ChoiceQuestion']},
            'choicequestion_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['qhmobile.ChoiceQuestion']", 'unique': 'True', 'primary_key': 'True'})
        },
        'qhmobile.stockphoto': {
            'Meta': {'object_name': 'StockPhoto'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'img': ('django.db.models.fields.files.ImageField', [], {'max_length': '100'})
        },
        'qhmobile.string': {
            'Meta': {'ordering': "['-id']", 'object_name': 'String'},
            'en': ('django.db.models.fields.TextField', [], {}),
            'es': ('django.db.models.fields.TextField', [], {'default': "'needs translation'"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'needsTranslation': ('django.db.models.fields.BooleanField', [], {'default': 'True', 'db_index': 'True'})
        },
        'qhmobile.tipdoc': {
            'Meta': {'object_name': 'TipDoc'},
            'active': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'id': ('django.db.models.fields.CharField', [], {'max_length': '24', 'primary_key': 'True'}),
            'image': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['qhmobile.StockPhoto']"}),
            'nameString': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['qhmobile.String']"})
        }
    }

    complete_apps = ['qhmobile']