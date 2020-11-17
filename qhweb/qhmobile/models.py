# coding=utf-8
#
# Copyright © 2020 Quick Help For Meals, LLC. All rights reserved.
#
# This file is part of VeggieBook.
#
# VeggieBook is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, version 3 of the license only.
#
# VeggieBook is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or fitness for a particular purpose. See the
# GNU General Public License for more details.
#

import random
import string

from django.contrib.auth.models import User
from django.db import models, IntegrityError
from django.utils.encoding import smart_str
from django.db.models.signals import post_save
from django.dispatch import receiver
from geopy import geocoders
from imagekit.models import ImageSpecField
from imagekit.processors import ResizeToFill, ResizeToCover, SmartResize, Transpose
from qhmobile.tasks import lazyCacheStockPhoto, lazyCachePhoto, createPdf
from django.contrib.sites.models import Site
from django.conf import settings
from easy_maps.models import Address
from urllib import urlencode


class QuickHelpUser(models.Model):
    name = models.CharField(max_length=255)
    lastFourDigits = models.CharField(max_length=4)
    imageUrl = models.URLField()


class String(models.Model):
    en = models.TextField()
    es = models.TextField(default='needs translation')
    needsTranslation = models.BooleanField(default=True, db_index=True)

    class Meta:
        ordering = ['-id']

    def __unicode__(self):
        s = 'en: ' + self.en + ", es: " + self.es
        return s if len(s) < 60 else s[0:57] + '...'

    def jdata(self, language, substitute=None):
        retval = self.__dict__[language]
        count = retval.count('%s')
        if substitute is None or count < 1:
            return retval
        else:
            return retval % tuple([substitute for i in range(count)])

    def jdataAll(self):
        return {'en': self.en, 'es': self.es, 'id': self.id}


class BookType(models.Model):
    id = models.CharField(max_length=24, primary_key=True)


class LibraryData(models.Model):
    version = models.DateTimeField(auto_now_add=True, blank=True, db_index=True)

    def __unicode__(self):
        return self.version.strftime("%s")

    def jdata(self):
        return {"version": self.version.strftime("%s")}


class Attribute(models.Model):
    name = models.CharField(max_length=24, primary_key=True)

    def __unicode__(self):
        return self.name


class OrRequirement(models.Model):
    attributes = models.ManyToManyField(Attribute)

    def __unicode__(self):
        out = u''
        for attribute in self.attributes.all():
            if len(out) > 0:
                out += u' OR '

            out += attribute.__unicode__()
        return out

    @classmethod
    def getMatchingOrRequirements(cls, attributes):
        """
        takes a list of attributes and returns all matching or requirements
        """
        return cls.objects.filter(attributes__name__in=attributes).distinct()


class PhotoBase(models.Model):
    """ This abstract base class requires that you create a
        field img = models.ImageField(upload_to='your upload dir')
        Once that image is added you get dynamic resizing for the
        following sizes:
            thumbnail (50x50 square cropped)
            img80 (will cover 50 x 5 )
            img200 (will cover 200 x 5 )
            img300 (will cover 300 x 5 )
            img500 (will cover 500 x 5 )
            all the above fields are created and cached on upload
    """
    thumbnail = ImageSpecField([Transpose(Transpose.AUTO), SmartResize(50, 50)], image_field='img',
                               format='JPEG', options={'quality': 90})
    img100 = ImageSpecField([Transpose(Transpose.AUTO), ResizeToCover(width=100, height=5)], image_field='img',
                            format='JPEG', options={'quality': 90})
    img200 = ImageSpecField([Transpose(Transpose.AUTO), ResizeToCover(width=200, height=5)], image_field='img',
                            format='JPEG', options={'quality': 90})

    img300 = ImageSpecField([Transpose(Transpose.AUTO), ResizeToCover(width=300, height=5)], image_field='img',
                            format='JPEG', options={'quality': 90})
    img500 = ImageSpecField([Transpose(Transpose.AUTO), ResizeToCover(width=500, height=5)], image_field='img',
                            format='JPEG', options={'quality': 90})
    img1024 = ImageSpecField([Transpose(Transpose.AUTO), ResizeToCover(width=1024, height=5)], image_field='img',
                            format='JPEG', options={'quality': 90})
    imgPrintThin = ImageSpecField([Transpose(Transpose.AUTO), ResizeToFill(600, 250)], image_field='img',
                                  format='JPEG', options={'quality': 90})
    imgPrintThick = ImageSpecField([Transpose(Transpose.AUTO), ResizeToFill(600, 350)], image_field='img',
                                   format='JPEG', options={'quality': 90})

    def __unicode__(self):
        try:
            return self.img.url
        except ValueError:
            return "missing image"

    def jdata(self):
        data = {x: self.__dict__[x].url for x in self.__dict__ if x.startswith('img') or x.startswith('thumbnail')}
        data.pop('img')
        data['id'] = self.id
        return data

    def cacheAllSizes(self):
        {x: self.__dict__[x].url for x in self.__dict__ if x.startswith('img') or x.startswith('thumbnail')}

    def save_with_lazy_caching(self, task, force_insert=False, force_update=False, using=None):
        """Save the image, then create an asynchronous task to cache all the other sizes
            It is the job of the subclass to implement a celery task, and pass that task here on save.
        """
        ret_val = super(PhotoBase, self).save(force_insert=force_insert, force_update=force_update, using=using)
        task.delay(self.id)
        return ret_val


    class Meta:
        abstract = True


