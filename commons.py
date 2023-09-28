""" 
commons.py

Module that implements functions for accessing the Wikimedia Commons

Artwork class encapsulates the wikimedia commons temlate Artwork

Category class encapsulates the wikimedia commons category pages

For more details, refer to the bot user page on Commons:
https://commons.wikimedia.org/wiki/User:WLKBot
"""

from dataclasses import dataclass
from typing import Any, Optional, List, TypeVar, Type, Callable, cast
from enum import Enum
from datetime import datetime
import dateutil.parser
from abc import ABCMeta, abstractmethod
import hashlib
import json
import requests
import sys
import smkitem
import pywikibot
from pywikibot.specialbots import UploadRobot

@dataclass
class BaseTemplate(metaclass=ABCMeta):
    @abstractmethod
    def GenerateWikiText(self):
        #complete this once if applies to all files
        pass

@dataclass
class ArtworkTemplate(BaseTemplate):
    _artist: str
    _artist_name: str
    _nationality: str
    _author: str
    _title: str
    _desc: str
    _depicted_people: str
    _date: str
    _medium: str
    _dimensions: str
    _institution: str
    _department: str
    _place_of_discovery: str
    _exhibition_history: str
    _object_history: str 
    _credit_line: str
    _inscriptions: str
    _notes: str
    _accession_number: str
    _place_of_creation: str
    _source: str
    _permission: str
    _other_versions: str
    _references: str
    _depicted_place: str
    _wikidata: str
    _categories: str
    _orientation: str
    _wikitext: str
    _csvline: str
    _csvheader: str
    _imageurl: str
    _image_height: str
    _image_width: str
    _object_type: str
    _location: str
    _other_fields: str
    _artists_filename: str
    _has_artist_wikidata: bool
    _museumtitle: str
    _templates: str
    _artist_wikidata: str
    _unknown_artist = bool 


    @property
    def artist(self):
        return self._artist

    @property
    def artist_name(self):
        return self._artist_name

    @property
    def nationality(self):
        return self._nationality

    @property
    def author(self):
        return self._author

    @property
    def title(self):
        return self._title

    @property
    def desc(self):
        return self._desc

    @property
    def depicted_people(self):
        return self._depicted_people

    @property
    def date(self):
        return self._date

    @property
    def medium(self):
        return self._medium

    @property
    def dimensions(self):
        return self._dimensions

    @property
    def institution(self):
        return self._institution

    @property
    def department(self):
        return self._department

    @property
    def place_of_discovery(self):
        return self._place_of_discovery

    @property
    def exhibition_history(self):
        return self._exhibition_history

    @property
    def object_history(self):
        return self._object_history

    @property
    def credit_line(self):
        return self._credit_line

    @property
    def inscriptions(self):
        return self._inscriptions

    @property
    def notes(self):
        return self._notes

    @property
    def accession_number(self):
        return self._accession_number

    @property
    def place_of_creation(self):
        return self._place_of_creation

    @property
    def source(self):
        return self._source

    @property
    def permission(self):
        return self._permission

    @property
    def other_versions(self):
        return self._other_versions

    @property
    def references(self):
        return self._references

    @property
    def depicted_place(self):
        return self._depicted_place

    @property
    def wikidata(self):
        return self._wikidata

    @property
    def categories(self):
        return self._categories

    @property
    def orientation(self):
        return self._orientation

    @property
    def wikitext(self):
        return self._wikitext

    @property
    def csvline(self):
        return self._csvline

    @property
    def csvheader(self):
        return self._csvheader

    @property
    def imageurl(self):
        return self._imageurl

    @property
    def image_height(self):
        return self._image_height

    @property
    def image_width(self):
        return self._image_width

    @property
    def object_type(self):
        return self._object_type

    @property
    def location(self):
        return self._location

    @property
    def other_fields(self):
        return self._other_fields

    @property
    def artists_filename(self):
        return self._artists_filename

    @property
    def has_artist_wikidata(self):
        return self._has_artist_wikidata

    @property
    def museumtitle(self):
        return self._museumtitle

    @property
    def templates(self):
        return self._templates

    @property
    def artist_wikidata(self):
        return self._artist_wikidata

    @property
    def unknown_artist(self):
        return self._unknown_artist

    def __init__(self, *objs):
        # Constructor, supports several object types in the objs argument
    
            # iterate over passed objects
            for obj in objs:
                # Is this of type SMKItem?
                if type(obj) == smkitem.SMKItem:
                    smk_item:smkitem.SMKItem
                    smk_item=obj

                    # for item in smk_item.items:
                        
                    # artist
                    self.artist = ''
                        
                    # artist_name
                    self.artist_name = ''
                        
                    # nationality
                    self.nationality = ''


                    #     self.author: str

                    self.title = ''
                    self.desc = ''
                        
                    #     self.depicted_people: str
                        
                    #     self.date: str
                        
                    #     self.medium: str
                        
                    #     self.dimensions: str
                        
                        
                    #     self.institution: str
                    #     self.department: str
                    #     self.place_of_discovery: str
                    #     self.exhibition_history: str
                    #     self.object_history: str 
                    #     self.credit_line: str
                    self.inscriptions = ''
                    #     self.notes: str

                    #     # accession_number
                    #     self.accession_number = item.object_number

                    #     self.place_of_creation: str
                    #     self.source: str
                    #     self.permission: str
                    #     self.other_versions: str
                    #     self.references: str
                    #     self.depicted_place: str
                    #     self.wikidata: str
                    #     self.categories: str
                    #     self.orientation: str
                    #     self.wikitext: str
                    #     self.csvline: str
                    #     self.csvheader: str
                    #     self.imageurl: str
                    #     self.image_height: str
                    #     self.image_width: str
                    #     self.object_type: str
                    #     self.location: str
                    # Other fields
                    self.other_fields = ''
                    self.artists_filename = ''
                    self.has_artist_wikidata = ''
                    self.museumtitle = ''

    @property
    def accession_number(self):
        return self._accession_number
    
    @accession_number.setter
    def accession_number(self, new_accession_number):
        self._accession_number = new_accession_number
   
    @property
    def author(self):
        return self._author
    
    @author.setter
    def author(self, new_author):
        self._author = new_author
   
    @artist.setter
    def artist(self, new_artist):
        self._artist = new_artist
   
    @artist_name.setter
    def artist_name(self, new_artist_name):
        self._artist_name = new_artist_name
   
    @nationality.setter
    def nationality(self, new_nationality):
        self._nationality = new_nationality
      
    @title.setter
    def title(self, new_title):
        self._title = new_title
   
    @desc.setter
    def desc(self, new_desc):
        self._desc = new_desc
   
    @depicted_people.setter
    def depicted_people(self, new_depicted_people):
        self._depicted_people = new_depicted_people
   
    @date.setter
    def date(self, new_date):
        self._date = new_date
   
    @medium.setter
    def medium(self, new_medium):
        self._medium = new_medium
   
    @dimensions.setter
    def dimensions(self, new_dimensions):
        self._dimensions = new_dimensions
   
    @institution.setter
    def institution(self, new_institution):
        self._institution = new_institution
   
    @department.setter
    def department(self, new_department):
        self._department = new_department
   
    @place_of_discovery.setter
    def place_of_discovery(self, new_place_of_discovery):
        self._place_of_discovery = new_place_of_discovery
   
    @object_history.setter
    def object_history(self, new_object_history):
        self._object_history = new_object_history
   
    @exhibition_history.setter
    def exhibition_history(self, new_exhibition_history):
        self._exhibition_history = new_exhibition_history
   
    @credit_line.setter
    def credit_line(self, new_credit_line):
        self._credit_line = new_credit_line
   
    @inscriptions.setter
    def inscriptions(self, new_inscriptions):
        self._inscriptions = new_inscriptions
   
    @notes.setter
    def notes(self, new_notes):
        self._notes = new_notes
   
    @accession_number.setter
    def accession_number(self, new_accession_number):
        self._accession_number = new_accession_number
   
    @place_of_creation.setter
    def place_of_creation(self, new_place_of_creation):
        self._place_of_creation = new_place_of_creation
   
    @source.setter
    def source(self, new_source):
        self._source = new_source
   
    @permission.setter
    def permission(self, new_permission):
        self._permission = new_permission
   
    @other_versions.setter
    def other_versions(self, new_other_versions):
        self._other_versions = new_other_versions
   
    @references.setter
    def references(self, new_references):
        self._references = new_references
   
    @depicted_place.setter
    def depicted_place(self, new_depicted_place):
        self._depicted_place = new_depicted_place
   
    @wikidata.setter
    def wikidata(self, new_wikidata):
        self._wikidata = new_wikidata
   
    @categories.setter
    def categories(self, new_categories):
        self._categories = new_categories
   
    @imageurl.setter
    def imageurl(self, new_imageurl):
        self._imageurl = new_imageurl
   
    @image_height.setter
    def image_height(self, new_image_height):
        self._image_height = new_image_height
   
    @image_width.setter
    def image_width(self, new_image_width):
        self._image_width = new_image_width
   
    @object_type.setter
    def object_type(self, new_object_type):
        self._object_type = new_object_type
   
    @location.setter
    def location(self, new_location):
        self._location = new_location
   
    @other_fields.setter
    def other_fields(self, new_other_fields):
        self._other_fields = new_other_fields

    @csvline.setter
    def csvline(self, new_csvline):
        self._csvline = new_csvline

    @csvheader.setter
    def csvheader(self, new_csvheader):
        self._csvheader = new_csvheader

    @artists_filename.setter
    def artists_filename(self, new_artists_filename):
        self._artists_filename = new_artists_filename

    @has_artist_wikidata.setter
    def has_artist_wikidata(self, new_has_artist_wikidata):
        self._has_artist_wikidata = new_has_artist_wikidata

    @museumtitle.setter
    def museumtitle(self, new_museumtitle):
        self._museumtitle = new_museumtitle

    @templates.setter
    def templates(self, new_templates):
        self._templates = new_templates

    @artist_wikidata.setter
    def artist_wikidata(self, new_artist_wikidata):
        self._artist_wikidata = new_artist_wikidata


    @unknown_artist.setter
    def unknown_artist(self, new_unknown_artist):
        self._unknown_artist = new_unknown_artist


    def GenerateWikiText(self):
        #complete this once if applies to all files
        
        self._wikitext = u"""== {{int:filedesc}} ==
{{Artwork
 |artist             = """ + str(self.artist).rstrip() + """
 |author             = """ + str(self.author).rstrip() + """
 |title              = """ + str(self.title).rstrip() + """
 |description        = """ + str(self.desc).rstrip() + """
 |depicted people    = """ + str(self.depicted_people).rstrip() + """
 |date               = """ + str(self.date).rstrip() + """
 |medium             = """ + str(self.medium).rstrip() + """
 |dimensions         = """ + str(self.dimensions).rstrip() + """
 |institution        = """ + str(self.institution).rstrip() + """
 |department         = """ + str(self.department).rstrip() + """
 |place of discovery = """ + str(self.place_of_discovery).rstrip() + """
 |object history     = """ + str(self.object_history).rstrip() + """ 
 |exhibition history = """ + str(self.exhibition_history).rstrip() + """
 |credit line        = """ + str(self.credit_line).rstrip() + """
 |inscriptions       = """ + str(self.inscriptions).rstrip() + """
 |notes              = """ + str(self.notes).rstrip() + """
 |accession number   = """ + str(self.accession_number).rstrip() + """
 |place of creation  = """ + str(self.place_of_creation).rstrip() + """
 |source             = """ + str(self.source).rstrip() + """
 |other_versions     = """ + str(self.other_versions).rstrip() + """
 |references         = """ + str(self.references).rstrip() + """
 |depicted place     = """ + str(self.depicted_place).rstrip() + """
 |object type        = """ + str(self.object_type).rstrip() + """
 |location           = """ + str(self.location).rstrip() + """
 |other_fields       = """ + str(self.other_fields) + """
 |wikidata           = """ + str(self.wikidata).rstrip() + """
}} 

== {{int:license-header}} ==
""" + str(self.permission) + """
"""

    def GenerateCSVLine(self, csvdelim=';'):
        """
        Generates CSV-line

        Example:
            GenerateCSVLine(";")
        
        Keyword arguments:
            char -- delimiter to use
            
            <csvdelim> ::=<char>
        
        Returns:
            Nothing
        """

        self.csvline = ''
        self.csvline = self.csvline + str(self.artist).replace(';', '&semi') + csvdelim
        self.csvline = self.csvline + str(self.artist_name).replace(';', '&semi') + csvdelim
        self.csvline = self.csvline + str(self.nationality).replace(';', '&semi') + csvdelim
        self.csvline = self.csvline + str(self.author).replace(';', '&semi') + csvdelim
        self.csvline = self.csvline + str(self.title).replace(';', '&semi') + csvdelim
        self.csvline = self.csvline + str(self.desc).replace(';', '&semi') + csvdelim
        self.csvline = self.csvline + str(self.depicted_people).replace(';', '&semi') + csvdelim
        self.csvline = self.csvline + str(self.date).replace(';', '&semi') + csvdelim
        self.csvline = self.csvline + str(self.medium).replace(';', '&semi') + csvdelim
        self.csvline = self.csvline + str(self.dimensions).replace(';', '&semi') + csvdelim
        self.csvline = self.csvline + str(self.institution).replace(';', '&semi') + csvdelim
        self.csvline = self.csvline + str(self.department).replace(';', '&semi') + csvdelim
        self.csvline = self.csvline + str(self.place_of_discovery).replace(';', '&semi') + csvdelim
        self.csvline = self.csvline + str(self.object_history).replace(';', '&semi') + csvdelim
        self.csvline = self.csvline + str(self.exhibition_history).replace(';', '&semi') + csvdelim
        self.csvline = self.csvline + str(self.credit_line).replace(';', '&semi') + csvdelim
        self.csvline = self.csvline + str(self.inscriptions).replace(';', '&semi') + csvdelim
        self.csvline = self.csvline + str(self.notes).replace(';', '&semi') + csvdelim
        self.csvline = self.csvline + str(self.accession_number).replace(';', '&semi') + csvdelim
        self.csvline = self.csvline + str(self.place_of_creation).replace(';', '&semi') + csvdelim
        self.csvline = self.csvline + str(self.source).replace(';', '&semi') + csvdelim
        self.csvline = self.csvline + str(self.permission).replace(';', '&semi') + csvdelim
        self.csvline = self.csvline + str(self.other_versions).replace(';', '&semi') + csvdelim
        self.csvline = self.csvline + str(self.references).replace(';', '&semi') + csvdelim
        self.csvline = self.csvline + str(self.depicted_place).replace(';', '&semi') + csvdelim
        self.csvline = self.csvline + str(self.categories).replace(';', '&semi') + csvdelim
        self.csvline = self.csvline + str(self.wikidata).replace(';', '&semi') + csvdelim
        self.csvline = self.csvline + str(self.image_height).replace(';', '&semi') + csvdelim
        self.csvline = self.csvline + str(self.image_width).replace(';', '&semi') + csvdelim
        self.csvline = self.csvline + str(self.imageurl).replace(';', '&semi') + csvdelim
        self.csvline = self.csvline + str(self.object_type).replace(';', '&semi') + csvdelim
        self.csvline = self.csvline + str(self.location).replace(';', '&semi') + csvdelim 
        self.csvline = self.csvline + str(self.medium).replace(';', '&semi') + csvdelim
        self.csvline = self.csvline + str(self.other_fields).replace(';', '&semi') 
    
        return self.csvline

    def GenerateCSVHeader(self, csvdelim=';'):
        """
        Generates header for CSV-file)

        Example:
            GenerateCSVHeader(";")
        
        Keyword arguments:
            char -- delimiter to use
            
            <csvdelim> ::=<char>
        
        Returns:
            Nothing
        """

        csvheader = 'id' + csvdelim + \
          'created' + csvdelim + \
          'modified' + csvdelim + \
          'artist' + csvdelim + \
          'artist_name' + csvdelim + \
          'nationality' + csvdelim + \
          'author' + csvdelim + \
          'title' + csvdelim + \
          'description' + csvdelim + \
          'depicted_people' + csvdelim + \
          'date' + csvdelim + \
          'medium' + csvdelim + \
          'dimensions' + csvdelim + \
          'institution' + csvdelim + \
          'department' + csvdelim + \
          'place_of_discovery' + csvdelim + \
          'object_history' + csvdelim + \
          'exhibition_history' + csvdelim + \
          'credit_line' + csvdelim + \
          'inscriptions' + csvdelim + \
          'notes' + csvdelim + \
          'accession_number' + csvdelim + \
          'place_of_creation' + csvdelim + \
          'source' + csvdelim + \
          'permission' + csvdelim + \
          'other_versions' + csvdelim + \
          'references' + csvdelim + \
          'depicted_place' + csvdelim + \
          'categories' + csvdelim + \
          'wikidata' + csvdelim + \
          'image_height' + csvdelim + \
          'image_width' + csvdelim + \
          'imageurl' + csvdelim + \
          'object_type' + csvdelim + \
          'location' + csvdelim + \
          'medium' + csvdelim + \
          'public_domain' + csvdelim + \
          'has_image' + csvdelim + \
          'file_hash' + csvdelim + \
          'creator_forename' + csvdelim + \
          'creator_surname' + csvdelim + \
          'creator_date_of_death' + csvdelim + \
          'creator_date_of_birth' + csvdelim + \
          'creator_gender' + csvdelim + \
          'creator_lref' + csvdelim + \
          'creator_wikidata' + csvdelim + \
          'other_fields'
    
        return csvheader

