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

from django import forms
from django.contrib.admin.util import unquote
from django.db import transaction
from django.http import HttpResponse
from easy_maps.widgets import AddressWithMapWidget
from qhmobile.models import *
from django.contrib import admin
from imagekit.admin import AdminThumbnail
from django.utils.html import escape, escapejs
from django.contrib.admin import widgets, helpers
from django.contrib.admin.options import get_ul_class, csrf_protect_m
from django.utils.translation import ugettext as _
from django.contrib.auth.admin import UserAdmin

from django.conf import settings
from django.contrib.admin.widgets import RelatedFieldWidgetWrapper
from django.core.urlresolvers import reverse
from django.template.loader import render_to_string
from django.utils.safestring import mark_safe
from django.forms.widgets import SelectMultiple


class UserProfileInline(admin.StackedInline):
    model = UserProfile
    readonly_fields = ('deviceId', )
    can_delete = False


class UserProfileAdmin(admin.ModelAdmin):
    inlines = [UserProfileInline, ]
    list_display = UserAdmin.list_display + ('device_id', )
    search_fields = UserAdmin.search_fields + ('userprofile__deviceId', )

    def device_id(self, obj):
        return obj.userprofile.deviceId if hasattr(obj, 'userprofile') else None

    device_id.short_description = 'Device ID'


# Register the user with the added device ID field.
admin.site.unregister(User)
admin.site.register(User, UserProfileAdmin)


class RelatedFieldWidgetWrapper(RelatedFieldWidgetWrapper):
    class Media:
        js = ("%srelatedwidget/js/relatedwidget.js?v=2" % settings.STATIC_URL,)

    def __init__(self, *args, **kwargs):
        self.can_change_related = kwargs.pop('can_change_related', None)
        self.can_delete_related = kwargs.pop('can_delete_related', None)
        super(RelatedFieldWidgetWrapper, self).__init__(*args, **kwargs)

    @classmethod
    def from_contrib_wrapper(cls, wrapper, can_change_related, can_delete_related):
        return cls(wrapper.widget, wrapper.rel, wrapper.admin_site,
                   can_add_related=wrapper.can_add_related,
                   can_change_related=can_change_related,
                   can_delete_related=can_delete_related)

    def get_related_url(self, rel_to, info, action, args=[]):
        return reverse("admin:%s_%s_%s" % (info + (action,)), current_app=self.admin_site.name, args=args)

    def render(self, name, value, attrs={}, *args, **kwargs):
        rel_to = self.rel.to
        info = (rel_to._meta.app_label, rel_to._meta.object_name.lower())
        self.widget.choices = self.choices
        attrs['class'] = ' '.join((attrs.get('class', ''), 'related-widget-wrapper'))
        context = {'widget': self.widget.render(name, value, attrs, *args, **kwargs),
                   'name': name,
                   'STATIC_URL': settings.STATIC_URL,
                   'can_change_related': self.can_change_related,
                   'can_add_related': self.can_add_related,
                   'can_delete_related': False}
        if self.can_change_related:
            if value:
                context['change_url'] = self.get_related_url(rel_to, info, 'change', [value])
            template = self.get_related_url(rel_to, info, 'change', ['%s'])
            context.update({
                'change_url_template': template,
                'change_help_text': _('Change related model')
            })
        if self.can_add_related:
            context.update({
                'add_url': self.get_related_url(rel_to, info, 'add'),
                'add_help_text': _('Add Another')
            })
        if self.can_delete_related:
            if value:
                context['delete_url'] = self.get_related_url(rel_to, info, 'delete', [value])
            template = self.get_related_url(rel_to, info, 'delete', ['%s'])
            context.update({
                'delete_url_template': template,
                'delete_help_text': _('Delete related model')
            })

        return mark_safe(render_to_string('relatedwidget/widget.html', context))


class RelatedWidgetWrapperBase(object):
    def formfield_for_dbfield(self, db_field, **kwargs):
        formfield = super(RelatedWidgetWrapperBase, self).formfield_for_dbfield(db_field, **kwargs)
        if (formfield and
                isinstance(formfield.widget, admin.widgets.RelatedFieldWidgetWrapper) and
                not isinstance(formfield.widget.widget, SelectMultiple)):
            request = kwargs.pop('request', None)
            related_modeladmin = self.admin_site._registry.get(db_field.rel.to)
            can_change_related = bool(related_modeladmin and
                                      related_modeladmin.has_change_permission(request))
            can_delete_related = bool(related_modeladmin and
                                      related_modeladmin.has_delete_permission(request))
            widget = RelatedFieldWidgetWrapper.from_contrib_wrapper(formfield.widget,
                                                                    can_change_related,
                                                                    can_delete_related)
            formfield.widget = widget
        return formfield

    def response_change(self, request, obj):
        if '_popup' in request.REQUEST:
            pk_value = obj._get_pk_val()
            return HttpResponse(
                '<script type="text/javascript">opener.dismissEditRelatedPopup(window, "%s", "%s");</script>' % \
                    # escape() calls force_unicode.
                (escape(pk_value), escapejs(obj)))
        else:
            return super(RelatedWidgetWrapperBase, self).response_change(request, obj)


