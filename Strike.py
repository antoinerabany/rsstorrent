import requests
import json

class Strike:
    url = 'https://getstrike.net/api/v2/torrents/'

    def listToHash(self, episodes):
        res = []
        for episode in episodes:
            r = requests.get(self.url + 'search/', params = {'phrase': episode, 'category': 'TV'})
            #r.raise_for_status()
            if (r.status_code == 404):
                print('pas de résultat pour ' + episode)
            else:
                res.append(self.choose(r.json()['torrents'])['torrent_hash'])
        return res

    def choose(self, torrents):
        return torrents[0]