class Photo(PhotoBase):
    img = models.ImageField(upload_to='img')

    def save(self, force_insert=False, force_update=False, using=None):
        task = lazyCachePhoto
        return self.save_with_lazy_caching(task, force_insert=force_insert, force_update=force_update, using=using)


class StockPhoto(PhotoBase):
    img = models.ImageField(upload_to='stock')
    imgFixedHieght = ImageSpecField([Transpose(Transpose.AUTO), ResizeToCover(width=5, height=16)], image_field='img',
                                    format='JPEG', options={'quality': 90})

    def save(self, force_insert=False, force_update=False, using=None):
        task = lazyCacheStockPhoto
        return self.save_with_lazy_caching(task, force_insert=force_insert, force_update=force_update, using=using)


class Annotation(models.Model):
    en_img = models.ForeignKey(StockPhoto, related_name='en_img', blank=True, null=True)
    es_img = models.ForeignKey(StockPhoto, related_name='es_img', blank=True, null=True)
    text = models.ForeignKey(String, related_name='annotation', default=1)
    color = models.CharField(max_length=6, default="ffffff")

    displayedIf = models.ForeignKey(OrRequirement)

    def __unicode__(self):
        return self.displayedIf.__unicode__()


class RecipeAnnotation(models.Model):
    name = models.CharField(max_length=24, primary_key=True)


# 29 December 2012

class Question(models.Model):
    mnemonic = models.TextField()
    PHASE_TYPE = (
        (u'P', u'Preliminary'),
        (u'I', u'Interview'),
    )
    phase = models.CharField(max_length=1, choices=PHASE_TYPE)
    intro = models.ForeignKey(String, related_name="intro")
    subIntro = models.ForeignKey(String, related_name="subintro", blank=True, null=True)
    ATTRIBUTE_TYPE = (
        (u'M', u'MultipleChoice minimum 1 selection'),
        (u'Z', u'MultipleChoice no selections required'),
        (u'S', u'SingleChoice'),
        (u'F', u'FreeText'),
        (u'H', u"Hidden"),
    )
    qtype = models.CharField(max_length=1, choices=ATTRIBUTE_TYPE)
    orderPriority = models.IntegerField(default=100)

    def __unicode__(self):
        return str(self.orderPriority) + ": " + self.mnemonic

    def jdata(self, language='en', substitute=None):
        return {"mnemonic": self.mnemonic,
                "phase": self.phase,
                "intro": self.intro.jdata(language, substitute),
                "qtype": self.qtype,
                "choices": [c.jdata(language, substitute) for c in self.questionchoice_set.all()]
        }

    class Meta:
        ordering = ['orderPriority', 'id']


class ChoiceQuestion(Question):
    cardinality = None


class MultipleChoiceQuestion(ChoiceQuestion):
    cardinality = float("inf")


class SingleChoiceQuestion(ChoiceQuestion):
    cardinality = 1


