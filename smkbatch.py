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
    ObjectCategory_id=8
    ArtistCategory_id=9
    categories=''

    # Get object_names
    for item in smk_item.items:
        for object_name in item.object_names:
            try:
                # Attempt to lookup the artwork_type by object_name 
                artwork_type_object=csvlookup.find_artwork_type_object(object_name.name)
                if artwork_type_object:
                    # Artwork type found

                    # Get object and artist categories

                    object_category = artwork_type_object[ObjectCategory_id]

                    # get artists
                    for artist in item.artist:
                        artist_name = str(artist)
                        if artist_name.lower() == 'ubekendt':
                            artist_name = 'unknown artists'

                        # find wikidata item from artist name
                        smk_artist_wikidata_q = csvlookup.find_wikidata_from_creator_name(artist_name)
                        smk_artist_wikidata = csvlookup.find_creator_from_creator_name(artist_name)
                        
                        # Find commons category name, and try to use it as artist name
                        if smk_artist_wikidata_q.startswith('Q'):
                            # The artist has a wikidata-Q
                            commons_category_name = wikidata.get_property_value("P373", smk_artist_wikidata_q)
                        else:
                            commons_category_name = None

                        if commons_category_name != None:
                            artist_name_en = commons_category_name
                        else:
                            # Commons category not found
                            if smk_artist_wikidata != None:
                                artist_name_en = smk_artist_wikidata[3]
                            else:
                                artist_name_en = artist_name

                        # Generate <object name> by <category_artist_name> in the Statens Museum for Kunst
                        # First check if object name> by <category_artist_name> in Statens Museum for Kunst exists - without "the"
                        # if it does use that for the category
                        artist_category = artwork_type_object[ArtistCategory_id]

                        artist_category = artist_category.replace("xxxx (name)", artist_name_en)
                        
                        if artist_category != "":
                            # only add artist category, if it doesn't already exist
                           if categories.find(artist_category) == -1:
                                categories = categories + '[[Category:' + artist_category + ']]\n' 
#                        if object_category != "":
                            # only add object category, if it doesn't already exist
#                        if categories.find(object_category) == -1:
#                            categories = categories + '[[Category:' + object_category + ']]\n' 

                        # Try to create object category
                        if object_category != "":
                            object_category_wikitext= '{{SMKNavBox}}\n'

                            object_category_wikitext= object_category_wikitext + \
                                '[[Category:Collections of the Statens Museum for Kunst]]\n'

                            try:
                                commons.CreateCategory('Category:' + object_category, object_category_wikitext, upload_to_commons)

                                # Save wikitext
                                if save_wikitext:
                                    path = folder + object_category + '.txt'
                                    open(path, 'w').write(object_category_wikitext)

                            except Exception as e:
                                debug_msg('EXCEPTION!' + str(e))
                                logging.exception(e)

                        # Try to create artist category
                        # Attempt to create artist category
                        if artist_category != "":
                            # if smk_artist_wikidata_q.startswith('Q'):
                            #     # The artist has a wikidata Q-number
                            #     artist_commons_category = '{{Data|item=' + smk_artist_wikidata_q + '|property=p373|numval=1}}'
                            # else:
                            #     artist_commons_category = artist_name_en
                            artist_commons_category = wikidata.get_property_value("P373", smk_artist_wikidata_q)
                            
                            if artist_commons_category == None:
                                artist_commons_category = artist_name_en

                            defaultsort=item.defaultsort(artist_name_en)

                            if defaultsort != '':
                                artist_category_wikitext ='{{DEFAULTSORT:' + defaultsort + '}}\n'
                            else:
                                artist_category_wikitext =''

                            artist_category_wikitext= artist_category_wikitext + \
                                '[[Category:'+ object_category + ']]\n' + \
                                '[[Category:' + artist_commons_category +']]\n'
                                #'[[Category:' + artist_name +']]\n' \
                            try:
                                # Save wikitext
                                if save_wikitext:
                                    path = folder + artist_category + '.txt'
                                    open(path, 'w').write(artist_category_wikitext)

                                commons.CreateCategory("Category:" + artist_category, artist_category_wikitext, upload_to_commons)

                                # Get the category of the artist's commons category (p373) 

                                if smk_artist_wikidata_q.startswith('Q'):
                                    # Generate category content with reference to the artist wikidata item (p373)
                                    # but only if an artist Wikidata Q-number was found
                                    #artist_category_wikidata = '{{Data|item=' + smk_artist_wikidata_q + '|property=p373|numval=1}}'
                                    artist_category_wikidata = '{{Wikidata Infobox|qid=' + smk_artist_wikidata_q + '}}\n'

                                    if defaultsort != '':
                                        artist_category_wikidata = artist_category_wikidata + '{{DEFAULTSORT:' + defaultsort + '}}\n'

                                    category_pagetitle=artist_name_en

                                    if save_wikitext:
                                        path = folder + category_pagetitle + '.txt'
                                        open(path, 'w').write(artist_category_wikidata)

                                        commons.CreateCategory('Category:' +category_pagetitle, artist_category_wikidata, upload_to_commons)

                            except Exception as e:
                                debug_msg('EXCEPTION!' + str(e))
                                logging.exception(e)
    
                # use only one object type for the artwork, so break out of loop
                break
            except Exception as e:
                categories = categories + ''
                debug_msg('EXCEPTION!' + str(e))
                logging.exception(e)

    return(categories)


