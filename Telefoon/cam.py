import time
import urllib.request
import requests


base_url = "http://192.168.1.148:80"
picture_url = 'https://images.basishoef.nl'

picture_folder = '/var/www/images.basishoef.nl/public_html'


def take_picture(date):
    capture()
    time.sleep(2.5)
    return picture_url + get_picture(date)


def capture():
    requests.get(base_url + '/capture')


def get_picture(date):
    picture_name = "/picture" + date.replace(' ', '_') + ".jpg"
    server_picture = base_url + '/saved-photo/photo.jpg'
    local_picture = picture_folder + picture_name

    urllib.request.urlretrieve(server_picture, local_picture)
    return picture_name
