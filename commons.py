# commons - module than implements helper classes for Wikimedia Commons
#
# Artwork class encapsulates the wikimedia commons temlate Artwork
#  
# This code parses date/times, so please
#
#     pip install python-dateutil
#

from dataclasses import dataclass
from typing import Any, Optional, List, TypeVar, Type, Callable, cast
from enum import Enum
from datetime import datetime
import dateutil.parser
from abc import ABCMeta, abstractmethod

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
        image_width = ''):

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
        self.GenerateWikiText()

    def GenerateWikiText(self):
        #complete this once if applies to all files

        self.wikitext = u"""{{Artwork
    |artist             = """ + '{{Creator:' + self.artist + '}}' + """
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
    |permission         = """ + str(self.permission) + """
    |other_versions     = """ + str(self.other_versions) + """
    |references         = """ + str(self.references) + """
    |depicted place     = """ + str(self.depicted_place) + """
    """
        if self.wikidata != '':
            self.wikitext = self.wikitext + """
    |wikidata           = """ + self.wikidata + """
    """

        self.wikitext = self.wikitext + """
}}
    """

    def GenerateCSVLine(self, csvdelim=';'):
        #complete this once if applies to all files
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
        self.csvline = self.csvline + self.imageurl 
    
        return self.csvline

    def GenerateCSVHeader(self, csvdelim=';'):
        #complete this once if applies to all files

        self.csvheader = 'artist' + csvdelim + \
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
          'imageurl'
    
        return self.csvheader
