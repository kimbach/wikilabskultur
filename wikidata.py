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
# importing enum for enumerations 
import enum 

# creating enumerations using class 
class outputformat(enum.Enum): 
    csv = 'CSV'
    html = 'HTML'

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

def GetInstitutionWikidataItems(wd_institution, output_filename):
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
        f_csv=open(output_filename+'.csv', 'w+')
        f_html=open(output_filename+'.html', 'w+')
        wikidata_site = pywikibot.Site("wikidata", "wikidata")
        generator = pg.WikidataSPARQLPageGenerator(query, site=wikidata_site)

        # CSV header item;number;title;image;url;smk_id;smk_object_number;smk_image_native
        f_csv.write('item;number;title;image;url;smk_id;smk_object_number;smk_image_native\r\n')

        # HTML header
        f_html.write('<html>\r\n')
        f_html.write('<head><title>'+output_filename+'</title></head>\r\n')
        f_html.write('<body>\r\n')
        f_html.write('<table>\r\n')
        f_html.write('<tr><th>Wikidata Id</th><th>Accension number</th><th>Title</th><th>SMK Id</th><th>SMK Object Number</th><th>SMK URL</th><th>Commons Image</th><th>SMK Image</th><tr>\r\n')

        for wikidata_item in generator:
            try:
                smk_image_native=''
                smk_id=''
                smk_object_number=''
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
                    # [[commons:File:No_image_available.svg]]->
                    # https://commons.wikimedia.org/wiki/Special:FilePath/No_image_available.svg
                    image=str(claims.get(u'P18')[0].target)
                    # strip [[
                    image=image.replace("[[", "")
                    # strip ]]
                    image=image.replace("]]", "")
                    # replace commons:File with https://commons.wikimedia.org/wiki/Special:FilePath/
                    image=image.replace("commons:File:", "https://commons.wikimedia.org/wiki/Special:FilePath/")
                except:
                    image='https://commons.wikimedia.org/wiki/Special:FilePath/No_image_available.svg'
                print(image)

                # Claim 1476 is the title
                title=str(claims.get(u'P1476')[0].target.text)
                print(title)

                # Claim 973 is the documentation url                

                url=str(claims.get(u'P973')[0].target)
                print(url)

                # Add line to CSV
                f_csv.write(wikidata_item.id+';'+number+';'+title+';'+image+';'+url+';'+smk_id+';'+smk_object_number+';'+smk_image_native+'\r\n')

                # Add line to HTML
                f_html.write('<tr>'+
                    '<td><a href="https://wikidata.org/wiki/'+wikidata_item.id+'">'+wikidata_item.id+'</a></td>'
                    '<td>'+number+'</td>'+
                    '<td>'+title+'</td>'+
                    '<td>'+smk_id+'</td>'+
                    '<td>'+smk_object_number+'</td>'+
                    '<td><a href="'+url+'">'+url+'</a></td>'+
                    '<td><a href="'+image+'"><img src="'+image+'" width="100"/></a></td>'+
                    '<td><a href="'+smk_image_native+'"><img src="'+smk_image_native+'" width="100"/></a></td>'+
                    '</tr>\r\n')

                items=items+1
            except Exception as e:
                logging.error(str(e))
        
        # HTML footer
        f_html.write('</body>\r\n')
        f_html.write('</html>\r\n')
        
        f_csv.close() 
        f_html.close() 

    except Exception as e:
        logging.error(str(e))
    finally:
        print('items:'+str(items))

# Get all items from Statens Museum for Kunst, Wikidata Object Q671384
#GetInstitutionWikidataItems('Q671384', 'wikidata_smk.csv')
