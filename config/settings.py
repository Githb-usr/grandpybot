#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
    Settings file
    To manage application constants
"""
import os

WIKI_API_URL = "https://fr.wikipedia.org/w/api.php"
MAP_API_URL = "https://geocode.search.hereapi.com/v1/geocode"
REGEX1 = (r".*concernant \s?(.*)?", 1)
REGEX2 = (r".*(adresse|adresse postale) d[e|'|u]\s?(.*)?", 2)
REGEX3 = (r".*(a propos|au sujet) (des|d[e|'|u])\s?(.*)?", 3)
REGEX4 = (r".*racont(ez|e)([\-\s](moi|nous))\s?(.*)?", 4)
REGEX5 = (r".*ou (est|sont|se (trouv|situ)(ent|e))\s?(.*)?", 4)
REGEX6 = (r".*parl(ez|ons|e)([\-\s](moi|nous)\s|\s)(des|d[e|'|u])\s?(.*)?", 5)
PARSER_REGEX = [REGEX1, REGEX2, REGEX3, REGEX4, REGEX5, REGEX6]
STOPWORDS = ["-","a","abord","absolument","afin","ah","ai","aie","ailleurs","ainsi","ait","allaient","allo","allons","allô","alors","anterieur","anterieure","anterieures","apres","après","as","assez","attendu","au","aucun","aucune","aujourd","aujourd'hui","aupres","auquel","aura","auraient","aurait","auront","aussi","autre","autrefois","autrement","autres","autrui","aux","auxquelles","auxquels","avaient","avais","avait","avant","avec","avoir","avons","ayant","b","bah","bas","basee","bat","beau","beaucoup","bien","bigre","bot","boum","bravo","brrr","c","c'est","car","ce","ceci","cela","celle","celle-ci","celle-là","celles","celles-ci","celles-là","celui","celui-ci","celui-là","cent","cependant","certain","certaine","certaines","certains","certes","ces","cest","cet","cette","ceux","ceux-ci","ceux-là","chacun","chacune","chaque","cher","chers","chez","chiche","chut","chère","chères","ci","cinq","cinquantaine","cinquante","cinquantième","cinquième","clac","clic","combien","comme","comment","comparable","comparables","compris","concernant","contre","couic","crac","d","da","dans","de","debout","dedans","dehors","deja","delà","depuis","dernier","derniere","derriere","derrière","des","desormais","desquelles","desquels","dessous","dessus","deux","deuxième","deuxièmement","devant","devers","devra","different","differentes","differents","différent","différente","différentes","différents","dire","directe","directement","dis-moi","dis-nous","dit","dite","dits","divers","diverse","diverses","dix","dix-huit","dix-neuf","dix-sept","dixième","doit","doivent","donc","dont","douze","douzième","dring","du","duquel","durant","dès","désormais","e","effet","egale","egalement","egales","eh","elle","elle-même","elles","elles-mêmes","en","encore","enfin","entre","envers","environ","es","est","et","etant","etc","etre","eu","euh","eux","eux-mêmes","exactement","excepté","extenso","exterieur","f","fais","faisaient","faisant","fait","façon","feront","fi","flac","floc","font","g","gens","grandma","grandpy","grandpybot","h","ha","hein","hem","hep","hi","ho","holà","hop","hormis","hors","hou","houp","hue","hui","huit","huitième","hum","hurrah","hé","hélas","i","il","ils","importe","j","je","jusqu","jusque","juste","k","l","la","laisser","laquelle","las","le","lequel","les","lesquelles","lesquels","leur","leurs","localise","longtemps","lors","lorsque","lui","lui-meme","lui-même","là","lès","m","ma","maint","maintenant","mais","malgre","malgré","maximale","me","meme","memes","merci","mes","mien","mienne","miennes","miens","mille","mince","minimale","moi","moi-meme","moi-même","moindres","moins","mon","moyennant","multiple","multiples","même","mêmes","n","na","naturel","naturelle","naturelles","ne","neanmoins","necessaire","necessairement","neuf","neuvième","ni","nombreuses","nombreux","non","nos","notamment","notre","nous","nous-mêmes","nouveau","nt","nul","néanmoins","nôtre","nôtres","o","oh","ohé","ollé","olé","on","ont","onze","onzième","ore","ou","ouf","ouias","oust","ouste","outre","ouvert","ouverte","ouverts","o|","où","p","paf","pan","par","parce","parfois","parle","parlent","parler","parmi","parseme","partant","particulier","particulière","particulièrement","pas","passé","pendant","pense","permet","personne","peu","peut","peuton","peuvent","peux","peuxtu","pff","pfft","pfut","pif","pire","plait","plein","plouf","plus","plusieurs","plutôt","possessif","possessifs","possible","possibles","pouah","pour","pourquoi","pourrais","pourraisje", "pourraistu","pourrait","pourraiton","pourriezvous","pouvait","prealable","precisement","premier","première","premièrement","pres","probable","probante","procedant","proche","propos","près","psitt","pu","puis","puisje","puisque","pur","pure","q","qu","quand","quant","quant-à-soi","quanta","quarante","quatorze","quatre","quatre-vingt","quatrième","quatrièmement","que","quel","quelconque","quelle","quelles","quelqu'un","quelque","quelques","quels","qui","quiconque","quinze","quoi","quoique","r","rare","rarement","rares","relative","relativement","remarquable","rend","rendre","restant","reste","restent","restrictif","retour","revoici","revoilà","rien","s","sa","sacrebleu","sais-tu","sait","sans","sapristi","sauf","savez-vous","savons-nous","se","sein","seize","selon","semblable","semblaient","semble","semblent","sent","sept","septième","sera","seraient","serait","seront","ses","seul","seule","seulement","si","sien","sienne","siennes","siens","sinon","situant","six","sixième","soi","soi-même","soit","soixante","son","sont","sous","souvent","specifique","specifiques","speculatif","stop","strictement","subtiles","suffisant","suffisante","suffit","suis","suit","suivant","suivante","suivantes","suivants","suivre","sujet","superpose","sur","surtout","t","ta","tac","tant","tardive","te","tel","telle","tellement","telles","tels","tenant","tend","tenir","tente","tes","tic","tien","tienne","tiennes","tiens","toc","toi","toi-même","ton","touchant","toujours","tous","tout","toute","toutefois","toutes","treize","trente","tres","trois","troisième","troisièmement","trop","trouvant","trouve","trouvent","trouver","très","tsoin","tsouin","tu","té","u","un","une","unes","uniformement","unique","uniques","uns","v","va","vais","vas","vers","via","vif","vifs","vingt","vivat","vive","vives","vlan","voici","voilà","vont","vos","votre","vous","vous-mêmes","vu","vé","vôtre","vôtres","w","x","y","z","zut","à","â","ça","ès","étaient","étais","était","étant","été","être","ô"]
NO_DATA = "no_data"
BAD_DATA = "bad_data"
DEFAULT_COORDINATES = (54.525961, 15.255119)
DEFAULT_TITLE = "unknown place"
DEFAULT_EXTRACT = "no extract"
POSITIVE_GRANDPY_MESSAGES = [
    "Ah ah, excellente question !",
    "A ce sujet, on peut dire que mes souvenirs sont excellents !",
    "Oh oh oh, j'en ai des choses à te raconter sur cet endroit ^^",
    "A question pertinente, réponse détaillée !",
    "Ca tombe bien, je connais très bien cet endroit !",
    "On peut dire que tu as bien choisi ta question ^^",
    "Tant de choses à dire sur ce lieu magique !",
    "J'ai vécu par là-bas assez longtemps pour pouvoir te répondre :)",
    "Installe-toi conformablement, je vais tout te dire !",
    "Alors cette question-ci, on ne me l'avait encore jamais posée, hi hi hi"
]
NEGATIVE_GRANDPY_MESSAGES = [
    "Je suis sincèrement désolé mais je n'ai pas d'informations à ce sujet...",
    "Malheureusement je ne connais pas cet endroit, je ne pourrais rien te dire :(",
    "Alors là, pas de chance, je n'y suis jamais allé donc pas d'anecdote ce coup-ci malheureusement...",
    "J'ai roulé ma bosse un peu partout, mais pas à cet endroit, je suis vraiment désolé de ne pas pouvoir t'en dire plus...",
    "Il parait que c'est un super coin, mais je n'ai pas eu la chance d'y aller moi-même, alors je n'en sais pas plus...",
    "Ralala, j'ai toujours voulu y faire un tour, mais ça ne s'est jamais fait alors je ne connais pas :(",
    "Tu dois probablement en savoir plus que moi sur cet endroit, je ne le connais pas :(",
    "J'ai beau avoir beaucoup bourlingué, je n'y suis jamais allé, désolé...",
    "Alors là, tu me poses une sacrée colle ! Je ne connais même pas de nom !",
    "Je me demandais justement comment était cet endroit que je ne connais pas encore, désolé de ne pas pouvoir te répondre :("
]
DEFAULT_WIKI_DATA = {
                    "wiki_page_title": DEFAULT_TITLE,
                    "wiki_extract": DEFAULT_EXTRACT,
                    "wiki_coordinates": DEFAULT_COORDINATES
                    }
DEFAULT_RESPONSE = {
                "map": DEFAULT_COORDINATES,
                "wiki": DEFAULT_WIKI_DATA,
                "apiKey": os.environ.get('HERE_JS_API_KEY'),
                "default_title": DEFAULT_TITLE,
                "default_extract": DEFAULT_EXTRACT,
                "positive_messages": POSITIVE_GRANDPY_MESSAGES,
                "negative_messages": NEGATIVE_GRANDPY_MESSAGES        
            }
