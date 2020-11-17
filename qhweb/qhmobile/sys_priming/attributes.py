#!/usr/bin/python
# -*- coding: utf-8 -*-

from qhmobile.models import *


a=Attribute(name="ALL_USERS")
a.save()
o=OrRequirement()
o.save()
o.attributes.add(a)
o.save()


a=Attribute(name="AgreeAsianCooking")
a.save()
asianReq=OrRequirement()
asianReq.save()
asianReq.attributes.add(a)
asianReq.save()

a=Attribute(name="AgreeHispanicCooking")
a.save()
latinoReq=OrRequirement()
latinoReq.save()
latinoReq.attributes.add(a)
latinoReq.save()

a=Attribute(name="AgreeSoulFoodCooking")
a.save()
soulFoodReq=OrRequirement()
soulFoodReq.save()
soulFoodReq.attributes.add(a)
soulFoodReq.save()

a=Attribute(name="AgreeChicken")
a.save()
o=OrRequirement()
o.save()
o.attributes.add(a)
o.save()

a=Attribute(name="AgreeSoup")
a.save()
o=OrRequirement()
o.save()
o.attributes.add(a)
o.save()

a=Attribute(name="HasOven")
a.save()
o=OrRequirement()
o.save()
o.attributes.add(a)
o.save()

a=Attribute(name="HasCrockPot")
a.save()
o=OrRequirement()
o.save()
o.attributes.add(a)
o.save()

a=Attribute(name="HasJuicer")
a.save()
o=OrRequirement()
o.save()
o.attributes.add(a)
o.save()

a=Attribute(name="HasMicrowave")
a.save()
o=OrRequirement()
o.save()
o.attributes.add(a)
o.save()

a=Attribute(name="HasSteamer")
a.save()
o=OrRequirement()
o.save()
o.attributes.add(a)
o.save()

a=Attribute(name="HasBlender")
a.save()
o=OrRequirement()
o.save()
o.attributes.add(a)
o.save()

a=Attribute(name="AgreeKidFriendly")
a.save()
kidFriendlyReq=OrRequirement()
kidFriendlyReq.save()
kidFriendlyReq.attributes.add(a)
kidFriendlyReq.save()

a=Attribute(name="AgreeDiabetes")
a.save()
diabetesReq=OrRequirement()
diabetesReq.save()
diabetesReq.attributes.add(a)
diabetesReq.save()

a=Attribute(name="PrepareSmallFamily")
a.save()
o=OrRequirement()
o.save()
o.attributes.add(a)
o.save()

a=Attribute(name="NutritionChild")
a.save()
o=OrRequirement()
o.save()
o.attributes.add(a)
o.save()

a=Attribute(name="Snacks")
a.save()
o=OrRequirement()
o.save()
o.attributes.add(a)
o.save()

a=Attribute(name="PrepareChild")
a.save()
o=OrRequirement()
o.save()
o.attributes.add(a)
o.save()

a=Attribute(name="NutritionAdultSenior")
a.save()
o=OrRequirement()
o.save()
o.attributes.add(a)
o.save()

a=Attribute(name="Storage")
a.save()
o=OrRequirement()
o.save()
o.attributes.add(a)
o.save()

a=Attribute(name="Freezing")
a.save()
o=OrRequirement()
o.save()
o.attributes.add(a)
o.save()

a=Attribute(name="NutritionGeneral")
a.save()
o=OrRequirement()
o.save()
o.attributes.add(a)
o.save()

a=Attribute(name="Serving")
a.save()
o=OrRequirement()
o.save()
o.attributes.add(a)
o.save()

a=Attribute(name="InterestedInSpoilage")
a.save()
o=OrRequirement()
o.save()
o.attributes.add(a)
o.save()

####
#Annotation
ann = Annotation(displayedIf=asianReq)
ann.save()

ann = Annotation(displayedIf=latinoReq)
ann.save()

ann = Annotation(displayedIf=soulFoodReq)
ann.save()

ann = Annotation(displayedIf=kidFriendlyReq)
ann.save()

ann = Annotation(displayedIf=diabetesReq)
ann.save()



