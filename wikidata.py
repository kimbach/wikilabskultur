# Wikidata support
#
# 
from dataclasses import dataclass
from typing import Any, Optional, List, TypeVar, Type, Callable, cast
from enum import Enum
from datetime import datetime
import dateutil.parser
import pywikibot
from pywikibot import pagegenerators as pg
import logging
import smkapi

def recursive_iter_1(obj):
    if isinstance(obj, dict):
        for item in obj.values():
            yield from recursive_iter(item)
    elif any(isinstance(obj, t) for t in (list, tuple)):
        for item in obj:
            yield from recursive_iter(item)
    else:
        yield obj

def recursive_iter(obj, keys=()):
    if isinstance(obj, dict):
        for k, v in obj.items():
            yield from recursive_iter(v, keys + (k,))
    elif any(isinstance(obj, t) for t in (list, tuple)):
        for idx, item in enumerate(obj):
            yield from recursive_iter(item, keys + (idx,))
    else:
        yield keys, obj

def GetInstitutionWikidataItems(wd_institution, csv_filename):
    # Generates a CSV file of items from the institution with the wikidata Q-number given by
    # institution and saves the results to the file given by csv_filename 
    #
    # The format is item;number;title;image;url
    #
    # The Wikidata Item for the Statens Museum for Kunst colelction is Q671384
    
    # Set up logging
    wikidata_error_log = "wikidata_error.log"
    logging.basicConfig(filename=wikidata_error_log,level=logging.ERROR,format='%(asctime)s %(message)s', datefmt='%Y-%m-%d %H:%M:%S')

    # SPARQL query to execute 
    query = u"""# SPARQL forespørgsel der returnerer wikidata emner for SMK
SELECT DISTINCT ?item ?billeder ?inventarnummer ?titel ?beskrevet_ved_URL WHERE {
?item wdt:P195 wd:""" + wd_institution + """.
SERVICE wikibase:label { bd:serviceParam wikibase:language "[AUTO_LANGUAGE]". }
OPTIONAL { ?item wdt:P18 ?billeder. }
OPTIONAL { ?item wdt:P217 ?inventarnummer. }
OPTIONAL { ?item wdt:P1476 ?titel. }
OPTIONAL { ?item wdt:P973 ?beskrevet_ved_URL. }
}
ORDER BY (?item)"""

    items = 0
    try:
        f = open(csv_filename, 'w+')
        wikidata_site = pywikibot.Site("wikidata", "wikidata")
        generator = pg.WikidataSPARQLPageGenerator(query, site=wikidata_site)

        # CSV header item;number;title;image;url;smk_id;smk_object_number;smk_image_native
        f.write('item;number;title;image;url;smk_id;smk_object_number;smk_image_native\r\n')

        for wikidata_item in generator:
            try:
                print(wikidata_item.id)

                data = wikidata_item.get()
                claims = data.get('claims')
                # Claim 217 is the item number
                number=str(claims.get(u'P217')[0].target)
                print(number)

                smk_object = smkapi.get_smk_object(number)

                for keys, item in recursive_iter(smk_object['items']):
                    if 'image_native'==keys[1]:
                        smk_image_native=item
                        print('smk_image_native='+smk_image_native)
                    if 'id'==keys[1]:
                        smk_id=item
                        print('smk_id='+smk_id)
                    if 'object_number'==keys[1]:
                        smk_object_number=item
                        print('smk_object_number='+smk_object_number)

                #for item in smk_items:
                #    smk_id = item.id
                #    print ('id           =' + item.id)
                #    smk_object_number = item.object_number
                #    print ('object_number=' + item.object_number)
                #    smk_image_native = item.image_native
                #    print ('image_native =' + item.image_native)

                # Claim 18 is the image
                try:
                    image=str(claims.get(u'P18')[0].target)
                except:
                    image='<no image>'
                print(image)

                # Claim 1476 is the title
                title=str(claims.get(u'P1476')[0].target.text)
                print(title)

                # Claim 973 is the documentation url                

                url=str(claims.get(u'P973')[0].target)
                print(url)

                # Add line to CSV
                f.write(wikidata_item.id+';'+number+';'+title+';'+image+';'+url+';'+smk_id+';'+smk_object_number+';'+smk_image_native+'\r\n')
                items=items+1
            except Exception as e:
                logging.error(str(e))
        
        f.close() 

    except Exception as e:
        logging.error(str(e))
    finally:
        print('items:'+str(items))

# Get all items from Statens Museum for Kunst, Wikidata Object Q671384
#GetInstitutionWikidataItems('Q671384', 'wikidata_smk.csv')
