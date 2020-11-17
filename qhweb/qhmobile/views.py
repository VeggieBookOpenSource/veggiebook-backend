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
from itertools import chain
import random
import string
import tempfile
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
import urllib

from django.http import HttpResponse, Http404, HttpResponseRedirect, HttpResponseServerError, HttpResponseBadRequest
from django.utils.decorators import method_decorator
from django.views.generic import TemplateView

from qhmobile.auth import DeviceIdBackend
from qhmobile.forms import CoverPhotoForm
from Users import settings
from django_openid_auth.exceptions import DjangoOpenIDException
from django_openid_auth.models import UserOpenID
from django_openid_auth.signals import openid_login_complete
from qhmobile.models import *
from django.shortcuts import render_to_response, get_object_or_404, get_list_or_404, render
from django.views.decorators.http import require_http_methods
from qhmobile import builders, pdf, tasks
from django.core.cache import cache
from django_openid_auth.views import default_render_failure, parse_openid_response
from openid.consumer.consumer import (
    Consumer, SUCCESS, CANCEL, FAILURE)
from django import http
from django.shortcuts import render_to_response
from django.template.loader import get_template
from django.template import Context
import xhtml2pdf.pisa as pisa
import cStringIO as StringIO
import cgi
from django.core.servers.basehttp import FileWrapper
from mobi.decorators import detect_mobile

from django.contrib.auth import (
    REDIRECT_FIELD_NAME, authenticate, login as auth_login)
from qhmobile.tasks import record_event_task

try:
    import simplejson as json
    from simplejson import JSONEncoder
except ImportError:
    import json
    from json import JSONEncoder


def index(request):
    return HttpResponse("I'm Alive!!")


from objcode import ObjectEncoder
from django.views.decorators.csrf import csrf_exempt


def getQuestion(request, question_id):
    q = get_object_or_404(Question, qid=question_id)
    jdata = q.jdata()
    response_data = ObjectEncoder().encode(jdata)
    return HttpResponse(response_data, content_type="application/json")


def getQuestions(request, foodstuff, language_id, lat, lon, user=None):
    try:
        qs = Question.objects.all()
    except Question.DoesNotExist:
        raise Http404
    foodstuff = get_object_or_404(FoodStuff, id=foodstuff)
    if not String().__dict__.has_key(language_id):
        raise Http404

    builder = builders.InterviewBuilder(qs, foodstuff, language_id, lat=lat, lon=lon, user=user)

    jdata = builder.build()
    response_data = ObjectEncoder().encode(jdata)
    return HttpResponse(response_data, content_type="application/json")


@csrf_exempt
@require_http_methods(["POST"])
def questions(request):
    in_json = json.loads(request.body)

    # required fields
    if in_json is None or in_json['language'] is None or in_json['bookType'] is in_json['bookId'] is None or in_json[
        'lat'] is None or in_json['lon'] is None:
        raise Http404

    # if its a recipe book we can modify the bookId and use the getQuestions view

    if in_json['bookType'] == 'RECIPE_BOOK':
        foodstuff = in_json['bookId'].split('_')[1]
        language = in_json['language']
        userId = in_json['profileId']
        if userId is None:
            user = None
        else:
            user = get_object_or_404(User, id=userId)
        return getQuestions(request, foodstuff, language, in_json['lat'], in_json['lon'], user)

    raise Http404


def getFoodStuffs(request, language_id):
    try:
        foodstuffs = FoodStuff.objects.all()
    except Question.DoesNotExist:
        raise Http404
    jdata = [fs.jdata(language=language_id) for fs in foodstuffs]
    response_data = ObjectEncoder().encode(jdata)
    return HttpResponse(response_data, content_type="application/json")


@csrf_exempt
@require_http_methods(["POST"])
def getRecipes(request, foodstuff):
    foodstuff = get_object_or_404(FoodStuff, id=foodstuff)

    # every user has the attribute ALL_USERS
    attributes = json.loads(request.body)['attributes']

    or_reqs = OrRequirement.getMatchingOrRequirements(attributes)

    recipes = Recipe.objects.filter(foodStuff=foodstuff).filter(isActive=True)
    recipe_ids = []
    for recipe in recipes:
        if recipe.matchesRequirements(or_reqs):
            recipe_ids.append(recipe.jdata(or_reqs=or_reqs))
    response_data = ObjectEncoder().encode(recipe_ids)
    return HttpResponse(response_data, content_type="application/json")


