#!/usr/bin/python3
# -*- coding: utf-8 -*-

#Script téléchargeant des torrents listés dans des flux rss du fichier
#rsslist.txt. il stoke la liste des torrents téléchargés dans downlodedlist.db
#Ce script est fortement inspiré d'un script de maxime niankouri ecrit en perl.
#Copyright Antoine Rabany, Maxime Niankouri

#imports
import feedparser
import shelve
from datetime import date
import requests
import os

#On doit ajouter la ligne suivante dans cron pour executer le script toutes les
#heures : crontab -e
#15 * * * * ~/rsstorrent/rsstorrent.py

def main():
  #On définit la position des fichiers
  curdir = os.path.dirname(__file__)
  downloadedlist = os.path.join(curdir, 'downloadedlist')
  rsslist =os.path.join(curdir, 'rsslist.txt')
  watchfolder="~/torrents/"

  #On regarde tout les flux qui sont dans la liste rrslist
  with open(rsslist,'r') as f:
    for line in f:

      #On récupère le flux
      feed = feedparser.parse(line)

      #Pour chaque entrée du flux rss
      for entry in feed.entries:
        for link in entry.links:
          if link.type == "application/x-bittorrent":
            #On récupère les info qui nous serons utiles.
            url = link.href
            title = entry.title
            filename = entry.torrent_filename
            torrent_hash = entry.torrent_infohash
            print(url)            
            #On ouvre le shelve avec tout ce qu'on a deja telechargé
            #le hash sert de clé
            db = shelve.open(downloadedlist)
            #si le hash n'est pas présent dans la base alors le torrent n'a pas
            #été téléchargé
            if torrent_hash not in db:
              #On télécharge le torrent dans le dossier watchfolder
              os.system("curl -s -g -L --compressed -o " +watchfolder + filename 
                  + " " + url)
              db[torrent_hash]=[title,date.today()]
            db.close()

if __name__ == "__main__":
  main()