class QuestionChoice(models.Model):
    questionId = models.ForeignKey(Question)
    content = models.ForeignKey(String)
    attribute = models.ForeignKey(Attribute, unique=True)
    firstDefault = models.BooleanField(default=False)

    class Meta:
        ordering = ['questionId', 'id']

    def __unicode__(self):
        return 'en: ' + str(self.content.en)

    def jdata(self, language='en', substitute=None):
        return {
            'content': self.content.jdata(language, substitute),
            'attribute': self.attribute_id,
            'defaultChoice': self.firstDefault,
        }


class BookSubjectBase(models.Model):
    id = models.CharField(max_length=24, primary_key=True)
    nameString = models.ForeignKey(String)
    active = models.BooleanField(default=False)
    image = models.ForeignKey(StockPhoto)

    def __unicode__(self):
        return self.id

    def jdata(self):
        return {
            'id': self.id,
            'title': self.nameString.jdataAll(),
            'image': self.image.jdata()
        }

    def name(self, language):
        return self.nameString.jdata(language=language)

    def save(self, force_insert=False, force_update=False, using=None):
        """Write a new library version number on save"""
        LibraryData.objects.create().save()
        return super(BookSubjectBase, self).save(force_insert=force_insert, force_update=force_update, using=using)

    def delete(self, *args, **kwargs):
        LibraryData.objects.create().save()
        return super(BookSubjectBase, self).delete(*args, **kwargs)

    class Meta:
        abstract = True


class FoodStuff(BookSubjectBase):
    def jdata(self):
        data = dict(super(FoodStuff, self).jdata().items() + {"type": "RECIPE_BOOK"}.items())
        data['id'] = "RB_" + data['id']
        data['hasSelectables'] = True
        data['loadingUrl_en'] = \
            "%s://%s/qhmobile/recipesLoading/en/%s/" % (
                settings.SITE_PROTOCOL, Site.objects.get(id=settings.SITE_ID).domain, self.id, )
        data['loadingUrl_es'] = \
            "%s://%s/qhmobile/recipesLoading/es/%s/" % (
                settings.SITE_PROTOCOL, Site.objects.get(id=settings.SITE_ID).domain, self.id, )
        return data


class TipDoc(BookSubjectBase):
    def jdata(self):
        data = dict(super(TipDoc, self).jdata().items() + {"type": "SECRETS_BOOK"}.items())
        data['id'] = "TB_" + data['id']
        return data


