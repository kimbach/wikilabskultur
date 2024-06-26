# smkbatch
#
# Functions for SMK Batch Upload
#
# This code parses date/times, so please
#
#     pip install python-dateutil
#
# To use this code, make sure you
#
#     import json
#
# and then, to convert JSON from a string, do
#
#     result = empty_from_dict(json.loads(json_string))

from dataclasses import dataclass
from typing import Any, Optional, List, TypeVar, Type, Callable, cast
from enum import Enum
from datetime import datetime
import dateutil.parser
import json
import requests
import pathlib
import smkitem
import commons
import wikidata
import os
import pywikibot
from pywikibot import pagegenerators as pg
import logging
import traceback
import sys
import textwrap
import re
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

def string_convert(obj, keys=(object)):
    if isinstance(obj, dict):
        for k, v in obj.items():
            yield from recursive_iter(v, keys + (k,))
    elif any(isinstance(obj, t) for t in (list, tuple)):
        for idx, item in enumerate(obj):
            yield from recursive_iter(item, keys + (idx,))
    else:
        yield keys, obj

def TestSMKAPI():
    #url = [ filename ]
    #keepFilename = False        #set to True to skip double-checking/editing destination filename
    keepFilename = True        #set to True to skip double-checking/editing destination filename
    #verifyDescription = True    #set to False to skip double-checking/editing description => change to bot-mode
    verifyDescription = False    #set to False to skip double-checking/editing description => change to bot-mode
    #targetSite = pywikibot.Site('beta', 'commons')

    #bot = UploadRobot(url, description=description, useFilename=pagetitle, keepFilename=keepFilename, verifyDescription=verifyDescription, targetSite=targetSite)
    #bot.run()

    # Get JSON from the SMK API
    #json_string = json.loads(requests.get("https://api.smk.dk/api/v1/art/search/?keys=*&filters=%5Bpublic_domain%3Atrue%5D,%5Bhas_image%3Atrue%5D&offset=0&rows=10").text)
    #json_string = json.loads(requests.get("https://api.smk.dk/api/v1/art/search/?keys=*&filters=%5Bobject_number%3AKMS1%5D").text)

    #THIS_FOLDER = os.path.dirname(os.path.abspath(__file__))
    #my_file = os.path.join(THIS_FOLDER, 'smkitems.json')

    #json_file = open(my_file)
    #json_string = json.load(json_file)

    # Map to obejct model
    #smk_items = smkitem.empty_from_dict(json_string)

    # Add categories
    smk_categories  = """[[Category:Wiki Labs Kultur]]
    [[Category:Paintings in Statens Museum for Kunst]]"""

    # Iterate over Items
    # for item in smk_items.items:
    
    #     # Check for image
    #     if item.has_image: 
    #         filename=item.image_native
    #         path=pathlib.Path(filename)
            
    #         # Generate page title
    #         pagetitle='SMK-' + item.id + '-' + item.object_number + ':' + item.titles[0].title + path.suffix

    #         # Generate description
    #         desc = ''
    #         if item.content_description is not None:
    #             for line in item.content_description:
    #                 desc=desc+line
            
    #         # Generate date
    #         production_date = ''
    #         for date in item.production_date:
    #             production_date = production_date+date.start.strftime("%Y-%m-%d")+' - '+date.end.strftime("%Y-%m-%d")+'\n'  


    #         #complete_artwork_desc_and_upload(filename, pagetitle, desc, production_date, categories)

    #         # Generate artwork template
    #         artwork = commons.ArtworkTemplate(artist = '',
    #             author = '',
    #             title = '',
    #             desc = desc,
    #             depicted_people = '',
    #             date = production_date,
    #             medium = '',
    #             dimensions = '',
    #             institution = '',
    #             department = '',
    #             place_of_discovery = '',
    #             object_history = '', 
    #             exhibition_history = '',
    #             credit_line = '',
    #             inscriptions = '',
    #             notes = '',
    #             accession_number = item.object_number,
    #             place_of_creation = '',
    #             source = '',
    #             permission = '',
    #             other_versions = '',
    #             references = '',
    #             depicted_place = '',
    #             wikidata = '',
    #             categories = categories)

    #             #artwork.GenerateWikiText()

    #         print ('id           =' + item.id)
    #         print ('object_number=' + item.object_number)
    #         print ('image_native =' + item.image_native)
    #         print (artwork.wikitext)

