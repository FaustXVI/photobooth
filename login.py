import urllib.parse
import requests
import logging
import re
import configparser
#import http.client as http_client
#http_client.HTTPConnection.debuglevel = 1
#logging.basicConfig()
#logger = logging.getLogger()
#logger.setLevel(logging.DEBUG)
#logger.propagate = True

config = configparser.ConfigParser()
config.read('config')
config = config['cluster.co']

url = "https://cluster.co/login/"


s = requests.Session()
r = s.get(url)
csrfmiddlewaretoken = re.findall("name=.csrfmiddlewaretoken.+value=[\"'](.*)[\"']",r.text)[0]

login = {
        'email_or_phone' : config['login'],
        'password' : config['password'],
        'csrfmiddlewaretoken' : csrfmiddlewaretoken,
        'redirect' : '/'
        }

headers = {
        'Referer' : url
        }

s.post(url, login, headers = headers)

files = {'upload': open('images/unicorns.jpg', 'rb')}

upload_url = 'https://cluster-blobstoreimages.appspot.com/image_upload'

res_upload = s.post(upload_url, files=files)

upload_id = str(res_upload.json()['uploadId'])

post_url = 'https://cluster.co/__proxy__/cluster'
post = {
        'url':'photos',
        'method':'POST',
        'headers':'Content-Type=application%2Fx-www-form-urlencoded',
        'body': 'cluster_id='+ config['album_id'] + '&gae_upload_id=' + upload_id,
        'csrfToken': s.cookies['csrf_cluster']
        }

r = s.post(post_url,post)

