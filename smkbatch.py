""" 
smkbatch.py

Module that implements functions for performing upload of media from
Statens Museum for Kunst (SMK) to Wikimedia Commons 
using the pwikiibot framework as part of a collaboration between 
SMK and Wikimedia Denmark

For more details, refer to the project page on Commons:
https://commons.wikimedia.org/wiki/Commons:SMK_-_Statens_Museum_for_Kunst

Use:
MapSMKAPIToCommons(batch_title,smk_filter,smk_number_list,download_images, upload_images, max_number_of_images)
"""

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
import smkitem
import testobjectmodel

debug_level=1

folder = './downloads2/'

def debug_msg(msg, debug_level=1):
    if debug_level>0:
        print(msg)

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

def MapSMKAPIToCommons(batch_title,smk_filter,smk_number_list,download_images, upload_to_commons, batch_size, save_json, save_wikitext, debug_level=0):
    """
    Maps SMK API to Wikimedia Commons. Two files is generated for each item (inventory number/assension number)
    <mediafilename> ::=<filename>"."<fileextension>
    <textfilename>  ::=<filename>".txt"

    Example:
        batch_title='selected_works'
        smk_filter=""
        download_images=True

        MapSMKAPIToCommons('selected_works','','',True,10)
    
    Keyword arguments:
        batch_title -- name of the batch, used as prefix for HTML and CSV output files, so that batches can be distingushed  
        smk_filter -- dictionary containg filters for the SMK API
        smk_number_list -- dictionary containg specific SMK item numbers to filter on
        download_images -- True if images should be downloaded 
        upload_to_commons -- True if images should be uploaded 
        batch_size -- The max number of items to upload (batch size), set to -1 to generate full batch
        save_json -- True if RAW JSON should be saved 
        save_wikitext -- True if wikitext should be saved 
        debug_level

        <batch_title>       ::= {<char>}  
        <smk_filter>        ::= {<filter>}
        <smk_number_list>   ::= {<number>}
        <download_images>   ::= <boolean>
        <upload_to_commons> ::= <boolean>
        batch_size          ::= [-1] | <number>{<number>}
    
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
        batch_log_filename = output_filename
        f_batch_log=open(batch_log_filename+'.log', 'w+')
        f_batch_log.writelines("time;pagetitle;accession_number;wikidata;image_exists;bot_status;file_hash\n")

        f_csv=open(output_filename+'.csv', 'w+')
        f_html=open(output_filename+'.html', 'w+')

        artwork = commons.ArtworkTemplate()

        # Print CSV Header
        #csv_header=artwork.GenerateCSVHeader()
        csv_header=artwork.GenerateCSVHeader()
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

        files_uploaded=0
        while True:
            smk_json=""
            # Check for batch size
            if batch_size > 0:
                if files_uploaded>=batch_size:
                    break
            try:
                if SMKItemList==None:
                    smk_json=smkapi.get_smk_objects(smk_filter,offset, rows)
                else:
                    if len(SMKItemList)==0:
                        break
                    else:
                        current_number=SMKItemList[0]
                        SMKItemList.remove(current_number)
                        smk_json=smkapi.get_smk_object(current_number)
                
                # Convert json string to object
                smk_objects=json.loads(smk_json)
                
                #smk_object_model = testobjectmodel.welcome_from_dict(smk_objects)
                #print(smk_object_model)

                items=items+1

                try:
                    debug_msg('offset='+str(smk_objects['offset']),debug_level)
                    offset=smk_objects['offset']
                    debug_msg('rows='+str(smk_objects['rows']),debug_level)
                    rows=smk_objects['rows']
                    debug_msg('found='+str(smk_objects['found']),debug_level)
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
                file_hash=0
                smk_other_fields = ''

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
                        debug_msg('smk_object_number =' + smk_object_number,debug_level)

                        #if smk_object_number not in SMKItemList:
                        #    continue

                    smk_id = ''
                    if item.get('id'):
                        try:
                            smk_id = str(item.get('id'))
                        except:
                            smk_id = ''
                    debug_msg('smk_id=' + smk_id,debug_level)

                    smk_created = ''
                    if item.get('created'):
                        try:
                            smk_created = str(item.get('created'))
                        except:
                            smk_created = ''
                    if smk_created!='':
                        smk_other_fields=smk_other_fields+'{{Information field|SMK record created|'+smk_created+'}}\n'
                    debug_msg('smk_created=' + smk_created,debug_level)

                    smk_modified = ''
                    if item.get('modified'):
                        try:
                            smk_modified = str(item.get('modified'))
                        except:
                            smk_modified = ''
                    debug_msg('smk_modified=' + smk_modified,debug_level)
                    if smk_modified!='':
                        smk_other_fields=smk_other_fields+'{{Information field|SMK record modified|'+smk_modified+'}}\n'

                    smk_iiif_manifest=''
                    if item.get('iiif_manifest'):
                        try:
                            smk_iiif_manifest = str(item.get('iiif_manifest'))
                        except:
                            smk_iiif_manifest = ''
                    debug_msg('smk_iiif_manifest=' + smk_iiif_manifest,debug_level)
                    
                    if smk_iiif_manifest!='':
                        smk_other_fields=smk_other_fields+'{{Information field|iiif manifest|'+'{{Url|'+smk_iiif_manifest+'|link}}}}\n'

                    if item.get('image_native'):
                        smk_image_native=''
                        try:
                            if item.get('image_native'):
                                smk_image_native=str(item['image_native'])
                        except:
                            smk_image_native=''
                        debug_msg('smk_image_native =' + smk_image_native,debug_level)
                    if item.get('image_width'):
                        smk_image_width=''
                        try:
                            if item.get('smk_image_width'):
                                smk_image_width=str(item['image_width'])
                        except:
                            smk_image_width=''
                        debug_msg('smk_image_width =' + smk_image_width,debug_level)

                    if item.get('image_height'):
                        smk_image_height=''
                        try:
                            if item.get('smk_image_height'):
                                smk_image_height=str(item['image_height'])
                        except:
                            smk_image_height=''
                        debug_msg('smk_image_height =' + smk_image_height,debug_level)

                    try:
                        smk_public_domain = str(item['public_domain'])
                    except:
                        smk_public_domain = ''

                    try:
                        smk_has_image = str(item['has_image'])
                    except:
                        smk_has_image = '' 

                    if item.get('production'):
                        smk_creators=''
                        smk_creators_filename=''
                        try:
                            debug_msg(item['production'],debug_level)
                            for production in item['production']:
                                smk_creator=''
                                smk_creator_forename=''
                                smk_creator_surname=''
                                smk_creator_date_of_death = ''
                                smk_creator_nationality = ''
                                smk_creator_date_of_birth =''
                                smk_creator_gender=''
                                smk_creator_lref=''

                                try:
                                    smk_creator_forename = str(production['creator_forename'])
                                    smk_temp=smk_creator_forename.lower()
                                    if smk_temp == 'none':
                                        smk_creator_forename=''
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
                                    smk_creator_nationality = str(production['creator_nationality'])
                                except:
                                    smk_creator_nationality = ''
                                try:
                                    smk_creator_date_of_birth=str(production['creator_date_of_birth'])                       
                                except:
                                    smk_creator_date_of_birth =''
                                try:
                                    smk_creator_gender=str(production['creator_gender'])                                    
                                except:
                                    smk_creator_gender=''
                                try:
                                    smk_creator_lref=str(production['creator_lref'])
                                except:
                                    smk_creator_lref=''
                        except:
                            smk_creator=''
                            smk_creator_date_of_death = ''
                            smk_creator_nationality = ''
                        
                        smk_creators=smk_creators + '{{Creator:'+smk_creator + '}}\n'

                        debug_msg('smk_period=' + smk_period,debug_level)

                        debug_msg('smk_creator='+smk_creator,debug_level)
                        debug_msg('smk_creator_nationality='+smk_creator_nationality,debug_level)
                    if item.get('production_date'):
                        smk_period = ''
                        try:
                            for production_date in item['production_date']:
                                try:
                                    smk_period = smk_period + production_date.get('period')
                                except:
                                    smk_period = smk_period + ''
                        except:
                            smk_period = smk_period + ''

                        debug_msg('smk_period=' + smk_period,debug_level)
                    smk_titles=''

                    if item.get('titles'):
                        smk_museumstitel=''
                        smk_title=''

                        # assume that the first title is the museumstitle
                        try:
                            if len(item['titles'])>0: 
                                smk_museumstitel = str(item['titles'][0]['title']) 
                        except:
                            smk_museumstitel=''

                        for title in item['titles']: 
                            smk_language=''
                            smk_type=''
                            try:
                                if title['title']:
                                    smk_title=str(title['title'])
                            except:
                                smk_title=''
                            debug_msg('smk_title='+smk_title,debug_level)
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
                            except:
                                smk_type = ''
                            
                            debug_msg('smk_type='+smk_type,debug_level)

                            iso_code = smkapi.smk_language_code_to_iso_code(smk_language)
                            if smk_museumstitel!='':
                                smk_titles='{{title|'+smk_title + '|lang=' + iso_code +'}}' + smk_titles
                            else:
                                smk_titles='{{' + iso_code +'|' + smk_title + '}}' + smk_titles

                        if smk_museumstitel!='':
                            smk_title=smk_museumstitel
                        else:
                            smk_title = 'Untitled' 
                        
                    if item.get('content_description'):
                        smk_description=''
                        for description in item['content_description']: 
                            try:
                                smk_description = smk_description + '* {{da|' + str(description) + '}}\n'
                            except:
                                smk_description = smk_description + ''
                        debug_msg('smk_description='+smk_description,debug_level)

                    if item.get('object_names'):
                        smk_object_names = ''
                        smk_categories = ''
                        for object_name in item['object_names']: 
                            try:
                                smk_object_name = object_name.get('name')

                                if smk_object_name != '':
                                    #object_name_en = smkapi.smk_danish_to_english(smk_object_name)
                                    object_name_en = csvlookup.find_english_label_from_artwork_type(smk_object_name).lower()

                                    smk_category = '[[Category:' + object_name_en.capitalize() + 's in the Statens Museum for Kunst]]'
                                    smk_categories = smk_categories + smk_category + '\n'
                                    # Check if object_name has a wikidata entry
                                    #smk_object_name_wikidata=csvlookup.find_wikidata_from_object_name(smk_object_name)
                                    #if smk_object_name_wikidata == '':
                                    if object_name_en==object_name:
                                        smk_object_names = smk_object_names + '{{da|' + object_name_en.capitalize() + '}}\n'
                                    else:
                                        smk_object_names = smk_object_names + object_name_en.capitalize() + '\n'
                                    #else:
                                    #    smk_object_names = smk_object_names + '{{item|'+smk_object_name_wikidata+'|show_q=no}}\n'
                            except Exception as e:
                                smk_categories = smk_categories + ''
                                smk_object_names = smk_object_names + ''
                        debug_msg('smk_object_names='+smk_object_names,debug_level)
                        debug_msg('smk_categories='+smk_categories,debug_level)

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
                        debug_msg('smk_inscription='+smk_inscriptions,debug_level)

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
                        debug_msg('smk_labels='+smk_labels,debug_level)

                    if item.get('dimensions'):
                        try:
                            for dimension in item['dimensions']: 
                                debug_msg(dimension['type'],debug_level)
                                debug_msg(dimension['value'],debug_level)
                                debug_msg(dimension['unit'],debug_level)
                                if 'højde'==dimension['type']:
                                    unit_height=""
                                    height=str(dimension['value'])
                                    if dimension['unit']:
                                        unit_height=""
                                        if dimension['unit']=='milimeter':
                                            unit_height="mm"
                                        if dimension['unit']=='centimeter':
                                            unit_height="cm"
                                            height=str(float(height)*10)    
                                if 'bredde'==dimension['type']:
                                    width=str(dimension['value'])
                                    if dimension['unit']:
                                        # Unit of input (must be one of: cm, m, mm, km, in, ft, yd, mi).
                                        unit_width=""
                                        if dimension['unit']=='milimeter':
                                            unit_width="mm"
                                        if dimension['unit']=='centimeter':
                                            unit_width="cm"
                                            width=str(float(width)*10)    

                            # If there is no unit on height and width, skip dimensions
                            if unit_height!='' and unit_width!='':
                                smk_dimensions='{{Size|unit='+'mm'+'|width='+str(width)+'|height='+str(height)+'}}'
                            else:
                                smk_dimensions=''

                        except:
                            smk_dimensions = ''
                    if item.get('techniques'):
                        smk_techniques = ''
                        for technique in item['techniques']: 
                            try:
                                if str(technique) != '':
                                    technique_en=smkapi.smk_danish_to_english(str(technique))
                                    if technique_en==str(technique):
                                        smk_techniques = smk_techniques + '{{da|' + smkapi.smk_danish_to_english(str(technique))+'}}\n'
                                    else:
                                        smk_techniques = smk_techniques + '{{Technique|' + smkapi.smk_danish_to_english(str(technique))+'}}\n'
                            except:
                                smk_techniques = smk_techniques + ''
                        debug_msg('smk_techniques='+smk_techniques,debug_level)

                    if item.get('notes'):
                        for note in item['notes']: 
                            try:
                                smk_notes = smk_notes + '* {{da|'+str(note)+'}}\n'
                            except:
                                smk_notes = smk_notes + ''
                        debug_msg('smk_notes='+smk_notes,debug_level)


                    if item.get('object_history_note'):
                        smk_object_history_note = ''
                        for object_history in item['object_history_note']: 
                            try:
                                smk_object_history_note = smk_object_history_note + '* {{da|'+str(object_history) + '}}\n'
                            except:
                                smk_object_history_note = smk_object_history_note + ''
                        debug_msg('smk_object_history_note=' + smk_object_history_note,debug_level)
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
                        debug_msg('smk_exhibitions='+smk_exhibitions,debug_level)
                    if item.get('collection'):
                        smk_collection = ''
                        for collection in item['collection']: 
                            try:
                                smk_collection = smk_collection + str(collection) + '\n'
                            except:
                                smk_collection = smk_collection + ''
                        debug_msg('smk_collection='+smk_collection,debug_level)
                    if item.get('artist'):
                        smk_artists = ''
                        smk_artists_filename=''
                        unknown_artist = False 
                        has_artist_wikidata=False 

                        for artist in item['artist']:
                            smk_artist = ''
                            try:
                                smk_artist = str(artist)
                            except:
                                smk_artist = ''
                            if smk_artist != '':
                                smk_artists_filename=smk_artists_filename+smk_artist+' - '
                                if smk_artist.lower() == 'ubekendt':
                                    unknown_artist = True 
                                    smk_artist='{{da|' + smk_artist + '}}'
                                    #smk_artists=smk_artists+'{{Creator:'+smk_artist+'}}\n'
                                else:
                                    # find wikidata item from artist name
                                    smk_artist_wikidata = csvlookup.find_wikidata_from_creator_name(smk_artist)
 
                                    if smk_artist_wikidata=='':
                                        smk_artists=smk_artists+smk_artist+'\n'
                                    else:
                                        smk_artists=smk_artists+smk_artist_wikidata+'\n'
                                        has_artist_wikidata=True 
                            if unknown_artist != True: 
                                smk_category = '[[Category:' + object_name_en.capitalize() + 's by ' + smk_artist + ']]'
                                smk_categories = smk_categories + smk_category + '\n'

                            debug_msg('smk_artist='+smk_artist,debug_level)
                        # Strip trailing delimiter " - "
                        artists_filename_delim = str(' - ')
                        artists_filename_delim_length = len(artists_filename_delim)
                        if smk_artists_filename[-artists_filename_delim_length:] == ' - ':
                            smk_artists_filename=smk_artists_filename[0:-artists_filename_delim_length]
                        debug_msg('smk_artists='+smk_artists,debug_level)
                        if unknown_artist:
                            # If we encountered and unknown artist of the painting, add the Category:Artwork Cateogry:Paintings by unknown artists in the Statens Museum for Kunst
                            smk_categories=smk_categories+'[[Category:Paintings by unknown artists in the Statens Museum for Kunst]]\n'                             
                             
                    # Note:department is not used yet 
                    #if item.get('responsible_department'):
                    #    try:
                    #        smk_responsible_department = item.get('responsible_department')
                    #    except:
                    #        smk_responsible_department = ''
                    #    debug_msg('smk_responsible_department='+str(smk_responsible_department))
                    line = ''
                    if item.get('documentation'):
                        smk_documentation = ''
                        for documentation in item['documentation']: 
                            try:
                                line = smkapi.smk_documentation_to_commons_citation(documentation)
                                smk_documentation = smk_documentation + '*' + line + '\n'
                            except Exception as e:
                                smk_documentation = smk_documentation + ''
                        debug_msg('smk_documentation='+str(smk_documentation),debug_level)

                    # Current location is not static
                    # if item.get('current_location_name'):
                    #    smk_current_location_name = ''
                    #    try:
                    #        smk_current_location_name = item.get('current_location_name')
                    #    except:
                    #        smk_current_location_name = ''
                    #    debug_msg('smk_current_location_name='+str(smk_current_location_name))
                    if item.get('acquisition_date'):
                        smk_acquisition_date = ''
                        try:
                            smk_acquisition_date = item.get('acquisition_date')
                        except:
                            smk_acquisition_date = ''
                        debug_msg('smk_acquisition_date='+str(smk_acquisition_date),debug_level)
                    if item.get('acquisition_date_precision'):
                        smk_acquisition_date_precision = ''
                        try:
                            smk_acquisition_date_precision = item.get('acquisition_date_precision')
                        except:
                            smk_acquisition_date_precision = ''
                        debug_msg('smk_acquisition_date_precision='+str(smk_acquisition_date_precision),debug_level)

                # try to get wikidatanumber

                wd_number = csvlookup.find_wikidata_item(smk_object_number)
                # wd_number = wikidata.GetSMKWikidataItem(smk_object_number)

                # Generate artwork template
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
                    location = smk_current_location_name,
                    other_fields = smk_other_fields)

                #artwork.GenerateWikiText()

                filetype = pathlib.Path(smk_image_native).suffix
                filename = 'SMK_' + smk_object_number + '_' + smk_artist + '_-_' + smk_museumstitel
                filename = 'SMK_' + smk_object_number + '_' + smk_artist + '_-_' + smk_museumstitel
                # <kunstnernavn>, <titel>, <årstal>, <inventarnummer>, <samling>                 
                filename = smk_artists_filename + ', ' + smk_museumstitel + ', ' + smk_period + ', ' + accession_number + ', ' + 'Statens Museum for Kunst' 
                filename = filename.replace("\"", " ")
                filename = filename.replace("?", " ")
                filename = filename.replace("/", "-")
                filename = filename.replace("(", " ")
                filename = filename.replace(")", " ")
                filename = filename.replace(":", "-")
                filename = filename.replace(".", "")

                # download smk_image_native
                short_filename=""
                pagetitle=""
                imagepath=""
                image_exists=False
                if smk_has_image == 'True':
                    short_filename = textwrap.shorten(filename, width=235-len('.'+filetype), placeholder='...')
                    imagepath = folder + short_filename + filetype
                    if download_images:
                        if not os.path.exists(imagepath):
                            # only download file if it doens't already exist
                            r = requests.get(smk_image_native, allow_redirects=True)
                            open(imagepath, 'wb').write(r.content)

                    # Check if image allready exists
                    file_hash = '0'
                    if os.path.exists(imagepath):
                        file_hash = commons.get_file_hash(imagepath)
                        image_exists = commons.check_file_hash(file_hash)

                    pagetitle = os.path.basename(imagepath)
                else:
                    imagepath=''

                # attempt to find wikidata item of creator
                #creator_wd_number = csvlookup.find_wikidata_from_creator_lref(smk_creator_lref)

                #if creator_wd_number!='':
                #    smk_artists = creator_wd_number

                artwork.GenerateWikiText()
                license = ''
                #smk_category = '[[Category:' + batch_title + ']]'
                #smk_categories = smk_categories + smk_category + '\n'
                wikitext = artwork.wikitext + '\n' + license + '\n' + str(smk_categories)
                # Save wikitext
                if save_wikitext:
                    path = folder + short_filename + '.txt'
                    open(path, 'w').write(wikitext)

                # Save RAW json
                if save_json:
                    path = folder + short_filename + '.json'
                    open(path, 'w').write(smk_json)

                f_html.writelines('<tr>')
                f_html.writelines('</td><td><a href="' + smk_image_native + '"><img src="' + imagepath + '" width="300" /> <br/></a><a href="' + smk_image_native + '">' + artwork.title + '</a></td><td>' + wikitext.replace('\n', '<br/>'))
                f_html.writelines('</tr>')

#                   csvline = artwork.GenerateCSVLine()


                csvline = str(smk_id) + ';' + str(smk_created) + ';' + str(smk_modified) + ';' + artwork.GenerateCSVLine() + ';' + str(smk_public_domain) + ';'+ str(smk_has_image) + ';'+ str(file_hash) + ';' + \
                  smk_creator_forename + ';' + \
                  smk_creator_surname + ';' + \
                  smk_creator_date_of_death + ';' + \
                  smk_creator_date_of_birth + ';' + \
                  smk_creator_gender + ';' + \
                  smk_creator_lref + ';' + \
                  smk_artists

                csvline = csvline.replace('\n', '<br/>')

                # Print CSV line
                f_csv.write(csvline + '\n')

                bot_status = "Not run"
                #Attempt upload to commons if there is an imagepath
                if upload_to_commons and imagepath!='':
                    if has_artist_wikidata:
                        if not image_exists:
                            # image not already uploaded attempting upload to commons

                            try:
                                debug_msg('Attempting upload of:' + pagetitle,debug_level)
                            #    commons.complete_desc_and_upload(filename, pagetitle, '', '', '')

                                commons.complete_desc_and_upload(imagepath, pagetitle, desc=wikitext, date='', categories='')
                                files_uploaded=files_uploaded+1
                                bot_status = "Media uploaded"
                            except Exception as e:
                                f_batch_log.writelines('</table>')
                                debug_msg('EXCEPTION! '+ str(e))
                                typeerror=TypeError(e)
                                bot_status = "Exception:" + str(e)
                                logging.exception(e)
                        else:
                            bot_status = 'Media already uploaded'
                    else:
                        bot_status = 'Artist has no wikidata item'

                now = datetime.now()
                current_time = now.strftime('%Y-%m-%d %H:%M:%S')
                debug_msg("current_time="+current_time,debug_level)
                f_batch_log.writelines(current_time + ';' + pagetitle + ';' + artwork.accession_number + ';' + artwork.wikidata + ';' + str(image_exists) + ";" + bot_status + ";" + str(file_hash) + '\n')  
        
            except Exception as e:
                debug_msg('EXCEPTION! '+ str(e))
                typeerror=TypeError(e)
                logging.exception(e)
            finally:
                #debug_msg('items='+str(items))
                print('\r' + str(items), end='', flush=True)

                offset=offset+1

            if 0==rows:
                break

        f_html.writelines('</table>')
        f_html.writelines('</body></html>')
        f_html.close()
        f_csv.close() 
        f_batch_log.close()
        
    except Exception as e:
        debug_msg('EXCEPTION! '+ str(e))
        logging.exception(e)
    finally:
        debug_msg('Export finished',debug_level)
        debug_msg('items='+str(items),debug_level)
        offset=offset+1

url="https://api.smk.dk/api/v1/art/search/?keys=*&filters=%5Bpublic_domain%3Atrue%5D&offset=0&rows=10"

#result = smkitem.smkitem_from_dict(json.loads(requests.get(url).text))

#smk_number_list = ["KKSgb29511"]
#smk_number_list = ["KKS13568"]
#smk_number_list = ["KMS7270"]
smk_number_list=None
#smk_number_list = ["KMS1806"]
smk_filter_list = [["public_domain","true"],
    ["has_image", "true"],
    ["creator_gender", "kvinde"],
    ["creator_nationality", "dansk"]]
#smk_filter_list = "",
smk_filter_list = [["public_domain","true"],
    ["has_image", "true"]]

# Generate SMK API filters from filter list
smk_filter=smkapi.generate_smk_filter(smk_filter_list)
#url='https://api.smk.dk/api/v1/art/search/?keys=*&filters=%5Bpublic_domain%3Atrue%5D,%5Bhas_image%3Atrue%5D,%5Bcreator_gender%3Akvinde%5D,%5Bcreator_nationality%3Adansk&offset='+str(offset)+'&rows='+str(rows)
offset=0
rows=1

#smk_filter=""
#batch_title='all_public_domain_images'
batch_title='2022-12-03_smkbot_test_batch'
#batch_title='KMS1806'
download_images=True
#download_images=False
upload_images=True
#upload_images=False
#batch_size=24
batch_size=-1
batch_size=20
save_json=True
save_wikitext=True
debug_level=1
MapSMKAPIToCommons(batch_title,smk_filter,smk_number_list,download_images, upload_images, batch_size, save_json, save_wikitext)

#test upload
#filename    = "./downloads/Ambrosius Bosschaerts d.Æ., Blomsterbuket i en stenniche, 1618, KMSsp211, Statens Museum for Kunst.jpg"
#pagetitle = os.path.basename(filename)

#pagetitle   = "Ambrosius Bosschaerts d.Æ., Blomsterbuket i en stenniche, 1618, KMSsp211, Statens Museum for Kunst.jpg"
#commons.complete_artwork_desc_and_upload(filename, pagetitle, desc='', date='', categories='')
#try:
#    commons.complete_desc_and_upload(filename, pagetitle, '', '', '')
#    commons.complete_desc_and_upload(filename, pagetitle, desc='', date='', categories='')
#except Exception as e:
#    debug_msg(str(e))