# Get all wikidata items for SMK Wikidata object Q671384
#wikidata.GetInstitutionWikidataItems('Q671384', 'wikidata_smk')
try:
    accession_number:str
    # Set up logging
    commons_error_log = "commons_error.log"
    logging.basicConfig(filename=commons_error_log,level=logging.ERROR,format='%(asctime)s %(message)s', datefmt='%Y-%m-%d %H:%M:%S')

    offset=27670+31231+17920+10750
    rows=1
    items=0

    output_filename='commons_smk'

    f_csv=open(output_filename+'.csv', 'w+')

    artwork = commons.ArtworkTemplate()

    # Print CSV Header
    #csv_header=artwork.GenerateCSVHeader()
    csv_header=artwork.GenerateCSVHeader() + ';public_domain;has_image'
    f_csv.write(csv_header + '\n')

    while True:
        try:
            #smkapi.get_smk_object('KMS1')

            items=items+1
            # smk_objects=smkapi.get_smk_objects(offset, rows)
            smk_objects=smkapi.get_smk_objects(offset, rows)
            print('offset='+str(smk_objects['offset']))
            offset=smk_objects['offset']
            print('rows='+str(smk_objects['rows']))
            rows=smk_objects['rows']
            print('found='+str(smk_objects['found']))
            found=smk_objects['found']

            accession_number=''
            smk_creator=''
            smk_title=''
            smk_period=''
            production_date=''
            desc=''
            smk_dimensions = ''
            smk_object_names = ''
            smk_inscriptions = ''
            smk_production_date = ''
            smk_categories  = '[[Category:SMKOpen Batch Upload]]\n'
            smk_image_native  = ''
            smk_image_height = ''
            smk_image_width = ''
            smk_has_image = ''
            smk_public_domain = ''
            smk_creator_nationality = ''
            smk_techniques = ''
            smk_object_history_note = ''
            smk_exhibitions = ''
            smk_collection = ''
            smk_responsible_department = ''
            smk_documentation = ''
            smk_description = ''

            for item in smk_objects['items']:
                smk_id = ''
                if item.get('id'):
                    try:
                        smk_id = str(item.get('id'))
                    except:
                        smk_id = ''
                print('smk_id=' + smk_id)

                if item.get('image_native'):
                    smk_image_native=''
                    try:
                        if item.get('image_native'):
                            smk_image_native=str(item['image_native'])
                    except:
                        smk_image_native=''
                    print('smk_image_native =' + smk_image_native)
                if item.get('image_width'):
                    smk_image_width=''
                    try:
                        if item.get('smk_image_width'):
                            smk_image_width=str(item['image_width'])
                    except:
                        smk_image_width=''
                    print('smk_image_width =' + smk_image_width)

                if item.get('image_height'):
                    smk_image_height=''
                    try:
                        if item.get('smk_image_height'):
                            smk_image_height=str(item['image_height'])
                    except:
                        smk_image_height=''
                    print('smk_image_height =' + smk_image_height)
                if item.get('object_number'):
                    accession_number=''
                    smk_object_number=''
                    try:
                        if item.get('object_number'):
                            accession_number=str(item['object_number'])
                    except:
                        accession_number=''
                    smk_object_number=accession_number
                    print('smk_object_number =' + smk_object_number)
                if item.get('public_domain'):
                    smk_public_domain = ''
                    try:
                        if item.get('public_domain'):
                            smk_public_domain = str(item['public_domain'])
                    except:
                        smk_public_domain = ''
                    print(smk_public_domain)
                if item.get('has_image'):
                    smk_has_image = '' 
                    try:
                        if item.get('has_image'):
                            smk_has_image = str(item['has_image'])
                    except:
                        smk_has_image = '' 
                    print(smk_has_image)
                if item.get('production'):
                    smk_creator=''
                    smk_creator_date_of_death = ''
                    smk_creator_date_of_death_year = ''
                    smk_creator_nationality = ''
                    try:
                        if item.get('production'):
                            print(item['production'])
                            try:
                                smk_creator_forename = str(item['production'][0].get('creator_forename'))
                            except:
                                smk_creator_forename = ''

                            try:
                                smk_creator_surname = str(item['production'][0].get('creator_surname'))
                            except:
                                smk_creator_surname = ''

                            # last name, first name
                            try:
                                smk_creator=smk_creator_forename+' '+ smk_creator_surname
                                smk_creator = smk_creator.lstrip()
                            except:
                                smk_creator = ''
                            try:
                                smk_creator_date_of_death = str(item['production'][0].get('creator_date_of_death'))
                            except:
                                smk_creator_date_of_death = ''
                            try:
                                smk_creator_date_of_death_year = str(smk_creator_date_of_death[:4])
                            except:
                                smk_creator_date_of_death_year = ''
                            try:
                                smk_creator_nationality = str(item['production'][0].get('creator_nationality'))
                            except:
                                smk_creator_nationality = ''
                    except:
                        smk_creator=''
                        smk_creator_date_of_death = ''
                        smk_creator_date_of_death_year = ''
                        smk_creator_nationality = ''

                    print('smk_creator='+smk_creator)
                    print('smk_creator_date_of_death_year='+smk_creator_date_of_death_year)
                    print('smk_creator_nationality='+smk_creator_nationality)
                if item.get('production_date'):
                    smk_period = ''
                    try:
                        for production_date in item['production_date']:
                            try:
                                smk_period = smk_period + str(production_date.get('period'))
                            except:
                                smk_period = smk_period + ''
                    except:
                        smk_period = smk_period + ''

                    print('smk_period=' + smk_period)
                if item.get('titles'):
                    for title in item['titles']: 
                        smk_language=''
                        smk_type=''
                        try:
                            if title['title']:
                                    smk_title=str(title['title'])
                        except:
                            smk_title=''
                        print('smk_title='+smk_title)

                        try:
                            if title['language']:
                                smk_language=str(title['language'])
                        except:
                            smk_language=''

                        try:
                            if title['type']:
                                smk_type=str(title['type'])
                        except:
                            smk_type = ''
                        
                        print('smk_type='+smk_type)

                if item.get('content_description'):
                    smk_description=''
                    for description in item['content_description']: 
                        try:
                            smk_description = smk_description + str(description) + '\n'
                        except:
                            smk_description = smk_description + ''
                    print('smk_description='+smk_description)

                if item.get('object_names'):
                    smk_object_names = ''
                    smk_categories = ''
                    for object_name in item['object_names']: 
                        try:
                            smk_object_names = smk_object_names + str(object_name.get('name'))
                            if object_name.get('name') == 'kobberstik':
                                # kobberstik
                                smk_category = '[[Cateogry:Engravings in Statens Museum for Kunst]]'
                            elif object_name.get('name') == 'maleri':
                                # maleri
                                smk_category = '[[Cateogry:Paintings in Statens Museum for Kunst]]'
                            elif object_name.get('name') == 'tegning':
                                # maleri
                                smk_category = '[[Cateogry:Drawings in Statens Museum for Kunst]]'
                            elif object_name.get('name') == 'skulptur':
                                # skulptur
                                smk_category = '[[Category:Sculptures in Statens Museum for Kunst]]'
                            
                            smk_categories = smk_categories + smk_category + '\n'
                        except:
                            smk_object_names = smk_object_names + ''
                    print('smk_object_names='+smk_object_names)
                    print('smk_categories='+smk_categories)

                if item.get('inscriptions'):
                    for inscription in item['inscriptions']: 
                        try:
                            line = ''
                            content = ''
                            language=''
                            position='' 
                            if inscription.get('content') is not None:
                                content = str(inscription.get('content'))

                            if inscription.get('language') is not None:
                                language = str(inscription.get('language')) 

                            if inscription.get('position') is not None:
                                position = str(inscription.get('position'))
                            line = content + ', ' + language + ', ' + position 
                            smk_inscriptions = smk_inscriptions + line + '\n'
                        except:
                            smk_inscriptions = smk_inscriptions + ''
                    print('smk_inscription='+smk_inscriptions)

                if item.get('label'):
                    for label in item['label']: 
                        try:
                            text = ''
                            type=''
                            source= ''
                            date='' 
                            if label.get('text') is not None:
                                text = str(label.get('text'))
                            if label.get('type') is not None:
                                type = str(label.get('type')) 
                            if label.get('source') is not None:
                                source = str(label.get('source'))
                            if label.get('date') is not None:
                                date = str(label.get('date'))
                            line = text + ', ' + type + ', ' + source + ', ' + date 
                            smk_label = smk_label + line + '\n'
                        except:
                            smk_label = smk_label + ''
                    print('smk_label='+smk_label)

                if item.get('dimensions'):
                    try:
                        for dimension in item['dimensions']: 
                            print(dimension['type'])
                            print(dimension['value'])
                            print(dimension['unit'])
                            if 'hojde'==dimension['type']:
                                height=str(dimension['value'])
                            if 'bredde'==dimension['type']:
                                width=str(dimension['value'])
                            if 'mm'==dimension['unit']:
                                unit=str(dimension['unit'])
                        smk_dimensions='{{Size|unit='+str(unit)+'|width='+str(width)+'|height='+str(height)+'}}'
                    except:
                        smk_dimensions = ''
                if item.get('techniques'):
                    for technique in item['techniques']: 
                        try:
                            smk_techniques = smk_techniques + str(technique) + '\n'
                        except:
                            smk_techniques = smk_techniques + ''
                    print('smk_techniques='+smk_techniques)

                if item.get('object_history_note'):
                    smk_object_history_note = ''
                    for object_history in item['object_history_note']: 
                        try:
                            smk_object_history_note = smk_object_history_note + str(object_history) + '\n'
                        except:
                            smk_object_history_note = smk_object_history_note + ''
                    print('smk_object_history_note=' + smk_object_history_note)
                if item.get('exhibitions'):
                    smk_exhibitions = ''
                    for exhibition in item['exhibitions']: 
                        try:
                            smk_exhibitions = smk_exhibitions + str(exhibition) + '\n'
                        except:
                            smk_exhibitions = smk_exhibitions + ''
                    print('smk_exhibitions='+smk_exhibitions)
                if item.get('collection'):
                    smk_collection = ''
                    for collection in item['collection']: 
                        try:
                            smk_collection = smk_collection + str(collection) + '\n'
                        except:
                            smk_collection = smk_collection + ''
                    print('smk_collection='+smk_collection)
                if item.get('responsible_department'):
                    try:
                        smk_responsible_department = item.get('responsible_department')
                    except:
                        smk_responsible_department = ''
                    print('smk_responsible_department='+str(smk_responsible_department))
                if item.get('documentation'):
                    smk_documentation = ''
                    for documentation in item['documentation']: 
                        try:
                            title = ''
                            author = ''
                            notes = ''
                            shelfmark  = ''
                            if documentation.get('title') is not None:
                                title = str(documentation.get('title'))
                            if documentation.get('author') is not None:
                                author = str(documentation.get('author')) 
                            if documentation.get('notes') is not None:
                                notes = str(documentation.get('notes'))
                            if documentation.get('shelfmark') is not None:
                                shelfmark = str(documentation.get('shelfmark'))
                            line = title + ', ' + author + ', ' + notes + ', ' + shelfmark 
                            smk_documentation = smk_documentation + line + '\n'
                        except:
                            smk_documentation = smk_documentation + ''
                    print('smk_documentation='+str(smk_documentation))

                #artwork.GenerateWikiText()
                #print(artwork.GenerateCSVLine())

            wd_number = ''
            # try to get wikidatanumber
            # wd_number = wikidata.GetSMKWikidataItem(smk_object_number)

            # Generate artwork template