@csrf_exempt
@require_http_methods(["POST"])
def getSecrets(request, categoryId):
    foodstuff = get_object_or_404(SecretCategory, id=categoryId)

    secrets = [s.jdata() for s in Secret.objects.filter(category_id=categoryId)]

    response_data = ObjectEncoder().encode(secrets)
    return HttpResponse(response_data, content_type="application/json")


def getMobileRecipe(request, id, language):
    r = get_object_or_404(Recipe, recipeId=id)
    ids = request.GET.getlist('a')

    annotations = [get_object_or_404(Annotation, id=a) for a in ids]
    is_ios = 'VeggieBook' in request.META.get('HTTP_USER_AGENT', '')

    if language == 'es':
        return render_to_response(
            'recipe_mobile_es.html',
            {
                'iidd': id,
                'recipe': r,
                'navOn': False,
                'annotations': annotations,
                'is_ios': is_ios
            })
    else:
        return render_to_response(
            'recipe_mobile.html',
            {
                'iidd': id,
                'recipe': r,
                'navOn': False,
                'annotations': annotations,
                'is_ios': is_ios
            })


def previewMobileRecipe(request, id, language):
    r = get_object_or_404(Recipe, recipeId=id)
    annotations = [a for a in r.annotations.all()]
    if language == 'es':
        return render_to_response('recipe_mobile_es.html',
                                  {'iidd': id, 'recipe': r, 'navOn': True, 'annotations': annotations})
    else:
        return render_to_response('recipe_mobile.html',
                                  {'iidd': id, 'recipe': r, 'navOn': True, 'annotations': annotations})


@detect_mobile
def getRecipe(request, id, language):
    user_agent = request.META.get('HTTP_USER_AGENT', None)

    is_mobile = request.mobile or 'VeggieBook' in user_agent
    if is_mobile:
        return getMobileRecipe(request, id, language)

    r = get_object_or_404(Recipe, recipeId=id)
    ids = request.GET.getlist('a')
    annotations = [get_object_or_404(Annotation, id=a) for a in ids]

    if language == 'es':
        return render_to_response('recipe_new_es.html',
                                  {'iidd': id, 'recipe': r, 'navOn': False, 'annotations': annotations,})
    else:
        return render_to_response('recipe_new_en.html',
                                  {'iidd': id, 'recipe': r, 'navOn': False, 'annotations': annotations,})


@csrf_exempt
@require_http_methods(["POST", "GET"])
def libraryInfo(request):
    cached_version = cache.get('libraryInfoVersion')
    response_data = cache.get('libraryInfoResponse')
    current_version = builders.VersionBuilder().build()['version']
    if cached_version is not None and response_data is not None and cached_version == current_version:
        return HttpResponse(response_data)

    jdata = builders.LibraryInfoBuilder().build()
    response_data = ObjectEncoder().encode(jdata)
    cache.set('libraryInfoVersion', current_version)
    cache.set('libraryInfoResponse', response_data)
    return HttpResponse(response_data, content_type="application/json")


@csrf_exempt
@require_http_methods(["POST"])
def getSelectables(request):
    json_in = json.loads(request.body)
    bookType = json_in['bookType']
    bookId = json_in['bookId']

    if bookType is None or bookId is None:
        raise Http404

    if bookType == 'RECIPE_BOOK':
        return getRecipes(request, foodstuff=bookId.split('_')[1])

    if bookType == 'SECRETS_BOOK':
        return getSecrets(request, categoryId=int(bookId.split('_')[1]))

    raise Http404


