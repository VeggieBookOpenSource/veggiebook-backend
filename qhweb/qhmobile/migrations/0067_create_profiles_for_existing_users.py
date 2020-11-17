# -*- coding: utf-8 -*-
from south.v2 import DataMigration


class Migration(DataMigration):

    def forwards(self, orm):
        for user in orm['auth.User'].objects.all():
            orm['qhmobile.UserProfile'].objects.get_or_create(user=user)

    def backwards(self, orm):
        raise RuntimeError("Cannot reverse this migration.")

    models = {
        u'auth.group': {
            'Meta': {'object_name': 'Group'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        u'auth.permission': {
            'Meta': {'ordering': "(u'content_type__app_label', u'content_type__model', u'codename')", 'unique_together': "((u'content_type', u'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['contenttypes.ContentType']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        u'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "u'user_set'", 'blank': 'True', 'to': u"orm['auth.Group']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "u'user_set'", 'blank': 'True', 'to': u"orm['auth.Permission']"}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        u'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        u'easy_maps.address': {
            'Meta': {'object_name': 'Address'},
            'address': ('django.db.models.fields.CharField', [], {'max_length': '255', 'db_index': 'True'}),
            'computed_address': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'geocode_error': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'latitude': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'longitude': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'})
        },
        u'qhmobile.annotation': {
            'Meta': {'object_name': 'Annotation'},
            'color': ('django.db.models.fields.CharField', [], {'default': "'ffffff'", 'max_length': '6'}),
            'displayedIf': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['qhmobile.OrRequirement']"}),
            'en_img': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'en_img'", 'null': 'True', 'to': u"orm['qhmobile.StockPhoto']"}),
            'es_img': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'es_img'", 'null': 'True', 'to': u"orm['qhmobile.StockPhoto']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'text': ('django.db.models.fields.related.ForeignKey', [], {'default': '1', 'related_name': "'annotation'", 'to': u"orm['qhmobile.String']"})
        },
        u'qhmobile.attribute': {
            'Meta': {'object_name': 'Attribute'},
            'name': ('django.db.models.fields.CharField', [], {'max_length': '24', 'primary_key': 'True'})
        },
        u'qhmobile.booktype': {
            'Meta': {'object_name': 'BookType'},
            'id': ('django.db.models.fields.CharField', [], {'max_length': '24', 'primary_key': 'True'})
        },
        u'qhmobile.choicequestion': {
            'Meta': {'ordering': "['orderPriority', 'id']", 'object_name': 'ChoiceQuestion', '_ormbases': [u'qhmobile.Question']},
            u'question_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['qhmobile.Question']", 'unique': 'True', 'primary_key': 'True'})
        },
        u'qhmobile.coverphoto': {
            'Meta': {'ordering': "('order', 'id')", 'object_name': 'CoverPhoto'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'img': ('django.db.models.fields.files.ImageField', [], {'max_length': '100'}),
            'order': ('django.db.models.fields.IntegerField', [], {'default': '1000'}),
            'owner': ('django.db.models.fields.related.ForeignKey', [], {'default': 'None', 'to': u"orm['auth.User']", 'null': 'True', 'blank': 'True'}),
            'restrictTo': ('django.db.models.fields.related.ForeignKey', [], {'default': 'None', 'to': u"orm['qhmobile.FoodStuff']", 'null': 'True', 'blank': 'True'})
        },
        u'qhmobile.externallink': {
            'Meta': {'object_name': 'ExternalLink'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'language': ('django.db.models.fields.CharField', [], {'max_length': '2'}),
            'linkString': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['qhmobile.String']"}),
            'secret': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['qhmobile.Secret']"}),
            'url': ('django.db.models.fields.URLField', [], {'max_length': '200'})
        },
        u'qhmobile.foodpantry': {
            'Meta': {'object_name': 'FoodPantry', '_ormbases': [u'easy_maps.Address']},
            u'address_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['easy_maps.Address']", 'unique': 'True', 'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '256'}),
            'printerEmail': ('django.db.models.fields.EmailField', [], {'default': "'tdi2048cynp656@print.epsonconnect.com'", 'max_length': '75'}),
            'printer_name': ('django.db.models.fields.CharField', [], {'max_length': '48', 'null': 'True', 'blank': 'True'}),
            'printingAvailable': ('django.db.models.fields.BooleanField', [], {'default': 'False'})
        },
        u'qhmobile.foodstuff': {
            'Meta': {'object_name': 'FoodStuff'},
            'active': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'id': ('django.db.models.fields.CharField', [], {'max_length': '24', 'primary_key': 'True'}),
            'image': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['qhmobile.StockPhoto']"}),
            'nameString': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['qhmobile.String']"})
        },
        u'qhmobile.foodtip': {
            'Meta': {'ordering': "('foodStuff', 'fsIndex', 'id')", 'object_name': 'FoodTip'},
            'foodStuff': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['qhmobile.FoodStuff']"}),
            'fsIndex': ('django.db.models.fields.IntegerField', [], {'default': '10000'}),
            'heading': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'heading'", 'to': u"orm['qhmobile.String']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'requirement': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['qhmobile.OrRequirement']"})
        },
        u'qhmobile.librarydata': {
            'Meta': {'object_name': 'LibraryData'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'version': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'db_index': 'True', 'blank': 'True'})
        },
        u'qhmobile.multiplechoicequestion': {
            'Meta': {'ordering': "['orderPriority', 'id']", 'object_name': 'MultipleChoiceQuestion', '_ormbases': [u'qhmobile.ChoiceQuestion']},
            u'choicequestion_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['qhmobile.ChoiceQuestion']", 'unique': 'True', 'primary_key': 'True'})
        },
        u'qhmobile.orderabletip': {
            'Meta': {'ordering': "('position', 'id')", 'object_name': 'OrderableTip'},
            'content': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['qhmobile.String']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'photo': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['qhmobile.Photo']", 'null': 'True', 'blank': 'True'}),
            'position': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'tipId': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['qhmobile.FoodTip']"})
        },
        u'qhmobile.orrequirement': {
            'Meta': {'object_name': 'OrRequirement'},
            'attributes': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['qhmobile.Attribute']", 'symmetrical': 'False'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        u'qhmobile.photo': {
            'Meta': {'object_name': 'Photo'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'img': ('django.db.models.fields.files.ImageField', [], {'max_length': '100'})
        },
        u'qhmobile.question': {
            'Meta': {'ordering': "['orderPriority', 'id']", 'object_name': 'Question'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'intro': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'intro'", 'to': u"orm['qhmobile.String']"}),
            'mnemonic': ('django.db.models.fields.TextField', [], {}),
            'orderPriority': ('django.db.models.fields.IntegerField', [], {'default': '100'}),
            'phase': ('django.db.models.fields.CharField', [], {'max_length': '1'}),
            'qtype': ('django.db.models.fields.CharField', [], {'max_length': '1'}),
            'subIntro': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'subintro'", 'null': 'True', 'to': u"orm['qhmobile.String']"})
        },
        u'qhmobile.questionchoice': {
            'Meta': {'ordering': "['questionId', 'id']", 'object_name': 'QuestionChoice'},
            'attribute': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['qhmobile.Attribute']", 'unique': 'True'}),
            'content': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['qhmobile.String']"}),
            'firstDefault': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'questionId': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['qhmobile.Question']"})
        },
        u'qhmobile.quickhelpuser': {
            'Meta': {'object_name': 'QuickHelpUser'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'imageUrl': ('django.db.models.fields.URLField', [], {'max_length': '200'}),
            'lastFourDigits': ('django.db.models.fields.CharField', [], {'max_length': '4'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        u'qhmobile.recipe': {
            'Meta': {'object_name': 'Recipe'},
            'annotations': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': u"orm['qhmobile.Annotation']", 'null': 'True', 'blank': 'True'}),
            'canBeFrozen': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'canBeFrozen'", 'to': u"orm['qhmobile.String']"}),
            'canBeMadeAhead': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'canBeMadeAhead'", 'to': u"orm['qhmobile.String']"}),
            'foodStuff': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['qhmobile.FoodStuff']"}),
            'goodForLeftovers': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'goodForLeftovers'", 'to': u"orm['qhmobile.String']"}),
            'isActive': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'recipeId': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'requirements': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': u"orm['qhmobile.OrRequirement']", 'null': 'True', 'blank': 'True'}),
            'rid': ('django.db.models.fields.CharField', [], {'max_length': '6', 'null': 'True', 'blank': 'True'}),
            'servings': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'servings'", 'to': u"orm['qhmobile.String']"}),
            'storyLine': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'storyline'", 'null': 'True', 'to': u"orm['qhmobile.String']"}),
            'timeToCook': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'timeToCook'", 'to': u"orm['qhmobile.String']"}),
            'timeToPrepare': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'timeToPrepare'", 'to': u"orm['qhmobile.String']"}),
            'title': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'title'", 'to': u"orm['qhmobile.String']"})
        },
        u'qhmobile.recipeannotation': {
            'Meta': {'object_name': 'RecipeAnnotation'},
            'name': ('django.db.models.fields.CharField', [], {'max_length': '24', 'primary_key': 'True'})
        },
        u'qhmobile.recipebook': {
            'Meta': {'object_name': 'RecipeBook'},
            'attributes': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['qhmobile.Attribute']", 'symmetrical': 'False'}),
            'coverPhoto': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['qhmobile.CoverPhoto']"}),
            'createdAt': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'foodStuff': ('django.db.models.fields.related.ForeignKey', [], {'default': 'None', 'to': u"orm['qhmobile.FoodStuff']", 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'latitude': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'longitude': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'pantry': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['qhmobile.FoodPantry']", 'null': 'True', 'blank': 'True'}),
            'pdf_en': ('django.db.models.fields.files.FileField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'pdf_es': ('django.db.models.fields.files.FileField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'selections': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['qhmobile.RecipeBookSelection']", 'symmetrical': 'False'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']"})
        },
        u'qhmobile.recipebookselection': {
            'Meta': {'object_name': 'RecipeBookSelection'},
            'extras': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'recipe': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['qhmobile.Recipe']"}),
            'scrolled': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'selected': ('django.db.models.fields.BooleanField', [], {'default': 'True'})
        },
        u'qhmobile.recipeingredient': {
            'Meta': {'ordering': "('position', 'id')", 'object_name': 'RecipeIngredient'},
            'content': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['qhmobile.String']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'position': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'recipeId': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['qhmobile.Recipe']"})
        },
        u'qhmobile.recipenote': {
            'Meta': {'ordering': "('position', 'id')", 'object_name': 'RecipeNote'},
            'content': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['qhmobile.String']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'position': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'recipeId': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['qhmobile.Recipe']"})
        },
        u'qhmobile.recipephoto': {
            'Meta': {'ordering': "('position', 'id')", 'object_name': 'RecipePhoto'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'photo': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['qhmobile.Photo']"}),
            'position': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'recipeId': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['qhmobile.Recipe']"})
        },
        u'qhmobile.recipestep': {
            'Meta': {'ordering': "('position', 'id')", 'object_name': 'RecipeStep'},
            'content': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['qhmobile.String']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'position': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'recipeId': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['qhmobile.Recipe']"})
        },
        u'qhmobile.secret': {
            'Meta': {'object_name': 'Secret'},
            'attachment_en': ('django.db.models.fields.files.FileField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'attachment_es': ('django.db.models.fields.files.FileField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'category': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['qhmobile.SecretCategory']"}),
            'coverImage': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['qhmobile.CoverPhoto']", 'null': 'True', 'on_delete': 'models.PROTECT', 'blank': 'True'}),
            'coverImage_es': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'coverImage_es'", 'null': 'True', 'on_delete': 'models.PROTECT', 'to': u"orm['qhmobile.CoverPhoto']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'image_es': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'isActive': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'secret': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'secretText'", 'to': u"orm['qhmobile.String']"}),
            'title': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'secretTitle'", 'to': u"orm['qhmobile.String']"}),
            'whyItWorks': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'whyItWorks'", 'to': u"orm['qhmobile.String']"})
        },
        u'qhmobile.secretbook': {
            'Meta': {'object_name': 'SecretBook'},
            'category': ('django.db.models.fields.related.ForeignKey', [], {'default': 'None', 'to': u"orm['qhmobile.SecretCategory']", 'null': 'True', 'blank': 'True'}),
            'coverPhoto': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['qhmobile.CoverPhoto']"}),
            'createdAt': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'latitude': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'longitude': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'pantry': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['qhmobile.FoodPantry']", 'null': 'True', 'blank': 'True'}),
            'pdf_en': ('django.db.models.fields.files.FileField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'pdf_es': ('django.db.models.fields.files.FileField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'selections': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['qhmobile.SecretBookSelection']", 'symmetrical': 'False'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']"}),
            'who_says_so_viewed': ('django.db.models.fields.BooleanField', [], {'default': 'False'})
        },
        u'qhmobile.secretbookselection': {
            'Meta': {'object_name': 'SecretBookSelection'},
            'extras': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'scrolled': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'secret': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['qhmobile.Secret']"}),
            'selected': ('django.db.models.fields.BooleanField', [], {'default': 'True'})
        },
        u'qhmobile.secretcategory': {
            'Meta': {'ordering': "('positionIndex', 'id')", 'object_name': 'SecretCategory'},
            'color': ('django.db.models.fields.CharField', [], {'default': "'69d0ee'", 'max_length': '6'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'positionIndex': ('django.db.models.fields.IntegerField', [], {'default': '100'}),
            'title': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'secretCategory'", 'to': u"orm['qhmobile.String']"})
        },
        u'qhmobile.singlechoicequestion': {
            'Meta': {'ordering': "['orderPriority', 'id']", 'object_name': 'SingleChoiceQuestion', '_ormbases': [u'qhmobile.ChoiceQuestion']},
            u'choicequestion_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['qhmobile.ChoiceQuestion']", 'unique': 'True', 'primary_key': 'True'})
        },
        u'qhmobile.stockphoto': {
            'Meta': {'object_name': 'StockPhoto'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'img': ('django.db.models.fields.files.ImageField', [], {'max_length': '100'})
        },
        u'qhmobile.string': {
            'Meta': {'ordering': "['-id']", 'object_name': 'String'},
            'en': ('django.db.models.fields.TextField', [], {}),
            'es': ('django.db.models.fields.TextField', [], {'default': "'needs translation'"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'needsTranslation': ('django.db.models.fields.BooleanField', [], {'default': 'True', 'db_index': 'True'})
        },
        u'qhmobile.tipdoc': {
            'Meta': {'object_name': 'TipDoc'},
            'active': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'id': ('django.db.models.fields.CharField', [], {'max_length': '24', 'primary_key': 'True'}),
            'image': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['qhmobile.StockPhoto']"}),
            'nameString': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['qhmobile.String']"})
        },
        u'qhmobile.userprofile': {
            'Meta': {'object_name': 'UserProfile'},
            'deviceId': ('django.db.models.fields.TextField', [], {'max_length': '38', 'null': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'user': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['auth.User']", 'unique': 'True'})
        },
        u'qhmobile.viewingdata': {
            'Meta': {'object_name': 'ViewingData'},
            'book_id': ('django.db.models.fields.CharField', [], {'max_length': '56'}),
            'data': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'event': ('django.db.models.fields.CharField', [], {'max_length': '1'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'recipe': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['qhmobile.Recipe']", 'null': 'True', 'blank': 'True'}),
            'recipeBook': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['qhmobile.RecipeBook']", 'null': 'True', 'blank': 'True'}),
            'secret': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['qhmobile.Secret']", 'null': 'True', 'blank': 'True'}),
            'secretBook': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['qhmobile.SecretBook']", 'null': 'True', 'blank': 'True'}),
            'timeStamp': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'type': ('django.db.models.fields.CharField', [], {'max_length': '1'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']"})
        }
    }

    complete_apps = ['qhmobile']
    symmetrical = True