#            if smk_description != '': 
#                smk_description = str('{{da|1=' + smk_description + '}}'),

            artwork = commons.ArtworkTemplate(artist = smk_creator,
                nationality =  smk_creator_nationality,
                author = '',
                title = smk_title,
                desc = smk_description,
                depicted_people = '',
                date = smk_period,
                medium = smk_techniques,
                dimensions = smk_dimensions,
                institution = '{{Institution:Statens Museum for Kunst, Copenhagen}}',
                department = smk_responsible_department,
                place_of_discovery = '',
                object_history = smk_object_history_note, 
                exhibition_history = smk_exhibitions,
                credit_line = '',
                inscriptions = smk_inscriptions,
                notes = smk_object_names,
                accession_number = smk_object_number,
                place_of_creation = '',
                #'https://collection.smk.dk/#/en/detail/'+accession_number
                source = '{{SMK online|'+accession_number+'}}',
                permission = '{{Licensed-PD-Art|PD-old-auto-1923|Cc-zero|deathyear=' + smk_creator_date_of_death_year+ '}}',
                other_versions = '',
                references = smk_documentation,
                depicted_place = '',
                wikidata = wd_number,
                categories = smk_categories,
                imageurl = smk_image_native,
                image_height = smk_image_height,
                image_width = smk_image_width)

            artwork.GenerateWikiText()
            