def get_file_hash(filename):
    """
    Generates SHA1 hash for a file

    Example:
        get_file_hash("test.jpg")
    
    Keyword arguments:
        filename -- filename to get the hash for
        
        <filename> ::=<char>
    
    Returns:
        The file hash
    """
    file = filename # Location of the file (can be set a different way)
    BLOCK_SIZE = 65536 # The size of each read from the file

    file_hash = hashlib.sha1() # Create the hash object, can use something other than `.sha256()` if you wish
    with open(file, 'rb') as f: # Open the file to read it's bytes
        fb = f.read(BLOCK_SIZE) # Read from the file. Take in the amount declared above
        while len(fb) > 0: # While there is still data being read from the file
            file_hash.update(fb) # Update the hash
            fb = f.read(BLOCK_SIZE) # Read the next block from the file

    return(file_hash.hexdigest())

def check_file_hash(file_hash):
    """
    Checks the image SHA1 hash for a filename, to determine if file
    has already been uploaded to commons

    Example:
        check_file_hash("ffff")
    
    Keyword arguments:
        file_hash -- image hash to check the commons hash for
        
        <file_hash> ::={<char>}
    
    Returns:
        True if image hash already exists on Commons
    """
    
    url= "https://commons.wikimedia.org/w/api.php?action=query&format=json&list=allimages&prop=imageinfo&aisha1=" + file_hash
    data = json.loads(requests.get(url).text)
    if len(data['query']['allimages']) != 0:
        # file hash found
        retval=True 
    else:
        retval=False 
    return(retval)

