import requests
import re

url = "https://cluster.co/login/"
upload_url = 'https://cluster-blobstoreimages.appspot.com/image_upload'
post_url = 'https://cluster.co/__proxy__/cluster'


class Cluster:
    def __init__(self, config):
        self.album_id = config['album_id']
        self.s = requests.Session()

    def upload(self, images):
        try:
            r = self.s.get(url)
            csrfmiddlewaretoken = re.findall("name=.csrfmiddlewaretoken.+value=[\"'](.*)[\"']", r.text)[0]
            login = {
                'email_or_phone': config['login'],
                'password': config['password'],
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
            return False
