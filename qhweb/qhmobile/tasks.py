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

from celery import task


@task()
def lazyCachePhoto(id):
    from qhmobile.models import Photo
    photo = Photo.objects.filter(id=id)[0]
    photo.cacheAllSizes()

@task()
def lazyCacheStockPhoto(id):
    from qhmobile.models import StockPhoto
    photo = StockPhoto.objects.filter(id=id)[0]
    photo.cacheAllSizes()

@task()
def createPdf(recipeBookId, language):
    from qhmobile.models import RecipeBook
    from qhmobile import pdf
    rb = RecipeBook.objects.filter(id=recipeBookId)[0]
    pdf.createPdf(rb, language)

@task()
def printPdf(recipeBookId, language, pantryId, pin):
    from qhmobile.models import RecipeBook, FoodPantry
    from qhmobile.pdf import printPdf
    rb = RecipeBook.objects.filter(id=recipeBookId)[0]
    pantry = FoodPantry.objects.filter(id=pantryId)[0]
    if pantry.printingAvailable:
        print "PRINTING RB"
        printPdf(rb, language, pantry, pin)
        print "Complete"
    else:
        print "Pantry is closed, not printing."

@task()
def printSecretPdf(secretBookId, language, pantryId, pin):
    from qhmobile.models import SecretBook, FoodPantry
    from qhmobile.pdf import printSecretPdf as pPdf
    sb = SecretBook.objects.filter(id=secretBookId)[0]
    pantry = FoodPantry.objects.filter(id=pantryId)[0]
    if pantry.printingAvailable:
        print "PRINTING RB"
        pPdf(sb, language, pantry, pin)
        print "Complete"
    else:
        print "Pantry is closed, not printing."

@task()
def record_event_task(user_id, event, book_id, item_id, data="", source_book_id=None):
    from qhmobile.models import User, Recipe, Secret, ViewingData
    book_type = book_id.split('_')[0]
    try:
        if book_type == 'RB':
            if item_id == "TIPS":
                event_type = "T"
                recipe = None
            else:
                event_type = 'R'
                recipe = Recipe.objects.get(pk=item_id)
                recipe_book_id = source_book_id
            secret = None
            secret_book_id = None
        else:
            event_type = 'S'
            recipe = None
            recipe_book_id = None
            secret_book_id = source_book_id
            secret = Secret.objects.get(pk=item_id)

        user = User.objects.get(pk=user_id)
        event = ViewingData(
            type=event_type,
            user=user,
            event=event,
            data=data,
            secret=secret,
            recipe=recipe,
            book_id=book_id,
            recipeBook_id=recipe_book_id,
            secretBook_id=secret_book_id
        )
        event.save()
    except User.DoesNotExist:
        return "Bad User Id"
    except Recipe.DoesNotExist:
        return "Bad Recipe Id"
    except Secret.DoesNotExist:
        return "Bad Secret Id"
    except:
        print "here"

