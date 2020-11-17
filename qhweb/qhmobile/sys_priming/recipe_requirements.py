from qhmobile import models

RID = 0
AgreeAsianCooking = 2
AgreeHispanicCooking= 3
AgreeSoulFoodCooking= 4
AgreeChicken = 5
AgreeSoup=6
HasCrockPot=7
HasJuicer=8
HasMicrowave=9
HasSteamer=10
AgreeKidFriendly=11

convert = {
    'ZU': 19000,
    'SW': 18000,
    'RV': 17000,
    'PO': 16000,
    'ON': 15000,
    'GB': 14000,
    'CL': 13000,
    'CB': 12000,
    'CA': 11000,
    'BR': 10000,
}


def addAnnotation(recipe, annotationId):
    print '    addAnnotation %s' % annotationId
    orRequirement = models.OrRequirement_Attributes.objects.get(attribute_id=annotationId).orrequirement
    annotation = models.Annotation.objects.get(displayedIf=orRequirement)
    recipe.annotations.add(annotation)
    recipe.save()

def addOrRequirement(recipe, requirementId):
    print '    addRequirement %s' % requirementId
    orRequirement = models.OrRequirement_Attributes.objects.get(attribute_id=requirementId).orrequirement
    recipe.requirements.add(orRequirement)



with open('requirementsAndAnnotations.csv', 'r') as f:
    lines = f.readlines()
    for line in lines:
        attribs =  line.split(',')
        rid_list = attribs[RID].split('-')
        rid = convert[rid_list[0]] + int(rid_list[1])
        try:
            recipe = models.Recipe.objects.get(rid=rid)
            print recipe
            addOrRequirement(recipe, 'ALL_USERS')
            if attribs[AgreeAsianCooking]=='TRUE':
                addAnnotation(recipe, 'AgreeAsianCooking')
            if attribs[AgreeHispanicCooking] == 'TRUE':
                addAnnotation(recipe, 'AgreeHispanicCooking')
            if attribs[AgreeSoulFoodCooking] == 'TRUE':
                addAnnotation(recipe, 'AgreeSoulFoodCooking')
            if attribs[AgreeKidFriendly] == 'TRUE':
                addAnnotation(recipe, 'AgreeKidFriendly')
            if attribs[AgreeChicken] == 'TRUE':
                addOrRequirement(recipe, 'AgreeChicken')
            if attribs[AgreeSoup] == 'TRUE':
                addOrRequirement(recipe, 'AgreeSoup')
            if attribs[HasCrockPot] == 'TRUE':
                addOrRequirement(recipe, 'HasCrockPot')
            if attribs[HasJuicer] == 'TRUE':
                addOrRequirement(recipe, 'HasJuicer')
            if attribs[HasMicrowave] == 'TRUE':
                addOrRequirement(recipe, 'HasMicrowave')
            if attribs[HasSteamer] == 'TRUE':
                addOrRequirement(recipe, 'HasSteamer')

        except:
            print rid





