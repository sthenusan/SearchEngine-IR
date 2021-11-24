# Index Details for Famous People (Cricket Players)
## Project in CS4642- Data Mining & Information Retrieval module 

### Project Description
Need to create an Index for famous peoples using SOLR or Elasticsearch

### Requirements
1. Data (Search Data)
2. Elasticsearch (Build Index)
3. Kibana (Visualization)
4. Python (Data Scraping and Perprocessing)

This repo contains players data scraped from [Cricbuzz](https://www.cricbuzz.com) stored at ```player_details.json``` file. ```Web Scraping Cricbuzz for a player.ipynb``` is used to scrap the data from Cricbuzz web. Those 100 players details are mainly focused on one day international cricket for runs and wickets datas.



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
After scrapping, I preprocessed the data to convert it into Tamil language and simplified data in the prefocessing step. I added an extra metadata for players named "விபரம்" using [espncricinfo](https://www.espncricinfo.com/) to improve the quality of the data and stored in ```player_details.json``` file.

## Sample JSON data of a processed player data

```
{
"பெயர்": "விராட் கோலி", 
"வயது": 33, 
"வகை": "துடுப்பாட்டவீரர்", 
"துடுப்பாட்டம்": "வலதுகை துடுப்பாட்டம்",
"பந்துவீச்சு": "வலதுகை வேகபந்துவீச்சு",
"அணி": "இந்தியா", 
"இலக்குகள்": 4, 
"ஓட்டங்கள்": 12169,
"விபரம்":"இவர் தற்போது அணித் தலைவராக உள்ளார். வலது கை மட்டையாளரான இவர் சர்வதேச சிறந்த துடுப்பாட வீரர்களில் ஒருவராகக் கருதப்படுகிறார்"
}
```

Bulk API format of players are stored as ```datascript_es.txt``` file

The following Query DSL are supported for all the diiferent types of user queries.

###  Query DSL for ElasticSearch search engine

```
#deleting an index(database)
DELETE /cricsearch

 ```
 ```
##########################################################################################
#########          This must be done before creating the index                ############
#######      Make a folder named analysis in elasticserach config folder       ###########
####   Please copy stopwords.txt, stem.txt and synonym.txt to the analysis folder #######
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

#### Similar Word Support
```
GET /cricsearch/_analyze
{
  "text": ["பாரதம்"],
  "analyzer": "my_analyzer"
}

GET /cricsearch/_analyze
{
"text": ["சிலிங்கா "],
"analyzer": "my_analyzer"
}

GET /cricsearch/_analyze
{
"text": ["மட்டையாளர் "],
"analyzer": "my_analyzer"
}
```
#### Stop Word Support
```
GET /cricsearch/_analyze
{
 "text": ["மிகவும் சிறந்த 10 வீரர்கள்"],
 "analyzer": "my_analyzer"
}

GET /cricsearch/_analyze
{
 "text": ["கேப்டன்கூல் எனப்படும் மற்ற வீரர்கள்"],
 "analyzer": "my_analyzer"
}

GET /cricsearch/_analyze
{
 "text": ["இதை விட  சிறந்த 10 வீரர்கள்"],
 "analyzer": "my_analyzer"
}
```
#### Stemming Support
```
GET /cricsearch/_analyze
{
 "text": ["தலைவராகவும் இருந்த துடுப்பு வீரர்"],
 "analyzer": "my_analyzer"
}

GET /cricsearch/_analyze
{
 "text": ["தரவரிசையில்  முன்னாள்  ஆத்திரேலிய வீரர்"],    
 "analyzer": "my_analyzer"
}

```
  
### Uploading data using bulk API
 ```
POST /_bulk
{ "index" : { "_index" : "cricsearch", "_type" : "_doc", "_id" :1 } }
{"பெயர்": "விராட் கோலி", "வயது": 33, "வகை": "துடுப்பாட்டவீரர்", "துடுப்பாட்டம்": "வலதுகை துடுப்பாட்டம்", "பந்துவீச்சு": "வலதுகை வேகபந்துவீச்சு", "அணி": "இந்தியா", "இலக்குகள்": 4, "ஓட்டங்கள்": 12169,"விபரம்":"இவர் தற்போது அணித் தலைவராக உள்ளார். வலது கை மட்டையாளரான இவர் சர்வதேச சிறந்த துடுப்பாட வீரர்களில் ஒருவராகக் கருதப்படுகிறார்."}
{ "index" : { "_index" : "cricsearch", "_type" : "_doc", "_id" :2 } }
{"பெயர்": "ரோஹித் சர்மா", "வயது": 34, "வகை": "துடுப்பாட்டவீரர்", "துடுப்பாட்டம்": "வலதுகை துடுப்பாட்டம்", "பந்துவீச்சு": "வலதுகை சுழல்பந்துவீச்சு", "அணி": "இந்தியா", "இலக்குகள்": 1, "ஓட்டங்கள்": 9205,"விபரம்":" ஒருநாள் மற்றும் 20 ஓவெர் பன்னாட்டுத் துடுப்பாட்ட இந்திய அணியின் உதவித் தலைவராக உள்ளார். இவர் வலது கை மட்டையாளர், அவ்வப்போது வலது கை புறத்திருப்ப பந்துவீச்சாளர் ஆவார். மும்பை மாநில அணிக்காக உள்ளூர்ப் போட்டிகளிலும், இந்தியன் பிரீமியர் லீக் போட்டிகளில் மும்பை இந்தியன்ஸ் அணித் தலைவராகவும் விளையாடி வருகிறார்."}
{ "index" : { "_index" : "cricsearch", "_type" : "_doc", "_id" :3 } }
{"பெயர்": "ராஸ் டெய்லர்", "வயது": 37, "வகை": "துடுப்பாட்டவீரர்", "துடுப்பாட்டம்": "வலதுகை துடுப்பாட்டம்", "பந்துவீச்சு": "வலதுகை சுழல்பந்துவீச்சு", "அணி": "நியூசிலாந்து", "இலக்குகள்": 0, "ஓட்டங்கள்": 8576,"விபரம்":" இவர் நியூசிலாந்து துடுப்பாட்ட அணிக்காக அனைத்து வகையான பன்னாட்டுப் போட்டிகளிலும் விளையாடி வருகிறார். இவர் ஜனவரி 2019இல் ஒருநாள் போட்டிகளில் தனது 20வது நூறைப் பெற்றதன் மூலம் எந்தவொரு போட்டி வகைகளிலும் 20 நூறுகள் எடுத்த முதல் நியூசிலாந்து வீரர் ஆனார்."}
{ "index" : { "_index" : "cricsearch", "_type" : "_doc", "_id" :4 } }
{"பெயர்": "ஜானி பேர்ஸ்டோவ்", "வயது": 32, "வகை": "காப்பாளர்", "துடுப்பாட்டம்": "வலதுகை துடுப்பாட்டம்", "பந்துவீச்சு": "வலதுகை வேகபந்துவீச்சு", "அணி": "இங்கிலாந்து", "இலக்குகள்": 0, "ஓட்டங்கள்": 3498,"விபரம்":"  இவர் இங்கிலாந்து அணிக்காக அனைத்துவகை பன்னாட்டுப் போட்டிகளிலும் யார்க்சையர் அணிக்காக உள்ளூர்ப் போட்டிகளிலும் விளையாடி வருகிறார். இவர் 2019 துடுப்பாட்ட உலகக்கிண்ணத்தை வென்ற இங்கிலாந்து அணியில் இடம்பெற்றிருந்தார்."}
{ "index" : { "_index" : "cricsearch", "_type" : "_doc", "_id" :5 } }

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


### top 5 run getters with age from 30 to 35
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
### Players scored more than 10000 runs
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

### Players got இலக்குகள் 100 or more than 100
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
### Players involed in ஐபிஎல் using விபரம்.
```
GET /cricsearch/_search
{
  "query": {
    "multi_match": {
      "query": "ஐபிஎல்",
      "fields":["விபரம்"], 
      "fuzziness": "AUTO",
      "analyzer": "my_analyzer"
    }
  }
}

```

### top 5 player from இலங்கை ordering using ஓட்டங்கள்
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

### 5 சகலதுறைவீரர்
```
GET /cricsearch/_search
{
   "size":5,
   "query": {
       "multi_match": {
           "query" : "சகலதுறைவீரர்",
           "fields":["வகை"],
           "fuzziness": "AUTO"
       }
   }
}
```

## Top 5 காப்பாளர் using ஓட்டங்கள்
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

### Top இலங்கை player with more than 50 இலக்குகள் and 500 ஓட்டங்கள்.
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

## WildCard Queries

### Player first name or last name end with கோ
```
GET /cricsearch/_search
{
    "query": {
        "wildcard" : {
	        "பெயர்" : "கோ*"     
	        }
    }
}
```
### Player first name or last name end with லி
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
### Player first name or last name start with கிறிஸ்
```
GET /cricsearch/_search
{
    "query": {
        "wildcard": {
            "query" : "கிறிஸ்*"
        }
    }
}
```

### Player first name or last name ending in ட்
```
GET /cricsearch/_search
{
   "query": {
       "wildcard" : {
           "பெயர்" : "*ட்"
       }
   }
}
```
### Player name with in ர்ன middle
```

GET /cricsearch/_search
{
   "query": {
       "wildcard" : {
           "பெயர்" : "*ர்ன*"
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
           "பந்துவீச்சு" :  "சுழல்பந்துவீச்சு"
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

### Bowler with வலதுகை வேகபந்துவீச்சு and more than 60 இலக்குகள் and வகை (சகலதுறை வீரர் or பந்து வீச்சாளர்) and not அஸ்திரேலியா player.
```
GET /cricsearch/_search
{
 "query": {
   "bool": {
     "must": {
       "bool" : { 
         "should": [
           { "match": { "வகை": "சகலதுறைவீரர்" }},
           { "match": { "வகை": "பந்துவீச்சாளர்" }} 
         ],
         "filter": [ 
       {
         "range": {
           "இலக்குகள்" : {
               "gte" : "60"
           }
         }
       }
     ],
         "must": { "match": { "பந்துவீச்சு": "வலதுகை வேகபந்துவீச்சு" }} 
       }
     },
     "must_not": { "match": {"அணி": "அஸ்திரேலியா" }}
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
           { "match": { "வகை": " துடுப்பாட்டவீரர்" }},
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

### Can search for players only with விபரம் (Text Mining)

```
GET /cricsearch/_search
{
  "query": {
    "more_like_this" : {
      "fields" : ["விபரம்"],  
      "like" : "இவர் ஐசிசியின் ஒருநாள் பன்னாட்டுத் துடுப்பாட்டத்தின் பன்முக ஆட்டக்காரர்கள்",
      "min_term_freq" : 7,
      "max_query_terms" : 12
    }
  }
}
```
