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

# Wikidata properties and items
wd_reference_url = 'S854'   # wikidata reference url
wd_inception = 'S571'       # wikidata inception date
wd_retrived = 'S813'        # wikidata retrieved date
wd_last_update = 'S5017'    # wikidata last_update date
wd_publisher = 'S123'       # wikidata publisher
wd_inventory_number = 'S217'# wikidata inventory number
wd_has_works_in_collection = 'P6379'    # wikidata har works in the collection of
wd_statens_museum_for_kunst = 'Q671384' # item for Statens Museum for Kunst
wd_gender_or_sex = 'P21'    # property for gender
wd_country_of_citizenship = 'P27' # property for country of citizenship
wd_date_of_birth = 'P569'   # property for date of birth
wd_date_of_death = 'P570'   # property for date of death
wd_occupation = 'P106'      # property for occupation
wd_artist = 'Q483501'       # item for artist
wd_instance_of = 'P31'      # instance of
wd_given_name = 'P735'      # given name
wd_family_name = 'P734'     # family name
wb_human = 'Q5'             # human item
wb_lastest_date = 'P1326'   # latest date

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
SELECT DISTINCT ?item ?skaberLabel ?billeder ?inventarnummer ?titel ?beskrevet_ved_URL ?creator WHERE {
?item wdt:P195 wd:""" + wd_institution + """.
SERVICE wikibase:label { bd:serviceParam wikibase:language "[AUTO_LANGUAGE]". }
OPTIONAL { ?item wdt:P18 ?billeder. }
OPTIONAL { ?item wdt:P217 ?inventarnummer. }
OPTIONAL { ?item wdt:P1476 ?titel. }
OPTIONAL { ?item wdt:P973 ?beskrevet_ved_URL. }
OPTIONAL { ?item wdt:P170 ?skaber. }
}
ORDER BY (?inventarnummer)"""

    items = 0
    try:
        f_csv=open(output_filename, 'w+')
        #f_html=open(output_filename+'.html', 'w+')
        wikidata_site = pywikibot.Site("wikidata", "wikidata")
        generator = pg.WikidataSPARQLPageGenerator(query, site=wikidata_site)

        # CSV header item;number;title;image;url;height;width;mime;smk_id;smk_object_number;smk_image_native;smk_image_height;smk_image_width;smk_public_domain;smk_has_image
        f_csv.write('inventorynumber;wikidataitem;creator;title;image;url;height;width;mime\n')

        # HTML header
        #f_html.write('<html>\r\n')
        #f_html.write('<head><title>'+output_filename+'</title></head>\r\n')
        #f_html.write('<body>\r\n')
        #f_html.write('<table>\r\n')
        #f_html.write('<tr><th>Wikidata Id</th><th>Accension number</th><th>Title</th><th>SMK Id</th><th>SMK Object Number</th><th>SMK URL</th><th>Commons Image</th><th>SMK Image</th><tr>\r\n')

        for wikidata_item in generator:
            try:
                wikidata_width=''
                wikidata_height=''
                wikidata_mime=''
                image=''
                number=''

                print(wikidata_item.id)

                data = wikidata_item.get()
                claims = data.get('claims')

                # Claim 217 is the accension number
                if claims.get(u'P217'):
                    number=str(claims.get(u'P217')[0].target)
                print(number)

                # smk_object = smkapi.get_smk_object(number)

                # for keys, item in recursive_iter(smk_object['items']):
                #     if 'image_native'==keys[1]:
                #         smk_image_native=item
                #         print('smk_image_native='+smk_image_native)
                #     if 'id'==keys[1]:
                #         smk_id=item
                #         print('smk_id='+smk_id)
                #     if 'object_number'==keys[1]:
                #         smk_object_number=item
                #         print('smk_object_number='+smk_object_number)
                #     if 'public_domain'==keys[1]:
                #         smk_public_domain=item
                #         print('smk_public_domain='+str(smk_public_domain))
                #     if 'image_width'==keys[1]:
                #         smk_image_width=item
                #         print('smk_image_width='+str(smk_image_width))
                #     if 'image_height'==keys[1]:
                #         smk_image_height=item
                #         print('smk_image_height='+str(smk_image_height))
                #     if 'has_image'==keys[1]:
                #         smk_has_image=item
                #         print('smk_has_image='+str(smk_has_image))

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
                    if claims.get(u'P18'):
                        image=str(claims.get(u'P18')[0].target)
                        # strip [[
                        image=image.replace("[[", "")
                        # strip ]]
                        image=image.replace("]]", "")
                        # replace commons:File with https://commons.wikimedia.org/wiki/Special:FilePath/
                        image=image.replace("commons:File:", "https://commons.wikimedia.org/wiki/Special:FilePath/")
                        
                        wikidata_height=claims.get(u'P18')[0].target.latest_file_info.height
                        wikidata_width=claims.get(u'P18')[0].target.latest_file_info.width
                        wikidata_mime=claims.get(u'P18')[0].target.latest_file_info.mime

                except Exception as e:
                    logging.exception(e)
                print(image)

                # Claim 1476 is the title
                if claims.get(u'P1476'):
                    title=str(claims.get(u'P1476')[0].target.text)
                    print(title)

                # Claim 973 is the documentation url                

                if claims.get(u'P973'):
                    url=str(claims.get(u'P973')[0].target)
                    print(url)

                if claims.get(u'P170'):
                    creator=str(claims.get(u'P170')[0].target)
                    print(creator)

                # Add line to CSV
                f_csv.write(str(number)+ ';' + wikidata_item.id+';'+creator+';'+title+';'+image+';'+url+';'+str(wikidata_height)+';'+str(wikidata_width)+';'+wikidata_mime + '\n')

                # Add line to HTML
                #f_html.write('<tr>'+
                #    '<td><a href="https://wikidata.org/wiki/'+wikidata_item.id+'">'+wikidata_item.id+'</a></td>'
                #    '<td>'+number+'</td>'+
                #    '<td>'+title+'</td>'+
                #    '<td>'+smk_id+'</td>'+
                #    '<td>'+smk_object_number+'</td>'+
                #    '<td><a href="'+url+'">'+url+'</a></td>'+
                #    '<td><a href="'+image+'"><img src="'+image+'" width="100"/></a></td>'+
                #    '<td><a href="'+smk_image_native+'"><img src="'+smk_image_native+'" width="100"/></a></td>'+
                #    '</tr>\r\n')

                items=items+1
            except Exception as e:
                logging.exception(e)
        
        # HTML footer
        #f_html.write('</body>\r\n')
        #f_html.write('</html>\r\n')
        
        #f_csv.close() 
        #f_html.close() 

    except Exception as e:
        logging.error(str(e))
    finally:
        print('items:'+str(items))

# Get all items from Statens Museum for Kunst, Wikidata Object Q671384
#GetInstitutionWikidataItems('Q671384', 'wikidata_smk.csv')

def GetSMKWikidataItem(smk_id):
    # Returns a wikidata item smk_id (P217)
    #
    # The Wikidata Item for the Statens Museum for Kunst colelction is Q671384

    wd_institution = 'Q671384'
    
    # Set up logging
    wikidata_error_log = "wikidata_error.log"
    logging.basicConfig(filename=wikidata_error_log,level=logging.ERROR,format='%(asctime)s %(message)s', datefmt='%Y-%m-%d %H:%M:%S')

    # SPARQL query to execute 
    query = u"""SELECT DISTINCT ?item ?inventarnummer WHERE {
?item wdt:P195 wd:""" + wd_institution + """;
wdt:P217 \"""" + smk_id + """\".
SERVICE wikibase:label { bd:serviceParam wikibase:language "[AUTO_LANGUAGE]". }
OPTIONAL { ?item wdt:P217 ?inventarnummer. }
}
ORDER BY (?inventarnummer)"""


    items = 0
    number = ''
    wikidata_id=''
    try:
        #f_csv=open(output_filename+'.csv', 'w+')
        #f_html=open(output_filename+'.html', 'w+')
        wikidata_site = pywikibot.Site("wikidata", "wikidata")
        generator = pg.WikidataSPARQLPageGenerator(query, site=wikidata_site)

        # CSV header item;number;title;image;url;height;width;mime;smk_id;smk_object_number;smk_image_native;smk_image_height;smk_image_width;smk_public_domain;smk_has_image
        #f_csv.write('number;item;title;image;url;height;width;mime\n')

        # HTML header
        #f_html.write('<html>\r\n')
        #f_html.write('<head><title>'+output_filename+'</title></head>\r\n')
        #f_html.write('<body>\r\n')
        #f_html.write('<table>\r\n')
        #f_html.write('<tr><th>Wikidata Id</th><th>Accension number</th><th>Title</th><th>SMK Id</th><th>SMK Object Number</th><th>SMK URL</th><th>Commons Image</th><th>SMK Image</th><tr>\r\n')

        for wikidata_item in generator:
            try:
                wikidata_id=wikidata_item.id

                print(wikidata_item.id)

                data = wikidata_item.get()
                claims = data.get('claims')
                # Claim 217 is the item number
                number=str(claims.get(u'P217')[0].target)
                print(number)

                # Add line to CSV
                #f_csv.write(wikidata_item.id+';'+str(number)+';'+title+';'+image+';'+url+';'+str(wikidata_height)+';'+str(wikidata_width)+';'+wikidata_mime+';'+smk_id+';'+smk_object_number+';'+smk_image_native+';'+str(smk_image_height)+';'+str(smk_image_width)+';'+str(smk_public_domain)+';'+str(smk_has_image)+'\r\n')

                # Add line to HTML
                #f_html.write('<tr>'+
                #    '<td><a href="https://wikidata.org/wiki/'+wikidata_item.id+'">'+wikidata_item.id+'</a></td>'
                #    '<td>'+number+'</td>'+
                #    '<td>'+title+'</td>'+
                #    '<td>'+smk_id+'</td>'+
                #    '<td><a href="'+image+'"><img src="'+image+'" width="100"/></a></td>'+
                #    '<td>'+smk_object_number+'</td>'+
                #    '<td><a href="'+url+'">'+url+'</a></td>'+
                #    '<td><a href="'+smk_image_native+'"><img src="'+smk_image_native+'" width="100"/></a></td>'+
                #    '</tr>\r\n')

                items=items+1
            except Exception as e:
                logging.exception(e)
        
        # HTML footer
        #f_html.write('</body>\r\n')
        #f_html.write('</html>\r\n')
        
        #f_csv.close() 
        #f_html.close() 

    except Exception as e:
        logging.error(str(e))
    finally:
        print('items:'+str(items))
        
        # return the wikidatanumber
        return wikidata_id

def GetInstitutionWikidataWorksBy(wd_institution, output_filename):
    # Generates a CSV file of artists from the institution with the wikidata Q-number given by
    # institution and saves the results to the file given by csv_filename 
    #
    # The format is item;number;title;image;url
    #
    # The Wikidata Item for the Statens Museum for Kunst colelction is Q671384
    
    # Set up logging
    wikidata_error_log = "wikidata_error.log"
    logging.basicConfig(filename=wikidata_error_log,level=logging.ERROR,format='%(asctime)s %(message)s', datefmt='%Y-%m-%d %H:%M:%S')

    # SPARQL query to execute 
    query = u"""SELECT DISTINCT ?item ?itemLabel WHERE {
  SERVICE wikibase:label { bd:serviceParam wikibase:language "[AUTO_LANGUAGE]". }
  {
    SELECT DISTINCT ?item WHERE {
      ?item p:P6379 ?statement0.
      ?statement0 (ps:P6379/(wdt:P279*)) wd:""" + wd_institution + """.
    }
  }
}"""

    items = 0
    try:
        f_csv=open(output_filename, 'w+')
        #f_html=open(output_filename+'.html', 'w+')
        wikidata_site = pywikibot.Site("wikidata", "wikidata")
        generator = pg.WikidataSPARQLPageGenerator(query, site=wikidata_site)

        # CSV header item;itemLabel
        f_csv.write('item;given_name;family_name\n')
        repo = wikidata_site.data_repository()

        for wikidata_item in generator:
            try:
                item=''
                itemLabel=''

                item = wikidata_item.id
                print(item)

                data = wikidata_item.get()
                claims = data.get('claims')

                # Claim 735 is the given name
                if claims.get(u'P735'):
                    given_name=str(claims.get(u'P735')[0].target.id)
                    item_page = pywikibot.ItemPage(repo, given_name)
                    data = item_page.get()
                    given_name=data['labels']._data['en']
                print(given_name)

                # Claim 735 is the family name
                if claims.get(u'P734'):
                    family_name=str(claims.get(u'P734')[0].target.id)
                    item_page = pywikibot.ItemPage(repo, family_name)
                    data = item_page.get()
                    family_name=data['labels']._data['en']
                print(family_name)

                # Add line to CSV
                f_csv.write(str(item) + ';' + str(given_name) + ';' + str(family_name) + '\n')
                items=items+1
            except Exception as e:
                logging.exception(e)
        
    except Exception as e:
        logging.error(str(e))
    finally:
        print('\r' + str(items), end='', flush=True)

# Get all items from Statens Museum for Kunst, Wikidata Object Q671384
#GetInstitutionWikidataItems('Q671384', 'wikidata_smk.csv')

# Get all works from artist from Statens Museum for Kunst, Wikidata Object Q671384
#GetInstitutionWikidataWorksBy('Q671384', 'wikidata_worksby_smk.csv')

def get_property_value(wikidata_property_id, wikidata_entity_id):
    # Connect to Wikidata
    site = pywikibot.Site("wikidata", "wikidata")

    # Get the Wikidata entity
    entity = pywikibot.ItemPage(site, wikidata_entity_id)

    try:
        # Fetch the P373 value
        property_claim = entity.claims[wikidata_property_id][0]
        property_value = property_claim.getTarget()

        return property_value
    except KeyError:
        # If the P373 property is not found, return None
        return None

# Replace 'Q42' with the Wikidata entity ID you want to query
# wikidata_entity_id = 'Q42'
# wikidata_property_id = 'P373'
# property_value = get_property_value(wikidata_property_id, wikidata_entity_id)

# if property_value:
#     print(f"{wikidata_property_id} value for {wikidata_entity_id}: {property_value}")
# else:
#     print(f"No {wikidata_property_id} value found for {wikidata_entity_id}.")
