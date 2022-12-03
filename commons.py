""" 
commons.py

Module that implements functions for accessing the Wikimedia Commons

Artwork class encapsulates the wikimedia commons temlate Artwork

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
    artist: str
    nationality: str
    author: str
    title: str
    desc: str
    depicted_people: str
    date: str
    medium: str
    dimensions: str
    institution: str
    department: str
    place_of_discovery: str
    object_history: str 
    exhibition_history: str
    credit_line: str
    inscriptions: str
    notes: str
    accession_number: str
    place_of_creation: str
    source: str
    permission: str
    other_versions: str
    references: str
    depicted_place: str
    wikidata: str
    categories: str
    orientation: str
    wikitext: str
    csvline: str
    csvheader: str
    imageurl: str
    image_height: str
    image_width: str
    object_type: str
    location: str
    other_fields: str

    def __init__(self, 
        artist = '',
        nationality = '',
        author = '',
        title = '',
        desc = '',
        depicted_people = '',
        date = '',
        medium = '',
        dimensions = '',
        institution = '',
        department = '',
        place_of_discovery = '',
        object_history = '', 
        exhibition_history = '',
        credit_line = '',
        inscriptions = '',
        notes = '',
        accession_number = '',
        place_of_creation = '',
        source = '',
        permission = '',
        other_versions = '',
        references = '',
        depicted_place = '',
        wikidata = '',
        categories = '',
        imageurl = '',
        image_height = '',
        image_width = '',
        object_type = '',
        location = '',
        other_fields = ''):

        self.artist = artist.rstrip('\n')
        self.nationality = nationality.rstrip('\n')
        self.author = author.rstrip('\n')
        self.title = title.rstrip('\n')
        self.depicted_people = depicted_people.rstrip('\n')
        self.desc = desc.rstrip('\n')
        self.date = date.rstrip('\n')
        self.medium = medium.rstrip('\n')
        self.dimensions = dimensions.rstrip('\n')
        self.institution = institution.rstrip('\n')
        self.department = department.rstrip('\n')
        self.place_of_discovery = place_of_discovery.rstrip('\n')
        self.object_history = object_history.rstrip('\n')
        self.exhibition_history = exhibition_history.rstrip('\n')
        self.credit_line = credit_line.rstrip('\n')
        self.inscriptions = inscriptions.rstrip('\n')
        self.notes = notes.rstrip('\n')
        self.accession_number = accession_number.rstrip('\n')
        self.place_of_creation = place_of_creation.rstrip('\n')
        self.source = source.rstrip('\n')
        self.permission = permission.rstrip('\n')
        self.other_versions = other_versions.rstrip('\n')
        self.references = references.rstrip('\n')
        self.depicted_place = depicted_place.rstrip('\n')
        self.wikidata = wikidata.rstrip('\n')
        self.categories = categories.rstrip('\n')
        self.image_height = image_height.rstrip('\n')
        self.image_width = image_width.rstrip('\n')
        self.imageurl = imageurl.rstrip('\n')
        self.object_type = object_type.rstrip('\n')
        self.location = location.rstrip('\n')
        self.other_fields = other_fields.rstrip('\n')

        self.GenerateWikiText()

    def GenerateWikiText(self):
        #complete this once if applies to all files
        self.wikitext = u"""{{Artwork
    |artist             = """ + str(self.artist) + """
    |author             = """ + str(self.author) + """
    |title              = """ + str(self.title) + """
    |description        = """ + str(self.desc) + """
    |depicted people    = """ + str(self.depicted_people) + """
    |date               = """ + str(self.date) + """
    |medium             = """ + str(self.medium) + """
    |dimensions         = """ + str(self.dimensions) + """
    |institution        = """ + str(self.institution) + """
    |department         = """ + str(self.department) + """
    |place of discovery = """ + str(self.place_of_discovery) + """
    |object history     = """ + str(self.object_history) + """ 
    |exhibition history = """ + str(self.exhibition_history) + """
    |credit line        = """ + str(self.credit_line) + """
    |inscriptions       = """ + str(self.inscriptions) + """
    |notes              = """ + str(self.notes) + """
    |accession number   = """ + str(self.accession_number) + """
    |place of creation  = """ + str(self.place_of_creation) + """
    |source             = """ + str(self.source) + """
    |other_versions     = """ + str(self.other_versions) + """
    |references         = """ + str(self.references) + """
    |depicted place     = """ + str(self.depicted_place) + """
    |object type        = """ + str(self.object_type) + """
    |location           = """ + str(self.location) + """
    |other_fields       = """ + str(self.other_fields) + """
    """
        if self.wikidata != '':
            self.wikitext = self.wikitext + """
    |wikidata           = """ + self.wikidata + """
    """
        self.wikitext = self.wikitext + """
}} 
=={{int:license-header}}==
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
        self.csvline = self.csvline + self.artist.replace(';', '&semi') + csvdelim
        self.csvline = self.csvline + self.nationality.replace(';', '&semi') + csvdelim
        self.csvline = self.csvline + self.author.replace(';', '&semi') + csvdelim
        self.csvline = self.csvline + self.title.replace(';', '&semi') + csvdelim
        self.csvline = self.csvline + self.desc.replace(';', '&semi') + csvdelim
        self.csvline = self.csvline + self.depicted_people.replace(';', '&semi') + csvdelim
        self.csvline = self.csvline + self.date.replace(';', '&semi') + csvdelim
        self.csvline = self.csvline + self.medium.replace(';', '&semi') + csvdelim
        self.csvline = self.csvline + self.dimensions.replace(';', '&semi') + csvdelim
        self.csvline = self.csvline + self.institution.replace(';', '&semi') + csvdelim
        self.csvline = self.csvline + self.department.replace(';', '&semi') + csvdelim
        self.csvline = self.csvline + self.place_of_discovery.replace(';', '&semi') + csvdelim
        self.csvline = self.csvline + self.object_history.replace(';', '&semi') + csvdelim
        self.csvline = self.csvline + self.exhibition_history.replace(';', '&semi') + csvdelim
        self.csvline = self.csvline + self.credit_line.replace(';', '&semi') + csvdelim
        self.csvline = self.csvline + self.inscriptions.replace(';', '&semi') + csvdelim
        self.csvline = self.csvline + self.notes.replace(';', '&semi') + csvdelim
        self.csvline = self.csvline + self.accession_number.replace(';', '&semi') + csvdelim
        self.csvline = self.csvline + self.place_of_creation.replace(';', '&semi') + csvdelim
        self.csvline = self.csvline + self.source.replace(';', '&semi') + csvdelim
        self.csvline = self.csvline + self.permission.replace(';', '&semi') + csvdelim
        self.csvline = self.csvline + self.other_versions.replace(';', '&semi') + csvdelim
        self.csvline = self.csvline + self.references.replace(';', '&semi') + csvdelim
        self.csvline = self.csvline + self.depicted_place.replace(';', '&semi') + csvdelim
        self.csvline = self.csvline + self.categories.replace(';', '&semi') + csvdelim
        self.csvline = self.csvline + self.wikidata.replace(';', '&semi') + csvdelim
        self.csvline = self.csvline + self.image_height.replace(';', '&semi') + csvdelim
        self.csvline = self.csvline + self.image_width.replace(';', '&semi') + csvdelim
        self.csvline = self.csvline + self.imageurl.replace(';', '&semi') + csvdelim
        self.csvline = self.csvline + self.object_type.replace(';', '&semi') + csvdelim
        self.csvline = self.csvline + self.location.replace(';', '&semi') + csvdelim 
        self.csvline = self.csvline + self.medium.replace(';', '&semi') + csvdelim
        self.csvline = self.csvline + self.other_fields.replace(';', '&semi') 
    
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

        self.csvheader = 'id' + csvdelim + \
          'created' + csvdelim + \
          'modified' + csvdelim + \
          'artist' + csvdelim + \
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
    
        return self.csvheader

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

