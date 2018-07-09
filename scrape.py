# purpose of this module is to use
# python technologies to scrape player
# data from bbref, and eventually store it
# in some datastore (maybe PostgreSQL)
import requests
import os
from bs4 import BeautifulSoup
import pandas as pd

# pre: needs list of features which are to be selected from stat table
# and name of player for which data is being scraped
# post: returns statistical data for given player
base_url = 'https://www.basketball-reference.com/players/'
important_stats = ["age", "g", "gs", "mp_per_g"]
alphabet = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']
def scrape_stats(req, playerSoup, features):
    # parse page data with BeautifulSoup
    # use CSS selectors to get appropriate elements from table
    # get the stats table for all career per_game stats
    # 25 stats per row
    all_stats = []
    # get stats for each provided stat in the features param
    for feature in features:
        per_game_stats = playerSoup.select('#all_per_game tr.full_table > td[data-stat="' + feature + '"]')
        stat_text = []
        # get text values for stats and append list to list of lists all_stats
        for stat in per_game_stats:
            if len(stat.getText()) > 0:
                stat_text.append(stat.getText())
        all_stats.append(stat_text)
    return all_stats

def get_seasons(req, playerSoup):
    seasons = []
    all_seasons = playerSoup.select('#all_per_game th.left a')
    for season in all_seasons:
        seasons.append(season.getText())
    return seasons

def makeAllPlayerReq():
    # list of all NBA players
    allPlayers = []
#    for letter in alphabet:
#        # make request for current letter
#        req = requests.get(base_url + letter)
#        try:
#            req.raise_for_status()
#        except Exception as exc:
#            print('There was a problem: %s' % (exc))
#        playerSoup = BeautifulSoup(req.text, "html.parser")
        # select tags with player names
#        players = playerSoup.select('th.left a')
        # add all player names to list
#        for player in players:
#            allPlayers.append(player.getText())
#    return allPlayers

def makePlayerReq(name):
    name = name.lower().split(',')
    endpoint = name[0][0:1] + '/' + name[0][0:5] + name[1][0:2]
    print(endpoint)
    req = requests.get(base_url + endpoint + '01.html')
    try:
        req.raise_for_status()
    except Exception as exc:
        print('There was a problem: %s' % (exc))
    playerSoup = BeautifulSoup(req.text, "html.parser")
    return req, playerSoup

def writePlayersToFile(all_players):
    if not os.path.isfile(os.path.join(os.getcwd(), "players.txt")):
        file = open(os.path.join(os.getcwd(), "players.txt"), "w+")
        for player in all_players:
            malformed = False
            req, playerSoup = makePlayerReq(player)
            years = get_seasons(req, playerSoup)
            stats = (scrape_stats(req, playerSoup, important_stats))
            for stat in stats:
                if(len(stat) != len(years)):
                    malformed = True
            if not malformed:
                file.write("%s\n" % player)
    
# get all players
with open('names.txt','r') as file:
    for line in file:
        line = line.replace(" ", "").replace(".","")
        print(line)
        req, ps = makePlayerReq(line)
        print(scrape_stats(req, ps, important_stats))   
#writePlayersToFile(makeAllPlayerReq())
#for player in all_players:
#    malformed = False
#    req, playerSoup = makePlay)erReq(player)
#    years = get_seasons(req, playerSoup)
#    stats = (scrape_stats(req, playerSoup, important_stats))
#    for stat in stats:
#        if(len(stat) != len(years)):
#            malformed = True
#    if not malformed:
        
#        for i, year in enumerate(years):
#            line = year + " "
#            for stat in stats:
#                line += stat[i] + " "
#        print("==================")
#        TODO: implement inserting data into PostgreSQL