class Recipe(models.Model):
    recipeId = models.AutoField(primary_key=True)
    title = models.ForeignKey(String, related_name="title")
    isActive = models.BooleanField(default=True)
    storyLine = models.ForeignKey(String, related_name="storyline", blank=True, null=True)
    timeToPrepare = models.ForeignKey(String, related_name="timeToPrepare")
    timeToCook = models.ForeignKey(String, related_name="timeToCook")
    servings = models.ForeignKey(String, related_name="servings")
    canBeMadeAhead = models.ForeignKey(String, related_name="canBeMadeAhead")
    canBeFrozen = models.ForeignKey(String, related_name="canBeFrozen")
    goodForLeftovers = models.ForeignKey(String, related_name="goodForLeftovers")
    rid = models.CharField(max_length=6, blank=True, null=True)
    foodStuff = models.ForeignKey(FoodStuff, db_index=True)
    requirements = models.ManyToManyField(OrRequirement, blank=True, null=True)
    annotations = models.ManyToManyField(Annotation, blank=True, null=True)

    def __unicode__(self):
        return self.rid + ' en: ' + self.title.en

    def jdata(self, or_reqs=None):
        qs = "?" + "&".join('a=%d' % s for s in self.getMatchingAnnotations(or_reqs=or_reqs))
        return {
            'id': self.recipeId,
            'title_en': self.title.jdata(language='en'),
            'title_es': self.title.jdata(language='es'),
            'url_en': "%s://%s/qhmobile/mobileRecipe/en/%d/%s" % (settings.SITE_PROTOCOL,
                                                                  Site.objects.get(id=settings.SITE_ID).domain,
                                                                  self.recipeId, qs),
            'url_es': "%s://%s/qhmobile/mobileRecipe/es/%d/%s" % (settings.SITE_PROTOCOL,
                                                                  Site.objects.get(id=settings.SITE_ID).domain,
                                                                  self.recipeId, qs),
            'photoUrl': self.defaultPhoto().photo.img300.url,
            'shareUrl_en': "%s://%s/qhmobile/recipe/%d/en/%s" % (settings.SITE_PROTOCOL,
                                                                 Site.objects.get(id=settings.SITE_ID).domain,
                                                                 self.recipeId, qs),

            'shareUrl_es': "%s://%s/qhmobile/recipe/%d/es/%s" % (settings.SITE_PROTOCOL,
                                                                 Site.objects.get(id=settings.SITE_ID).domain,
                                                                 self.recipeId, qs),
        }

    def url(self, language, or_reqs=None):
        qs = "?" + "&".join('a=%d' % s for s in self.getMatchingAnnotations(or_reqs=or_reqs))
        return "%s://%s/qhmobile/recipe/%d/%s/%s" % (
            settings.SITE_PROTOCOL, Site.objects.get(id=settings.SITE_ID).domain, self.recipeId, language, qs)

    def matchesRequirements(self, or_reqs):
        """
        Given a set of fulfilled requirements, returns true if this recipe should be selected,
        false, otherwise.
        """
        return self.requirements.count() == self.requirements.filter(id__in=or_reqs).count()

    def getMatchingAnnotations(self, or_reqs):
        """
        Given a set of fulfilled or rquirements, returns a list of annot
        """
        return [a.id for a in self.annotations.filter(displayedIf__in=or_reqs)]

    def getStepAndNotesList(self):
        l = []
        for s in self.recipestep_set.all():
            l.append(s)
        for s in self.recipenote_set.all():
            l.append(s)
        return l

    def defaultPhoto(self):
        photos = self.recipephoto_set.all()
        if len(photos) == 0:
            return None
        return photos[len(photos) - 1]

    def getWebUrl(self, language, or_reqs=None):
        qs = "?" + "&".join('a=%d' % s for s in self.getMatchingAnnotations(or_reqs=or_reqs))
        if language == 'es':
            return "%s://%s/qhmobile/recipe/%d/es/%s" % (settings.SITE_PROTOCOL,
                                                         Site.objects.get(id=settings.SITE_ID).domain,
                                                         self.recipeId, qs)
        else:
            return "%s://%s/qhmobile/recipe/%d/en/%s" % (settings.SITE_PROTOCOL,
                                                         Site.objects.get(id=settings.SITE_ID).domain,
                                                         self.recipeId, qs)


class RecipeOrderable(models.Model):
    """Add extra field and default ordering column for and inline orderable model"""
    recipeId = models.ForeignKey(Recipe, db_index=True)
    position = models.IntegerField(blank=True,
                                   null=True,
                                   editable=True)

    class Meta:
        abstract = True
        ordering = ('position', 'id')

    def next_position(self):
        return len(self.__class__.objects.filter(recipeId_id=self.recipeId_id)) + 1


    def save(self, force_insert=False, force_update=False, using=None):
        """Calculate position (max+1) for new records"""
        if not self.position:
            try:
                self.position = self.next_position()
            except TypeError:
                self.position = 1
        return super(RecipeOrderable, self).save(force_insert=force_insert, force_update=force_update, using=using)


class RecipeIngredient(RecipeOrderable):
    content = models.ForeignKey(String)

    def __unicode__(self):
        return 'en: ' + self.content.en


class RecipeStep(RecipeOrderable):
    content = models.ForeignKey(String)

    def __unicode__(self):
        return 'en: ' + self.content.en


class RecipeNote(RecipeOrderable):
    content = models.ForeignKey(String)

    def __unicode__(self):
        return 'en: ' + self.content.en


class RecipePhoto(RecipeOrderable):
    photo = models.ForeignKey(Photo)

    def __unicode__(self):
        return self.photo.__unicode__()


class FoodTip(models.Model):
    heading = models.ForeignKey(String, related_name='heading')
    foodStuff = models.ForeignKey(FoodStuff, db_index=True)
    requirement = models.ForeignKey(OrRequirement)
    fsIndex = models.IntegerField(default=10000)

    def __unicode__(self):
        return self.foodStuff_id + ': ' + self.heading.__unicode__()

    class Meta:
        ordering = ('foodStuff', 'fsIndex', 'id', )