class FastStringBase(object):
    def formfield_for_foreignkey(self, db_field, request=None, **kwargs):
        """
        Get a form Field for a ForeignKey.
        """
        db = kwargs.get('using')

        if db_field.name in self.raw_id_fields:
            kwargs['widget'] = widgets.ForeignKeyRawIdWidget(db_field.rel,
                                                             self.admin_site, using=db)
        elif db_field.name in self.radio_fields:
            kwargs['widget'] = widgets.AdminRadioSelect(attrs={
                'class': get_ul_class(self.radio_fields[db_field.name]),
            })
            kwargs['empty_label'] = db_field.blank and _('None') or None

        if db_field.rel.to._meta.object_name == 'String':
            kwargs['widget'] = widgets.ForeignKeyRawIdWidget(db_field.rel,
                                                             self.admin_site, using=db)

        return db_field.formfield(**kwargs)


class FastStringAdmin(FastStringBase, admin.ModelAdmin):
    pass
    # #Override view for changing a value
    #
    # @csrf_protect_m
    # def change_view(self, request, object_id, form_url='', extra_context=None):
    #     """The 'change' admin view for this model."""
    #     obj = self.get_object(request, unquote(object_id))
    #     pk_value = obj._get_pk_val()
    #
    #     if request.method == 'POST' and "_popup" in request.POST:
    #         return HttpResponse(
    #             '<!DOCTYPE html><html><head><title></title></head><body>'
    #             '<script type="text/javascript">opener.dismissEditRelatedPopup(window, "%s", "%s");</script></body></html>' % \
    #                 # escape() calls force_unicode.
    #             (escape(pk_value), escapejs(obj)))
    #     return super(FastStringAdmin, self).change_view(request, object_id, form_url, extra_context)


class FastStringInline(FastStringBase, admin.TabularInline):
    pass


class IngredientsInline(FastStringInline, RelatedWidgetWrapperBase, admin.TabularInline):
    model = RecipeIngredient
    fields = ('position', 'content')
    extra = 0


class StepsInline(FastStringInline, RelatedWidgetWrapperBase, admin.TabularInline):
    model = RecipeStep
    fields = ('position', 'content')

    extra = 0


class NotesInline(FastStringInline, RelatedWidgetWrapperBase, admin.TabularInline):
    model = RecipeNote
    fields = ('position', 'content')

    extra = 0


class PhotosInLine(RelatedWidgetWrapperBase, admin.TabularInline):
    model = RecipePhoto
    extra = 0


class RecipeAdmin(FastStringAdmin, RelatedWidgetWrapperBase, admin.ModelAdmin):
    inlines = [PhotosInLine, IngredientsInline, StepsInline, NotesInline]
    search_fields = ['title__en', 'title__es', 'recipeId']
    list_select_related = True
    save_on_top = True
    list_display = ('recipeId', 'title', 'preview_en', 'preview_es', 'preview_mobile_en', 'preview_mobile_es',)
    list_display_links = ('recipeId', 'title',)
    list_filter = ('isActive', 'foodStuff',)
    filter_horizontal = ('requirements', 'annotations',)

    def preview_en(self, obj):
        return '<a href="preview/%s/en/">English</a>' % obj.recipeId

    def preview_es(self, obj):
        return '<a href="preview/%s/es/">Spanish</a>' % obj.recipeId

    def preview_mobile_en(self, obj):
        return '<a href="mobilePreview/en/%s/">Mobile En</a>' % obj.recipeId

    def preview_mobile_es(self, obj):
        return '<a href="mobilePreview/es/%s/">Mobile Es</a>' % obj.recipeId


    preview_en.short_description = "Preview En"
    preview_en.allow_tags = True

    preview_es.short_description = "Preview Es"
    preview_es.allow_tags = True

    preview_mobile_en.short_description = "Preview Es"
    preview_mobile_en.allow_tags = True

    preview_mobile_es.short_description = "Preview Es"
    preview_mobile_es.allow_tags = True


admin.site.register(Recipe, RecipeAdmin)


class SecretCategoryAdmin(FastStringAdmin, RelatedWidgetWrapperBase, admin.ModelAdmin):
    list_display = ('title', 'thumbnail', 'positionIndex',)
    list_editable = ('positionIndex',)
    list_display_links = ('title',)

    _thumbnail = AdminThumbnail(image_field='img200')

    def thumbnail(self, obj):
        return '' if obj.image is None else self._thumbnail.__call__(obj)

    thumbnail.short_description = "Image"
    thumbnail.allow_tags = True


