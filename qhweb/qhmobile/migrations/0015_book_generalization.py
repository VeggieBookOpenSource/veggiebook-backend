# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import DataMigration
from django.db import models

class Migration(DataMigration):

    def forwards(self, orm):
        "Write your forwards methods here."
        # Note: Remember to use orm['appname.ModelName'] rather than "from appname.models..."
        orm['qhmobile.LibraryData'].objects.create().save()

        for foodstuff in orm['qhmobile.FoodStuff'].objects.all():
            loc = "stock/%s.jpg" % foodstuff.id.lower()
            photo = orm['qhmobile.StockPhoto'].objects.create(img=loc)
            photo.save()
            foodstuff.image = photo
            foodstuff.active = True
            foodstuff.save()


    def backwards(self, orm):
        "Backward migration just deletes columns, so the schemamigration covers it."
        pass

    models = {
        'qhmobile.annotation': {
            'Meta': {'object_name': 'Annotation'},
            'displayedIf': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['qhmobile.OrRequirement']"}),
            'en_img': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'en_img'", 'null': 'True', 'to': "orm['qhmobile.StockPhoto']"}),
            'es_img': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'es_img'", 'null': 'True', 'to': "orm['qhmobile.StockPhoto']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
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
            'Meta': {'ordering': "['id']", 'object_name': 'ChoiceQuestion', '_ormbases': ['qhmobile.Question']},
            'question_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['qhmobile.Question']", 'unique': 'True', 'primary_key': 'True'})
        },
        'qhmobile.foodstuff': {
            'Meta': {'object_name': 'FoodStuff'},
            'active': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'id': ('django.db.models.fields.CharField', [], {'max_length': '24', 'primary_key': 'True'}),
            'image': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['qhmobile.StockPhoto']", 'null': 'True', 'blank': 'True'}),
            'nameString': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['qhmobile.String']"})
        },
        'qhmobile.librarydata': {
            'Meta': {'object_name': 'LibraryData'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'version': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'db_index': 'True', 'blank': 'True'})
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
        'qhmobile.recipeingredient': {
            'Meta': {'ordering': "('position', 'id')", 'object_name': 'RecipeIngredient'},
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
            'Meta': {'ordering': "['-id']", 'object_name': 'String'},
            'en': ('django.db.models.fields.TextField', [], {}),
            'es': ('django.db.models.fields.TextField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'needsTranslation': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'db_index': 'True'})
        },
        'qhmobile.tipdoc': {
            'Meta': {'object_name': 'TipDoc'},
            'active': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'id': ('django.db.models.fields.CharField', [], {'max_length': '24', 'primary_key': 'True'}),
            'image': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['qhmobile.StockPhoto']", 'null': 'True', 'blank': 'True'}),
            'nameString': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['qhmobile.String']"})
        }
    }

    complete_apps = ['qhmobile']
    symmetrical = True