class OrderableTip(models.Model):
    tipId = models.ForeignKey(FoodTip, db_index=True)
    content = models.ForeignKey(String)
    photo = models.ForeignKey(Photo, blank=True, null=True)
    position = models.IntegerField(blank=True,
                                   null=True,
                                   editable=True)

    def __unicode__(self):
        return self.content.__unicode__()

    class Meta:
        ordering = ('position', 'id')

    def next_position(self):
        return len(self.__class__.objects.filter(recipeId_id=self.recipeId_id)) + 1

    def save(self, force_insert=False, force_update=False, using=None):
        """Calculate position (max+1) for new records"""
        if not self.position:
            try:
                self.position = self.next_position()
            except TypeError:
                self.position = 1
        return super(OrderableTip, self).save(force_insert=force_insert, force_update=force_update, using=using)


class CoverPhoto(PhotoBase):
    img = models.ImageField(upload_to='coverPhoto')
    owner = models.ForeignKey(User, null=True, blank=True, default=None, on_delete=models.CASCADE)
    restrictTo = models.ForeignKey(FoodStuff, null=True, blank=True, default=None)
    order = models.IntegerField(default=1000)

    class Meta:
        ordering = ('order', 'id')


class FoodPantry(Address):
    name = models.CharField(max_length=256)
    printer_name = models.CharField(max_length=48, blank=True, null=True)
    printingAvailable = models.BooleanField(default=False)
    printerEmail = models.EmailField(default="tdi2048cynp656@print.epsonconnect.com")

    def fill_geocode_data(self):
        if not self.address:
            self.geocode_error = True
            return
        try:
            if hasattr(settings, "GOOGLE_API_CLIENT_ID") and hasattr(settings, "GOOGLE_API_SECRET_KEY"):
                g = geocoders.GoogleV3(client_id=settings.GOOGLE_API_CLIENT_ID,
                                       secret_key=settings.GOOGLE_API_SECRET_KEY)
            else:
                g = geocoders.GoogleV3()
            address = smart_str(self.address)
            self.computed_address, (self.latitude, self.longitude,) = g.geocode(address, exactly_one=False)[0]
            self.geocode_error = False
        except (UnboundLocalError, ValueError, geocoders.google.GQueryError):
            self.geocode_error = True

    def jdata(self):

        return {"name": self.printer_name if self.printer_name else self.name,
                "id": self.id, "address": self.computed_address, "lat": self.latitude,
                "lon": self.longitude, "open": self.printingAvailable}


class RecipeBookSelection(models.Model):
    recipe = models.ForeignKey(Recipe)
    selected = models.BooleanField(default=True)
    extras = models.IntegerField(default=0)
    scrolled = models.BooleanField(default=False)

    def __unicode__(self):
        return "%d: %s - %s" % (self.recipe.recipeId, self.recipe.title.en, 'SELECTED' if self.selected else "DROPPED")


class RecipeBook(models.Model):
    user = models.ForeignKey(User, db_index=True)
    attributes = models.ManyToManyField(Attribute)
    selections = models.ManyToManyField(RecipeBookSelection)
    coverPhoto = models.ForeignKey(CoverPhoto)
    pantry = models.ForeignKey(FoodPantry, null=True, blank=True)
    createdAt = models.DateTimeField(auto_now_add=True)
    foodStuff = models.ForeignKey(FoodStuff, null=True, blank=True, default=None)
    pdf_en = models.FileField(upload_to='pdfs', null=True, blank=True)
    pdf_es = models.FileField(upload_to='pdfs', null=True, blank=True)
    latitude = models.FloatField(null=True, blank=True)
    longitude = models.FloatField(null=True, blank=True)


    def getPdf(self, language):
        if language == 'es':
            return self.pdf_es
        else:
            return self.pdf_en

    def getFirstName(self):
        return self.user.first_name

    def getRecipeUrls(self, language):
        or_reqs = [o.id for o in OrRequirement.getMatchingOrRequirements(self.attributes.all())]

        recipeUrls = []

        for recipe in self.selections.all().order_by('recipe'):
            if recipe.selected:
                recipeUrls.append(recipe.recipe.getWebUrl(language, or_reqs))

        return recipeUrls

    def getExtrasUrls(self, language):
        or_reqs = [o.id for o in OrRequirement.getMatchingOrRequirements(self.attributes.all())]

        recipeUrls = []

        for recipe in self.selections.all().order_by('recipe'):
            for i in range(recipe.extras):
                recipeUrls.append(recipe.recipe.getWebUrl(language, or_reqs))

        return recipeUrls

    def getSelectedRecipes(self):

        selectedRecipes = []

        for recipe in self.selections.all().order_by('recipe'):
            if recipe.selected:
                selectedRecipes.append(recipe.recipe)

        return selectedRecipes

    def getCoverUrl(self, language, pantry=None):
        urlMap = {'t': unicode(self.foodStuff.name(language)).encode('utf-8'), 'img': self.coverPhoto_id,
                  'fs': self.foodStuff_id}
        if self.user and self.user.first_name:
            urlMap['n'] = self.user.first_name

        if pantry is not None:
            urlMap['p'] = unicode(pantry.name).encode('utf-8')

        return '%s://%s/qhmobile/cover/%s/?%s' % (settings.SITE_PROTOCOL,
                                                  Site.objects.get(id=settings.SITE_ID).domain,
                                                  language, urlencode(urlMap))

    def getTipsUrl(self, language):
        attributes = [a.name for a in self.attributes.all()]
        qs = urlencode({'a': attributes, 'fs': self.foodStuff_id}, True)
        return '%s://%s/qhmobile/tips/%s/?%s' % (settings.SITE_PROTOCOL,
                                                 Site.objects.get(id=settings.SITE_ID).domain,
                                                 language, qs)


