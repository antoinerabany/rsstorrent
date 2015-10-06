#!/usr/bin/python3
# -*- coding: utf-8 -*-
import requests
import hashlib
import getpass
import json

class Betapy:
    url = 'https://api.betaseries.com/'

    def __init__(self):
        self.headers = {'X-BetaSeries-Version': '2.4'}
        with open('parameters.json', 'r') as f:
            params = json.load(f)
            self.headers['X-BetaSeries-Key'] = params['betaseries']['api_key']
        with open('token.json', 'r') as f:
            token = json.load(f)
            if('token' in token):
                self.setToken(token['token'])
        self.episodes = None

    def auth(self):
        login = 'voctro'#input('Entrez votre login:')
        password = 'UF5AebyklC:g"aWy1KGl'.encode('utf-8') #getpass.getpass('Entrez votre mot de passe:').encode('utf-8')
        response = requests.post(self.url+'members/auth',
            data = {'login': login, 'password': hashlib.md5(password).hexdigest()},
            headers = self.headers
        )
        if(response.status_code == requests.codes.ok):
            self.setToken(response.json()['token'])
            with open('token.json', 'w') as f:
                json.dump({'token': self.getToken()}, f)
        elif(response.status_code == 400):
            print('Mauvais mot de passe')
            self.auth()
        else:
            reponse.raise_for_status()


    def getEpisodes(self, limit = 5):
        if self.episodes is None:
            self.verifyToken()
            r = requests.get(self.url + 'episodes/list', params = {'limit': limit}, headers = self.headers)
            self.episodes = r.json()['shows']
        return self.episodes

    def getEpisodesToDownload(self):
        ret = []
        self.getEpisodes()
        for show in self.episodes:
            for episode in show['unseen']:
                if not episode['user']['downloaded']:
                    ret.append(episode['show']['title'] + ' ' + episode['code'])
        return ret


    def setToken(self, token):
        self.headers['X-BetaSeries-Token'] = token

    def getToken(self):
        return self.headers['X-BetaSeries-Token']

    def hasToken(self):
        return 'X-BetaSeries-Token' in self.headers

    def verifyToken(self):
        if not self.hasToken():
            print('Vous devez vous connecter.')
            self.auth()
        else:
            print('Vous etes deja connecté.')
        print('Vous etes bien connecté avec pour token : ' + self.getToken())
