# ORIGIN #
This project is an exercise done as part of an OpenClassrooms training course for developers in the Python language.
It corresponds to project 7 of the training.


# GOAL OF THE APPLICATION #
This application in Python allows you to ask questions to "GrandPy" about places or monuments. He answers by telling anecdotes about the requested place. We use the API of Wikipedia to find the information on the place and the API of Here.com to display an interactive map allowing to locate this place.


# FEATURES #
* AJAX interactions: the user sends his question by pressing enter and the answer is displayed directly on the screen, without reloading the page.
* We use the Google Maps API and the Media Wiki API.
* Nothing is saved. If the user reloads the page, all history is lost.
* Option: invent several different responses from GrandPy.


# USER PATH #
The user opens their browser and enters the URL you have provided. They are presented with a page containing the following elements

    * header: logo and catchphrase
    * central zone: empty zone (which will be used to display the dialogue) and form field for sending a question.
    * footer: your first & last name, link to your Github repository and other social networks if you have them

The user types "Hi GrandPy! Do you know the address of OpenClassrooms?" in the form field and then press the Enter key. The message is displayed in the area above, which shows all messages exchanged. An icon rotates to indicate that GrandPy is thinking.

Then a new message appears: "Of course my chick! Here it is: 7 cité Paradis, 75010 Paris." Underneath, a Google Maps map also appears with a marker indicating the requested address.

GrandPy sends a new message: "But did I ever tell you the story of this neighbourhood that saw me in short pants? The Cité Paradis is a public road in the 10th arrondissement of Paris. It is tee-shaped, with one branch leading to 43 rue de Paradis, the second to 57 rue d'Hauteville and the third to a dead end. [Read more on Wikipedia]"


# CONSTRAINTS #
* Responsive interface
* Test Driven Development
* Code written entirely in English: functions, variables, comments, etc.
* Use of AJAX to send questions and display answers (questions and answers are in one language only, English or French)
* Tests using mocks for APIs


# EXAMPLES OF JSON RESPONSES FROM API #
JSON can contain several results but only the first one is shown in the examples

**Here.com API**

Example URL : search for coordinates using keywords

https://geocode.search.hereapi.com/v1/geocode?apiKey=9Qlt8XzxvTNNpAGkQc9TvDdKrC9P84BrgrsdjSb1IJY&lang=fr&q=musee+confluences+lyon

JSON response : 

```json
{
    "items": [
        {
            "title": "Musée des Confluences",
            "id": "here:pds:place:250jx7ps-4d8aeaf036150f3ebaf2791039b1c32a",
            "resultType": "place",
            "address": {
                "label": "Musée des Confluences, 69002 Lyon, France",
                "countryCode": "FRA",
                "countryName": "France",
                "stateCode": "ARA",
                "state": "Auvergne-Rhône-Alpes",
                "county": "Rhône",
                "city": "Lyon",
                "district": "2e Arrondissement",
                "postalCode": "69002"
            },
            "position": {
                "lat": 45.73374,
                "lng": 4.81744
            },
            "access": [
                {
                    "lat": 45.73348,
                    "lng": 4.81763
                }
            ],
            "categories": [
                {
                    "id": "400-4100-0047",
                    "name": "Station de taxis",
                    "primary": true
                }
            ],
            "scoring": {
                "queryScore": 0.9,
                "fieldScore": {
                    "city": 1.0,
                    "placeName": 0.74
                }
            }
        }
    ]
}
```

------------------------------------
------------------------------------

**Wikipedia API**

Example URL1 : keyword search

https://fr.wikipedia.org/w/api.php?action=query&format=json&list=search&srsearch=musee%20confluencer%20lyon

JSON response : 

```json
{
    "batchcomplete": "",
    "continue": {
        "sroffset": 10,
        "continue": "-||"
    },
    "query": {
        "searchinfo": {
            "totalhits": 873
        },
        "search": [
            {
                "ns": 0,
                "title": "Musée des Confluences",
                "pageid": 1322917,
                "size": 43058,
                "wordcount": 4430,
                "snippet": "modifier Wikidata Le <span class=\"searchmatch\">musée</span> des <span class=\"searchmatch\">Confluences</span> est un <span class=\"searchmatch\">musée</span> d'histoire naturelle, d'anthropologie, des sociétés et des civilisations situé à <span class=\"searchmatch\">Lyon</span>, dans la région",
                "timestamp": "2021-03-30T15:54:17Z"
            }
        ]
    }
}
```

------------------------------------

Example URL2 : search for coordinates from the page title

https://fr.wikipedia.org/w/api.php?action=query&format=json&titles=Musée%20des%20Confluences&redirects&prop=coordinates

JSON response : 

```json
{
    "batchcomplete": "",
    "query": {
        "pages": {
            "1322917": {
                "pageid": 1322917,
                "ns": 0,
                "title": "Musée des Confluences",
                "coordinates": [
                    {
                        "lat": 45.732906,
                        "lon": 4.818304,
                        "primary": "",
                        "globe": "earth"
                    }
                ]
            }
        }
    }
}
```

------------------------------------

Example URL3 : search for the page extract from the page title

https://fr.wikipedia.org/w/api.php?action=query&format=json&prop=extracts&exchars=1200&exintro=true&titles=Musée%20des%20Confluences&explaintext=1

JSON response : 

```json
{
    "batchcomplete": "",
    "query": {
        "pages": {
            "1322917": {
                "pageid": 1322917,
                "ns": 0,
                "title": "Musée des Confluences",
                "extract": "Le musée des Confluences est un musée d'histoire naturelle, d'anthropologie, des sociétés et des civilisations situé à Lyon, dans la région Auvergne-Rhône-Alpes en France. Héritier du Musée d'histoire naturelle Guimet de Lyon, il est ouvert en 2014 et hébergé dans un bâtiment de style déconstructiviste de l’agence d'architecture Coop Himmelb(l)au, dans le quartier de La Confluence, sur la pointe sud de la Presqu'île de Lyon, au confluent du Rhône et de la Saône (2e arrondissement de Lyon).\nIl en reprend les collections et a pour vocation de compléter son fonds par des acquisitions. Il fait l'objet de dépôts et prêts de musées et institutions diverses (musées d'art et de la culture, jardins botaniques, fondations, congrégations religieuses...) pour ses espaces d'exposition temporaires et permanentes. Le musée a une activité orientée vers la scénographie (coopération avec des salles de spectacle musical et de théâtre) et a débuté celle d'éditeur de livres (romans autour de quelques objets fameux de sa collection en collaboration avec des auteurs de textes littéraires ou de dessins et de photographies).\nLe projet déclaré est celui de pédagogie distrayante et artistique, « les confluences..."
            }
        }
    }
}
```

------------------------------------

Example URL4 : search for page title and wiki coordinates from Here coordinates

https://fr.wikipedia.org/w/api.php?action=query&format=json&list=geosearch&gscoord=45.73374|4.81744&gsradius=250&gslimit=1&utf8=

JSON response : 

```json
{
    "batchcomplete": "",
    "query": {
        "geosearch": [
            {
                "pageid": 1322917,
                "ns": 0,
                "title": "Musée des Confluences",
                "lat": 45.732906,
                "lon": 4.818304,
                "dist": 114.4,
                "primary": ""
            }
        ]
    }
}
```