def DownloadImage(url: str, imagepath: str):
    """
    Downloads image from url and saves it. One file is generated for the file downloaded

    Example:
        url='https://example.com/image.jpg'
        imagepath='image.jpg'
    
    Keyword arguments:
        url -- the url address to donload image from  
        imagepath -- path to the file donwloaded  

        <url> ::=<url_address>
        <imagepath> ::=<path><filename>"."<fileextension>
    """

    try:
        print(f'Downloading {imagepath}\n')
        r = requests.get(url, allow_redirects=True)
        print("Download http status: " + str(r.status_code) + "\n")

        # Check http status code, throw HTTP exception using raise for ataus, if status isn't ok and skip downloading

        r.raise_for_status()

        # all is ok
        open(imagepath, 'wb').write(r.content)

    except Exception as e:
        debug_msg('EXCEPTION! '+ str(e))
        logging.exception(e)

        # re-raise error
        raise

def UploadImage(imagepath: str, pagetitle:str, wikitext:str, date:str, categories:str, edit_summary:str):
    debug_msg('Attempting upload of: ' + pagetitle,debug_level + '\n')
    commons.complete_desc_and_upload(imagepath, pagetitle, wikitext, date, categories, edit_summary)

def MapSMKAPIToCommons(batch_title,smk_filter,smk_number_list,download_images, upload_to_commons, batch_size, save_json, save_wikitext, offset, debug_level=0):
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
        offset -- the record to start looking for items in the API 
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

        # offset=0
        rows=1
        items=0

        output_filename=batch_title
        batch_log_filename = output_filename
        f_batch_log=open(batch_log_filename+'.log', 'w+')
        f_batch_log.writelines("time;pagetitle;accession_number;wikidata;image_exists;bot_status;file_hash;artist_name;artist_wikidata\n")
        f_batch_log.close()

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

                        # Remove escaped "{
                        #smk_json=smk_json.replace('"{', '{')

                        # Remove escaped \"
                        #smk_json=smk_json.replace('\\"', '"')

                        # Remove escaped (}")
                        #smk_json=smk_json.replace('}"', '}')

                        # # Remove escaped ('}"')
                        # smk_json=smk_json.replace('}"]', '"')

                        # # Remove escaped ('""')
                        # smk_json=smk_json.replace('""', '"')
            
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

                # DFAULTSORT template
                if not artwork.unknown_artist:
                    defaultsort = smk_item.items[0].defaultsort(artwork.artist_name)
                else:
                    defaultsort = 'Unknown'

                if defaultsort != '':
                    smk_templates = '{{DEFAULTSORT:' + defaultsort + '}}'
                else:
                    smk_templates = ''

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
                filename = filename.replace("[", "")
                filename = filename.replace("]", "")

                # download smk_image_native
                short_filename=""
                pagetitle=""
                imagepath=""
                imagepath_3d=""
                image_exists=False
                file_hash = '0'
                if smk_item.items[0].has_image == True:
                    short_filename = textwrap.shorten(filename, width=235-len('.'+filetype), placeholder='...')
                    imagepath = folder + short_filename + filetype
                    if download_images:
                        if not os.path.exists(imagepath):
                            # only download file if it doesn't already exist
                            DownloadImage(smk_item.items[0].image_native, imagepath)

                    if  os.path.exists(imagepath):
                        # check size of downloaded file, commons has a max size of 100MB
                        file_stats = os.stat(imagepath)
                        file_size = file_stats.st_size / (1024 * 1024)
                        print(f'File Size in MB: {round(file_size, 2)}\n')

                        # Check if image allready exists
                        file_hash = commons.get_file_hash(imagepath)
                        image_exists = commons.check_file_hash(file_hash)

                    pagetitle = os.path.basename(imagepath)
                else:
                    imagepath=''

                artwork.GenerateWikiText()


                # generate categories

                # Does one of the artists have a Wikidata Q-number og is one of the artists unknown?
                if artwork.has_artist_wikidata or artwork.unknown_artist:
                    smk_categories = generate_artwork_categories(smk_item, upload_to_commons)
                else:
                    smk_categories = ''
                wikitext = artwork.wikitext
                
                if smk_categories != '':
                    # Item has categories'

                    # Concatenate wikitext, templates and categories
                    wikitext = wikitext + '\n' + str(smk_templates) + '\n' + str(smk_categories) + '\n'

                else:
                    # Item has no categories, skip upload
                    debug_msg('Page has no categories: ' + pagetitle,debug_level)

                # Save wikitext
                if save_wikitext:
                    path = folder + short_filename + '.txt'
                    open(path, 'w').write(wikitext)

                f_html.writelines('<tr>')
                f_html.writelines('</td><td><a href="' + smk_item.items[0].image_native + '"><img src="' + imagepath + '" width="300" /> <br/></a><a href="' + smk_image_native + '">' + artwork.title + '</a></td><td>' + wikitext.replace('\n', '<br/>'))
                f_html.writelines('</tr>')

                license = ''
                #smk_category = '[[Category:' + batch_title + ']]'
                #smk_categories = smk_categories + smk_category + '\n'

                # Save RAW json
                if save_json:
                    path = folder + short_filename + '.json'
                    open(path, 'w').write(smk_json)

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
                if file_size < 100:
                    # The file size is smaller than 100MB, continue upload
                    
                    # Does one of the artists have a Wikidata Q-number og is one of the artists unknown?
                    if artwork.has_artist_wikidata or artwork.unknown_artist:
                        #Attempt upload to commons if there is an imagepath and categories
                        if upload_to_commons and imagepath!='' and smk_categories != '':
                        #if imagepath!='':
                            if not image_exists:
    #                        if True:
                                # image not already uploaded attempting upload to commons

                                try:
                                    # check if page already exists
                                    if not commons.PageExists(pagetitle):
                                        # page does not exist, continue with upload
                                        debug_msg('Attempting upload of: ' + pagetitle,debug_level)
                                        commons.complete_desc_and_upload(imagepath, pagetitle, desc=wikitext, date='', categories='', edit_summary='{{SMK Open|'+artwork.accession_number +'}}')

                                        files_uploaded=files_uploaded+1
                                        bot_status = "Media uploaded"
                                    else:
                                        debug_msg('Page already exists: ' + pagetitle,debug_level)
                                        bot_status = 'Page already uploaded'
                                except Exception as e:
                                    debug_msg('EXCEPTION! '+ str(e))
                                    typeerror=TypeError(e)
                                    bot_status = "Exception:" + str(e)
                                    logging.exception(e)
                            else:
                                bot_status = 'Media already uploaded'
                        else:
                            if smk_categories == '':
                                bot_status = 'no categories'
                            else:
                                bot_status = 'upload_to_commons set to False'
                    else:
                        bot_status = 'Artist has no wikidata item'

                        # add missiong artist lref_person to "./artists/creator_lref_without_q.csv"
                        creator_lref=open('./artists/creator_lref_without_q.csv','a')
                        creator_lref.write(smk_item.items[0].production[0].creator_lref+','+artwork.artist_name+'\n')
                        creator_lref.close()
                else:
                    bot_status = 'file size exeeds 100MB'

                # Handle possible 3d file
                if smk_item.items[0].has_3_d_file == True:
                    filetype_3d = pathlib.Path(smk_item.items[0].files_3D[0].url).suffix
                    imagepath_3d = folder + short_filename + ", 3D model" + filetype_3d

                    if download_images:
                        if not os.path.exists(imagepath_3d):
                            # only download file if it doens't already exist
                            DownloadImage(smk_item.items[0].files_3D[0].url, imagepath_3d)

                    #Attempt upload to commons if there is an imagepath and categories
                    if upload_to_commons and imagepath_3d!='' and smk_categories != '':
                    #if True:
                        # Check if image allready exists
                        if os.path.exists(imagepath_3d):
                        #if True:
                            file_hash_3d = commons.get_file_hash(imagepath_3d)
                            image_exists_3d = commons.check_file_hash(file_hash_3d)
                            if not image_exists_3d:
                            #if True:
                                artwork.other_versions = "[[File:" + pagetitle + "|thumbnail]]"
                                artwork.GenerateWikiText()
                                if smk_categories != '':
                                    # Item has categories'

                                    # Concatenate wikitext, templates and categories
                                    wikitext = artwork.wikitext + '\n' + str(smk_templates) + '\n' + str(smk_categories) + '\n'
                                wikitext = wikitext + "[[Category:3D models from the Statens Museum for Kunst]]" + "\n" 
                                pagetitle_3d = os.path.basename(imagepath_3d)

                                # Save wikitext for 3D file
                                if save_wikitext:
                                    path = folder + short_filename + ", 3D model" + '.txt'
                                    open(path, 'w').write(wikitext)

                                file_stats_3d = os.stat(imagepath_3d)
                                file_size_3d = file_stats_3d.st_size / (1024 * 1024)
                                print(f'File Size in MB: {round(file_size_3d, 2)}\n')
                                if file_size_3d < 100:
                                    debug_msg('Attempting upload of: ' + pagetitle_3d,debug_level)
                                    commons.complete_desc_and_upload(imagepath_3d, pagetitle_3d, desc=wikitext, date='', categories='Category:3D models from the Statens Museum for Kunst', edit_summary='{{SMK Open|'+artwork.accession_number +'}}')
                                else:
                                    bot_status = 'file size for 3D file exeeds 100MB'

                now = datetime.now()
                current_time = now.strftime('%Y-%m-%d %H:%M:%S')
                f_batch_log=open(batch_log_filename+'.log', 'a')
                f_batch_log.writelines(current_time + ';' + pagetitle + ';' + artwork.accession_number + ';' + artwork.wikidata + ';' + str(image_exists) + ";" + bot_status + ";" + str(file_hash) + ";" + artwork.artist_name  + ";" +  artwork.artist_wikidata + '\n')  
                f_batch_log.close()

            except requests.HTTPError:
                # http error occured, quit
                raise
            except Exception as e:
                debug_msg('EXCEPTION! '+ str(e))
                logging.exception(e)
            finally:
                print('\n' + "Uploaded " + str(files_uploaded) + "/" + str(items) + " files - " + bot_status + "\n", end='', flush=True)

                offset=offset+1

            if 0==rows:
                break
                f_html.writelines('</table>')
                f_html.writelines('</body></html>')
                f_html.close()
                f_csv.close() 

        
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
                        if production.creator_date_of_death != '':
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
            if iso_code != '':
                smk_description = smk_description + '{{' + iso_code +'|'  + title.title + '}}\n'
            else:
                smk_description = smk_description + title.title + '\n'
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
                    line = line + '|language='+ smkapi.smk_language_code_to_iso_code(language.lower())
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
        height = 0
        width = 0
        depth = 0

        # Look at all dimenstions, finding the smallest width, height and depth
        for dimension in Item.dimensions:
            unit = ''
            value=float(dimension.value)
            # Check dimenstion of the dimension
            if dimension.unit=='millimeter':
                unit="mm"
            if dimension.unit=='centimeter':
                unit="cm"

                # Unit is centimeter, multiply by 10
                value=value*10
            if dimension.type == "højde":
                # Find the lowest height
                if height == 0:
                    height = value
                else:
                    if value < height:
                        height=value
            elif dimension.type == "bredde":
                # Find the lowest width
                if width == 0:
                    width = value
                else:
                    if value < height:
                        width=value
            elif dimension.type == "dybde":
                    # Find the lowest depth
                    if depth == 0:
                        depth=value
                    else:
                        if value < depth:
                            depth=value

        # Do not set depth for paintings (Maleri), it is 2D
        if object_name.name == "Maleri":
            depth = 0

        if height>0 and width>0:
            # Artwork has a height and a width, generate Size tempålate
            smk_dimensions='{{Size|unit='+'mm'+'|width='+str(width)+'|height='+str(height)

            if depth > 0:
                # Artwork has a  depth, add depth parameter
                smk_dimensions=smk_dimensions+'|depth='+str(depth)
            smk_dimensions=smk_dimensions+'}}'
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
    artwork.artist_name = ''
    artwork.artist_wikidata = ''
    artwork.unknown_artist = False 

    has_several_artists=False

    for artist in Item.artist:
        smk_artist = str(artist)
        if len(Item.artist)>1:
            # More than one artist, add information about artists to smk_notes
            if not has_several_artists:
                has_several_artists = True
                smk_notes=smk_notes+"* {{en|This artwork has several artists:}}\n"
            smk_notes = smk_notes + "** " + smk_artist + '\n'

        if artist != '':
            artwork.artist_name = smk_artist

            smk_artists_filename=smk_artists_filename+smk_artist+' - '
            
            # Is one of the artists unknown?
            if smk_artist.lower() == 'ubekendt':
                unknown_artist = True 
                artwork.unknown_artist = True 
                smk_artist='Unknown'
                artwork.artist_name = 'Unknown'
                smk_artists=smk_artists+smk_artist+'\n'
            else:
                # find wikidata item from artist name
                smk_artist_wikidata_q = csvlookup.find_wikidata_from_creator_name(smk_artist)
                # was a Q-number for the artist found? first letter is a Q
                if smk_artist_wikidata_q.startswith('Q'):
                    smk_artists=smk_artists+smk_artist_wikidata_q+'\n'
                    artwork.has_artist_wikidata = True
                    artwork.artist_name = smk_artist
                    artwork.artist_wikidata = smk_artist_wikidata_q 
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
        '* [' + smk_image_native + ' {{en|image}}]\n'
        if Item.has_3_d_file:
            if Item.files_3D != None:
                artwork.source = artwork.source + \
                '* [' + Item.files_3D[0].url + ' {{en|3D model}}]\n'  
    except:
        artwork.source = ''
    try:
        try:
            if smk_creator_year_of_death == None:
                smk_creator_year_of_death = ''
        except:
            smk_creator_year_of_death = ''
        
        try:
            if smk_creator_year_of_death == '':
                PD_old_parameter = 'PD-old-100-expired'
            else:
                PD_old_parameter = 'PD-old-auto-expired|deathyear=' + str(smk_creator_year_of_death)
        except:
            smk_creator_year_of_death = ''
            PD_old_parameter = 'PD-old-100-expired'

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
#smk_number_list = ["KKSgb22216"]
# smk_number_list = ["KKSgb22216",
#    "KKSgb4762",
#    "KMS3716",
#    "KKSgb6423",
#    "KAS1179",
#    "KKSgb2950",
#    "KMS4223",
#    "KKSgb19863"]
smk_number_list = ["KMS1620"]
smk_number_list = ["KAS422"]
smk_number_list = ["KMS5808"]
smk_number_list = ["KMS8568"]
smk_number_list=None

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
# offset indicates at what row the SMK API should start generation, 0 indicates the first record
offset=27717
rows=1

#smk_filter=""
batch_title=datetime.now().strftime("%Y%m%d_%H%M%S") + '_Batch'
download_images=True
#download_images=False
#upload_images=True
upload_images=True
#batch_size=24
batch_size=-1
# batch_size=1000
save_json=True
save_wikitext=True
debug_level=1
MapSMKAPIToCommons(batch_title,smk_filter,smk_number_list,download_images, upload_images, batch_size, save_json, save_wikitext, offset)
