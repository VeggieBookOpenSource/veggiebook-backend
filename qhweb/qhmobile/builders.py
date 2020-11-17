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

"""
This package serves a a layer of abstraction between the data model and the views.
This will allow us to unit test our system independent of model changes and endpoint
changes.

"""

from abc import abstractmethod, ABCMeta
from qhmobile import models


try:
    import simplejson as json
    from simplejson import JSONEncoder
except ImportError:
    import json
    from json import JSONEncoder

__author__ = 'danieldipasquo'


class BuilderBase:
    """
    Here we implement the builder design pattern.
    Builders can add and run other builders and use those results.
    The build method should always return a dictionary.

    for example:

    class A(BuilderBase):
        def build(self):
            return {'a':'b'}

    class X(BuilderBase):
        def build(self):
            return {'xxx':'yyy'}

    class AandX(BuilderBase):
        def __init__(self):
            self.addBuilder(A(),'A')
            self.addBuilder(B(),'B')

        def build(self):
            self.runBuilders()
            return self.combineResults()

    AandX().build()
    returns
    {'a':'b','xxx':'yyy'}


    """
    __metaclass__ = ABCMeta
    builders = {}
    buildResults = {}

    @abstractmethod
    def build(self):
        """
        Returns a dictionary representation of what you are building
        """
        pass

    def addBuilder(self, builder, id):
        """
        add a builder and an id to use to reference that builder or its results
        """
        self.builders[id] = builder

    def runBuilders(self):
        for id in self.builders.keys():
            self.buildResults[id] = self.builders[id].build()

    def buildJson(self):
        return json.dumps(self.build())

    def combineResults(self, *ids):
        if len(ids) == 0:
            ids = self.builders.keys()

        data = []
        for itemList in [self.buildResults[x].items() for x in ids]:
            data += itemList
        return dict(data)


class ComboBuilder(BuilderBase):
    """
        This is a builder that combines other builders.
        look at the LibraryInfoBuilder for an example of how to use this.
    """

    def __init__(self, **kwargs):
        self.builders = kwargs

    def build(self):
        self.runBuilders()
        return self.combineResults()


class VersionBuilder(BuilderBase):
    def build(self):
        version = models.LibraryData.objects.order_by('-version')[0]
        return version.jdata()


class SystemLanguagesBuilder(BuilderBase):
    def build(self):
        languages = models.String.objects.all()[0].jdataAll().keys()
        languages.remove('id')
        return {'languages': languages}


class ImageSizesBuilder(BuilderBase):
    def build(self):
        image_sizes = models.StockPhoto.objects.all()[0].jdata().keys()
        image_sizes.remove('id')
        return {'imageSizes': image_sizes}


class BookTypesBuilder(BuilderBase):
    def build(self):
        return {'bookTypes': ['RECIPE_BOOK', 'SECRETS_BOOK']}


class BooksAvailableBuilder(BuilderBase):
    def getRecipeBooks(self):
        return [rb.jdata() for rb in models.FoodStuff.objects.all()]

    def getTipBooks(self):
        return [rb.jdata() for rb in models.SecretCategory.objects.all()]

    def build(self):
        return {'booksAvailable': self.getRecipeBooks() + self.getTipBooks()}


class LibraryInfoBuilder(ComboBuilder):
    def __init__(self):
        super(LibraryInfoBuilder, self).__init__(
            version=VersionBuilder(),
            languages=SystemLanguagesBuilder(),
            imageSizes=ImageSizesBuilder(),
            bookTypes=BookTypesBuilder(),
            booksAvailable=BooksAvailableBuilder()
        )


class LocalPantries(BuilderBase):
    def __init__(self, lat=0, lon=0):
        self.lat = lat
        self.lon = lon

    def build(self):
        lp = self.get_n_closest(10)
        pantries = []
        for p in lp:
            jdata = p.jdata()
            jdata['distance'] = p.distance
            pantries.append(jdata)

        return {"closestPantries": pantries}

    def get_n_closest(self, n):
        return models.FoodPantry.objects.raw('select address_ptr_id, name, easy_maps_address.computed_address, \
( 3959 * acos( cos( radians(%s) ) *cos( radians( easy_maps_address.latitude ) ) * \
cos( radians( easy_maps_address.longitude ) - radians(%s) ) + sin( radians(%s) ) * \
sin( radians( easy_maps_address.latitude ) ) ) ) AS distance \
from qhmobile_foodpantry, easy_maps_address where qhmobile_foodpantry.address_ptr_id = easy_maps_address.id and qhmobile_foodpantry.printingAvailable = 1 \
order by distance limit 0, %s;', [self.lat, self.lon, self.lat, n])




class RecentPantries(BuilderBase):
    def __init__(self, profileId=None):
        self.profileId = profileId

    def build(self):
        return {"recentPantries": []}


class QuestionsBuilder(BuilderBase):
    def __init__(self, questions, foodstuff, language='en', user=None):
        self.language = language
        self.questions = questions
        self.foodstuff = foodstuff
        self.user = user

    def build(self):
        questions = [q.jdata(language=self.language, substitute=self.foodstuff.name(self.language).lower()) for q
                     in
                     self.questions]
        if self.user is not None:
            lastRecipeBooks = models.RecipeBook.objects.filter(user_id=self.user.id, foodStuff_id=self.foodstuff.id).order_by('-createdAt')

            if len(lastRecipeBooks) == 0:
                lastRecipeBooks = models.RecipeBook.objects.filter(user_id=self.user.id).order_by('-createdAt')

            if len(lastRecipeBooks) > 0:
                lastRecipeBook = lastRecipeBooks[0]
                attributes = [a.name for a in lastRecipeBook.attributes.all()]
                for question in questions:
                    for choice in question["choices"]:
                        if choice["attribute"] in attributes:
                            choice["defaultChoice"] = True
        return {
            'questions': questions}


class InterviewBuilder(ComboBuilder):
    def __init__(self, questions, foodstuff, language, lat, lon,  user=None):
        super(InterviewBuilder, self).__init__(
            closestPantries=LocalPantries(lat, lon),
            recentPantries=RecentPantries(user.id if user is not None else 0),
            questions=QuestionsBuilder(questions, foodstuff, language, user)
        )

