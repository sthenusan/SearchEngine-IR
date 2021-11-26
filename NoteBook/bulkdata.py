from elasticsearch import Elasticsearch, helpers
from elasticsearch_dsl import Index
import json, re
import codecs
import unicodedata
# import queries

client = Elasticsearch(HOST="http://localhost", PORT=9200)
INDEX = 'cricsearch'

#Creating index if not manually created
def createIndex():
    index = Index(INDEX, using=client)
    res = index.create()
    print(res)

def read_all_players():
    with open('corpus/player_details.json', 'r', encoding='utf-8-sig') as f:
        all_players = json.loads("[" +
                          f.read().replace("}\n{", "},\n{") +"]")
        res_list = [i for n, i in enumerate(all_players) if i not in all_players[n + 1:]]
        return res_list

def genData(player_array):
    for player in player_array:
        # Fields-capturing
        # print(song)
        name = player.get("பெயர்", None)
        age = player.get("வயது",None)
        type = player.get("வகை", None)
        batting = player.get("துடுப்பாட்டம்", None)
        bowling = player.get("பந்துவீச்சு", None)
        team = player.get("அணி", None)
        wicket = player.get("இலக்குகள்", None)
        run = player.get("ஓட்டங்கள்",None)

        yield {
            "_index": "cricsearch",
            "_source": {
                "பெயர்": name,
                "வயது": age,
                "வகை": type,
                "துடுப்பாட்டம்": batting,
                "பந்துவீச்சு": bowling,
                "அணி": team,
                "இலக்குகள்": wicket,
                "ஓட்டங்கள்": run,
            },
        }

# createIndex()
all_players = read_all_players()
helpers.bulk(client,genData(all_players))
