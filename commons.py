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

    def __init__(self, 
        artist = '',
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
        categories = ''):

        self.artist = artist
        self.author = author
        self.title = title
        self.depicted_people = depicted_people
        self.desc = desc
        self.date = date
        self.medium = medium
        self.dimensions = dimensions
        self.institution = institution
        self.department = department
        self.place_of_discovery = place_of_discovery
        self.object_history = object_history
        self.exhibition_history = exhibition_history
        self.credit_line = credit_line
        self.inscriptions = inscriptions
        self.notes = notes
        self.accession_number = accession_number
        self.place_of_creation = place_of_creation
        self.source = source
        self.permission = permission
        self.other_versions = other_versions
        self.references = references
        self.depicted_place = depicted_place
        self.wikidata = wikidata
        self.categories = categories
        self.GenerateWikiText()

    def GenerateWikiText(self):
        #complete this once if applies to all files

        self.wikitext = u"""{{Artwork
    |artist             = """ + self.artist + """
    |author             = """ + self.author + """
    |title              = """ + self.title + """
    |description        = {{en|1=""" + self.desc + """}}
    |depicted people    = """ + self.depicted_people + """
    |date               = """ + self.date + """
    |medium             = """ + self.medium + """
    |dimensions         = """ + self.dimensions + """
    |institution        = """ + self.institution + """
    |department         = """ + self.department + """
    |place of discovery = """ + self.place_of_discovery + """
    |object history     = """ + self.object_history + """ 
    |exhibition history = """ + self.exhibition_history + """
    |credit line        = """ + self.credit_line + """
    |inscriptions       = """ + self.inscriptions + """
    |notes              = """ + self.notes + """
    |accession number   = """ + self.accession_number + """
    |place of creation  = """ + self.place_of_creation + """
    |source             = """ + self.source + """
    |permission         = """ + self.permission + """
    |other_versions     = """ + self.other_versions + """
    |references         = """ + self.references + """
    |depicted place     = """ + self.depicted_place + """
    |wikidata           = """ + self.wikidata + """
    }}
    =={{int:license-header}}==
    <!-- your license --->

    """ + self.categories + """
    """
