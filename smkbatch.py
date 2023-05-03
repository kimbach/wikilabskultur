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

debug_level=1

folder = './downloads2/'

def debug_msg(msg, debug_level=1):
    if debug_level>0:
        print(msg)

def generate_artwork_categories(smk_item: smkitem.SMKItem, upload_to_commons: bool):
    LEn_id=3
    LEnPlural_id=6
    categories=''

    # Get object_names
    for item in smk_item.items:
        for object_name in item.object_names:
            try:
                object_name_name_en_plural = ''
            
                # Attempt to lookup the artwork_type by object_name 
                artwork_type_object=csvlookup.find_artwork_type_object(object_name.name)
                if artwork_type_object:
                    # Artwork type found
                    object_name_name_en_plural = artwork_type_object[LEnPlural_id].lower()

                    # get artists
                    for artist in item.artist:
                        artist_name = str(artist)
                        if artist_name.lower() == 'ubekendt':
                            artist_name = 'unknown artists'

                        # Generate <object name> by <category_artist_name> in the Statens Museum for Kunst
                        # First check if object name> by <category_artist_name> in Statens Museum for Kunst exists - without "the"
                        # if it does use that for the category
                        category = f'Category:{object_name_name_en_plural.capitalize()} by {artist_name} in Statens Museum for Kunst'
                        
                        if not commons.PageExists(category):
                            # Existing category with the "the" clause not found, use it
                            category = f'Category:{object_name_name_en_plural.capitalize()} by {artist_name} in the Statens Museum for Kunst'
                        categories = categories + '[[' + category + ']]\n' 
                        
                        # Attempt to create category
                        category_wikitext='[[Category:Collections of the Statens Museum for Kunst]]\n' + \
                            '[[Category:Collections of ' + object_name_name_en_plural + ' by museum|statens]]\n' + \
                            '[[Category:'+ artist_name +']]\n'

                        # Try to create category
                        try:
                            commons.CreateCategory(category, category_wikitext, upload_to_commons)

                            # Get the category of the artist's commons category (p373) 

                            # find wikidata item from artist name
                            smk_artist_wikidata_q = csvlookup.find_wikidata_from_creator_name(artist_name)

                            # Generate category content with reference to the artist wikidata item (p373)
                            
                            artist_category_wikidata = '{{Data|item=' + smk_artist_wikidata_q + '|property=p373|numval=1}}'
                            category_pagetitle='Category:' + artist_name+'\n'

                            commons.CreateCategory(category_pagetitle, artist_category_wikidata, upload_to_commons)

                        except Exception as e:
                            debug_msg('EXCEPTION!' + str(e))
                            logging.exception(e)
    
            except Exception as e:
                categories = categories + ''
                debug_msg('EXCEPTION!' + str(e))
                logging.exception(e)

    return(categories)