admin.site.register(SecretCategory, SecretCategoryAdmin)


class ExternalLinkInline(FastStringInline, RelatedWidgetWrapperBase, admin.TabularInline):
    model = ExternalLink
    extra = 0


class SecretAdmin(FastStringAdmin, RelatedWidgetWrapperBase, admin.ModelAdmin):
    list_select_related = True
    save_on_top = True
    list_display = ('title', 'secret', 'whyItWorks', 'preview_en', 'preview_es', 'thumbnail')
    search_fields = ['title__en', 'title__es', 'secret__en', 'secret__es']
    list_filter = ('category',)
    exclude = ('coverImage', 'coverImage_es')
    inlines = [ExternalLinkInline]

    _thumbnail = AdminThumbnail(image_field='img300')

    def thumbnail(self, obj):
        return '' if obj.image is None else self._thumbnail.__call__(obj)

    thumbnail.short_description = "Image"
    thumbnail.allow_tags = True

    def preview_en(self, obj):
        return "<a href='/qhmobile/mobileSecret/en/%d/'> Preview English</a>" % obj.id

    def preview_es(self, obj):
        return "<a href='/qhmobile/mobileSecret/es/%d/'> Preview Spanish</a>" % obj.id



    preview_en.short_description = "Preview En"
    preview_en.allow_tags = True

    preview_es.short_description = "Preview Es"
    preview_es.allow_tags = True



admin.site.register(Secret, SecretAdmin)


class StringAdmin(admin.ModelAdmin):
    list_display = ('id', 'en', 'es', 'needsTranslation')
    search_fields = ['en', 'es']
    list_editable = ('en', 'es', 'needsTranslation')
    list_display_links = ('id',)
    list_filter = ('needsTranslation',)
    save_on_top = True

    def response_change(self, request, obj):
        if '_popup' in request.REQUEST:
            pk_value = obj._get_pk_val()
            return HttpResponse(
                '<!DOCTYPE html><html><head><title></title></head><body>'
                '<script>opener.dismissEditRelatedPopup(window, "%s", "%s");</script></body></html>' % \
                (escape(pk_value), escapejs(obj)))
        else:
            return super(StringAdmin, self).response_change(request, obj)


admin.site.register(String, StringAdmin)


class OrRequiremntAdmin(admin.ModelAdmin):
    filter_horizontal = ('attributes', )


admin.site.register(OrRequirement, OrRequiremntAdmin)


class BookSubjectAdmin(RelatedWidgetWrapperBase, admin.ModelAdmin):
    list_display = ('id', 'thumbnail',)
    actions = ['really_delete_selected']

    def get_actions(self, request):
        actions = super(BookSubjectAdmin, self).get_actions(request)
        del actions['delete_selected']
        return actions

    def really_delete_selected(self, request, queryset):
        for obj in queryset:
            obj.delete()

        if queryset.count() == 1:
            message_bit = "1 entry was"
        else:
            message_bit = "%s entries were" % queryset.count()
        self.message_user(request, "%s successfully deleted." % message_bit)

    really_delete_selected.short_description = "Delete selected entries"

    def req_display(self, obj):
        return obj.displayedIf.__unicode__()

    _thumbnail = AdminThumbnail(image_field='img200')

    def thumbnail(self, obj):
        return '' if obj.image is None else self._thumbnail.__call__(obj.image)

    thumbnail.allow_tags = True


admin.site.register(FoodStuff, BookSubjectAdmin)
admin.site.register(TipDoc, BookSubjectAdmin)
admin.site.register(Attribute)


class PhotoAdmin(admin.ModelAdmin):
    list_display = ('img', 'thumbnail',)
    thumbnail = AdminThumbnail(image_field='img100')


admin.site.register(Photo, PhotoAdmin)
admin.site.register(StockPhoto, PhotoAdmin)


class RecipeIngredientAdmin(RelatedWidgetWrapperBase, admin.ModelAdmin):
    raw_id_fields = ("recipeId",)
    list_display = ('recipeId', 'content', 'position',)
    ordering = ['recipeId', 'position', 'id']


admin.site.register(RecipeIngredient, RecipeIngredientAdmin)


class RecipeStepAdmin(RelatedWidgetWrapperBase, admin.ModelAdmin):
    raw_id_fields = ("recipeId",)
    list_display = ('recipeId', 'content', 'position',)
    ordering = ['recipeId', 'position', 'id']


admin.site.register(RecipeStep, RecipeStepAdmin)