# -*- coding: utf-8  -*-

def complete_desc_and_upload(filename, pagetitle, desc, date, categories, edit_summary):
    """
    Uploads image to commons

    Example:
        complete_desc_and_upload("test.jpg", "test.jpg", "testpage", "", "[[Category:Test]]", "Uploaded artwork")
    
    Keyword arguments:
        filename -- filename to use
        pagetitle  -- title of page to use
        desc -- description to use
        date -- date to use
        categories -- categories to use
        edit_summary -- edit summary to use
        
        <filename>      ::= {<char>}
        <pagetitle>     ::= {<char>}
        <desc>          ::= {<char>}
        <date>          ::= {<char>}
        <categories>    ::= {<char>}
        <edit_summary>  ::= {<char>}
    
    Returns:
        Nothing
    """

    url = [ filename ]
    #keepFilename = False        #set to True to skip double-checking/editing destination filename
    keepFilename = True        #set to True to skip double-checking/editing destination filename
    #verifyDescription = True    #set to False to skip double-checking/editing description => change to bot-mode
    verifyDescription = False    #set to False to skip double-checking/editing description => change to bot-mode
    #targetSite = pywikibot.Site('commons', 'commons')
    #targetSite = pywikibot.Site(fam='commons',code='commons', user='Kim Bach', sysop='Kim Bach')
    try:
        targetSite = pywikibot.Site()
    except Exception as e:
        print(str(e))

    print(targetSite)
    targetSite = pywikibot.Site('commons', 'commons')

    bot = UploadRobot(url, description=desc, useFilename=pagetitle, keepFilename=keepFilename, verifyDescription=verifyDescription, targetSite=targetSite, summary=edit_summary)
    bot.run()

