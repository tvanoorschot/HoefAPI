import time
import urllib.request
import requests


base_url = "http://192.168.1.148:80"
picture_url = 'https://images.basishoef.nl'

picture_folder = '/var/www/images.basishoef.nl/public_html'


def take_picture(date):
    try:
        capture()
        return get_picture(date)
    except requests.exceptions.ConnectionError:
        return picture_url + "/no_cam.jpg"


def capture():
    requests.get(base_url + '/capture')
    time.sleep(1)
    while True:
        if requests.get(base_url + '/check').text == 'false':
            break
        time.sleep(0.2)


def get_picture(date):
    picture_name = "/picture" + date.replace(' ', '_') + ".jpg"
    server_picture = base_url + '/saved-photo/photo.jpg'
    local_picture = picture_folder + picture_name

    urllib.request.urlretrieve(server_picture, local_picture)
    return picture_url + picture_name