def MapSMKAPIToCommons(batch_title,smk_filter,smk_number_list,download_images, upload_to_commons, batch_size, save_json, save_wikitext, debug_level=0):
    """
    Maps SMK API to Wikimedia Commons. Three files is generated for each item (inventory number/assension number)
    <mediafilename> ::=<filename>"."<fileextension>
    <textfilename>  ::=<filename>".txt"
    <jsonfilename>  ::=<filename>".json"

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

    artwork: commons.ArtworkTemplate

    keepFilename = True        #set to True to skip double-checking/editing destination filename
    verifyDescription = False    #set to False to skip double-checking/editing description => change to bot-mode
    #targetSite = pywikibot.Site('beta', 'commons')

    # Get all wikidata items for SMK Wikidata object Q671384
    #wikidata.GetInstitutionWikidataItems('Q671384', 'wikidata_smk')
    try:
        # list of items/assencion number to get
        SMKItemList = smk_number_list

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
        csv_header=artwork.GenerateCSVHeader()
        f_csv.write(csv_header + '\n')

        # Print HTML Header
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
                
                # Initialize object model smk_item from json object 
                smk_item: smkitem.SMKItem
                smk_item = smkitem.smk_item_from_dict(smk_objects)

                items = items + 1

                try:
                    offset=smk_item.items[0].offset
                    offset=smk_objects['offset']
                    rows=smk_objects['rows']
                    found=smk_objects['found']
                    if offset>found:
                        break
                except:
                    rows=1

                smk_image_native  = ''
                artwork = SMKHelper(smk_item.items[0])

                artwork.GenerateWikiText()

                filetype = pathlib.Path(smk_item.items[0].image_native).suffix

                # <kunstnernavn>, <titel>, <årstal>, <inventarnummer>, <samling>                 
                filename = artwork.artists_filename + ', ' + artwork.museumtitle + ', ' + artwork.date + ', ' + artwork.accession_number + ', ' + 'Statens Museum for Kunst' 
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
                file_hash = '0'
                if smk_item.items[0].has_image == True:
                    short_filename = textwrap.shorten(filename, width=235-len('.'+filetype), placeholder='...')
                    imagepath = folder + short_filename + filetype
                    if download_images:
                        if not os.path.exists(imagepath):
                            # only download file if it doens't already exist
                            r = requests.get(smk_item.items[0].image_native, allow_redirects=True)
                            open(imagepath, 'wb').write(r.content)

                    # Check if image allready exists
                    if os.path.exists(imagepath):
                        file_hash = commons.get_file_hash(imagepath)
                        image_exists = commons.check_file_hash(file_hash)

                    pagetitle = os.path.basename(imagepath)
                else:
                    imagepath=''

                license = ''
                #smk_category = '[[Category:' + batch_title + ']]'
                #smk_categories = smk_categories + smk_category + '\n'
                
                # generqte categories
                smk_categories = generate_artwork_categories(smk_item, upload_to_commons)

                # Concatenate wikitext and categories
                wikitext = artwork.wikitext + '\n' + str(smk_categories)
                
                # Save wikitext
                if save_wikitext:
                    path = folder + short_filename + '.txt'
                    open(path, 'w').write(wikitext)

                # Save RAW json
                if save_json:
                    path = folder + short_filename + '.json'
                    open(path, 'w').write(smk_json)

                f_html.writelines('<tr>')
                f_html.writelines('</td><td><a href="' + smk_item.items[0].image_native + '"><img src="' + imagepath + '" width="300" /> <br/></a><a href="' + smk_image_native + '">' + artwork.title + '</a></td><td>' + wikitext.replace('\n', '<br/>'))
                f_html.writelines('</tr>')

#                   csvline = artwork.GenerateCSVLine()


                csvline = str(smk_item.items[0].id) + ';' + str(smk_item.items[0].created) + ';' + str(smk_item.items[0].modified) + ';' + artwork.GenerateCSVLine() + ';' + str(smk_item.items[0].public_domain) + ';'+ str(smk_item.items[0].has_image) + ';'+ str(file_hash) + ';'
                #   smk_creator_forename + ';' + \
                #   smk_creator_surname + ';' + \
                #   smk_creator_date_of_death + ';' + \
                #   smk_creator_date_of_birth + ';' + \
                #   smk_creator_gender + ';' + \
                #   smk_creator_lref + ';' + \
                #   smk_artists

                csvline = csvline.replace('\n', '<br/>')

                # Print CSV line
                f_csv.write(csvline + '\n')

                bot_status = "Not run"
                #Attempt upload to commons if there is an imagepath
                if upload_to_commons and imagepath!='':
                    if artwork.has_artist_wikidata:
                        if not image_exists:
                            # image not already uploaded attempting upload to commons

                            try:
                                if not commons.PageExists(pagetitle):
                                    debug_msg('Attempting upload of: ' + pagetitle,debug_level)

                                    commons.complete_desc_and_upload(imagepath, pagetitle, desc=wikitext, date='', categories='', edit_summary='{{SMK Open|'+artwork.artwork.accession_number +'}}')
                                    files_uploaded=files_uploaded+1
                                    bot_status = "Media uploaded"
                                else:
                                    debug_msg('Page already exists: ' + pagetitle,debug_level)
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
                f_batch_log.writelines(current_time + ';' + pagetitle + ';' + artwork.accession_number + ';' + artwork.wikidata + ';' + str(image_exists) + ";" + bot_status + ";" + str(file_hash) + '\n')  
        
            except Exception as e:
                debug_msg('EXCEPTION! '+ str(e))
                typeerror=TypeError(e)
                logging.exception(e)
            finally:
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

def SMKHelper(Item: smkitem.Item):
    artwork = commons.ArtworkTemplate(Item)
    smk_image_native = Item.image_native
    smk_image_width = Item.image_width
    smk_image_height = Item.image_height

    smk_creators=''
    smk_description=''
    smk_notes=''

    try:
        # Item.Production
        smk_all_creators_date_of_death=None

        for production in Item.production:
            smk_creator=''
            smk_creator_forename=''
            smk_creator_surname=''
            smk_creator_date_of_death = ''
            smk_creator_nationality = ''
            smk_creator_year_of_death = ''
            smk_creator_date_of_birth =''
            smk_creator_gender=''
            smk_creator_lref=''

            try:
                smk_creator_forename = str(production.creator_forename)
                smk_temp=smk_creator_forename.lower()
                if smk_temp == 'none':
                    smk_creator_forename=''
            except Exception as e:
                smk_creator_forename = ''
                debug_msg('EXCEPTION! '+ str(e))
                logging.exception(e)

            try:
                smk_creator_surname = str(production.creator_surname)
            except Exception as e:
                debug_msg('EXCEPTION! '+ str(e))
                logging.exception(e)

            try:
                smk_creator_history = str(production.creator_history)
            except Exception as e:
                smk_creator_history = ''
                debug_msg('EXCEPTION! '+ str(e))
                logging.exception(e)

            if smk_creator_history != '':
                smk_notes = smk_notes + '* {{da|'+smk_creator_history +'}}\n'

            # last name, first name
            try:
                smk_creator= smk_creator_forename + ' ' + smk_creator_surname
                smk_creator = smk_creator.lstrip()
                smk_creators=smk_creators + '{{Creator:'+smk_creator+'}}'

            except Exception as e:
                smk_creator_forename = ''
                debug_msg('EXCEPTION! '+ str(e))
                logging.exception(e)
            try:
                if production.creator_date_of_death != None:
                    if smk_creator_year_of_death != '':
                        if int(production.creator_date_of_death.strftime("%Y-%m-%d")[:4]) > smk_creator_year_of_death:
                            smk_creator_year_of_death = smk_creator_date_of_death.strftime("%Y-%m-%d")[:4]
                            smk_all_creators_date_of_death = smk_creator_year_of_death
                    else:
                        smk_creator_year_of_death = production.creator_date_of_death.strftime("%Y-%m-%d")[:4]

            except Exception as e:
                debug_msg('EXCEPTION! '+ str(e))
                logging.exception(e)
                smk_creator_date_of_death = ''
                smk_creator_year_of_death = ''
            try:
                smk_creator_nationality = str(production.creator_nationality)
            except Exception as e:
                debug_msg('EXCEPTION! '+ str(e))
                logging.exception(e)
                smk_creator_nationality = ''
            try:
                smk_creator_date_of_birth=str(production.creator_date_of_birth)                       
            except Exception as e:
                debug_msg('EXCEPTION! '+ str(e))
                logging.exception(e)
                smk_creator_date_of_birth =''
            try:
                smk_creator_gender=str(production.creator_gender)                                    
            except Exception as e:
                debug_msg('EXCEPTION! '+ str(e))
                logging.exception(e)
                smk_creator_gender=''
            try:
                smk_creator_lref=str(production.creator_lref)
            except Exception as e:
                debug_msg('EXCEPTION! '+ str(e))
                logging.exception(e)
                smk_creator_lref=''
        
        # Convert smk_all_creators_date_of_death to string
        try:
            if smk_all_creators_date_of_death == None:
                smk_all_creators_date_of_death = ''

        except Exception as e:
            smk_all_creators_date_of_death=''
            smk_creator_forename = ''
            debug_msg('EXCEPTION! '+ str(e))
            logging.exception(e)

    except Exception as e:
        debug_msg('EXCEPTION! '+ str(e))
        logging.exception(e)
        smk_creator=''
        smk_creator_date_of_death = ''
        smk_creator_nationality = ''
    
    # Production date
    smk_period = ''
    try:
        for production_date in Item.production_date:
            try:
                smk_period = smk_period + str(production_date.period)
            except Exception as e:
                debug_msg('EXCEPTION! '+ str(e))
                smk_period = smk_period + ''
                logging.exception(e)
    except Exception as e:
        debug_msg('EXCEPTION! '+ str(e))
        smk_period = smk_period + ''
        logging.exception(e)
    
    # Production date notes
    smk_notes = ''
    try:
        for production_dates_note in Item.production_dates_notes:
            try:
                smk_notes = smk_notes + '* {{da|'+str(production_dates_note)+'}}\n'
            except Exception as e:
                debug_msg('EXCEPTION! '+ str(e))
                logging.exception(e)
                smk_notes = smk_notes + ''
    except Exception as e:
        debug_msg('EXCEPTION! '+ str(e))
        logging.exception(e)
        smk_notes = smk_notes + ''
    
    # Titles
    smk_titles=''

    for title in Item.titles: 
        try:
            iso_code = smkapi.smk_language_code_to_iso_code(title.language)
            smk_description = smk_description + '{{'
            if iso_code != '':
                smk_description = smk_description + iso_code +'|'
            smk_description = smk_description + title.title + '}}\n'
        except Exception as e:
            debug_msg('EXCEPTION! '+ str(e))
            logging.exception(e)

    # Check if first title is empty
    artwork.museumtitle = Item.titles[0].title
    if artwork.museumtitle != '':
        iso_code = smkapi.smk_language_code_to_iso_code(Item.titles[0].language)
        smk_titles='{{title|'+ artwork.museumtitle
        if iso_code != '':
            smk_titles = smk_titles + '|lang=' + iso_code
        smk_titles = smk_titles + '}}'
    else:
        artwork.museumtitle = 'Untitled' 

    # Description
    for description in Item.content_description: 
        try:
            smk_description = smk_description + '* {{da|' + str(description) + '}}\n'
        except Exception as e:
            debug_msg('EXCEPTION! '+ str(e))
            logging.exception(e)
            smk_description = smk_description + ''

    # Object names
    smk_object_names = ''
    smk_categories = ''
    for object_name in Item.object_names: 
        try:
            if object_name.name != '':
                object_name_en = csvlookup.find_english_label_from_artwork_type(object_name.name).lower()
                
                if smk_object_names == '':
                    smk_object_names = object_name_en 

                # Make English object name plural
                if object_name_en[-1:]!='s':
                    object_name_en_plural = object_name_en+'s'
 

        except Exception as e:
            smk_categories = smk_categories + ''
            smk_object_names = smk_object_names + ''
            debug_msg('EXCEPTION! '+ str(e))
            logging.exception(e)

    # Item.inscriptions
    smk_inscriptions = ''
    for inscription in Item.inscriptions: 
        try:
            line = ''
            content = ''
            language=''
            position='' 
            content = inscription.content

            language = str(inscription.language) 

            position = inscription.position

            if content!="":  
                line = '{{inscription '
                if content != "":
                    line = line + '|1=' + content
                if position != "":
                    line = line + '|position=' + smkapi.smk_to_commons_position(position)
                if  language != "":
                    line = line + '|language='+ smkapi.smk_language_code_to_iso_code(language)
                line = line + '}}'
                smk_inscriptions = smk_inscriptions + line + '\n'
        except Exception as e:
            smk_inscriptions = smk_inscriptions + ''
            debug_msg('EXCEPTION! '+ str(e))
            logging.exception(e)

    # Item.labels
    smk_labels = ''
    for label in Item.labels: 
        try:
            text = ''
            type=''
            source= ''
            date='' 
            text = str(label.text)
            type = str(label.type) 
            source = str(label.source)
            date = str(f"{label.date:%Y-%m-%d}")
            line = text + ', ' + type + ', ' + source + ', ' + date 
            smk_labels = smk_labels + '* {{da|' + text + '}}\n'
        except Exception as e:
            smk_labels = smk_labels + ''
            debug_msg('EXCEPTION! '+ str(e))
            logging.exception(e)

    # Item.dimensions
    try:
        unit_height = ''
        unit_width = ''
        for dimension in Item.dimensions:
 
            if 'højde'==dimension.type:
                unit_height=""
                height=str(dimension.value)
                if dimension.unit:
                    unit_height=""
                    if dimension.unit=='millimeter':
                        unit_height="mm"
                    if dimension.unit=='centimeter':
                        unit_height="cm"
                        height=str(float(height)*10)    
            if 'bredde'==dimension.type:
                width=str(dimension.value)
                if dimension.unit:
                    # Unit of input (must be one of: cm, m, mm, km, in, ft, yd, mi).
                    unit_width=""
                    if dimension.unit=='millimeter':
                        unit_width="mm"
                    if dimension.unit=='centimeter':
                        unit_width="cm"
                        width=str(float(width)*10)    

        # If there is no unit on height and width, skip dimensions
        if unit_height!='' and unit_width!='':
            smk_dimensions='{{Size|unit='+'mm'+'|width='+str(width)+'|height='+str(height)+'}}'
        else:
            smk_dimensions=''

    except Exception as e:
        smk_dimensions = ''
        debug_msg('EXCEPTION! '+ str(e))
        logging.exception(e)

    # Item.techniques
    smk_techniques = ''
    for technique in Item.techniques: 
        try:
            if str(technique) != '':
                technique_en=smkapi.smk_danish_to_english(str(technique))
                if technique_en==str(technique):
                    smk_techniques = smk_techniques + '{{da|' + smkapi.smk_danish_to_english(str(technique))+'}}\n'
                else:
                    smk_techniques = smk_techniques + '{{Technique|' + smkapi.smk_danish_to_english(str(technique))+'}}\n'
        except Exception as e:
            smk_techniques = smk_techniques + ''
            debug_msg('EXCEPTION! '+ str(e))
            logging.exception(e)

    # Item.notes
    for note in Item.notes: 
        try:
            smk_notes = smk_notes + '* {{da|'+str(note)+'}}\n'
        except:
            smk_notes = smk_notes + ''

    # Item.distinguishing_features
    for distinguishing_features in Item.distinguishing_features: 
        try:
            smk_notes = smk_notes + '* {{da|'+str(distinguishing_features)+'}}\n'
        except Exception as e:
            debug_msg('EXCEPTION! '+ str(e))
            logging.exception(e)
            smk_notes = smk_notes + ''

    # Item.object_history_note
    smk_object_history_note = ''

    for object_history in Item.object_history_note: 
        try:
            smk_object_history_note = smk_object_history_note + '* {{da|'+str(object_history) + '}}\n'
        except Exception as e:
            smk_object_history_note = smk_object_history_note + ''
            debug_msg('EXCEPTION! '+ str(e))
            logging.exception(e)

    # Item.exhibitions
    smk_exhibitions = ''
    for exhibition in Item.exhibitions: 
        try:
            smk_exhibitions = smk_exhibitions + "* {{Temporary Exhibition |name=" + exhibition.exhibition + \
                " |institution= |place= " + exhibition.venue + " |begin=" + \
                f"{exhibition.date_start:%Y-%m-%d}" + " |end=" + \
                f"{exhibition.date_end:%Y-%m-%d}" + "}}\n"
        except Exception as e:
            smk_exhibitions = smk_exhibitions + ''
            debug_msg('EXCEPTION! '+ str(e))
            logging.exception(e)
    smk_collection = ''
    for collection in Item.collection: 
        try:
            smk_collection = smk_collection + str(collection) + '\n'
        except Exception as e:
            smk_collection = smk_collection + ''
            debug_msg('EXCEPTION! '+ str(e))
            logging.exception(e)

    # Artist
    smk_artists = ''
    smk_artists_filename=''
    unknown_artist = False 
    artwork.has_artist_wikidata = False 

    for artist in Item.artist:
        smk_artist = str(artist)
        if artist != '':
            smk_artists_filename=smk_artists_filename+smk_artist+' - '
            if smk_artist.lower() == 'ubekendt':
                unknown_artist = True 
                smk_artist='{{da|' + smk_artist + '}}'
            else:
                # find wikidata item from artist name
                smk_artist_wikidata_q = csvlookup.find_wikidata_from_creator_name(smk_artist)

                if smk_artist_wikidata_q!='':
                    smk_artists=smk_artists+smk_artist_wikidata_q+'\n'
                    artwork.has_artist_wikidata = True
                else:
                    smk_artists=smk_artists+smk_artist+'\n'
         
    # Strip trailing delimiter " - "
    artists_filename_delim = str(' - ')
    artists_filename_delim_length = len(artists_filename_delim)
    if smk_artists_filename[-artists_filename_delim_length:] == ' - ':
        smk_artists_filename=smk_artists_filename[0:-artists_filename_delim_length]

    artwork.artists_filename = smk_artists_filename

    if unknown_artist:
        # If we encountered and unknown artist of the painting, add the Category:Artwork Cateogry:Paintings by unknown artists in the Statens Museum for Kunst
        smk_category='[[Category:'+object_name_en.capitalize()+' by unknown artists in the Statens Museum for Kunst]]'
        smk_categories=smk_categories+smk_category                             

        #Check if unknown artist category exists
        category_pagetitle=smk_category
        
        category_wikitext='[[Category:'+object_name_en.capitalize()+' by unknown artists]]'

    smk_responsible_department = ''
    # Note:department is not used yet 
    #if item.get('responsible_department'):
    #    try:
    #        smk_responsible_department = item.get('responsible_department')
    #    except:
    #        smk_responsible_department = ''
    #    debug_msg('smk_responsible_department='+str(smk_responsible_department))
    line = ''

    # Documentation
    smk_documentation = ''
    for documentation in Item.documentation: 
        try:
            line = smkapi.smk_documentation_to_commons_citation(documentation)
            smk_documentation = smk_documentation + '*' + line + '\n'
        except Exception as e:
            smk_documentation = smk_documentation + ''
            debug_msg('EXCEPTION! '+ str(e))
            logging.exception(e)

    # Current location
    smk_current_location_name = ''
    # Current location is not static
    # if item.get('current_location_name'):
    #    try:
    #        smk_current_location_name = item.get('current_location_name')
    #    except:
    #        smk_current_location_name = ''
    #    debug_msg('smk_current_location_name='+str(smk_current_location_name))
    # Generate artwork template
    if Item.acquisition_date_precision!=None:
        smk_object_history_note = smk_object_history_note + \
            '* {{ProvenanceEvent|date='+f"{Item.acquisition_date_precision:%Y-%m-%d}"f""+'|type=acquisition|newowner=[[Statens Museum for Kunst]]}}'
    
    artwork.artist = smk_artists
    try:
        artwork.nationality = smk_creator_nationality
    except Exception as e:
        artwork.nationality = ''
        debug_msg('EXCEPTION! '+ str(e))
        logging.exception(e)

    artwork.author = ''
    try:
        artwork.title = smk_titles
    except:
        artwork.title = ''
    try:
        artwork.desc = smk_description
    except:
        artwork.desc = ''
    
    artwork.depicted_people = ''
    try:
        artwork.date = smk_period
    except:
        artwork.date = ''
    try:
        artwork.medium = smk_techniques
    except:
        artwork.medium = ''
    try:
        artwork.dimensions = smk_dimensions
    except:
        artwork.dimensions = ''
    
    artwork.institution = '{{Institution:Statens Museum for Kunst, Copenhagen}}'
    try:
        artwork.department = smk_responsible_department
    except:
        artwork.department = ''
    
    artwork.place_of_discovery = ''
    try:
        artwork.object_history = smk_object_history_note 
    except:
        artwork.object_history = '' 
    try:
        artwork.exhibition_history = smk_exhibitions
    except:
        artwork.exhibition_history = ''
    
    artwork.credit_line = ''
    try:
        artwork.inscriptions = smk_inscriptions
    except:
        artwork.inscriptions = ''
    try:
        artwork.notes = smk_notes+smk_labels
    except:
        artwork.notes = ''
    try:
        artwork.accession_number = Item.object_number
    except:
        artwork.accession_number = ''
    
    artwork.place_of_creation = ''
    #'https://collection.smk.dk/#/en/detail/'+accession_number
    try:
        artwork.source = '* {{SMK API|'+Item.object_number+'}}\n' +  \
        '* {{SMK Open|'+Item.object_number+'}}\n' + \
        '* [' + smk_image_native + ' image]'                    
    except:
        artwork.source = ''
    try:
        if smk_creator_year_of_death == None:
            smk_creator_year_of_death = ''
        
        if smk_creator_year_of_death == '':
            PD_old_parameter = 'PD-old-100-expired'
        else:
            PD_old_parameter = 'PD-old-auto-expired|deathyear=' + str(smk_creator_year_of_death)
        artwork.permission = '{{Licensed-PD-Art|' + PD_old_parameter + '|Cc-zero}}\n' + \
        '{{Statens Museum for Kunst collaboration project}}'
    except Exception as e:
        artwork.permission = ''
        debug_msg('EXCEPTION! '+ str(e))
        logging.exception(e)

    artwork.other_versions = ''
    try:
        artwork.references = smk_documentation
    except:
        artwork.references = ''
    
    artwork.depicted_place = ''
    try:
        artwork.categories = smk_categories
    except:
        artwork.categories = ''
    try:
        artwork.imageurl = smk_image_native
    except:
        artwork.imageurl = ''
    try:
        artwork.image_height = smk_image_height
    except:
        artwork.image_height = ''
    try:
        artwork.image_width = smk_image_width
    except:
        artwork.image_width = ''
    try:
        artwork.object_type = smk_object_names
    except:
        artwork.object_type = ''
    try:
        artwork.location = smk_current_location_name
    except:
        artwork.location = ''
    artwork.other_fields = ''

    # try to get wikidatanumber
    wd_number = csvlookup.find_wikidata_item(artwork.accession_number)
    artwork.wikidata = wd_number
    
    return(artwork)

url="https://api.smk.dk/api/v1/art/search/?keys=*&filters=%5Bpublic_domain%3Atrue%5D&offset=0&rows=10"

#result = smkitem.smkitem_from_dict(json.loads(requests.get(url).text))

#smk_number_list = ["KKSgb29511"]
#smk_number_list = ["KKS13568"]
#smk_number_list = ["KMS7270"]
#smk_number_list = ["KMS1806"]
#smk_number_list = ["KKSgb22345"]
smk_number_list = ["KKSgb22216"]
#smk_number_list = ["KKSgb22216"],
#    "KKSgb4762",
#    "KMS3716",
#    "KKSgb6423",
#    "KAS1179",
#    "KKSgb2950",
#    "KMS4223",
#    "KKSgb19863"]
#smk_number_list=None

#smk_filter_list = [["public_domain","true"],
#    ["has_image", "true"],
#    ["creator_gender", "kvinde"],
#    ["creator_nationality", "dansk"]]
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
batch_title='2023-04-29_WLKBot_test'
#batch_title='KMS1806'
#download_images=True
download_images=False
upload_images=False
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


