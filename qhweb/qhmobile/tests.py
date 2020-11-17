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
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""

from django.test import TestCase
from qhmobile import models, builders



class Smoketest(TestCase):
    fixtures = ['testdata.json']

    def test_can_get_all_recipes(self):
        """
        in the testdata fixture we import 200 recipes
        this makes sure we get them all when we check the
        database
        """
        print models.Recipe.objects.count()
        self.assertEqual(models.Recipe.objects.count(),200)

    def test_version_builder(self):
        """
        tests to see if the version builder returns a valid version.
        and tests to see if saving a foodstuff revs the version
        """
        vb = builders.VersionBuilder()
        data = vb.build()
        self.assertItemsEqual(['version'],data.keys(),msg='Version builder expects {"version":...}')
        version = data['version']
        self.assertIsNotNone(version,msg='No version returned')
        stockPhoto = models.StockPhoto.objects.all()[0]
        nameString = models.String.objects.create(en='test',es='skljfhdkljh')
        nameString.save()
        fs = models.FoodStuff.objects.create(id="TEST",nameString=nameString,image=stockPhoto)
        fs.save()
        data = vb.build()
        self.assertNotEqual(version,data['version'],msg="Version should have change with new book added")
        self.assertItemsEqual(['version'],data.keys(),msg='Version builder expects {"version":...}')
        version = data['version']
        self.assertIsNotNone(version,msg='No version returned')