class SecretCategory(models.Model):
    title = models.ForeignKey(String, related_name="secretCategory")
    image = models.ImageField(upload_to="secretCat", blank=True, null=True)
    img200 = ImageSpecField([Transpose(Transpose.AUTO), ResizeToCover(width=200, height=5)], image_field='image',
                            options={'quality': 90})
    img500 = ImageSpecField([Transpose(Transpose.AUTO), ResizeToCover(width=500, height=5)], image_field='image',
                            options={'quality': 90})
    color = models.CharField(max_length=6, default="69d0ee")
    positionIndex = models.IntegerField(default=100)

    def __unicode__(self):
        return self.title.en

    class Meta:
        ordering = ('positionIndex', 'id',)

    def jdata(self):
        data = {"type": "SECRETS_BOOK", 'id': self.id, 'title': self.title.jdataAll()}
        data['id'] = "SB_%d" % data['id']
        data['hasSelectables'] = True
        data['pIndex'] = self.positionIndex
        data['image'] = dict(id=self.id, img100=self.img200.url if self.img200 else None,
                             img200=self.img200.url if self.img200 else None,
                             img300=self.img500.url if self.img500 else None,
                             img500=self.img500.url if self.img500 else None,
                             imgFixedHieght=self.img500.url if self.img500 else None,
                             imgPrintThick=self.img500.url if self.img500 else None,
                             imgPrintThin=self.img500.url if self.img500 else None,
                             thumbnail=self.img500.url if self.img500 else None)
        data['loadingUrl_en'] = \
            "%s://%s/qhmobile/secretsLoading/en/%s/" % (
                settings.SITE_PROTOCOL, Site.objects.get(id=settings.SITE_ID).domain, self.id, )
        data['loadingUrl_es'] = \
            "%s://%s/qhmobile/secretsLoading/es/%s/" % (
                settings.SITE_PROTOCOL, Site.objects.get(id=settings.SITE_ID).domain, self.id, )
        return data

    def save(self, force_insert=False, force_update=False, using=None):
        """Write a new library version number on save"""
        LibraryData.objects.create().save()
        return super(SecretCategory, self).save(force_insert=force_insert, force_update=force_update, using=using)

    def delete(self, *args, **kwargs):
        LibraryData.objects.create().save()
        return super(SecretCategory, self).delete(*args, **kwargs)


class ExternalLink(models.Model):
    secret = models.ForeignKey('Secret')
    linkString = models.ForeignKey(String)
    LANGUAGE_CHOICES = ((u'en', u'Inglés'), (u'es', u'Español'),)
    language = models.CharField(max_length=2, choices=LANGUAGE_CHOICES)
    url = models.URLField()


