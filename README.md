# SearchEngine--IR
#### Project in Data Mining & Information Retrieval module 

This repo contains 100 players data scraped from https://www.cricbuzz.com and stored at scraped_lyrics.txt file. Web Scraping Cricbuzz for a player.ipynb is used to scrap the data from web.

## Sample JSON data of scraped player

```
{
"Name": "Virat Kholi", 
"Age": 33, 
"Tyep": "Batsman", 
"Batting": "Right hand Bat",
"Bowling": "Right Arm Fast Medium",
"Team": "India", 
"Wickets": 4, 
"Runs": 12169
}
```

## Sample JSON data of a processed player data

```
{
"பெயர்": "விராட் கோலி", 
"வயது": 33, 
"வகை": "துடுப்பாட்ட வீரர்", 
"துடுப்பாட்டம்": "வலதுகை துடுப்பாட்டம்",
"பந்துவீச்சு": "வலதுகை வேக பந்துவீச்சு",
"அணி": "இந்தியா", 
"இலக்குகள்": 4, 
"ஓட்டங்கள்": 12169
}
```

Bulk API format of those 100 players are stored as ```player_details.json``` file

The following Query DSL are supported for all the diiferent types of user queries.

##  Query DSL for ElasticSearch search engine

 ```
 # deleting an index(database)
DELETE /cricsearch


##########################################################################################
#########          This must be run before creating the index(database)       ############
#######      Make a folder named analysis in elasticserach config folder       ###########
####   Please copy stopwords.txt & stem.txt to the analysis folder #######
##########################################################################################


# custom stop words and stemming new analyzer along with the standard analyzer
PUT /cricsearch/
{
        "settings": {
            "analysis": {
                "analyzer": {
                    "my_analyzer": {
                        "tokenizer": "standard",
                        "filter": ["custom_stopper","custom_stems"]
                    }
                },
                "filter": {
                    "custom_stopper": {
                        "type": "stop",
                        "stopwords_path": "analysis/stopwords.txt"
                    },
                    "custom_stems": {
                        "type": "stemmer_override",
                        "rules_path": "analysis/stem.txt"
                    }
                }
            }
        }
    }

