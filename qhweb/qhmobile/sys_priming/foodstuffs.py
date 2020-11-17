#!/usr/bin/python
# -*- coding: utf-8 -*-

from qhmobile.models import *

# foodstuffs 

s=String(en="Broccoli",es="Brócoli")
s.save()
broccoli=FoodStuff(id="BROCCOLI",nameString=s)
broccoli.save()

s=String(en="Cabbage",es="Repollo")
s.save()
cabbage=FoodStuff(id="CABBAGE",nameString=s)
cabbage.save()

s=String(en="Carrrot",es="Zanahoria")
s.save()
carrot=FoodStuff(id="CARROT",nameString=s)
carrot.save()

s=String(en="Cauliflower",es="Coliflor")
s.save()
cauliflower=FoodStuff(id="CAULIFLOWER",nameString=s)
cauliflower.save()

s=String(en="Green Bean",es="Ejote")
s.save()
greenbean=FoodStuff(id="GREENBEAN",nameString=s)
greenbean.save()

s=String(en="Onion",es="Cebolla")
s.save()
onion=FoodStuff(id="ONION",nameString=s)
onion.save()

s=String(en="Potato",es="Papa")
s.save()
potato=FoodStuff(id="POTATO",nameString=s)
potato.save()

s=String(en="Root Vegetable",es="Hortaliza Tipo Raíz")
s.save()
rootvegetable=FoodStuff(id="ROOTVEGETABLE",nameString=s)
rootvegetable.save()

s=String(en="Sweet Potato",es="Camote")
s.save()
sweetpotato=FoodStuff(id="SWEETPOTATO",nameString=s)
sweetpotato.save()

s=String(en="Zucchini",es="Calabacita")
s.save()
zucchini=FoodStuff(id="ZUCCHINI",nameString=s)
zucchini.save()