class Secret(models.Model):
    title = models.ForeignKey(String, related_name="secretTitle")
    category = models.ForeignKey(SecretCategory)
    isActive = models.BooleanField(default=True)
    image = models.ImageField(upload_to="secrets", blank=True, null=True)
    img300 = ImageSpecField([Transpose(Transpose.AUTO), ResizeToCover(width=300, height=5)],
                            image_field='image',
                            options={'quality': 90})
    img600 = ImageSpecField([Transpose(Transpose.AUTO), ResizeToCover(width=600, height=5)],
                            image_field='image',
                            options={'quality': 90})
    image_es = models.ImageField(upload_to="secrets", blank=True, null=True)
    img300_es = ImageSpecField([Transpose(Transpose.AUTO), ResizeToCover(width=300, height=5)],
                               image_field='image_es',
                               options={'quality': 90})
    img600_es = ImageSpecField([Transpose(Transpose.AUTO), ResizeToCover(width=600, height=5)],
                               image_field='image_es',
                               options={'quality': 90})
    coverImage = models.ForeignKey('CoverPhoto', blank=True, null=True, on_delete=models.PROTECT)
    coverImage_es = models.ForeignKey('CoverPhoto', blank=True, null=True, related_name="coverImage_es",
                                      on_delete=models.PROTECT)
    secret = models.ForeignKey(String, related_name="secretText")
    whyItWorks = models.ForeignKey(String, related_name="whyItWorks")
    attachment_en = models.FileField(upload_to="secret_attachments", null=True, blank=True)
    attachment_es = models.FileField(upload_to="secret_attachments", null=True, blank=True)

    def __unicode__(self):
        return self.title.en

    def jdata(self):
        return {
            'id': -1 * self.id,
            'title_en': self.title.jdata(language='en'),
            'title_es': self.title.jdata(language='es'),
            'url_en': "%s://%s/qhmobile/mobileSecret/en/%d/" % (settings.SITE_PROTOCOL,
                                                                Site.objects.get(id=settings.SITE_ID).domain,
                                                                self.id),
            'url_es': "%s://%s/qhmobile/mobileSecret/es/%d/" % (settings.SITE_PROTOCOL,
                                                                Site.objects.get(id=settings.SITE_ID).domain,
                                                                self.id),
            'photoUrl': self.img600.url if self.image else None,
            'photoUrl_es': self.img600_es.url if self.image_es else None,
            'coverPhotoId': self.coverImage_id,
            'coverPhotoId_es': self.coverImage_es_id,
            'shareUrl_en': "%s://%s/qhmobile/secret/%d/en/" % (settings.SITE_PROTOCOL,
                                                               Site.objects.get(id=settings.SITE_ID).domain,
                                                               self.id),

            'shareUrl_es': "%s://%s/qhmobile/secret/%d/es/" % (settings.SITE_PROTOCOL,
                                                               Site.objects.get(id=settings.SITE_ID).domain,
                                                               self.id),
        }

    def get_absolute_url(self):
        return '/qhmobile/mobileSecret/en/%d/' % self.id

    def getWebUrl(self, language):
        if language == 'es':
            return "%s://%s/qhmobile/mobileSecret/es/%d/" % (settings.SITE_PROTOCOL,
                                                                Site.objects.get(id=settings.SITE_ID).domain,
                                                                self.id)
        else:
            return "%s://%s/qhmobile/mobileSecret/en/%d/" % (settings.SITE_PROTOCOL,
                                                                Site.objects.get(id=settings.SITE_ID).domain,
                                                                self.id)

    def save(self, force_insert=False, force_update=False, using=None):
        if not self.image:
            self.coverImage = None
        else:
            if not self.coverImage or self.image.url != self.coverImage.img.url:
                u, created = User.objects.get_or_create(username="secrets_cover")
                cp = CoverPhoto(img=self.image, owner=u)
                cp.save()
                self.coverImage = cp

        if not self.image_es:
            self.coverImage_es = None
        else:
            if not self.coverImage_es or self.image_es.url != self.coverImage_es.img.url:
                u, created = User.objects.get_or_create(username="secrets_cover")
                cp = CoverPhoto(img=self.image_es, owner=u)
                cp.save()
                self.coverImage_es = cp
        super(Secret, self).save(force_insert, force_update, using)

    def english_external_links(self):
        return self.externallink_set.filter(language='en')

    def spanish_external_links(self):
        return self.externallink_set.filter(language='es')

class SecretBookSelection(models.Model):
    secret = models.ForeignKey(Secret)
    selected = models.BooleanField(default=True)
    extras = models.IntegerField(default=0)
    scrolled = models.BooleanField(default=False)

    def __unicode__(self):
        return "%d: %s - %s" % (self.secret.id, self.secret.title.en, 'SELECTED' if self.selected else "DROPPED")


