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

from django.core.files import File
from django.core.files.storage import default_storage
from django.core.mail import EmailMessage

__author__ = 'danieldipasquo'

from wkhtmltox import Pdf
from tempfile import mkstemp
import os


def createPdf(recipeBook, language, pantry=None, printNow=False):

    pdf = Pdf()
    f, path = mkstemp()
    os.close(f)

    path += '.pdf'

    pdf.set_global_setting('out', path)
    pdf.set_global_setting('size.paperSize', 'Letter')
    pdf.set_global_setting('documentTitle', unicode(recipeBook.foodStuff.name(language=language)).encode('utf-8'))


    # cover page
    # No header or footer
    pdf.add_page({'page': recipeBook.getCoverUrl(language, pantry)})

    # recipe pages
    common_settings = {'footer.right': '[page]', 'footer.left': 'VeggieBook', 'footer.line': 'true'}
    for recipeUrl in recipeBook.getRecipeUrls(language):
        page = {'page': recipeUrl}
        page.update(common_settings)
        pdf.add_page(page)

    #tips page
    page = {'page': recipeBook.getTipsUrl(language)}
    page.update(common_settings)
    pdf.add_page(page)

    #extras should not have have footers
    for recipeUrl in recipeBook.getExtrasUrls(language):
        page = {'page': recipeUrl}
        pdf.add_page(page)

    pdf.convert()

    with open(path, 'r') as f:
        localFile = File(f)
        permPath = default_storage.save('pdf/' + os.path.basename(path), localFile)

    os.remove(path)

    if language == 'es':
        recipeBook.pdf_es = permPath
    else:
        recipeBook.pdf_en = permPath

    recipeBook.save()


def createSecretPdf(secretBook, language, pantry=None):
    pdf = Pdf()
    f, path = mkstemp()
    os.close(f)

    path += '.pdf'

    pdf.set_global_setting('out', path)
    pdf.set_global_setting('size.paperSize', 'Letter')
    pdf.set_global_setting('documentTitle', unicode(secretBook.category.title.es if language == 'es' else secretBook.category.title.en).encode('utf-8'))


    # cover page
    # No header or footer
    pdf.add_page({'page': secretBook.getCoverUrl(language, pantry)})

    # recipe pages
    common_settings = {'footer.right': '[page]', 'footer.left': 'VeggieBook', 'footer.line': 'true'}

    #secrets page
    page = {'page': secretBook.getSecretsUrl(language)}
    page.update(common_settings)
    pdf.add_page(page)

    #extras should not have have footers
    for sUrl in secretBook.getExtrasUrls(language):
        print sUrl
        page = {'page': sUrl}
        pdf.add_page(page)


    pdf.convert()

    with open(path, 'r') as f:
        localFile = File(f)
        permPath = default_storage.save('pdf/' + os.path.basename(path), localFile)

    os.remove(path)

    if language == 'es':
        secretBook.pdf_es = permPath
    else:
        secretBook.pdf_en = permPath

    secretBook.save()


def printPdf(recipeBook, language, pantry, pin):
    createPdf(recipeBook, language, pantry)

    message = 'User: %s, Name: %s, Print Code: %s' % (recipeBook.user.email, recipeBook.getFirstName(), pin)

    print "Email to %s" % pantry.printerEmail

    email = EmailMessage("Print your veggiebook", message,
                         'veggiebook.project@gmail.com', [pantry.printerEmail])
    email.attach('veggiebook.pdf', recipeBook.getPdf(language).read(), 'application/pdf')
    email.send()


def printSecretPdf(secretBook, language, pantry, pin):
    createSecretPdf(secretBook, language, pantry)

    message = 'User: %s, Name: %s, Print Code: %s' % (secretBook.user.email, secretBook.getFirstName(), pin)

    print "Email to %s" % pantry.printerEmail

    email = EmailMessage("Print your secretBook", message,
                         'veggiebook.project@gmail.com', [pantry.printerEmail])
    email.attach('secretbook.pdf', secretBook.getPdf(language).read(), 'application/pdf')
    if language == 'es':
        for s in secretBook.selections.filter(selected=True, secret__attachment_es__isnull=False):
            if s.secret.attachment_es:
                email.attach(s.secret.title.es + '.pdf', s.secret.attachment_es.read(), 'application/pdf')
    else:
        for s in secretBook.selections.filter(selected=True, secret__attachment_en__isnull=False):
            if s.secret.attachment_en:
                email.attach(s.secret.title.en + '.pdf', s.secret.attachment_en.read(), 'application/pdf')
    email.send()