#    page = pywikibot.Page(targetSite, 'File:' + filename)
#    page = pywikibot.Page(targetSite, 'File:' + filename)
#    print(page.text)
#    page.text = description
#    page.save('Replacing description')  # Saves the page

# def complete_artwork_desc_and_upload(filename, pagetitle, desc, date, categories):
#     #complete this once if applies to all files

#     description = u"""{{Artwork
# |Description    = {{en|1=""" + desc + """}}
# |Source         = [[Statens Museeum for Kunst]]
# |Author         = 
# |Date           = """ + date + """
# |Permission     = 
# |other_versions = 
# }}
# =={{int:license-header}}==
# {{PD-old-70}}

# """ + categories + """
# """
#     url = [ filename ]
#     #keepFilename = False        #set to True to skip double-checking/editing destination filename
#     keepFilename = True        #set to True to skip double-checking/editing destination filename
#     #verifyDescription = True    #set to False to skip double-checking/editing description => change to bot-mode
#     verifyDescription = False    #set to False to skip double-checking/editing description => change to bot-mode
#     targetSite = pywikibot.Site(code='commons', fam='commons', user='Kim Bach')
    
#     #bot = UploadRobot(url, description=description, useFilename=pagetitle, keepFilename=keepFilename, verifyDescription=verifyDescription, targetSite=targetSite)
#     #bot.run()