def complete_desc_and_upload(filename, pagetitle, desc, date, categories):
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
    except Exception as e:
        print(str(e))

    print(targetSite)
    targetSite = pywikibot.Site('commons', 'commons')

    bot = UploadRobot(url, description=desc, useFilename=pagetitle, keepFilename=keepFilename, verifyDescription=verifyDescription, targetSite=targetSite, summary='Created artwork')
    bot.run()

#    page = pywikibot.Page(targetSite, 'File:' + filename)
#    page = pywikibot.Page(targetSite, 'File:' + filename)
#    print(page.text)
#    page.text = description
#    page.save('Replacing description')  # Saves the page

def complete_artwork_desc_and_upload(filename, pagetitle, desc, date, categories):
    #complete this once if applies to all files

    description = u"""{{Artwork
|Description    = {{en|1=""" + desc + """}}
|Source         = [[Statens Museeum for Kunst]]
|Author         = 
|Date           = """ + date + """
|Permission     = 
|other_versions = 
}}
=={{int:license-header}}==
{{PD-old-70}}

""" + categories + """
"""
    url = [ filename ]
    #keepFilename = False        #set to True to skip double-checking/editing destination filename
    keepFilename = True        #set to True to skip double-checking/editing destination filename
    #verifyDescription = True    #set to False to skip double-checking/editing description => change to bot-mode
    verifyDescription = False    #set to False to skip double-checking/editing description => change to bot-mode
    targetSite = pywikibot.Site(code='commons', fam='commons', user='Kim Bach')
    
    #bot = UploadRobot(url, description=description, useFilename=pagetitle, keepFilename=keepFilename, verifyDescription=verifyDescription, targetSite=targetSite)
    #bot.run()

#    page = pywikibot.Page(targetSite, 'File:' + filename)
    page = pywikibot.Page(targetSite, 'File:' + filename)
#    print(page.text)
    #page.text = description
    #page.save('Replacing description')  # Saves the page

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
    complete_artwork_desc_and_upload(filename, pagetitle, desc, date, categories)


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
