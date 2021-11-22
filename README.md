# SearchEngine--IR
## Project in Data Mining & Information Retrieval module 

This repo contains 100 players data scraped from https://www.cricbuzz.com and stored at player_details.json file. Web Scraping Cricbuzz for a player.ipynb is used to scrap the data from web.

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

###  Query DSL for ElasticSearch search engine

```
 # deleting an index(database)
DELETE /cricsearch


##########################################################################################
#########          This must be run before creating the index(database)       ############
#######      Make a folder named analysis in elasticserach config folder       ###########
####   Please copy stopwords.txt & stem.txt to the analysis folder #######
##########################################################################################

 ```
### Custom stop words, stemming and synonym new analyzer along with the standard analyzer

```
PUT /cricsearch/
{
        "settings": {
            "analysis": {
                "analyzer": {
                    "my_analyzer": {
                        "tokenizer": "standard",
                        "filter": ["custom_stopper","custom_stems","custom_synonym"]
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
                    },
                    "custom_synonym": {
                        "type": "synonym",
                        "synonyms_path": "analysis/synonym.txt"                
                    }
                }
            }
        }
    }
 ```
 
### checking the custom analyzer(stopwords, stemming, synonym)
```
##similar word support
GET /cricsearch2/_analyze
{
 "text": ["போலர் "],
 "analyzer": "my_analyzer"
}
```
  
### Uploading data using bulk API
 ```
POST /_bulk
{ "index" : { "_index" : "cricsearch", "_type" : "_doc", "_id" :2 } }
{"பெயர்": "ரோஹித் சர்மா", "வயது": 34, "வகை": "துடுப்பாட்ட வீரர்", "துடுப்பாட்டம்": "வலதுகை துடுப்பாட்டம்", "பந்துவீச்சு": "வலதுகை சுழல் பந்துவீச்சு", "அணி": "இந்தியா", "இலக்குகள்": 1, "ஓட்டங்கள்": 9205}
{ "index" : { "_index" : "cricsearch", "_type" : "_doc", "_id" :3 } }
{"பெயர்": "ராஸ் டெய்லர்", "வயது": 37, "வகை": "துடுப்பாட்ட வீரர்", "துடுப்பாட்டம்": "வலதுகை துடுப்பாட்டம்", "பந்துவீச்சு": "வலதுகை சுழல் பந்துவீச்சு", "அணி": "நியூசிலாந்து", "இலக்குகள்": 0, "ஓட்டங்கள்": 8576}
{ "index" : { "_index" : "cricsearch", "_type" : "_doc", "_id" :4 } }
{"பெயர்": "ஜானி பேர்ஸ்டோவ்", "வயது": 32, "வகை": "காப்பாளர்", "துடுப்பாட்டம்": "வலதுகை துடுப்பாட்டம்", "பந்துவீச்சு": "வலதுகை வேக பந்துவீச்சு", "அணி": "இங்கிலாந்து", "இலக்குகள்": 0, "ஓட்டங்கள்": 3498}
{ "index" : { "_index" : "cricsearch", "_type" : "_doc", "_id" :5 } }

```

### விராட் கோலி  name spelling mistake
```
GET /cricsearch/_search
{
   "query": {
       "multi_match" : {
           "query" : "விராட் கல",
           "fuzziness": "AUTO",
       "analyzer": "my_analyzer"
       }
   }
}
```

### விராட் கோலி name without spell mistake
```

GET /cricsearch/_search
{
   "query": {
       "multi_match" : {
           "query" : "விராட் கோலி",
           "fuzziness": "AUTO",
       "analyzer": "standard"
       }
   }
}
```

### top 5 bastmans age from 30 to 35
```
GET /cricsearch/_search
{
   "size" : 5,
    "sort" : [
       { "ஓட்டங்கள்" : {"order" : "desc"}}
   ],
   "query": {
       "range" : {
           "வயது" : {
               "gte" : "30",
               "lte" :  "35"
           }
       }
   }
}
```

### top 5 bastmans from இலங்கை
```
GET /cricsearch/_search
{
   "size":5,
   "sort" : [
       { "ஓட்டங்கள்" : {"order" : "desc"}}
   ],
   "query": {
       "multi_match": {
             "query" : "இலங்கை",
           "fields":["அணி"],
           "fuzziness": "AUTO"
       }
   }
}

```

### Batsmans scored more than 10000 runs
```
GET /cricsearch/_search
{
    "query": {
        "range": {
            "ஓட்டங்கள்" : {
                "gte" : "10000"
            }
        }
    }
}
```

### 5 சகலதுறை வீரர்
```
GET /cricsearch/_search
{
   "size":5,
   "query": {
       "multi_match": {
           "query" : "சகலதுறை வீரர்",
           "fields":["வகை"],
           "fuzziness": "AUTO"
       }
   }
}
```
### Bolwers got இலக்குகள் more than 100
```
GET /cricsearch/_search
{
    "query": {
        "range": {
            "இலக்குகள்" : {
                "gte" : "100"
            }
        }
    }
}
```
### Top இலங்கை சகலதுறை வீரர் with more than 50 இலக்குகள் and 500 ஓட்டங்கள்.
```
GET /cricsearch/_search
{
 "query": {
   "bool": {
     "must": [{
         "match": {
           "அணி": "இலங்கை"
         }
       },
       {
         "range": {
           "இலக்குகள்" : {
               "gte" : "50"
           }
         }
       },
       {
          "range": {
           "ஓட்டங்கள்" : {
               "gte" : "500"
           }
         }
       }
     ]
   }
 }
}
