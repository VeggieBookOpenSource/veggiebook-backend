__author__ = 'danieldipasquo'

from qhmobile.models import Photo, StockPhoto

for photo in Photo.objects.all():
    print photo.jdata()

for photo in StockPhoto.objects.all():
    print photo.jdata()