@csrf_exempt
def login_complete(request, redirect_field_name=REDIRECT_FIELD_NAME,
                   render_failure=None):
    redirect_to = request.REQUEST.get(redirect_field_name, '')
    render_failure = render_failure or \
                     getattr(settings, 'OPENID_RENDER_FAILURE', None) or \
                     default_render_failure

    openid_response = parse_openid_response(request)
    if not openid_response:
        return render_failure(
            request, 'This is an OpenID relying party endpoint.')

    if openid_response.status == SUCCESS:
        try:
            user = authenticate(openid_response=openid_response)
        except DjangoOpenIDException, e:
            return render_failure(request, e.message, exception=e)

        if user is not None:
            if user.is_active:
                auth_login(request, user)
                response = render_to_response('login_success.html',
                                              {'userId': user.id, 'awsAccessKey': settings.AWS_ACCESS_KEY_ID,
                                               'awsSecretKey': settings.AWS_SECRET_ACCESS_KEY})

                # Notify any listeners that we successfully logged in.
                openid_login_complete.send(sender=UserOpenID, request=request,
                                           openid_response=openid_response)

                return response
            else:
                return render_failure(request, 'Disabled account')
        else:
            return render_failure(request, 'Unknown user')
    elif openid_response.status == FAILURE:
        return render_failure(
            request, 'OpenID authentication failed: %s' %
                     openid_response.message)
    elif openid_response.status == CANCEL:
        return render_failure(request, 'Authentication cancelled')
    else:
        assert False, (
            "Unknown OpenID response type: %r" % openid_response.status)


class CoverView(TemplateView):
    template_name = 'cover_en.html'

    def get_context_data(self, **kwargs):
        coverPhoto = get_object_or_404(CoverPhoto, id=self.request.GET.get('img'))
        coverPhotoUrl = coverPhoto.img500.url
        foodStuff = get_object_or_404(FoodStuff, id=self.request.GET.get('fs'))

        if kwargs['language'] == 'es':
            self.template_name = 'cover_es.html'
        else:
            self.template_name = 'cover_en.html'

        data = {'title': self.request.GET.get('t'),
                'name': self.request.GET.get('n', None),
                'cover_image_url': coverPhotoUrl,
                'pantryName': self.request.GET.get('p', None),
                'fsImgUrl': foodStuff.image.img200.url,
                }
        return data


class SecretsCoverView(TemplateView):
    template_name = 'secret_cover_en.html'

    def get_context_data(self, **kwargs):
        coverPhoto = get_object_or_404(CoverPhoto, id=self.request.GET.get('img'))
        coverPhotoUrl = coverPhoto.img500.url
        category = get_object_or_404(SecretCategory, id=self.request.GET.get('c'))

        if kwargs['language'] == 'es':
            self.template_name = 'secret_cover_es.html'
        else:
            self.template_name = 'secret_cover_en.html'

        data = {'title': self.request.GET.get('t'),
                'name': self.request.GET.get('n', None),
                'cover_image_url': coverPhotoUrl,
                'pantryName': self.request.GET.get('p', None),
                'fsImgUrl': category.img200.url,
                }
        return data


class AllTips(TemplateView):
    template_name = 'tip_en.html'

    def get_context_data(self, **kwargs):
        fs = self.request.GET.get('fs', None)
        tips = FoodTip.objects.filter(foodStuff_id=fs) if fs else FoodTip.objects.all()

        # attributes = self.request.GET.getlist('a')
        #
        # requirements_fulfilled = OrRequirement.getMatchingOrRequirements(attributes)
        # tips = tips.filter(requirement__in=requirements_fulfilled)

        return {'tipList': tips}


class Tips(TemplateView):
    template_name = 'tip_en.html'

    def get_context_data(self, **kwargs):
        if kwargs['language'] == 'es':
            self.template_name = 'tip_es.html'
        else:
            self.template_name = 'tip_en.html'
        fs = self.request.GET.get('fs', None)
        tips = FoodTip.objects.filter(foodStuff_id=fs) if fs else FoodTip.objects.all()

        attributes = self.request.GET.getlist('a')
        tips = tips.filter(requirement__attributes__name__in=attributes)
        user_agent = self.request.META.get('HTTP_USER_AGENT', None)
        is_mobile = self.request.mobile or 'VeggieBook' in user_agent

        return {'tipList': tips, 'mobile': is_mobile}

    @method_decorator(detect_mobile)
    def dispatch(self, request, *args, **kwargs):
        return super(Tips, self).dispatch(request, *args, **kwargs)


