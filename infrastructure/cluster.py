import requests
import re
import sys
import traceback

url = "https://cluster.co/login/"
upload_url = 'https://cluster-blobstoreimages.appspot.com/image_upload'
post_url = 'https://cluster.co/__proxy__/cluster'


class Cluster:
    def __init__(self, config):
        self.album_id = config['album_id']
        self.login = config['login']
        self.password = config['password']
        self.s = requests.Session()

    def upload(self, images):
        try:
            if len(self.s.cookies) == 0:
                r = self.s.get(url)
                csrfmiddlewaretoken = re.findall("name=.csrfmiddlewaretoken.+value=[\"'](.*)[\"']", r.text)[0]
                login = {
                    'email_or_phone': self.login,
                    'password': self.password,
                    'csrfmiddlewaretoken': csrfmiddlewaretoken,
                    'redirect': '/'
                }
                self.s.post(url, login, headers={'Referer': url})
            for image in images:
                files = {'upload': open(image, 'rb')}
                res_upload = self.s.post(upload_url, files=files)
                upload_id = str(res_upload.json()['uploadId'])
                post = {
                    'url': 'photos',
                    'method': 'POST',
                    'headers': 'Content-Type=application%2Fx-www-form-urlencoded',
                    'body': 'cluster_id=' + self.album_id + '&gae_upload_id=' + upload_id,
                    'csrfToken': self.s.cookies['csrf_cluster']
                }
                self.s.post(post_url, post)
            return True
        except:
            print("Cluster crash")
            traceback.print_exc()
            return False