class SecretBook(models.Model):
    user = models.ForeignKey(User, db_index=True)
    selections = models.ManyToManyField(SecretBookSelection)
    coverPhoto = models.ForeignKey(CoverPhoto)
    pantry = models.ForeignKey(FoodPantry, null=True, blank=True)
    createdAt = models.DateTimeField(auto_now_add=True)
    category = models.ForeignKey(SecretCategory, null=True, blank=True, default=None)
    pdf_en = models.FileField(upload_to='pdfs', null=True, blank=True)
    pdf_es = models.FileField(upload_to='pdfs', null=True, blank=True)
    who_says_so_viewed = models.BooleanField(default=False)
    latitude = models.FloatField(null=True, blank=True)
    longitude = models.FloatField(null=True, blank=True)

    def getPdf(self, language):
        if language == 'es':
            return self.pdf_es
        else:
            return self.pdf_en

    def getFirstName(self):
        return self.user.first_name

    def getCoverUrl(self, language, pantry=None):
        urlMap = {'t': unicode(self.category.title.es if language == 'es' else self.category.title.en).encode('utf-8'),
                  'img': self.coverPhoto_id,
                  'c': self.category_id}
        if self.user and self.user.first_name:
            urlMap['n'] = self.user.first_name

        if pantry is not None:
            urlMap['p'] = unicode(pantry.name).encode('utf-8')

        return '%s://%s/qhmobile/secretsCover/%s/?%s' % (settings.SITE_PROTOCOL,
                                                         Site.objects.get(id=settings.SITE_ID).domain,
                                                         language, urlencode(urlMap))

    def getSecretsUrl(self, language):
        return '%s://%s/qhmobile/secrets/%d/%s/' % (settings.SITE_PROTOCOL,
                                                    Site.objects.get(id=settings.SITE_ID).domain,
                                                    self.id,
                                                    language)

    def getExtrasUrls(self, language):
        sUrls = []

        for s in self.selections.all():
            for i in range(s.extras):
                sUrls.append(s.secret.getWebUrl(language))

        return sUrls


class ViewingData(models.Model):
    type = models.CharField(max_length=1, choices=(('R', 'Recipe'), ('S', 'Secret'), ('T', 'Tips')))
    recipe = models.ForeignKey('Recipe', null=True, blank=True)
    secret = models.ForeignKey('Secret', null=True, blank=True)
    recipeBook = models.ForeignKey('RecipeBook', null=True, blank=True)
    secretBook = models.ForeignKey('SecretBook', null=True, blank=True)
    book_id = models.CharField(max_length=56)
    timeStamp = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User)
    event_choices = (('S', 'Share'), ('V', 'Begin Viewing'), ('C', 'Complete Viewing'))
    event = models.CharField(max_length=1, choices=event_choices)
    data = models.TextField(blank=True, null=True)


class UserProfileManager(models.Manager):
    def create_user_and_user_profile_by_device_id(self, device_id):
        """Create a user given their device ID.

        Due to limitations with Django, a username will be randomly generated for the user.

        :param device_id: a device ID to create a user from
        :return: a user if the creation succeeded, `None` otherwise
        """
        if device_id is None or self.filter(deviceId=device_id).count() != 0:  # Device ID must not already be used.
            return None

        # Generate a unique username. A username is required for a user and a UUID device ID is too long to fit within
        # Django's username length constraints (30 characters) so the field will be filled with a randomly generated
        # string with a length of 30 characters. "iOS_" is prepended to the beginning of the string since this method
        # is used by iOS users and this helps identify those users. If there's a username collision, some attempts will
        # be made to create a new, unique username.
        username_chars = string.ascii_letters + string.digits
        attempts = 0

        while attempts < 1000:  # Avoid an infinite loop if a unique username can't be generated.
            attempts += 1
            try:
                # Create a new user with the given device ID and generated username.
                username = ''.join(['iOS_'] + [random.choice(username_chars) for _ in range(26)])
                user = User.objects.create_user(username=username, email=None, password=None)
                user.userprofile.deviceId = device_id
                user.save()
                return user
            except IntegrityError:
                pass

        return None


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    deviceId = models.TextField(max_length=38, null=True)
    objects = UserProfileManager()


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.userprofile.save()
