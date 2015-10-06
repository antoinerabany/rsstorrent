#!/usr/bin/python3
# -*- coding: utf-8 -*-

#    rsstorrent
#    Copyright (C) 2015 Antoine Rabany, Maxime Niankouri
#
#    This program is free software; you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation; either version 2 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#    You should have received a copy of the GNU General Public License along
#    with this program; if not, write to the Free Software Foundation, Inc.,
#    51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.

#Script téléchargeant des torrents listés dans des flux rss du fichier
#rsslist.txt. il stoke la liste des torrents téléchargés dans downlodedlist.db
#Ce script est fortement inspiré d'un script de maxime niankouri ecrit en perl.

#imports
import feedparser
import shelve
from datetime import date
import requests
import os
from Betapy import Betapy
from Strike import Strike

#On doit ajouter la ligne suivante dans cron pour executer le script toutes les
#heures : crontab -e
#15 * * * * ~/rsstorrent/rsstorrent.py

def main():
    stikeurl = 'https://getstrike.net/api/v2/torrents/';
    feed = feedparser.parse('https://www.betaseries.com/rss/episodes/all/voctro')
    entry = feed.entries[0]
    betapy = Betapy()
    strike = Strike()
    ep = betapy.getEpisodesToDownload()
    hs = strike.listToHash(ep)
    print(hs)
    #il faut ajouter le hash dans un shelve
    #marqué comme téléchargé
    #supprimer le hash


    # search = requests.get(stikeurl +'search',params={'phrase':entry.title, 'category': 'TV'})
    # print(search.json())
    # for entry in feed.entries:
    #     print(entry.title+' season: '+str(season(entry.title)))


#Vikings S03E10 donne 3
def season(title):
    return int(title[-5:-3])


if __name__ == "__main__":
  main()
