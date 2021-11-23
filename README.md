# SearchEngine Index for Famous People (Cricket Players)
## Project in CS4642- Data Mining & Information Retrieval module 

This repo contains 100 players data scraped from [Cricbuzz](https://www.cricbuzz.com) stored at ```player_details.json``` file. ```Web Scraping Cricbuzz for a player.ipynb``` is used to scrap the data from Cricbuzz web. Those 100 players details are mainly focused on one day international cricket for runs and wickets datas.

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
"Runs": 12169,
}
```
After scrapping, I preproceed data to convert it into Tamil language. I simplified data in the prefocessing step. I added an extra metadata named "விபரம்" is added to improve the quality of the data and stored as ```player_details.json``` file.

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
"ஓட்டங்கள்": 12169,
"விபரம்":"இவர் தற்போது அணித் தலைவராக உள்ளார். வலது கை மட்டையாளரான இவர் சர்வதேச சிறந்த துடுப்பாட வீரர்களில் ஒருவராகக் கருதப்படுகிறார்"
}
```

Bulk API format of those 100 players are stored as ```datascript_es.txt``` file

The following Query DSL are supported for all the diiferent types of user queries.

###  Query DSL for ElasticSearch search engine

```
#deleting an index(database)
DELETE /cricsearch

 ```
 ```
##########################################################################################
#########          This must be run before creating the index(database)       ############
#######      Make a folder named analysis in elasticserach config folder       ###########
####   Please copy stopwords.txt & stem.txt to the analysis folder #######
##########################################################################################
```

### Custom stop words, stemming and synonym new analyzer along with the standard analyzer
I have given stopword consideration in tokenitation, Stemming and synonym support as well.
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
 "text": ["பாரதம்"],
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
   "size":1,
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
   "size":1,
   "query": {
       "multi_match" : {
           "query" : "விராட் கோலி",
           "fuzziness": "AUTO",
       "analyzer": "my_analyzer"
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

```
## Top 5 WK Batsman  
```
GET /cricsearch/_search
{
   "size":5,
   "sort" : [
       { "ஓட்டங்கள்" : {"order" : "desc"}}
   ],
 "query": {
   "multi_match" : {
     "query":    "காப்பாளர்",
     "fields":["வகை"],
     "fuzziness": "AUTO"
   }
 }
}
```
### WildCard Queries

```GET /cricsearch/_search
{
    "query": {
        "wildcard" : {
	        "பெயர்" : "கோ*"     
	        }
    }
}
```
```
GET /cricsearch/_search
{
    "query": {
        "wildcard" : {
	        "பெயர்" : "*லி"     
	        }
    }
}
```
```
GET /cricsearch/_search
{
    "query": {
        "query_string": {
            "query" : "கிறிஸ்*"
        }
    }
}
```
```
#Player firstname or lastname ending in ட்
GET /cricsearch/_search
{
   "query": {
       "wildcard" : {
           "பெயர்" : "*ட்"
       }
   },
   "_source": ["பெயர்"],
   "highlight": {
       "fields" : {
           "பெயர்" : {}
       }
   }
}
```
```
## Player name with in ர்ன middle
GET /cricsearch/_search
{
   "query": {
       "wildcard" : {
           "பெயர்" : "*ர்ன*"
       }
   },
   "_source": ["பெயர்"],
   "highlight": {
       "fields" : {
           "பெயர்" : {}
       }
   }
}
```

### இலங்கை வேகபந்துவீச்சு players with more than 50 இலக்குகள்
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
          "match": {
           "பந்துவீச்சு" :  "வேகபந்துவீச்சு"
           
         }
       }
     ]
   }
 }
}

```

### வங்கதேசம் சுழல்பந்துவீச்சு players with more than  100 இலக்குகள் and 5000 ஓட்டங்கள் and  வயது 25 to 35
```
GET /cricsearch/_search
{
 "query": {
   "bool": {
     "must": [{
         "match": {
           "அணி": "வங்கதேசம்"
         }
       },
       {
         "range": {
           "இலக்குகள்" : {
               "gte" : "100"
           }
         }
       },
       {
          "match": {
           "பந்துவீச்சு" :  "சுழல்"
           
         }
       },
      {
         "range": {
           "ஓட்டங்கள்" : {
               "gte" : "5000"
           }
         }
       },
       {
          "range": {
            "வயது" : {
               "gte" : "25",
               "lte" :  "35"
               
           }
         }
       }
     ]
   }
 }
}
```

### Bowler with வலதுகை வேக பந்துவீச்சு and more than 106 இலக்குகள் and வகை (சகலதுறை வீரர் or பந்து வீச்சாளர்) and not அஸ்திரேலியா player.
```
GET /cricsearch/_search
{
 "query": {
   "bool": {
     "must": {
       "bool" : { 
         "should": [
           { "match": { "வகை": "சகலதுறை வீரர்" }},
           { "match": { "வகை": "பந்து வீச்சாளர்" }} 
         ],
         "filter": [ 
       {
         "range": {
           "இலக்குகள்" : {
               "gte" : "106"
           }
         }
       }
     ],
         "must": { "match": { "பந்துவீச்சு": "வலதுகை வேக பந்துவீச்சு" }} 
       }
     },
     "must_not": { "match": {"அணி": "அஸ்திரேலியா" }}
   }
 }
}
```
### வயது less than 25 in players from இந்தியா 
```
GET /cricsearch/_search
{
 "query": {
   "bool": {
     "must": [{
         "match": {
           "அணி": "இந்தியா"
         }
       }
     ],
     "filter": [ 
       {
         "range": {
           "வயது" : {
               "lte" : "25"
           }
         }
       }
     ]
   }
 }
}
```
### துடுப்பாட்ட வீரர் or காப்பாளர் with more than 2500 runs, batting not இடதுகை and அணி இங்கிலாந்து
```
GET /cricsearch/_search
{
 "query": {
   "bool": {
     "must": {
       "bool" : { 
         "should": [
           { "match": { "வகை": " துடுப்பாட்ட வீரர்" }},
           { "match": { "வகை": "காப்பாளர் " }} 
         ],
         "filter": [ 
       {
         "range": {
           "ஓட்டங்கள்" : {
               "gte" : "2500"
           }
         }
       }
     ],
         "must": { "match": { "அணி": "இங்கிலாந்து" }} 
       }
     },
     "must_not": { "match": {"துடுப்பாட்டம்": "இடதுகை" }}
   }
 }
}
```
### Players involed in ஐபிஎல் using விபரம்.
```
GET /cricsearch/_search
{
  "query": {
    "multi_match": {
      "query": "ஐபிஎல்",
      "fuzziness": "AUTO",
      "analyzer": "my_analyzer"
    }
  }
}
```
