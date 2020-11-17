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

from django.conf.urls import patterns, url

from qhmobile import views

urlpatterns = patterns('',
    url(r'^$', views.index, name='index'),

    # ex: /questions/5/
    url(r'^getQuestion/(?P<question_id>\d+)/$', views.getQuestion, name='getQuestion'),
    url(r'^questions/(?P<foodstuff>\w+)/(?P<language_id>\w\w)$', views.getQuestions, name='getQuestions'),
    url(r'^foodstuffs/(?P<language_id>\w\w)$', views.getFoodStuffs),
    url(r'^getInterview/?$', views.questions),

    url(r'^recipe/(?P<id>\d+)/(?P<language>\w\w)/$', views.getRecipe, name='getRecipe'),
    url(r'^recipePdf/(?P<id>\d+)/(?P<language>\w\w)/$', views.getRecipePdf, name='getRecipe'),
    url(r'^libraryInfo/?$', views.libraryInfo),
    url(r'^mobileRecipe/(?P<language>\w\w)/(?P<id>\d+)/$', views.getMobileRecipe),
    url(r'^recipes/(?P<foodstuff>\w+)/$', views.getRecipes),
    url(r'^secrets/(?P<categoryId>\d+)/$', views.getSecrets),
    url(r'^getSelectables/?$', views.getSelectables),
    url(r'^cover/(?P<language>\w\w)/$', views.CoverView.as_view(), name='cover'),
    url(r'^secretsCover/(?P<language>\w\w)/$', views.SecretsCoverView.as_view(), name='secrets_cover'),
    url(r'^allTips/$', views.AllTips.as_view()),
    url(r'^tips/(?P<language>\w\w)/$', views.Tips.as_view()),
    url(r'^createVeggieBook/$', views.createVeggieBook),
    url(r'^createSecretsBook/$', views.createSecretsBook),
    url(r"^uploadCoverPhoto/$", views.uploadCoverPhoto),
    url(r"^availableCoverPhotos/$", views.availableCoverPhotos),
    url(r"^register/$", views.register),
    url(r"^loginByDeviceId/$", views.login_by_device_id),
    url(r"^veggieBook/(?P<recipeBook_id>\d+)/$", views.vbPreview),
    url(r"^veggieBookPdf/(?P<language>\w\w)/(?P<recipeBook_id>\d+)/$", views.vbPdf),
    url(r"^secretsBookPdf/(?P<language>\w\w)/(?P<id>\d+)/$", views.sbPdf),
    url(r"^recipesLoading/(?P<language>\w\w)/(?P<foodstuff_id>\w+)/$", views.recipeInstructions),
    url(r"^secretsLoading/(?P<language>\w\w)/(?P<category_id>\w+)/$", views.secretsLoading),
    url(r"^printVeggieBook/$", views.printVeggieBook),
    url(r'^mobileSecret/(?P<language>\w\w)/(?P<secretId>\d+)/$', views.getMobileSecret),
    url(r'^secret/(?P<secretId>\d+)/(?P<language>\w\w)/$', views.getMobileSecret),
    url(r'^secrets/(?P<secretsBookId>\d+)/(?P<language>\w\w)/$', views.secrets),
    url(r'^pantries/$', views.pantries),
    url(r'^recordEvent/$', views.record_event)
)
