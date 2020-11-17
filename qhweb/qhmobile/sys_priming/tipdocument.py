__author__ = 'danieldipasquo'
from lxml import etree
from qhmobile import models

tree = etree.parse('master-4.4.3.xml')
tipTree = tree.find('{http://quickhelp.org/tailor/selector/xmlbean/masterdoc}TipDocument')
sections = tipTree.find('{http://quickhelp.org/tailor/selector/xmlbean/masterdoc}Sections')

fs_count = {}
for section in sections.findall('{http://quickhelp.org/tailor/selector/xmlbean/masterdoc}Section'):
    gate = section.get('Gate')
    print section.get('Id')
    fs = gate.split(' ')[3].strip(':').strip(')')
    if fs not in fs_count:
        fs_count[fs] = 0
    fs_count[fs] += 1

    req = 'ALL_USERS'
    if len(gate.split(' ')) > 8:
        req = section.get('Gate').split(' ')[8].strip(')').strip('$')

    if 'InterestedIn' in req and not 'Spoilage' in req:
        req = req[12:]

    print fs + ' ' + req

    title = section.find('{http://quickhelp.org/tailor/selector/xmlbean/masterdoc}Title')
    title_en = ''
    title_es = ''

    for text in title.findall('{http://quickhelp.org/tailor/selector/xmlbean/masterdoc}Text'):
        print etree.tounicode(text)
        etree.strip_tags(text, 'Font')
        if ':EN' in text.get('Gate'):
            title_en = text.text
        if ':ES' in text.get('Gate'):
            title_es = text.text
    print 'title_en: ' + title_en
    print 'title_es: ' + title_es

    titleString = models.String(en=title_en, es=title_es)
    titleString.save()
    foodStuff = models.FoodStuff.objects.get(id=fs)
    orRequirement = models.OrRequirement.getMatchingOrRequirements([req])[0].orrequirement

    fsIndex = fs_count[fs] * 100
    foodTip = models.FoodTip(heading=titleString, foodStuff=foodStuff, requirement=orRequirement,
                             fsIndex=fsIndex)
    foodTip.save()

    c = 0
    for tip in section.findall('{http://quickhelp.org/tailor/selector/xmlbean/masterdoc}Tip'):
        c += 1
        tip_en = ''
        tip_es = ''
        for text in tip.findall('{http://quickhelp.org/tailor/selector/xmlbean/masterdoc}Text'):
            print etree.tounicode(text)
            etree.strip_tags(text, '{http://quickhelp.org/tailor/selector/xmlbean/masterdoc}Font')
            print etree.tounicode(text)

            if ':EN' in text.get('Gate'):
                tip_en = text.text
            if ':ES' in text.get('Gate'):
                tip_es = text.text
        print "tip_en: " + tip_en
        print "tip_es: " + tip_es
        tipString = models.String(en=tip_en, es=tip_es)
        tipString.save()
        ns = dict(n='http://quickhelp.org/tailor/selector/xmlbean/masterdoc')
        pic = tip.find('n:Illustrations/n:Illustration/n:Image/n:Source', namespaces=ns)
        photo = None
        if pic:
            picPath = 'img' + pic.findall('n:Eval', namespaces=ns)[1].tail
            print picPath
            photo = models.Photo(img=picPath)
            photo.save()

        orderableTip = models.OrderableTip(tipId=foodTip, content=tipString, position=c, photo=photo)
        orderableTip.save()




