#!/usr/bin/python
# -*- coding: utf-8 -*-

from qhmobile.models import *


i201 = String(en='''I want recipes for %s that use..''',es="NEEDS TRANSLATION", needsTranslation=True)
i201.save()
i201sub = String(en="select all appliances that apply")
i201sub.save()
q201 = Question(mnemonic='''PREPEQUIP''',phase='I',intro=i201,qtype='M',subIntro=i201sub,orderPriority=100)
q201.save()


s20101 = String(en='''Microwave''',es='NEEDS TRANSLATION')
s20101.save()
c20101 = QuestionChoice(content=s20101,questionId=q201,attribute=Attribute.objects.get(name="HasMicrowave"))
c20101.save()
s20102 = String(en='''Crock Pot''',es='NEEDS TRANSLATION')
s20102.save()
c20102 = QuestionChoice(content=s20102,questionId=q201,attribute=Attribute.objects.get(name="HasCrockPot"))
c20102.save()
s20103 = String(en='''Juicer''',es='NEEDS TRANSLATION')
s20103.save()
c20103 = QuestionChoice(content=s20103,questionId=q201,attribute=Attribute.objects.get(name="HasJuicer"))
c20103.save()
s20104 = String(en='''Oven or Toaster Oven''',es='NEEDS TRANSLATION')
s20104.save()
c20104 = QuestionChoice(content=s20104,questionId=q201,attribute=Attribute.objects.get(name="HasOven"))
c20104.save()
s20105 = String(en='''Steamer''',es='NEEDS TRANSLATION')
s20105.save()
c20105 = QuestionChoice(content=s20105,questionId=q201,attribute=Attribute.objects.get(name="HasSteamer"))
c20105.save()
s20106 = String(en='''Blender or Food Processor''',es='NEEDS TRANSLATION')
s20106.save()
c20106 = QuestionChoice(content=s20106,questionId=q201,attribute=Attribute.objects.get(name="HasBlender"))
c20106.save()


i202 = String(en="I want recipes ...",es="NEEDS TRANSLATION")
i202.save()
i202sub = String(en="select all that apply")
i202sub.save()

q202 = Question(mnemonic='''RECIPESUBTYPES''',phase='I',intro=i202,qtype='M',subIntro=i202sub,orderPriority=200)
q202.save()
s20201 = String(en='''Children 9-14 would enjoy''',es='NEEDS TRANSLATION')
s20201.save()
c20201 = QuestionChoice(content=s20201,questionId=q202,attribute=Attribute.objects.get(name="AgreeKidFriendly"))
c20201.save()
s20202 = String(en='''Combining %s with chicken or meat''',es='NEEDS TRANSLATION')
s20202.save()
c20202 = QuestionChoice(content=s20202,questionId=q202,attribute=Attribute.objects.get(name="AgreeChicken"))
c20202.save()
s20203 = String(en='''For soup containing %s''',es='NEEDS TRANSLATION')
s20203.save()
c20203 = QuestionChoice(content=s20203,questionId=q202,attribute=Attribute.objects.get(name="AgreeSoup"))
c20203.save()

s20204 = String(en='''With Hispanic Flavors''',es='NEEDS TRANSLATION')
s20204.save()
c20204 = QuestionChoice(content=s20204,questionId=q202,attribute=Attribute.objects.get(name="AgreeHispanicCooking"))
c20204.save()
s20205 = String(en='''With Asian Flavors''',es='NEEDS TRANSLATION')
s20205.save()
c20205 = QuestionChoice(content=s20205,questionId=q202,attribute=Attribute.objects.get(name="AgreeAsianCooking"))
c20205.save()
s20206 = String(en='''With Soul Food or African-American Cooking''',es='NEEDS TRANSLATION')
s20206.save()
c20206 = QuestionChoice(content=s20206,questionId=q202,attribute=Attribute.objects.get(name="AgreeSoulFoodCooking"))
c20206.save()

i203 = String(en="I want information on..",es="NEEDS TRANSLATION")
i203.save()
q203 = Question(mnemonic='''INFOSUBTYPES''',phase='I',intro=i203,qtype='Z',subIntro=i202sub,orderPriority=400)
q203.save()

s20307 = String(en='''Making snacks with %s''',es='NEEDS TRANSLATION')
s20307.save()
c20307 = QuestionChoice(content=s20307,questionId=q203,attribute=Attribute.objects.get(name="Snacks"))
c20307.save()
s20301 = String(en='''Preparing %s for one or two people''',es='NEEDS TRANSLATION')
s20301.save()
c20301 = QuestionChoice(content=s20301,questionId=q203,attribute=Attribute.objects.get(name="PrepareSmallFamily"))
c20301.save()
s20302 = String(en='''Making baby food with %s for babies six months or older''',es='NEEDS TRANSLATION')
s20302.save()
c20302 = QuestionChoice(content=s20302,questionId=q203,attribute=Attribute.objects.get(name="PrepareChild"))
c20302.save()
s20306 = String(en='''Preparing %s for someone with diabetes''',es='NEEDS TRANSLATION')
s20306.save()
c20306 = QuestionChoice(content=s20306,questionId=q203,attribute=Attribute.objects.get(name="AgreeDiabetes"))
c20306.save()


i203 = String(en="Provide nutritional tips ..",es="NEEDS TRANSLATION")
i203.save()
q203 = Question(mnemonic='''NUTRITION''',phase='I',intro=i203,qtype='Z',subIntro=i202sub,orderPriority=500)
q203.save()

s20303 = String(en='''For %s''',es='NEEDS TRANSLATION')
s20303.save()
c20303 = QuestionChoice(content=s20303,questionId=q203,attribute=Attribute.objects.get(name="NutritionGeneral"))
c20303.save()
s20304 = String(en='''For children under 16 ''',es='NEEDS TRANSLATION')
s20304.save()
c20304 = QuestionChoice(content=s20304,questionId=q203,attribute=Attribute.objects.get(name="NutritionChild"))
c20304.save()
s20305 = String(en='''For adults and seniors''',es='NEEDS TRANSLATION')
s20305.save()
c20305 = QuestionChoice(content=s20305,questionId=q203,attribute=Attribute.objects.get(name="NutritionAdultSenior"))
c20305.save()


i204 = String(en="I would like suggestions on...",es="NEEDS TRANSLATION")
i204.save()
q204 = Question(mnemonic='''SUGGESTSUBTYPES''',phase='I',intro=i204,qtype='Z',subIntro=i202sub,orderPriority=600)
q204.save()

s20401 = String(en='''Storing %s''',es='NEEDS TRANSLATION')
s20401.save()
c20401 = QuestionChoice(content=s20401,questionId=q204,attribute=Attribute.objects.get(name="Storage"))
c20401.save()
s20402 = String(en='''Freezing %s''',es='NEEDS TRANSLATION')
s20402.save()
c20402 = QuestionChoice(content=s20402,questionId=q204,attribute=Attribute.objects.get(name="Freezing"))
c20402.save()
s20403 = String(en='''Preventing spoilage of %s''',es='NEEDS TRANSLATION')
s20403.save()
c20403 = QuestionChoice(content=s20403,questionId=q204,attribute=Attribute.objects.get(name="InterestedInSpoilage"))
c20403.save()

i205 =String(en="hidden",es="hidden")
i205.save()
q205 = Question(mnemonic='''HIDDEN''',phase='I',intro=i205,qtype='H',orderPriority=10)
q205.save()

c20501 = QuestionChoice(content=i205,questionId=q205,attribute=Attribute.objects.get(name="ALL_USERS"),firstDefault=True)
c20501.save()