# #    page = pywikibot.Page(targetSite, 'File:' + filename)
#     page = pywikibot.Page(targetSite, 'File:' + filename)
# #    print(page.text)
#     #page.text = description
#     #page.save('Replacing description')  # Saves the page


def get_file_hash(filename):
    """
    Generates SHA1 hash for a file

    Example:
        get_file_hash("test.jpg")
    
    Keyword arguments:
        filename -- filename to get the hash for
        
        <filename> ::=<char>
    
    Returns:
        The file hash
    """
    file = filename # Location of the file (can be set a different way)
    BLOCK_SIZE = 65536 # The size of each read from the file

    file_hash = hashlib.sha1() # Create the hash object, can use something other than `.sha256()` if you wish
    with open(file, 'rb') as f: # Open the file to read it's bytes
        fb = f.read(BLOCK_SIZE) # Read from the file. Take in the amount declared above
        while len(fb) > 0: # While there is still data being read from the file
            file_hash.update(fb) # Update the hash
            fb = f.read(BLOCK_SIZE) # Read the next block from the file

    return(file_hash.hexdigest())

def check_file_hash(file_hash):
    """
    Checks the image SHA1 hash for a filename, to determine if file
    has already been uploaded to commons

    Example:
        check_file_hash("ffff")
    
    Keyword arguments:
        file_hash -- image hash to check the commons hash for
        
        <file_hash> ::={<char>}
    
    Returns:
        True if image hash already exists on Commons
    """
    
    url= "https://commons.wikimedia.org/w/api.php?action=query&format=json&list=allimages&prop=imageinfo&aisha1=" + file_hash
    data = json.loads(requests.get(url).text)
    if len(data['query']['allimages']) != 0:
        # file hash found
        retval=True 
    else:
        retval=False 
    return(retval)

