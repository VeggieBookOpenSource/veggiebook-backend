# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import DataMigration
from django.db import models

class Migration(DataMigration):

    # current rid encoding
    # find the recipe whose rid is 10203
    # 10 means broccoli, 203 means recipe number 203

    # i = 'BR-203/photo1.jpg'
    # p = Photo(img='recipe/%s' % i, id=1020301)
    # p.save()
    # r = Recipe.objects.get(rid=10203)
    # r.recipephoto_set.create(photo=p)
    # r.save()

    nameMap = {'BR': 10,
               'CA': 12,
               'CB': 11,
               'CL': 13,
               'GB': 14,
               'ON': 15,
               'PO': 16,
               'RV': 17,
               'SW': 18,
               'ZU': 19}

    def link_recipe_photo(self, orm, i):
        # reify photo object
        p = orm.Photo(img='recipe/%s' % i)
        p.save()
        # reify recipe
        prefix = Migration.nameMap[i[0:2]]
        suffix = i[3:6]
        rid = int(str(prefix) + str(suffix))
        try:
            r = orm.Recipe.objects.get(rid=rid)
            # insert photo into recipe
            r.recipephoto_set.create(photo=p)
            r.save()
            print "Inserted %s : %s" % (r, p)
        except Exception, e:
            pass #print "Skipped %s : %s" % (rid, p)

    def forwards(self, orm):
        "Write your forwards methods here."
        # Note: Remember to use orm['appname.ModelName'] rather than "from appname.models..."

        for rp in orm.RecipePhoto.objects.all():
            try:
                digit = int(str(rp.photo.img)[-5])
                if digit == 1:
                    rp.position = 1
                    rp.save()
                elif digit == 2:
                    rp.position = 2
                    rp.save()
                else:
                    print "RecipePhoto %s position must be set manually" % rp
            except:
                print "Failed to extract from RecipePhoto %s" % rp


        self.link_recipe_photo(orm, 'BR-201/photo1.jpg')
        self.link_recipe_photo(orm, 'BR-202/photo1.jpg')
        self.link_recipe_photo(orm, 'BR-203/photo1.jpg')
        self.link_recipe_photo(orm, 'BR-203/photo2.jpg')
        self.link_recipe_photo(orm, 'BR-204/photo1.jpg')
        self.link_recipe_photo(orm, 'BR-205/photo1.jpg')
        self.link_recipe_photo(orm, 'BR-206/photo1.jpg')
        self.link_recipe_photo(orm, 'BR-207/photo1.jpg')
        self.link_recipe_photo(orm, 'BR-208/photo1.jpg')
        self.link_recipe_photo(orm, 'BR-209/photo1.jpg')
        self.link_recipe_photo(orm, 'BR-210/photo1.jpg')
        self.link_recipe_photo(orm, 'BR-211/photo1.jpg')
        self.link_recipe_photo(orm, 'BR-212/photo1.jpg')
        self.link_recipe_photo(orm, 'BR-213/photo1.jpg')
        self.link_recipe_photo(orm, 'BR-214/photo1.jpg')
        self.link_recipe_photo(orm, 'BR-215/photo1.jpg')
        self.link_recipe_photo(orm, 'BR-216/photo1.jpg')
        self.link_recipe_photo(orm, 'BR-217/photo1.jpg')
        self.link_recipe_photo(orm, 'BR-217/photo2.jpg')
        self.link_recipe_photo(orm, 'BR-218/photo1.jpg')
        self.link_recipe_photo(orm, 'BR-219/photo1.jpg')
        self.link_recipe_photo(orm, 'BR-220/photo1.jpg')
        self.link_recipe_photo(orm, 'CA-201/photo1.jpg')
        self.link_recipe_photo(orm, 'CA-202/photo1.jpg')
        self.link_recipe_photo(orm, 'CA-202/photo2.jpg')
        self.link_recipe_photo(orm, 'CA-203/photo1.jpg')
        self.link_recipe_photo(orm, 'CA-204/photo1.jpg')
        self.link_recipe_photo(orm, 'CA-205/photo1.jpg')
        self.link_recipe_photo(orm, 'CA-206/photo1.jpg')
        self.link_recipe_photo(orm, 'CA-207/photo1.jpg')
        self.link_recipe_photo(orm, 'CA-209/photo1.jpg')
        self.link_recipe_photo(orm, 'CA-210/photo1.jpg')
        self.link_recipe_photo(orm, 'CA-211/photo1.jpg')
        self.link_recipe_photo(orm, 'CA-212/photo1.jpg')
        self.link_recipe_photo(orm, 'CA-213/photo1.jpg')
        self.link_recipe_photo(orm, 'CA-214/photo1.jpg')
        self.link_recipe_photo(orm, 'CA-215/photo1.jpg')
        self.link_recipe_photo(orm, 'CA-216/photo1.jpg')
        self.link_recipe_photo(orm, 'CA-217/photo1.jpg')
        self.link_recipe_photo(orm, 'CA-218/photo1.jpg')
        self.link_recipe_photo(orm, 'CA-219/photo1.jpg')
        self.link_recipe_photo(orm, 'CA-220/photo1.jpg')
        self.link_recipe_photo(orm, 'CA-221/photo1.jpg')
        self.link_recipe_photo(orm, 'CA-221/photo2.jpg')
        self.link_recipe_photo(orm, 'CB-201/photo1.jpg')
        self.link_recipe_photo(orm, 'CB-202/photo1.jpg')
        self.link_recipe_photo(orm, 'CB-202/photo2.jpg')
        self.link_recipe_photo(orm, 'CB-203/photo1.jpg')
        self.link_recipe_photo(orm, 'CB-204/photo1.jpg')
        self.link_recipe_photo(orm, 'CB-205/photo1.jpg')
        self.link_recipe_photo(orm, 'CB-206/photo1.jpg')
        self.link_recipe_photo(orm, 'CB-207/photo1.jpg')
        self.link_recipe_photo(orm, 'CB-208/photo1.jpg')
        self.link_recipe_photo(orm, 'CB-209/photo1.jpg')
        self.link_recipe_photo(orm, 'CB-210/photo1.jpg')
        self.link_recipe_photo(orm, 'CB-211/photo1.jpg')
        self.link_recipe_photo(orm, 'CB-212/photo1.jpg')
        self.link_recipe_photo(orm, 'CB-213/photo1.jpg')
        self.link_recipe_photo(orm, 'CB-214/photo1.jpg')
        self.link_recipe_photo(orm, 'CB-215/photo1.jpg')
        self.link_recipe_photo(orm, 'CB-216/photo1.jpg')
        self.link_recipe_photo(orm, 'CB-217/photo1.jpg')
        self.link_recipe_photo(orm, 'CB-218/photo1.jpg')
        self.link_recipe_photo(orm, 'CB-219/photo1.jpg')
        self.link_recipe_photo(orm, 'CB-220/photo1.jpg')
        self.link_recipe_photo(orm, 'CB-220/photo2.jpg')
        self.link_recipe_photo(orm, 'CB-221/photo1.jpg')
        self.link_recipe_photo(orm, 'CL-201/photo1.jpg')
        self.link_recipe_photo(orm, 'CL-202/photo1.jpg')
        self.link_recipe_photo(orm, 'CL-203/photo1.jpg')
        self.link_recipe_photo(orm, 'CL-204/photo1.jpg')
        self.link_recipe_photo(orm, 'CL-204/photo2.jpg')
        self.link_recipe_photo(orm, 'CL-205/photo1.jpg')
        self.link_recipe_photo(orm, 'CL-206/photo1.jpg')
        self.link_recipe_photo(orm, 'CL-207/photo1.jpg')
        self.link_recipe_photo(orm, 'CL-208/photo1.jpg')
        self.link_recipe_photo(orm, 'CL-209/photo1.jpg')
        self.link_recipe_photo(orm, 'CL-210/photo1.jpg')
        self.link_recipe_photo(orm, 'CL-210/photo2.jpg')
        self.link_recipe_photo(orm, 'CL-211/photo1.jpg')
        self.link_recipe_photo(orm, 'CL-212/photo1.jpg')
        self.link_recipe_photo(orm, 'CL-212/photo2.jpg')
        self.link_recipe_photo(orm, 'CL-213/photo1.jpg')
        self.link_recipe_photo(orm, 'CL-214/photo1.jpg')
        self.link_recipe_photo(orm, 'CL-215/photo1.jpg')
        self.link_recipe_photo(orm, 'CL-216/photo1.jpg')
        self.link_recipe_photo(orm, 'CL-217/photo1.jpg')
        self.link_recipe_photo(orm, 'CL-218/photo1.jpg')
        self.link_recipe_photo(orm, 'CL-219/photo1.jpg')
        self.link_recipe_photo(orm, 'CL-220/photo1.jpg')
        self.link_recipe_photo(orm, 'CL-221/photo1.jpg')
        self.link_recipe_photo(orm, 'GB-201/photo1.jpg')
        self.link_recipe_photo(orm, 'GB-201/photo2.jpg')
        self.link_recipe_photo(orm, 'GB-202/photo1.jpg')
        self.link_recipe_photo(orm, 'GB-203/photo1.jpg')
        self.link_recipe_photo(orm, 'GB-204/photo1.jpg')
        self.link_recipe_photo(orm, 'GB-205/photo1.jpg')
        self.link_recipe_photo(orm, 'GB-206/photo1.jpg')
        self.link_recipe_photo(orm, 'GB-207/photo1.jpg')
        self.link_recipe_photo(orm, 'GB-208/photo1.jpg')
        self.link_recipe_photo(orm, 'GB-209/photo1.jpg')
        self.link_recipe_photo(orm, 'GB-209/photo2.jpg')
        self.link_recipe_photo(orm, 'GB-210/photo1.jpg')
        self.link_recipe_photo(orm, 'GB-211/photo1.jpg')
        self.link_recipe_photo(orm, 'GB-212/photo1.jpg')
        self.link_recipe_photo(orm, 'GB-213/photo1.jpg')
        self.link_recipe_photo(orm, 'GB-213/photo2.jpg')
        self.link_recipe_photo(orm, 'GB-214/photo1.jpg')
        self.link_recipe_photo(orm, 'GB-214/photo2.jpg')
        self.link_recipe_photo(orm, 'GB-215/photo1.jpg')
        self.link_recipe_photo(orm, 'GB-216/photo1.jpg')
        self.link_recipe_photo(orm, 'GB-217/photo1.jpg')
        self.link_recipe_photo(orm, 'GB-218/photo1.jpg')
        self.link_recipe_photo(orm, 'GB-219/photo1.jpg')
        self.link_recipe_photo(orm, 'GB-220/photo1.jpg')
        self.link_recipe_photo(orm, 'GB-220/photo2.jpg')
        self.link_recipe_photo(orm, 'ON-209/photo1.jpg')
        self.link_recipe_photo(orm, 'ON-212/photo1.jpg')
        self.link_recipe_photo(orm, 'ON-214/photo1.jpg')
        self.link_recipe_photo(orm, 'ON-215/photo1.jpg')
        self.link_recipe_photo(orm, 'ON-216/photo1.jpg')
        self.link_recipe_photo(orm, 'ON-217/photo1.jpg')
        self.link_recipe_photo(orm, 'ON-218/photo1.jpg')
        self.link_recipe_photo(orm, 'ON-219/photo1.jpg')
        self.link_recipe_photo(orm, 'ON-220/photo1.jpg')
        self.link_recipe_photo(orm, 'ON-221/photo1.jpg')
        self.link_recipe_photo(orm, 'ON-222/photo1.jpg')
        self.link_recipe_photo(orm, 'ON-223/photo1.jpg')
        self.link_recipe_photo(orm, 'ON-224/photo1.jpg')
        self.link_recipe_photo(orm, 'ON-225/photo1.jpg')
        self.link_recipe_photo(orm, 'ON-226/photo1.jpg')
        self.link_recipe_photo(orm, 'ON-227/photo1.jpg')
        self.link_recipe_photo(orm, 'ON-227/photo2.jpg')
        self.link_recipe_photo(orm, 'ON-228/photo1.jpg')
        self.link_recipe_photo(orm, 'ON-229/photo1.jpg')
        self.link_recipe_photo(orm, 'ON-230/photo1.jpg')
        self.link_recipe_photo(orm, 'ON-231/photo1.jpg')
        self.link_recipe_photo(orm, 'ON-232/photo1.jpg')
        self.link_recipe_photo(orm, 'ON-233/photo1.jpg')
        self.link_recipe_photo(orm, 'PO-202/photo1.jpg')
        self.link_recipe_photo(orm, 'PO-203/photo1.jpg')
        self.link_recipe_photo(orm, 'PO-204/photo1.jpg')
        self.link_recipe_photo(orm, 'PO-205/photo1.jpg')
        self.link_recipe_photo(orm, 'PO-206/photo1.jpg')
        self.link_recipe_photo(orm, 'PO-207/photo1.jpg')
        self.link_recipe_photo(orm, 'PO-208/photo1.jpg')
        self.link_recipe_photo(orm, 'PO-209/photo1.jpg')
        self.link_recipe_photo(orm, 'PO-210/photo1.jpg')
        self.link_recipe_photo(orm, 'PO-211/photo1.jpg')
        self.link_recipe_photo(orm, 'PO-211/photo2.jpg')
        self.link_recipe_photo(orm, 'PO-212/photo1.jpg')
        self.link_recipe_photo(orm, 'PO-212/photo2.jpg')
        self.link_recipe_photo(orm, 'PO-213/photo1.jpg')
        self.link_recipe_photo(orm, 'PO-214/photo1.jpg')
        self.link_recipe_photo(orm, 'PO-215/photo1.jpg')
        self.link_recipe_photo(orm, 'PO-216/photo1.jpg')
        self.link_recipe_photo(orm, 'PO-217/photo1.jpg')
        self.link_recipe_photo(orm, 'PO-218/photo1.jpg')
        self.link_recipe_photo(orm, 'PO-219/photo1.jpg')
        self.link_recipe_photo(orm, 'PO-219/photo2.jpg')
        self.link_recipe_photo(orm, 'PO-220/photo1.jpg')
        self.link_recipe_photo(orm, 'RV-202/photo1.jpg')
        self.link_recipe_photo(orm, 'RV-203/photo1.jpg')
        self.link_recipe_photo(orm, 'RV-204/photo1.jpg')
        self.link_recipe_photo(orm, 'RV-205/photo1.jpg')
        self.link_recipe_photo(orm, 'RV-206/photo1.jpg')
        self.link_recipe_photo(orm, 'RV-207/photo1.jpg')
        self.link_recipe_photo(orm, 'RV-208/photo1.jpg')
        self.link_recipe_photo(orm, 'RV-208/photo2.jpg')
        self.link_recipe_photo(orm, 'RV-209/photo1.jpg')
        self.link_recipe_photo(orm, 'RV-210/photo1.jpg')
        self.link_recipe_photo(orm, 'RV-211/photo1.jpg')
        self.link_recipe_photo(orm, 'RV-211/photo2.jpg')
        self.link_recipe_photo(orm, 'RV-212/photo1.jpg')
        self.link_recipe_photo(orm, 'RV-213/photo1.jpg')
        self.link_recipe_photo(orm, 'RV-213/photo2.jpg')
        self.link_recipe_photo(orm, 'RV-214/photo1.jpg')
        self.link_recipe_photo(orm, 'RV-215/photo1.jpg')
        self.link_recipe_photo(orm, 'RV-216/photo1.jpg')
        self.link_recipe_photo(orm, 'RV-217/photo1.jpg')
        self.link_recipe_photo(orm, 'RV-218/photo1.jpg')
        self.link_recipe_photo(orm, 'RV-219/photo1.jpg')
        self.link_recipe_photo(orm, 'RV-219/photo2.jpg')
        self.link_recipe_photo(orm, 'RV-220/photo1.jpg')
        self.link_recipe_photo(orm, 'RV-221/photo1.jpg')
        self.link_recipe_photo(orm, 'SW-202/photo1.jpg')
        self.link_recipe_photo(orm, 'SW-203/photo1.jpg')
        self.link_recipe_photo(orm, 'SW-204/photo1.jpg')
        self.link_recipe_photo(orm, 'SW-205/photo1.jpg')
        self.link_recipe_photo(orm, 'SW-206/photo1.jpg')
        self.link_recipe_photo(orm, 'SW-206/photo2.jpg')
        self.link_recipe_photo(orm, 'SW-207/photo1.jpg')
        self.link_recipe_photo(orm, 'SW-207/photo2.jpg')
        self.link_recipe_photo(orm, 'SW-208/photo1.jpg')
        self.link_recipe_photo(orm, 'SW-209/photo1.jpg')
        self.link_recipe_photo(orm, 'SW-209/photo2.jpg')
        self.link_recipe_photo(orm, 'SW-210/photo1.jpg')
        self.link_recipe_photo(orm, 'SW-211/photo1.jpg')
        self.link_recipe_photo(orm, 'SW-212/photo1.jpg')
        self.link_recipe_photo(orm, 'SW-213/photo1.jpg')
        self.link_recipe_photo(orm, 'SW-214/photo1.jpg')
        self.link_recipe_photo(orm, 'SW-215/photo1.jpg')
        self.link_recipe_photo(orm, 'SW-216/photo1.jpg')
        self.link_recipe_photo(orm, 'SW-217/photo1.jpg')
        self.link_recipe_photo(orm, 'SW-218/photo1.jpg')
        self.link_recipe_photo(orm, 'SW-219/photo1.jpg')
        self.link_recipe_photo(orm, 'SW-219/photo2.jpg')
        self.link_recipe_photo(orm, 'ZU-201/photo1.jpg')
        self.link_recipe_photo(orm, 'ZU-202/photo1.jpg')
        self.link_recipe_photo(orm, 'ZU-204/photo1.jpg')
        self.link_recipe_photo(orm, 'ZU-205/photo1.jpg')
        self.link_recipe_photo(orm, 'ZU-205/photo2.jpg')
        self.link_recipe_photo(orm, 'ZU-206/photo1.jpg')
        self.link_recipe_photo(orm, 'ZU-207/photo1.jpg')
        self.link_recipe_photo(orm, 'ZU-208/photo1.jpg')
        self.link_recipe_photo(orm, 'ZU-209/photo1.jpg')
        self.link_recipe_photo(orm, 'ZU-210/photo1.jpg')
        self.link_recipe_photo(orm, 'ZU-211/photo1.jpg')
        self.link_recipe_photo(orm, 'ZU-212/photo1.jpg')
        self.link_recipe_photo(orm, 'ZU-213/photo1.jpg')
        self.link_recipe_photo(orm, 'ZU-214/photo1.jpg')
        self.link_recipe_photo(orm, 'ZU-215/photo1.jpg')
        self.link_recipe_photo(orm, 'ZU-216/photo1.jpg')
        self.link_recipe_photo(orm, 'ZU-217/photo1.jpg')
        self.link_recipe_photo(orm, 'ZU-218/photo1.jpg')
        self.link_recipe_photo(orm, 'ZU-220/photo1.jpg')
        self.link_recipe_photo(orm, 'ZU-220/photo2.jpg')
        self.link_recipe_photo(orm, 'ZU-221/photo1.jpg')
        self.link_recipe_photo(orm, 'ZU-222/photo1.jpg')
        self.link_recipe_photo(orm, 'ZU-223/photo1.jpg')
        self.link_recipe_photo(orm, 'ZU-224/photo1.jpg')

    def backwards(self, orm):
        raise RuntimeError("Cannot reverse this migration.")

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
        }
    }

    complete_apps = ['qhmobile']
    symmetrical = True