#            csvline = artwork.GenerateCSVLine()
            csvline = artwork.GenerateCSVLine() + ';' + str(smk_public_domain) + ';'+ str(smk_has_image) 
            csvline = csvline.replace('\n', '<br/>')

            # Print CSV line
            f_csv.write(csvline + '\n')

            # download smk_image_native
            if smk_has_image == True:
                filetype = pathlib.Path(smk_image_native).suffix
                filename = 'SMK_' + smk_object_number + '_' + smk_creator + '_-_' + smk_title
                filename = 'SMK_' + smk_object_number + '_' + smk_creator + '_-_' + smk_title
                # <kunstnernavn>, <titel>, <årstal>, <inventarnummer>, <samling>                 
                filename = smk_creator + ', ' + smk_title + ', ' + smk_period + ', ' + accession_number + ', ' + 'Statens Museum for Kunst' 
                filename = filename.replace("\"", "")
                filename = filename.replace("?", "")
                filename = filename.replace("/", "-")
                filename = filename.replace("(", "")
                filename = filename.replace(")", "")
                short_filename = textwrap.shorten(filename, width=235-len('.'+filetype), placeholder='...')
                folder = './downloads/'
                path = folder + filename + filetype
                #if not os.path.exists(path):
                    # only download file if it doens't already exist
                    #r = requests.get(smk_image_native, allow_redirects=True)
                    #open(path, 'wb').write(r.content)
                path = folder + filename + '.txt'
                #artwork.GenerateWikiText()
                license = """=={{int:license-header}}==
{{Licensed-PD-Art|PD-old-auto-1923|Cc-zero|deathyear=""" + smk_creator_date_of_death_year+ """}}
"""
    
                wikitext = artwork.wikitext + '\n' + license + '\n' + str(smk_categories)
                # open(path, 'w').write(wikitext)

        except Exception as e:
            print('EXCEPTION!')
            typeerror=TypeError(e)
            logging.exception(e)
        finally:
            print('items='+str(items))
            offset=offset+1

        if 0==rows:
            break
    f_csv.close() 
    
except Exception as e:
    logging.exception(e)
finally:
    print('Export finished')
    print('items='+str(items))
    offset=offset+1


#TestSMKAPI()
#get_smk_object('KMS1')