class GetRecipe(TemplateView):
    def get_context_data(self, **kwargs):
        id = kwargs.get('id')
        language = kwargs.get('language')
        ids = self.request.GET.getlist('a')
        annotations = [get_object_or_404(Annotation, id=a) for a in ids]
        r = get_object_or_404(Recipe, recipeId=id)
        if language == 'es':
            self.template_name = 'recipe_es.html'
        else:
            self.template_name = 'recipe_new_en.html'
        return {'iidd': id, 'recipe': r, 'navOn': False, 'annotations': annotations,}


@csrf_exempt
@require_http_methods(["POST"])
def createVeggieBook(request):
    """

    :param request:
    :return: :raise:
    """
    json_in = json.loads(request.body)
    bookType = json_in['bookType']
    bookId = json_in['bookId']
    attributes = json_in['attributes']
    selectables = json_in['selectables']
    profileId = get_object_or_404(User, id=json_in['profileId'])
    language = json_in['language']
    coverUrl = get_object_or_404(CoverPhoto, id=json_in['coverPhoto'])
    latitude = json_in.get('latitude', None)
    longitude = json_in.get('longitude', None)

    # check for required fields
    if bookType is None or bookId is None or attributes is None or selectables is None or profileId is None or language is None:
        raise Http404

    pantry = None
    # for now default the pantry to Our Saviour Center
    pantryId = 6
    try:
        pantry = get_object_or_404(FoodPantry, id=json_in['pantryId'])
    except KeyError:
        pass

    if bookType == 'RECIPE_BOOK':
        foodStuff = get_object_or_404(FoodStuff, id=bookId.split('_')[1])

        # 1) create a new recipe book and save it in the database
        # 2) return the id and tips page
        # 3) create a background task to create the pdf and print it
        rb = RecipeBook(user_id=profileId.id, coverPhoto_id=coverUrl.id, foodStuff_id=foodStuff,
                        pantry_id=pantry.id if pantry is not None else None, latitude=latitude, longitude=longitude)
        rb.save()
        for r in selectables:
            rs = RecipeBookSelection(recipe_id=r['recipeId'], selected=r['selected'], extras=r['extras'])
            rs.save()
            rb.selections.add(rs.id)
        for attribute in attributes:
            rb.attributes.add(attribute)
        rb.save()
        response_data = ObjectEncoder().encode(
            {"id": rb.id, "createdAt": rb.createdAt.strftime('%s'),
             "tipsUrl_en": rb.getTipsUrl('en'),
             "tipsUrl_es": rb.getTipsUrl('es'),
             "coverUrl_en": rb.getCoverUrl('en'),
             "coverUrl_es": rb.getCoverUrl('es')})

        # pin = ''.join(random.choice(string.ascii_uppercase + string.digits) for x in range(4))
        # tasks.printPdf.delay(rb.id, language, pantryId, pin)

        return HttpResponse(response_data, content_type="application/json")
    else:
        category = get_object_or_404(SecretCategory, id=bookId.split('_')[1])

        sb = SecretBook(user=profileId, coverPhoto=coverUrl, category=category,
                        pantry_id=pantry.id if pantry is not None else None, latitude=latitude, longitude=longitude)

        sb.save()
        for r in selectables:
            sId = -1 * r['recipeId']
            rs = SecretBookSelection(secret_id=sId, selected=r['selected'], extras=r['extras'])
            rs.save()
            sb.selections.add(rs.id)
        sb.save()
        response_data = ObjectEncoder().encode(
            {"id": sb.id, "createdAt": sb.createdAt.strftime('%s'),
             "coverUrl_en": "",
             "coverUrl_es": ""})
        return HttpResponse(response_data, content_type="application/json")


@csrf_exempt
@require_http_methods(["POST"])
def uploadCoverPhoto(request):
    request.POST['order'] = 1000
    if 'owner' not in request.POST:
        return HttpResponseServerError("owner required")
    form = CoverPhotoForm(request.POST, request.FILES)
    if form.is_valid():
        coverPhoto = form.save()
        response_data = ObjectEncoder().encode({"id": coverPhoto.id, "url": coverPhoto.img300.url, "mine": True})
        return HttpResponse(response_data, content_type="application/json")
    else:
        return HttpResponseServerError("Invalid Request, img required.")