# -*- coding: utf-8  -*-

def complete_desc_and_upload(filename, pagetitle, desc, date, categories,edit_summary):
    """
    Uploads image to commons

    Example:
        complete_desc_and_upload("test.jpg", "test.jpg", "testpage", "", "[[Category:Test]]")
    
    Keyword arguments:
        filename -- filename to use
        pagetitle  -- title of page to use
        desc -- description to use
        date -- date to use
        categories  -- categories to use
        edit_summary  -- edit summary to use
        
        <filename>      ::= {<char>}
        <pagetitle>     ::= {<char>}
        <desc>          ::= {<char>}
        <date>          ::= {<char>}
        <categories>    ::= {<char>}
    
    Returns:
        Nothing
    """

    url = [ filename ]
    #keepFilename = False        #set to True to skip double-checking/editing destination filename
    keepFilename = True        #set to True to skip double-checking/editing destination filename
    #verifyDescription = True    #set to False to skip double-checking/editing description => change to bot-mode
    verifyDescription = False    #set to False to skip double-checking/editing description => change to bot-mode
    #targetSite = pywikibot.Site('commons', 'commons')
    #targetSite = pywikibot.Site(fam='commons',code='commons', user='Kim Bach', sysop='Kim Bach')
    try:
        targetSite = pywikibot.Site()
        try:
            print(targetSite)
            targetSite = pywikibot.Site('commons', 'commons')

