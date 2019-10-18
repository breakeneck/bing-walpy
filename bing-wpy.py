import requests
import json
import os
from ksetwallpaper import setwallpaper

dir_path = os.path.dirname(os.path.realpath(__file__))

BASE_URL = 'https://www.bing.com/'
URL = BASE_URL + 'HPImageArchive.aspx?format=js&idx=0&n=1&mkt=en-US'
CACHE_FILENAME = dir_path + '/cached.json'

cached_image = ''

def get_wallpaper_filename(image):
    return dir_path + '/' + image['hsh'] + '.jpg'


def print_command_output(data):
    print(data['title'] + "<br>" + data['copyright'])


def load_cached_image():
    if os.path.isfile(CACHE_FILENAME):
        with open(CACHE_FILENAME) as json_file:
            return json.load(json_file)


def cache_image(data):
    with open(CACHE_FILENAME, 'w') as outfile:
        json.dump(data, outfile)


def save_wallpaper(image):
    response = requests.get(BASE_URL + image['url'])
    with open(get_wallpaper_filename(image), 'wb') as f:
        f.write(response.content)


image = []
try:
    cached_image = load_cached_image()
    image = requests.get(URL).json()['images'][0]
except:
    if cached_image:
        print_command_output(cached_image)

if cached_image != image:
    cache_image(image)
    save_wallpaper(image)
    setwallpaper(get_wallpaper_filename(image))


print_command_output(image)