@csrf_exempt
@require_http_methods(["POST"])
def availableCoverPhotos(request):
    json_in = json.loads(request.body)
    user = get_object_or_404(User, id=json_in['profileId'])
    bt = json_in['bookId'].split('_')[0];
    if bt == 'RB':
        foodStuff = get_object_or_404(FoodStuff, id=json_in['bookId'].split('_')[1])
        photos = [{"id": p.id, "url": p.img300.url, "mine": p.owner_id is not None} for p in list(
            chain(CoverPhoto.objects.filter(owner_id=None).filter(restrictTo_id=foodStuff),
                  CoverPhoto.objects.filter(owner_id=None).filter(restrictTo_id=None)))]
    else:
        photos = [{"id": p.id, "url": p.img300.url, "mine": p.owner_id is not None} for p in
                  CoverPhoto.objects.filter(owner_id=None).filter(restrictTo_id=None)]

    response_data = ObjectEncoder().encode(photos)
    return HttpResponse(response_data, content_type="application/json")


@csrf_exempt
@require_http_methods(["POST"])
def register(request):
    json_in = json.loads(request.body)
    id_token = json_in.get('at').encode('utf-8')
    first_name = json_in.get('firstName')
    last_name = json_in.get('lastName')
    user = authenticate(token=id_token)
    if user is None:
        res = HttpResponse("Unauthorized")
        res.status_code = 401
        return res
    user.first_name = first_name
    user.last_name = last_name
    user.save()
    response_data = ObjectEncoder().encode({'profileId': user.id})
    return HttpResponse(response_data, content_type="application/json")


@csrf_exempt
@require_http_methods(['POST'])
def register_with_password(request):
    json_in = json.loads(request.body)
    first_name = json_in.get('firstName')
    last_name = json_in.get('lastName')
    email = json_in.get('email')
    password = json_in.get('password')


@csrf_exempt
@require_http_methods(['POST'])
def login_by_device_id(request):
    """Log a user in based on a device ID.

    If a user is not found for the device ID given, a new one will be created.

    :param request: an HTTP request containing a device ID.
    :return: a user ID for the user associated with the given device ID
    """
    json_in = json.loads(request.body)
    device_id = json_in.get('deviceId')

    # Run basic validation on the device ID.
    if not device_id:
        return HttpResponseBadRequest('Invalid request. Field "deviceId" required.')
    if not isinstance(device_id, str) and not isinstance(device_id, unicode):
        return HttpResponseBadRequest('Invalid request. Field "deviceId" is not a valid string type.')

    # Authenticate or create a user based on their device ID.
    user = authenticate(device_id=device_id)
    if user is None:
        user = UserProfile.objects.create_user_and_user_profile_by_device_id(device_id=device_id)
    if user is None:
        return HttpResponse('Unauthorized', status=401)

    # Respond with the user ID for the user to utilize in later requests.
    response_data = ObjectEncoder().encode({'profileId': user.id})
    return HttpResponse(response_data, content_type='application/json')


def render_to_pdf(template_src, context_dict):
    template = get_template(template_src)
    context = Context(context_dict)
    html = template.render(context)
    result = StringIO.StringIO()
    pdf = pisa.pisaDocument(StringIO.StringIO(html.encode("ISO-8859-1")), result)
    if not pdf.err:
        return http.HttpResponse(result.getvalue(), mimetype='application/pdf')
    return http.HttpResponse('We had some errors<pre>%s</pre>' % cgi.escape(html))


def getRecipePdf(request, id, language):
    r = get_object_or_404(Recipe, recipeId=id)
    ids = request.GET.getlist('a')
    annotations = [get_object_or_404(Annotation, id=a) for a in ids]

    if language == 'es':
        return render_to_pdf('recipe_mobile_es.html', {'iidd': id, 'recipe': r})
    else:
        return render_to_pdf('recipe_new_en.html',
                             {'iidd': id, 'recipe': r, 'navOn': False, 'annotations': annotations,})


def vbPreview(request, recipeBook_id):
    rb = get_object_or_404(RecipeBook, id=recipeBook_id)
    coverUrl = rb.getCoverUrl('en')
    recipeUrls = rb.getRecipeUrls('en')

    return render_to_response('veggiebookWeb.html', {'rb': rb, 'coverUrl': coverUrl, 'recipeUrls': recipeUrls})