class AnnotationAdmin(RelatedWidgetWrapperBase, admin.ModelAdmin):
    list_display = ('req_display', 'en_thumbnail', 'es_thumbnail')

    def req_display(self, obj):
        return obj.displayedIf.__unicode__()

    _thumbnail = AdminThumbnail(image_field='img200')

    def en_thumbnail(self, obj):
        return '' if obj.en_img is None else self._thumbnail.__call__(obj.en_img)

    def es_thumbnail(self, obj):
        return '' if obj.es_img is None else self._thumbnail.__call__(obj.es_img)

    en_thumbnail.allow_tags = True
    es_thumbnail.allow_tags = True


admin.site.register(Annotation, AnnotationAdmin)


class ChoicesInline(RelatedWidgetWrapperBase, admin.TabularInline):
    model = QuestionChoice
    extra = 0


class QuestionAdmin(RelatedWidgetWrapperBase, admin.ModelAdmin):
    inlines = [ChoicesInline]


class LibraryAdmin(admin.ModelAdmin):
    list_display = ('version',)


class QuestionChoiceAdmin(FastStringAdmin, RelatedWidgetWrapperBase, admin.ModelAdmin):
    list_display = ('content', 'attribute',)


admin.site.register(Question, QuestionAdmin)
admin.site.register(QuestionChoice, QuestionChoiceAdmin)
admin.site.register(LibraryData, LibraryAdmin)


class OrderableTipInline(FastStringInline, RelatedWidgetWrapperBase, admin.TabularInline):
    model = OrderableTip
    fields = ('position', 'content', 'photo',)
    extra = 0


class FoodTipAdmin(FastStringAdmin, RelatedWidgetWrapperBase, admin.ModelAdmin):
    inlines = [OrderableTipInline]
    list_filter = ('foodStuff',)


admin.site.register(OrderableTip)
admin.site.register(FoodTip, FoodTipAdmin)


class CoverPhotoAdmin(admin.ModelAdmin):
    list_display = ('id', 'img', 'thumbnail', 'order')
    list_editable = ('order', )
    list_display_links = ('img', )
    list_filter = ('owner',)
    raw_id_fields = ('owner',)
    thumbnail = AdminThumbnail(image_field='img100')

admin.site.register(CoverPhoto, CoverPhotoAdmin)


class RecipeBookAdmin(admin.ModelAdmin):
    list_display = ('id', 'createdAt', 'foodStuff', 'user', 'pdfLink_en', 'pdfLink_es', 'latitude', 'longitude')
    search_fields = ('user__email',)
    readonly_fields = ('user', 'attributes', 'selections', 'coverPhoto', 'pantry', 'createdAt', 'foodStuff',
                       'latitude', 'longitude',)


    def pdfLink_en(self, obj):
        return '<a href="/qhmobile/veggieBookPdf/en/%s/">Pdf En</a>' % obj.id

    pdfLink_en.allow_tags = True
    pdfLink_en.short_description = "Pdf Es"

    def webPreview_en(self, obj):
        return '<a href="/qhmobile/veggieBook/%s/">Preview En</a>' % obj.id

    webPreview_en.allow_tags = True
    webPreview_en.short_description = "Web Preview"

    def pdfLink_es(self, obj):
        return '<a href="/qhmobile/veggieBookPdf/es/%s/">Pdf Es</a>' % obj.id

    pdfLink_es.allow_tags = True
    pdfLink_es.short_description = "Pdf Es"

admin.site.register(RecipeBook, RecipeBookAdmin)


class SecretBookAdmin(admin.ModelAdmin):
    list_display = ('id', 'createdAt', 'category', 'user',  'pdfLink_en', 'pdfLink_es', 'latitude', 'longitude')
    search_fields = ('user__email',)

    def pdfLink_en(self, obj):
        return '<a href="/qhmobile/secretsBookPdf/en/%s/">Pdf En</a>' % obj.id

    pdfLink_en.allow_tags = True
    pdfLink_en.short_description = "Pdf Es"


    def pdfLink_es(self, obj):
        return '<a href="/qhmobile/secretsBookPdf/es/%s/">Pdf Es</a>' % obj.id

    pdfLink_es.allow_tags = True
    pdfLink_es.short_description = "Pdf Es"


admin.site.register(SecretBook, SecretBookAdmin)


class FoodPantryAdmin(admin.ModelAdmin):
    list_display = ('name', 'address')
    class form(forms.ModelForm):
        class Meta:
            widgets = {
                'address': AddressWithMapWidget({'class': 'vTextField'})
            }

admin.site.register(FoodPantry, FoodPantryAdmin)


class ViewDataAdmin(admin.ModelAdmin):
    list_display = ('type', 'event', 'user', 'book_id', 'recipe', 'secret', 'timeStamp', 'data', 'recipeBook', 'secretBook', )
    search_fields = ('user__email',)


admin.site.register(ViewingData, ViewDataAdmin)