#            bot = UploadRobot(url, description=desc, useFilename=pagetitle, keepFilename=keepFilename, verifyDescription=verifyDescription, targetSite=targetSite, summary=edit_summary)
            bot = UploadRobot(url, description=desc, use_filename=pagetitle, keep_filename=keepFilename, verify_description=verifyDescription, target_site=targetSite, summary=edit_summary)
            bot.run()
        except Exception as e:
            print(str(e))
    except Exception as e:
        print(str(e))

def create_wiki_page(pagetitle, desc, edit_summary):
    # Connect to the site you want to edit
    site = pywikibot.Site('commons', 'commons')


    # Set the title and text for the new page
    title = pagetitle
    text = desc

    # Create a new page object
    new_page = pywikibot.Page(site, title)

    # Check if the page already exists
    if new_page.exists():
        raise ValueError("Page already exists")

    # Edit the page with the new text
    new_page.text = text
    new_page.save(summary=edit_summary, minor=False)


#    page = pywikibot.Page(targetSite, 'File:' + filename)
#    page = pywikibot.Page(targetSite, 'File:' + filename)
#    print(page.text)
#    page.text = description
#    page.save('Replacing description')  # Saves the page

# def complete_artwork_desc_and_upload(filename, pagetitle, desc, date, categories):
#     #complete this once if applies to all files

