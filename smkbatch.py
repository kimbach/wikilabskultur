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
import csvlookup

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

def MapSMKAPIToCommons(batch_title,smk_filter,smk_number_list,download_images):
    """
    Maps SMK API to Wikimedia Commons. Two files is generated for each item (inventory number/assension number)
    <mediafilename> ::=<filename>"."<fileextension>
    <textfilename>  ::=<filename>".txt"

    Example:
        smk_filter=""
        batch_title='selected_works'
        download_images=True

        MapSMKAPIToCommons(batch_title,smk_filter,smk_number_list,download_images)
    
    Keyword arguments:
        batch_title -- name of the batch, used as prefix for HTML and CSV output files, so that batches can be distingushed  
        smk_filter -- dictionary containg filters for the SMK API
        smk_number_list -- dictionary containg specific SMK item numbers to filter on
        download_images -- True if images should be downloaded 

        <batch_title>       ::= {<char>}  
        <smk_filter>        ::= {<filter>}
        <smk_number_list>   ::= {<number>}
        <download_images>   ::= <boolean>
    
    Returns:
        Nothing
    """
    keepFilename = True        #set to True to skip double-checking/editing destination filename
    verifyDescription = False    #set to False to skip double-checking/editing description => change to bot-mode
    #targetSite = pywikibot.Site('beta', 'commons')

    # Get all wikidata items for SMK Wikidata object Q671384
    #wikidata.GetInstitutionWikidataItems('Q671384', 'wikidata_smk')
    try:
        accession_number:str

        # list of items/assencion number to get
        SMKItemList = smk_number_list

        # first item, stops search
        # SMKItemList = ["KKS13358d"]

        # Set up logging
        commons_error_log = "commons_error.log"
        logging.basicConfig(filename=commons_error_log,level=logging.ERROR,format='%(asctime)s %(message)s', datefmt='%Y-%m-%d %H:%M:%S')

        offset=0
        rows=1
        items=0

        output_filename=batch_title

        f_csv=open(output_filename+'.csv', 'w+')
        f_html=open(output_filename+'.html', 'w+')

        artwork = commons.ArtworkTemplate()

        # Print CSV Header
        #csv_header=artwork.GenerateCSVHeader()
        csv_header=artwork.GenerateCSVHeader() + ';public_domain;has_image'
        f_csv.write(csv_header + '\n')
        f_html.writelines('<html>')
        f_html.writelines('<head>')
        f_html.writelines('<title>smkbatch - preview</title>')
        f_html.writelines(u"""'<meta charset="utf-8">
        <meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no">
        <meta name="description" content="">
        <meta name="author" content="">
        <meta content="text/html; charset=UTF-8" http-equiv="content-type">

            <!-- Bootstrap core CSS -->
        <link href="vendor/bootstrap/css/bootstrap.min.css" rel="stylesheet" />

        <script src="js/includeHTML.js"></script>""")
        f_html.writelines('</head><body>')
        f_html.writelines('<table class="table"')
        f_html.writelines('<tr>')
        f_html.writelines('<th>billede</th><th>wikitext</th>')
        f_html.writelines('</tr>')


        while True:
            try:
                if SMKItemList==None:
                    smk_objects=smkapi.get_smk_objects(smk_filter,offset, rows)
                else:
                    if len(SMKItemList)==0:
                        break
                    else:
                        current_number=SMKItemList[0]
                        SMKItemList.remove(current_number)
                        smk_objects=smkapi.get_smk_object(current_number)
                
                items=items+1

                try:
                    print('offset='+str(smk_objects['offset']))
                    offset=smk_objects['offset']
                    print('rows='+str(smk_objects['rows']))
                    rows=smk_objects['rows']
                    print('found='+str(smk_objects['found']))
                    found=smk_objects['found']
                    if offset>found:
                        break
                except:
                    rows=1

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
                smk_categories  = ''
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
                smk_current_location_name = ''
                smk_acquisition_date = ''
                smk_acquisition_date_precision = ''
                smk_notes = ''
                smk_labels = ''

                for item in smk_objects['items']:
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

                        #if smk_object_number not in SMKItemList:
                        #    continue

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
                        smk_creators=''
                        smk_creators_filename=''
                        try:
                            print(item['production'])
                            for production in item['production']:
                                smk_creator=''
                                smk_creator_date_of_death = ''
                                smk_creator_date_of_death_year = ''
                                smk_creator_nationality = ''
                                try:
                                    if smk_creator_forename.tolower() != 'none':
                                        smk_creator_forename = str(production['creator_forename'])
                                except:
                                    smk_creator_forename = ''

                                try:
                                    smk_creator_surname = str(production['creator_surname'])
                                except:
                                    smk_creator_surname = ''

                                try:
                                    smk_creator_notes = str(production['notes'])
                                except:
                                    smk_creator_notes = ''

                                if smk_creator_notes != '':
                                    smk_notes = smk_notes + '* {{da|'+smk_creator_notes +'}}\n'

                                # last name, first name
                                try:
                                    smk_creator= smk_creator_forename + ' ' + smk_creator_surname
                                    smk_creator = smk_creator.lstrip()
                                    smk_creators=smk_creators + '{{Creator:'+smk_creator+'}}'

                                except:
                                    smk_creator = ''
                                try:
                                    smk_creator_date_of_death = str(production['creator_date_of_death'])
                                except:
                                    smk_creator_date_of_death = ''
                                try:
                                    smk_creator_date_of_death_year = str(production['creator_date_of_death_year'])
                                except:
                                    smk_creator_date_of_death_year = ''
                                try:
                                    smk_creator_nationality = str(production['smk_creator_nationality'])
                                except:
                                    smk_creator_nationality = ''
                        except:
                            smk_creator=''
                            smk_creator_date_of_death = ''
                            smk_creator_date_of_death_year = ''
                            smk_creator_nationality = ''
                        
                        smk_creators=smk_creators + '{{Creator:'+smk_creator + '}}\n'

                        print('smk_period=' + smk_period)

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
                    smk_titles=''

                    if item.get('titles'):
                        smk_museumstitel=''

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
                                    if smk_type=='museumstitel':
                                        smk_museumstitel=smk_title
                                        smk_museumstitel_language=str(title['language'])
                                    
                            except:
                                smk_type = ''
                            
                            print('smk_type='+smk_type)

                            iso_code = smkapi.smk_language_code_to_iso_code(smk_language)
                            if smk_museumstitel!='':
                                smk_titles='{{title|'+smk_title + '|lang=' + iso_code +'}}' + smk_titles
                            else:
                                smk_titles='{{' + iso_code +'|' + smk_title + '}}' + smk_titles

                    if item.get('content_description'):
                        smk_description=''
                        for description in item['content_description']: 
                            try:
                                smk_description = smk_description + '{{da|' + str(description) + '}}\n'
                            except:
                                smk_description = smk_description + ''
                        print('smk_description='+smk_description)

                    if item.get('object_names'):
                        smk_object_names = ''
                        smk_categories = '[[Category:Images released under the CC0 1.0 Universal license by Statens Museum for Kunst]]\n'
                        smk_categories = smk_categories + '[[Category:Images from the partnership with Statens Museum for Kunst]]\n'
                        for object_name in item['object_names']: 
                            try:
                                smk_object_name = object_name.get('name')

                                if smk_object_name != '':
                                    object_name_en = smkapi.smk_danish_to_english(smk_object_name)
                                    smk_category = '[[Category:' + object_name_en.capitalize() + 's in Statens Museum for Kunst]]'
                                    smk_categories = smk_categories + smk_category + '\n'
                                    smk_object_names = smk_object_names + object_name_en.capitalize() + '\n'
                            except Exception as e:
                                smk_categories = smk_categories + ''
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

                                if content!="":  
                                    line = '{{inscription '
                                    if content != "":
                                        line = line + '|1=' + content
                                    if position != "":
                                        line = line + '|position=' + smkapi.smk_to_commons_position(position)
                                    if  language != "":
                                        line = line + '|language='+ smkapi.smk_to_commons_language(language)
                                    line = line + '}}'
                                    smk_inscriptions = smk_inscriptions + line + '\n'
                            except:
                                smk_inscriptions = smk_inscriptions + ''
                        print('smk_inscription='+smk_inscriptions)

                    if item.get('labels'):
                        for label in item['labels']: 
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
                                label_date=dateutil.parser.parse(date).strftime("%Y-%m-%d")
                                smk_labels = smk_labels + '* {{da|' + text + '}}\n'
                            except:
                                smk_labels = smk_labels + ''
                        print('smk_labels='+smk_labels)

                    if item.get('dimensions'):
                        try:
                            for dimension in item['dimensions']: 
                                print(dimension['type'])
                                print(dimension['value'])
                                print(dimension['unit'])
                                if 'højde'==dimension['type']:
                                    height=str(dimension['value'])
                                if 'bredde'==dimension['type']:
                                    width=str(dimension['value'])
                                if 'mm'==dimension['unit']:
                                    unit=str(dimension['unit'])
                            smk_dimensions='{{Size|unit='+str(unit)+'|width='+str(width)+'|height='+str(height)+'}}'
                        except:
                            smk_dimensions = ''
                    if item.get('techniques'):
                        smk_techniques = ''
                        for technique in item['techniques']: 
                            try:
                                smk_techniques = smk_techniques + str(technique)+'\n'
                            except:
                                smk_techniques = smk_techniques + ''
                        print('smk_techniques='+smk_techniques)

                    if item.get('notes'):
                        for note in item['notes']: 
                            try:
                                smk_notes = smk_notes + '* {{da|'+str(note)+'}}\n'
                            except:
                                smk_notes = smk_notes + ''
                        print('smk_notes='+smk_notes)


                    if item.get('object_history_note'):
                        smk_object_history_note = ''
                        for object_history in item['object_history_note']: 
                            try:
                                smk_object_history_note = smk_object_history_note + '* {{da|'+str(object_history) + '}}\n'
                            except:
                                smk_object_history_note = smk_object_history_note + ''
                        print('smk_object_history_note=' + smk_object_history_note)
                    if item.get('exhibitions'):
                        smk_exhibitions = ''
                        for exhibition in item['exhibitions']: 
                            try:
                                smk_exhibition_title=str(exhibition['exhibition'])
                                smk_exhibition_date_start=str(exhibition['date_start'])
                                smk_exhibition_date_end=str(exhibition['date_end'])
                                smk_exhibition_venue=str(exhibition['venue'])
                                smk_exhibition_begin = dateutil.parser.parse(smk_exhibition_date_start).strftime("%Y-%m-%d")
                                smk_exhibition_end = dateutil.parser.parse(smk_exhibition_date_end).strftime("%Y-%m-%d")
                                smk_exhibitions = smk_exhibitions + "* {{Temporary Exhibition |name=" + smk_exhibition_title + \
                                  " |institution= |place= " + smk_exhibition_venue + " |begin=" + \
                                    smk_exhibition_begin + " |end=" + \
                                    smk_exhibition_end + "}}\n"
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
                    if item.get('artist'):
                        smk_artists = ''
                        smk_artists_filename=''

                        for artist in item['artist']:
                            smk_artist = ''
                            try:
                                smk_artist = str(artist)
                            except:
                                smk_artist = ''
                            if smk_artist != '':
                                smk_artists_filename=smk_artists_filename+smk_artist+' - '
                                if smk_artist.lower() != 'ubekendt':
                                    smk_artists=smk_artists+'{{Creator:'+smk_artist+'}}\n'
                                else:
                                    smk_artists=smk_artists+smk_artist+'\n'
                            print('smk_artist='+smk_artist)
                        # Strip trailing delimiter " - "
                        artists_filename_delim = str(' - ')
                        artists_filename_delim_length = len(artists_filename_delim)
                        if smk_artists_filename[-artists_filename_delim_length:] == ' - ':
                            smk_artists_filename=smk_artists_filename[0:-artists_filename_delim_length]
                        print('smk_artists='+smk_artists)
                    # Note:department is not used yet 
                    #if item.get('responsible_department'):
                    #    try:
                    #        smk_responsible_department = item.get('responsible_department')
                    #    except:
                    #        smk_responsible_department = ''
                    #    print('smk_responsible_department='+str(smk_responsible_department))
                    line = ''
                    if item.get('documentation'):
                        smk_documentation = ''
                        for documentation in item['documentation']: 
                            try:
                                line = smkapi.smk_documentation_to_commons_citation(documentation)
                                smk_documentation = smk_documentation + '*' + line + '\n'
                            except Exception as e:
                                smk_documentation = smk_documentation + ''
                        print('smk_documentation='+str(smk_documentation))

                    if item.get('current_location_name'):
                        smk_current_location_name = ''
                        try:
                            smk_current_location_name = item.get('current_location_name')
                        except:
                            smk_current_location_name = ''
                        print('smk_current_location_name='+str(smk_current_location_name))
                    if item.get('acquisition_date'):
                        smk_acquisition_date = ''
                        try:
                            smk_acquisition_date = item.get('acquisition_date')
                        except:
                            smk_acquisition_date = ''
                        print('smk_acquisition_date='+str(smk_acquisition_date))
                    if item.get('acquisition_date_precision'):
                        smk_acquisition_date_precision = ''
                        try:
                            smk_acquisition_date_precision = item.get('acquisition_date_precision')
                        except:
                            smk_acquisition_date_precision = ''
                        print('smk_acquisition_date_precision='+str(smk_acquisition_date_precision))

                # try to get wikidatanumber

                wd_number = csvlookup.find_wikidata_item(smk_object_number)
                # wd_number = wikidata.GetSMKWikidataItem(smk_object_number)

                # Generate artwork template
    #            if smk_description != '': 
    #                smk_description = str('{{da|1=' + smk_description + '}}'),
                smk_object_history_note = smk_object_history_note + \
                    '* {{ProvenanceEvent|date='+smk_acquisition_date_precision+'|type=acquisition|newowner=[[Statens Museum for Kunst]]}}'
                artwork = commons.ArtworkTemplate(artist = smk_artists,
                    nationality =  smk_creator_nationality,
                    author = '',
                    title = smk_titles,
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
                    notes = smk_notes+smk_labels,
                    accession_number = smk_object_number,
                    place_of_creation = '',
                    #'https://collection.smk.dk/#/en/detail/'+accession_number
                    source = '* {{SMK API|'+accession_number+'}}\n' +  \
                        '* {{SMK Open|'+accession_number+'}}\n' + \
                        '* [' + smk_image_native + ' image]',                    
                    permission = '{{Licensed-PD-Art|PD-old|Cc-zero}}\n' + \
                        '\t{{Statens Museum for Kunst collaboration project}}',
                    other_versions = '',
                    references = smk_documentation,
                    depicted_place = '',
                    wikidata = wd_number,
                    categories = smk_categories,
                    imageurl = smk_image_native,
                    image_height = smk_image_height,
                    image_width = smk_image_width,
                    object_type = smk_object_names,
                    location = smk_current_location_name)

                artwork.GenerateWikiText()
                
    #            csvline = artwork.GenerateCSVLine()
                csvline = artwork.GenerateCSVLine() + ';' + str(smk_public_domain) + ';'+ str(smk_has_image) 
                csvline = csvline.replace('\n', '<br/>')

                # Print CSV line
                f_csv.write(csvline + '\n')

                # download smk_image_native
                if smk_has_image == 'True':
                    filetype = pathlib.Path(smk_image_native).suffix
                    filename = 'SMK_' + smk_object_number + '_' + smk_artist + '_-_' + smk_museumstitel
                    filename = 'SMK_' + smk_object_number + '_' + smk_artist + '_-_' + smk_museumstitel
                    # <kunstnernavn>, <titel>, <årstal>, <inventarnummer>, <samling>                 
                    filename = smk_artists_filename + ', ' + smk_museumstitel + ', ' + smk_period + ', ' + accession_number + ', ' + 'Statens Museum for Kunst' 
                    filename = filename.replace("\"", "")
                    filename = filename.replace("?", "")
                    filename = filename.replace("/", "-")
                    filename = filename.replace("(", "")
                    filename = filename.replace(")", "")
                    short_filename = textwrap.shorten(filename, width=235-len('.'+filetype), placeholder='...')
                    folder = './downloads/'
                    imagepath = folder + short_filename + filetype
                    if download_images:
                        if not os.path.exists(imagepath):
                            # only download file if it doens't already exist
                            r = requests.get(smk_image_native, allow_redirects=True)
                            open(imagepath, 'wb').write(r.content)

                            image_found = commons.check_image_hash(imagepath)

                    path = folder + short_filename + '.txt'
                    artwork.GenerateWikiText()
                    license = """=={{int:license-header}}==
    {{Licensed-PD-Art|PD-old-auto-1923|Cc-zero|deathyear=""" + smk_creator_date_of_death_year+ """}}
    """
                    license = ''
                    wikitext = artwork.wikitext + '\n' + license + '\n' + str(smk_categories)
                    open(path, 'w').write(wikitext)
                    f_html.writelines('<tr>')
                    f_html.writelines('</td><td><a href="' + smk_image_native + '"><img src="' + imagepath + '" width="300" /> <br/></a><a href="' + smk_image_native + '">' + artwork.title + '</a></td><td>' + wikitext.replace('\n', '<br/>'))
                    f_html.writelines('</tr>')

            except Exception as e:
                print('EXCEPTION!')
                typeerror=TypeError(e)
                logging.exception(e)
            finally:
                print('items='+str(items))
                offset=offset+1

            if 0==rows:
                break

        f_html.writelines('</table>')
        f_html.writelines('</body></html>')
        f_html.close()
        f_csv.close() 
        
    except Exception as e:
        logging.exception(e)
    finally:
        print('Export finished')
        print('items='+str(items))
        offset=offset+1

smk_number_list = ["KMS3625", 
    "KMSsp211", 
    "DEP289", 
    "KKSgb7087", 
    "KKS13568", 
    "KMS7020", 
    "KMS4231", 
    "KMS8847", 
    "KKSgb5548", 
    "KKS2621"]
smk_filter_list = [["public_domain","true"],
    ["has_image", "true"],
    ["creator_gender", "kvinde"],
    ["creator_nationality", "dansk"]]

# Generate SMK API filters from filter list
smk_filter=smkapi.generate_smk_filter(smk_filter_list)
#url='https://api.smk.dk/api/v1/art/search/?keys=*&filters=%5Bpublic_domain%3Atrue%5D,%5Bhas_image%3Atrue%5D,%5Bcreator_gender%3Akvinde%5D,%5Bcreator_nationality%3Adansk&offset='+str(offset)+'&rows='+str(rows)
offset=0
rows=1

#smk_number_list=None
smk_filter=""
#batch_title='all_public_domain_images'
#batch_title='all_works'
batch_title='selected_works'
#download_images=False
download_images=True

MapSMKAPIToCommons(batch_title,smk_filter,smk_number_list,download_images)