def vbPdf(request, language, recipeBook_id):
    rb = get_object_or_404(RecipeBook, id=recipeBook_id)
    if language == 'es':
        if not rb.pdf_es:
            pdf.createPdf(rb, language)

        return HttpResponseRedirect(rb.pdf_es.url)

    if not rb.pdf_en:
        pdf.createPdf(rb, 'en')

    return HttpResponseRedirect(rb.pdf_en.url)


def sbPdf(request, language, id):
    sb = get_object_or_404(SecretBook, id=id)
    if language == 'es':
        if not sb.pdf_es:
            pdf.createSecretPdf(sb, language)

        return HttpResponseRedirect(sb.pdf_es.url)

    if not sb.pdf_en:
        pdf.createSecretPdf(sb, 'en')

    return HttpResponseRedirect(sb.pdf_en.url)


def recipeInstructions(request, language, foodstuff_id):
    return render_to_response('recipes_loading.html', {'fs': foodstuff_id, 'language': language})


@csrf_exempt
@require_http_methods(["POST"])
def printVeggieBook(request):
    json_in = json.loads(request.body)
    vb_id = json_in['id']
    pantry = get_object_or_404(FoodPantry, id=json_in['pantry'])
    pin = ''.join(random.choice(string.ascii_uppercase + string.digits) for x in range(4))
    language = json_in['language']
    book_type = json_in.get('type', "RECIPE_BOOK")

    if book_type == "RECIPE_BOOK":
        rb = get_object_or_404(RecipeBook, id=json_in['id'])
        tasks.printPdf.delay(rb.id, language, pantry.id, pin)
        response_data = ObjectEncoder().encode({'pin': pin})
        return HttpResponse(response_data, content_type="application/json")
    else:
        sb = get_object_or_404(SecretBook, pk=vb_id)
        tasks.printSecretPdf.delay(sb.id, language, pantry.id, pin)
        response_data = ObjectEncoder().encode({'pin': pin})
        return HttpResponse(response_data, content_type="application/json")


def getMobileSecret(request, secretId, language):
    s = get_object_or_404(Secret, id=secretId)
    selectionMode = 'selection' in request.GET
    is_ios = 'VeggieBook' in request.META.get('HTTP_USER_AGENT', '')

    if language == 'es':
        return render_to_response(
            'secret_mobile_es.html',
            {
                'iidd': secretId,
                'secret': s, 'navOn': True,
                'smode': selectionMode,
                'is_ios': is_ios
            }
        )
    else:
        return render_to_response(
            'secret_mobile_en.html',
            {
                'iidd': secretId,
                'secret': s,
                'navOn': True,
                'smode': selectionMode,
                'is_ios': is_ios
            }
        )


def getSecret(request, secretId, language):
    s = get_object_or_404(Secret, id=secretId)
    selectionMode = 'selection' in request.GET
    if language == 'es':
        return render_to_response('secret_es.html',
                                  {'secrets': [s]})
    else:
        return render_to_response('secrets_vertical_en.html',
                                  {'secrets': [s]})


def createSecretsBook(request):
    return None


def secretsLoading(request, language, category_id):
    return render_to_response('secrets_loading.html',
                              {'category': SecretCategory.objects.get(pk=category_id), 'language': language})


def secrets(request, secretsBookId, language):
    t = 'secrets_vertical_en.html'
    if language == 'es':
        t = 'secrets_vertical_es.html'
    sb = get_object_or_404(SecretBook, pk=secretsBookId)
    my_secrets = [s.secret for s in sb.selections.filter(selected=True)]
    return render_to_response(t, {'secrets': my_secrets})


@csrf_exempt
def pantries(request):
    response_data = ObjectEncoder().encode(builders.LocalPantries().build()["closestPantries"])
    return HttpResponse(response_data, content_type="application/json")


@csrf_exempt
@require_http_methods(["POST"])
def record_event(request):
    json_in = json.loads(request.body)
    record_event_task.delay(**json_in)
    # record_event_task(**json_in)
    return HttpResponse()


def support_page(request):
    return render_to_response('support.html', {})


def privacy_policy(request):
    return render_to_response('privacyPolicy.html', {})