#     description = u"""{{Artwork
# |Description    = {{en|1=""" + desc + """}}
# |Source         = [[Statens Museeum for Kunst]]
# |Author         = 
# |Date           = """ + date + """
# |Permission     = 
# |other_versions = 
# }}
# =={{int:license-header}}==
# {{PD-old-70}}
# """ + categories + """
# """
#     url = [ filename ]
#     #keepFilename = False        #set to True to skip double-checking/editing destination filename
#     keepFilename = True        #set to True to skip double-checking/editing destination filename
#     #verifyDescription = True    #set to False to skip double-checking/editing description => change to bot-mode
#     verifyDescription = False    #set to False to skip double-checking/editing description => change to bot-mode
#     targetSite = pywikibot.Site(code='commons', fam='commons', user='Kim Bach')
    
#     if (filename != ''):
#         bot = UploadRobot(url, description=description, useFilename=pagetitle, keepFilename=keepFilename, verifyDescription=verifyDescription, targetSite=targetSite)
#         bot.run()

# #    page = pywikibot.Page(targetSite, 'File:' + filename)
#     page = pywikibot.Page(targetSite, 'File:' + filename)
# #    print(page.text)
#     page.text = description
#     page.save('Replacing description')  # Saves the page

def PageExists(pagetitle):
    ret_val: bool = False
    try:
        # check if category exists
        result = requests.get('https://commons.wikimedia.org/wiki/' + pagetitle)
        if result.status_code == 200:  
            # the category exists
            ret_val = True
            pass  # blablabla
        else:
            # the category doesn't exists, attempt to create it
            ret_val = False
    except Exception as e:
        print('EXCEPTION!' + str(e))

    return(ret_val)

def CreateCategory(category_pagetitle, category_wikitext, upload_to_commons):
    # Create category wikitext
    try:
        # check if category exists
        result = requests.get('https://commons.wikimedia.org/wiki/' + category_pagetitle)
        if result.status_code == 200:  
            # the category exists
            pass  # blablabla
        else:
            # the category doesn't exists, attempt to create it
            if upload_to_commons:
                create_wiki_page(pagetitle=category_pagetitle, desc=category_wikitext, edit_summary='Created category')
    except Exception as e:
        print('EXCEPTION!' + str(e))


def UploadTest():
    #list each file here
    
    filename    = """https://iip.smk.dk/iiif/jp2/KMS1.tif.reconstructed.tif.jp2/full/full/0/native.jpg"""
    filename    = """KMS1.tif.reconstructed.tif.jpg"""
    filename    = "./downloads/Mesteren for Palazzo Venezia Madonna, Skt. Victor af Siena, 1348-1352, KMS3625, Statens Museum for Kunst.jpg"
    pagetitle   = "Mesteren for Palazzo Venezia Madonna, Skt. Victor af Siena, 1348-1352, KMS3625, Statens Museum for Kunst.jpg"
    desc        = """The Heart Of Wiki Labs Kultur - Updated Image"""
    date        = "2016-10-14 22:06"
    date        = "2019-09-10 19:00"
    categories  = """[[Category:Wiki Labs Test]]"""
    categories  = """[[Category:Wiki Labs Test]]"""
    #complete_artwork_desc_and_upload(filename, pagetitle, desc, date, categories)


    #sample with:  - local file name identical to file name at Commons
    #              - date as previous file
    #              - less quotes (no CR or " in fields)
    #filename   = "testimage-2.jpg"
    #pagetitle  = filename
    #desc       = "Mount St Helens as seen from ... at sunset"
    #categories = "[[Category:Locality]] [[Category:Theme]] [[Category:View type]] [[Category:Feature1]] [[Category:Feature2]]"
    #complete_desc_and_upload(filename, pagetitle, desc, date, categories)
   

#if __name__ == "__main__":
#    try:
#        main(sys.argv[1:])
#    finally:
#        pywikibot.stopme()
