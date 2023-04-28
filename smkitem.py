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
#     result = smk_item_from_dict(json.loads(json_string))

from typing import Any, List, TypeVar, Callable, Type, cast
from datetime import datetime
import dateutil.parser
import json
import logging
import smkapi

T = TypeVar("T")


def from_str(x: Any) -> str:
    assert isinstance(x, str)
    return x


def from_datetime(x: Any) -> datetime:
    return dateutil.parser.parse(x)


def from_bool(x: Any) -> bool:
    assert isinstance(x, bool)
    return x


def from_list(f: Callable[[Any], T], x: Any) -> List[T]:
    assert isinstance(x, list)
    return [f(y) for y in x]


def from_int(x: Any) -> int:
    assert isinstance(x, int) and not isinstance(x, bool)
    return x


def from_float(x: Any) -> float:
    assert isinstance(x, (float, int)) and not isinstance(x, bool)
    return float(x)


def to_class(c: Type[T], x: Any) -> dict:
    assert isinstance(x, c)
    return cast(Any, x).to_dict()


def to_float(x: Any) -> float:
    assert isinstance(x, float)
    return x


class Dimension:
    notes: str
    part: str
    type: str
    unit: str
    value: str

    def __init__(self, notes: str, part: str, type: str, unit: str, value: str) -> None:
        self.notes = notes
        self.part = part
        self.type = type
        self.unit = unit
        self.value = value

    @staticmethod
    def from_dict(obj: Any) -> 'Dimension':
        assert isinstance(obj, dict)
        notes = from_str(obj.get("notes", ""))
        part = from_str(obj.get("part", ""))
        type = from_str(obj.get("type", ""))
        unit = from_str(obj.get("unit", ""))
        value = from_str(obj.get("value", ""))
        return Dimension(notes, part, type, unit, value)

    def to_dict(self) -> dict:
        result: dict = {}
        result["notes"] = from_str(self.notes)
        result["part"] = from_str(self.part)
        result["type"] = from_str(self.type)
        result["unit"] = from_str(self.unit)
        result["value"] = from_str(self.value)
        return result


class Documentation:
    title: str
    author: str
    notes: str
    shelfmark: str
    year_of_publication: str

    def __init__(self, title: str, author: str, notes: str, shelfmark: str, year_of_publication: str) -> None:
        self.title = title
        self.author = author
        self.notes = notes
        self.shelfmark = shelfmark
        self.year_of_publication = year_of_publication

    @staticmethod
    def from_dict(obj: Any) -> 'Documentation':
        assert isinstance(obj, dict)
        title = from_str(obj.get("title", ""))
        author = from_str(obj.get("author", ""))
        notes = from_str(obj.get("notes", ""))
        shelfmark = from_str(obj.get("shelfmark", ""))
        year_of_publication = from_str(obj.get("year_of_publication", ""))
        return Documentation(title, author, notes, shelfmark, year_of_publication)

    def to_dict(self) -> dict:
        result: dict = {}
        result["title"] = from_str(self.title)
        result["author"] = from_str(self.author)
        result["notes"] = from_str(self.notes)
        result["shelfmark"] = from_str(self.shelfmark)
        result["year_of_publication"] = from_str(str(self.year_of_publication))
        return result

class Labels:
    text: str
    type: str
    source: str
    date: datetime 

    def __init__(self, text: str, type:str, source: str, date: datetime) -> None:
        self.text = text
        self.type = type
        self.source = source
        self.date = date 

    @staticmethod
    def from_dict(obj: Any) -> 'Labels':
        assert isinstance(obj, dict)
        text = from_str(obj.get("text"), "")
        type = from_str(obj.get("type"), "")
        source = from_str(obj.get("source"), "")
        date = from_datetime(obj.get("date"), None)
        return Labels(text, type, source, date)

    def to_dict(self) -> dict:
        result: dict = {}
        result["text"] = from_str(self.text)
        result["type"] = from_str(self.type)
        result["source"] = from_str(self.source)
        result["date"] = from_datetime(self.date)
        return result

class Exhibition:
    exhibition: str
    date_start: datetime
    date_end: datetime
    venue: str

    def __init__(self, exhibition: str, date_start: datetime, date_end: datetime, venue: str) -> None:
        self.exhibition = exhibition
        self.date_start = date_start
        self.date_end = date_end
        self.venue = venue

    @staticmethod
    def from_dict(obj: Any) -> 'Exhibition':
        assert isinstance(obj, dict)
        exhibition = from_str(obj.get("exhibition", ""))
        date_start = from_datetime(obj.get("date_start", None))
        date_end = from_datetime(obj.get("date_end", None))
        venue = from_str(obj.get("venue"))
        return Exhibition(exhibition, date_start, date_end, venue)

    def to_dict(self) -> dict:
        result: dict = {}
        result["exhibition"] = from_str(self.exhibition)
        result["date_start"] = self.date_start.isoformat()
        result["date_end"] = self.date_end.isoformat()
        result["venue"] = from_str(self.venue)
        return result


class Inscription:
    content: str
    type: str
    language: str
    position: str

    def __init__(self, content: str, type: str, language: str, position: str) -> None:
        self.content = content
        self.type = type
        self.language = language
        self.position = position

    @staticmethod
    def from_dict(obj: Any) -> 'Inscription':
        assert isinstance(obj, dict)
        content = from_str(obj.get("content", ""))
        type = from_str(obj.get("type", ""))
        language = from_str(obj.get("language", ""))
        position = from_str(obj.get("position", ""))
        return Inscription(content, type, language, position)

    def to_dict(self) -> dict:
        result: dict = {}
        result["content"] = from_str(self.content)
        result["type"] = from_str(self.type)
        result["language"] = from_str(self.language)
        return result


class ObjectName:
    name: str

    def __init__(self, name: str) -> None:
        self.name = name

    @staticmethod
    def from_dict(obj: Any) -> 'ObjectName':
        assert isinstance(obj, dict)
        name = from_str(obj.get("name", ""))
        return ObjectName(name)

    def to_dict(self) -> dict:
        result: dict = {}
        result["name"] = from_str(self.name)
        return result


class Production:
    creator: str
    creator_forename: str
    creator_surname: str
    creator_date_of_birth: datetime
    creator_date_of_death: datetime
    creator_nationality: str
    creator_gender: str
    creator_history: str
    creator_lref: str

    def __init__(self, creator: str, creator_forename: str, creator_surname: str, creator_date_of_birth: datetime, creator_date_of_death: datetime, creator_nationality: str, creator_gender: str, creator_history: str, creator_lref: str) -> None:
        self.creator = creator
        self.creator_forename = creator_forename
        self.creator_surname = creator_surname
        self.creator_date_of_birth = creator_date_of_birth
        self.creator_date_of_death = creator_date_of_death
        self.creator_nationality = creator_nationality
        self.creator_gender = creator_gender
        self.creator_history = creator_history
        self.creator_lref = creator_lref

    @staticmethod
    def from_dict(obj: Any) -> 'Production':
        assert isinstance(obj, dict)
        try:
            creator = from_str(obj.get("creator", ""))
        except:
            creator = ""
        try:
            creator_forename = from_str(obj.get("creator_forename", ""))
        except:
            creator_forename = ""
        try:
            creator_surname = from_str(obj.get("creator_surname", ""))
        except:
            creator_surname = ""
        try:
            creator_date_of_birth = from_datetime(obj.get("creator_date_of_birth", None))
        except:
            creator_date_of_birth = ""
        try:
            creator_date_of_death = from_datetime(obj.get("creator_date_of_death"), None)
        except:
            creator_date_of_death = ""
        try:
            creator_nationality = from_str(obj.get("creator_nationality", ""))
        except:
            creator_nationality = ""
        try:
            creator_gender = from_str(obj.get("creator_gender", ""))
        except:
            creator_gender = ""
        try:
            creator_history = from_str(obj.get("creator_history", ""))
        except:
            creator_history = ""
        try:
            creator_lref = from_str(obj.get("creator_lref", ""))
        except:
            creator_lref = ""
        return Production(creator, creator_forename, creator_surname, creator_date_of_birth, creator_date_of_death, creator_nationality, creator_gender, creator_history, creator_lref)

    def to_dict(self) -> dict:
        result: dict = {}
        result["creator"] = from_str(self.creator)
        result["creator_forename"] = from_str(self.creator_forename)
        result["creator_surname"] = from_str(self.creator_surname)
        result["creator_date_of_birth"] = self.creator_date_of_birth.isoformat()
        result["creator_date_of_death"] = self.creator_date_of_death.isoformat()
        result["creator_nationality"] = from_str(self.creator_nationality)
        result["creator_gender"] = from_str(self.creator_gender)
        result["creator_history"] = from_str(self.creator_history)
        result["creator_lref"] = from_str(self.creator_lref)
        return result

    def csv_header(self,delimiter=";"):
        csv_str = "creator" + delimiter
        csv_str = csv_str + "creator_forename" + delimiter
        csv_str = csv_str + "creator_surname" + delimiter
        csv_str = csv_str + "creator_date_of_birth.strftime" + delimiter
        csv_str = csv_str + "creator_date_of_death" + delimiter
        csv_str = csv_str + "creator_nationality" + delimiter
        csv_str = csv_str + "creator_gender" + delimiter
        csv_str = csv_str + "creator_history" + delimiter
        csv_str = csv_str + "creator_lref"
        return csv_str

    def csv_line(self,delimiter=";"):
        csv_str = '"' + self.creator + '"' + delimiter
        csv_str = csv_str + '"' + self.creator_forename + '"' + delimiter
        csv_str = csv_str + '"' + self.creator_surname + '"' + delimiter
        try:
            csv_str = csv_str + self.creator_date_of_birth.strftime("%Y-%m-%dT%H:%M:%SZ") + delimiter
        except:
            csv_str = csv_str + delimiter
        try:
            csv_str = csv_str + self.creator_date_of_death.strftime("%Y-%m-%dT%H:%M:%SZ") + delimiter
        except:
            csv_str = csv_str + delimiter
        csv_str = csv_str + '"' + self.creator_nationality + '"' +  delimiter
        csv_str = csv_str + '"' + self.creator_gender + '"' + delimiter
        csv_str = csv_str + '"' + self.creator_history + '"' + delimiter
        csv_str = csv_str + self.creator_lref
        return csv_str

class ProductionDate:
    start: datetime
    end: datetime
    period: int

    def __init__(self, start: datetime, end: datetime, period: int) -> None:
        self.start = start
        self.end = end
        self.period = period

    @staticmethod
    def from_dict(obj: Any) -> 'ProductionDate':
        assert isinstance(obj, dict)
        start = from_datetime(obj.get("start", None))
        end = from_datetime(obj.get("end", None))
        period = int(from_str(obj.get("period", None)))
        return ProductionDate(start, end, period)

    def to_dict(self) -> dict:
        result: dict = {}
        result["start"] = self.start.isoformat()
        result["end"] = self.end.isoformat()
        result["period"] = from_str(str(self.period))
        return result


class Title:
    title: str
    type: str
    language: str

    def __init__(self, title: str, type: str, language: str) -> None:
        self.title = title
        self.type = type
        self.language = language

    @staticmethod
    def from_dict(obj: Any) -> 'Title':
        assert isinstance(obj, dict)
        title = from_str(obj.get("title", ""))
        type = from_str(obj.get("type", ""))
        language = from_str(obj.get("language", ""))
        return Title(title, type, language)

    def to_dict(self) -> dict:
        result: dict = {}
        result["title"] = from_str(self.title)
        result["type"] = from_str(self.type)
        result["language"] = from_str(self.language)
        return result


class Item:
    id: str
    created: datetime
    modified: datetime
    responsible_department: str
    collection: List[str]
    backside_protection: bool
    acquisition_date: datetime
    acquisition_date_precision: datetime
    dimensions: List[Dimension]
    documentation: List[Documentation]
    labels: List[Labels]
    exhibitions: List[Exhibition]
    inscriptions: List[Inscription]
    materials: List[str]
    object_names: List[ObjectName]
    production: List[Production]
    production_date: List[ProductionDate]
    techniques: List[str]
    titles: List[Title]
    medium: List[str]
    number_of_parts: int
    notes: List[str]
    object_history_note: List[str]
    object_number: str
    object_url: str
    frontend_url: str
    iiif_manifest: str
    enrichment_url: str
    similar_images_url: str
    production_dates_notes: List[str]
    public_domain: bool
    rights: str
    on_display: bool
    has_image: bool
    image_width: int
    image_height: int
    image_thumbnail: str
    image_native: str
    colors: List[str]
    suggested_bg_color: List[str]
    entropy: float
    contrast: float
    saturation: float
    colortemp: float
    brightness: float
    has_text: bool
    has_3_d_file: bool
    artist: List[str]
    content_description: List[str]
    distinguishing_features: List[str]

    def __init__(self, id: str, created: datetime, modified: datetime, responsible_department: str, collection: List[str], backside_protection: bool, acquisition_date: datetime, acquisition_date_precision: datetime, dimensions: List[Dimension], documentation: List[Documentation], labels: List[Labels], exhibitions: List[Exhibition], inscriptions: List[Inscription], materials: List[str], object_names: List[ObjectName], production: List[Production], production_date: List[ProductionDate], techniques: List[str], titles: List[Title], medium: List[str], notes: List[str], object_history_note: List[str], number_of_parts: int, object_number: str, object_url: str, frontend_url: str, iiif_manifest: str, enrichment_url: str, similar_images_url: str, production_dates_notes: List[str], public_domain: bool, rights: str, on_display: bool, has_image: bool, image_width: int, image_height: int, image_thumbnail: str, image_native: str, colors: List[str], suggested_bg_color: List[str], entropy: float, contrast: float, saturation: float, colortemp: float, brightness: float, has_text: bool, has_3_d_file: bool, artist: List[str], content_description: List[str], distinguishing_features: List[str]) -> None:
        self.id = id
        self.created = created
        self.modified = modified
        self.responsible_department = responsible_department
        self.collection = collection
        self.backside_protection = backside_protection
        self.acquisition_date = acquisition_date
        self.acquisition_date_precision = acquisition_date_precision
        self.dimensions = dimensions
        self.documentation = documentation
        self.labels = labels
        self.exhibitions = exhibitions
        self.inscriptions = inscriptions
        self.materials = materials
        self.object_names = object_names
        self.production = production
        self.production_date = production_date
        self.techniques = techniques
        self.titles = titles
        self.medium = medium
        self.notes = notes
        self.object_history_note = object_history_note
        self.number_of_parts = number_of_parts
        self.object_number = object_number
        self.object_url = object_url
        self.frontend_url = frontend_url
        self.iiif_manifest = iiif_manifest
        self.enrichment_url = enrichment_url
        self.similar_images_url = similar_images_url
        self.production_dates_notes = production_dates_notes
        self.public_domain = public_domain
        self.rights = rights
        self.on_display = on_display
        self.has_image = has_image
        self.image_width = image_width
        self.image_height = image_height
        self.image_thumbnail = image_thumbnail
        self.image_native = image_native
        self.colors = colors
        self.suggested_bg_color = suggested_bg_color
        self.entropy = entropy
        self.contrast = contrast
        self.saturation = saturation
        self.colortemp = colortemp
        self.brightness = brightness
        self.has_text = has_text
        self.has_3_d_file = has_3_d_file
        self.artist = artist
        self.content_description = content_description
        self.distinguishing_features = distinguishing_features

    @staticmethod
    def from_dict(obj: Any) -> 'Item':
        assert isinstance(obj, dict)
        try:
            id = from_str(obj.get("id"), "")
        except:
            id = ""
        try:
            created = from_datetime(obj.get("created", None))
        except:
            created = None
        try:
            modified = from_datetime(obj.get("modified", None))
        except:
            modified = None
        try:
            responsible_department = from_str(obj.get("responsible_department"), "")
        except:
            responsible_department = ""
        try:
            collection = from_str(obj.get("collection"), [])
        except:
            collection = []
        try:
            backside_protection = from_bool(obj.get("backside_protection", None))
        except:
            backside_protection = None

        try:
            acquisition_date = from_datetime(obj.get("acquisition_date", None))
        except:
            acquisition_date = None
        try:
            acquisition_date_precision = from_datetime(obj.get("acquisition_date_precision", None))
        except:
            acquisition_date_precision = None
        try:
            dimensions = from_list(Dimension.from_dict, obj.get("dimensions", []))
        except Exception as e:
            dimensions = []
            print('EXCEPTION! '+ str(e))
            logging.exception(e)
        try:
            documentation = from_list(Documentation.from_dict, obj.get("documentation", []))
        except Exception as e:
            documentation = []
            print('EXCEPTION! '+ str(e))
            logging.exception(e)

        try:
            labels = from_list(Labels.from_dict, obj.get("labels", []))
        except:
            labels = []
        
        try:
            exhibitions = from_list(Exhibition.from_dict, obj.get("exhibitions", []))
        except:
            exhibitions = []
        
        try:
            inscriptions = from_list(Inscription.from_dict, obj.get("inscriptions", []))
        except:
            inscriptions = []

        try:
            materials = from_list(from_str, obj.get("materials", []))
        except:
            materials = []

        try:
            object_names = from_list(ObjectName.from_dict, obj.get("object_names", []))
        except:
            object_names = []
        
        try:
            production = from_list(Production.from_dict, obj.get("production", []))
        except:
            production = []
        
        try:
            production_date = from_list(ProductionDate.from_dict, obj.get("production_date", []))
        except:
            production_date = []
        
        try:
            techniques = from_list(from_str, obj.get("techniques", []))
        except:
            techniques = []

        try:
            titles = from_list(Title.from_dict, obj.get("titles", []))
        except:
            titles = []
        
        try:
            medium = from_list(from_str, obj.get("medium", []))
        except:
            medium = []
        
        try:
            notes = from_list(from_str, obj.get("notes", []))
        except:
            notes = []

        try:
            object_history_note = from_list(from_str, obj.get("object_history_note", []))
        except:
            object_history_note = []

        try:
            number_of_parts = from_int(obj.get("number_of_parts", None))
        except:
            number_of_parts = -1
        try:
            object_number = from_str(obj.get("object_number"))
        except:
            object_number = ""

        try:
            object_url = from_str(obj.get("object_url", ""))
        except:
            object_url = ""
        try:
            frontend_url = from_str(obj.get("frontend_url", ""))
        except:
            frontend_url = ""
        try:
            iiif_manifest = from_str(obj.get("iiif_manifest", ""))
        except:
            iiif_manifest = ""
        try:
            enrichment_url = from_str(obj.get("enrichment_url", ""))
        except:
            enrichment_url = ""
        try:
            similar_images_url = from_str(obj.get("similar_images_url", ""))
        except:
            similar_images_url = ""
        try:    
            production_dates_notes = from_list(from_str, obj.get("production_dates_notes", []))
        except:
            production_dates_notes = []
        try:
            public_domain = from_bool(obj.get("public_domain", None))
        except:
            public_domain = False
        try:
            rights = from_str(obj.get("rights", ""))
        except:
            rights = ""
        try:
            on_display = from_bool(obj.get("on_display", None))
        except:
            on_display = False
        try:
            has_image = from_bool(obj.get("has_image", None))
        except:
            has_image = False
        try:
            image_width = from_int(obj.get("image_width", None))
        except:
            image_width = -1
        try:
            image_height = from_int(obj.get("image_height", None))
        except:
            image_height = -1
        try:
            image_thumbnail = from_str(obj.get("image_thumbnail, """))
        except:
            image_thumbnail = ""
        try:
            image_native = from_str(obj.get("image_native", ""))
        except:
            image_native = ""
        try:
            colors = from_list(from_str, obj.get("colors", []))
        except:
            colors = []

        try:
            suggested_bg_color = from_list(from_str, obj.get("suggested_bg_color", []))
        except:
            suggested_bg_color = []

        try:
            entropy = from_float(obj.get("entropy", None))
        except:
            entropy = -1
        try:
            contrast = from_float(obj.get("contrast", None))
        except:
            contrast = -1
        try:
            saturation = from_float(obj.get("saturation", None))
        except:
            saturation = -1
        try:
            colortemp = from_float(obj.get("colortemp", None))
        except:
            colortemp = -1
        try:
            brightness = from_float(obj.get("brightness", None))
        except:
            brightness = -1
        try:
            has_text = from_bool(obj.get("has_text", None))
        except:
            has_text = -1
        try:
            has_3_d_file = from_bool(obj.get("has_3d_file", None))
        except:
            has_3_d_file = -1
        try:
            artist = from_list(from_str, obj.get("artist", []))
        except:
            artist = []
        try:
            content_description = from_list(from_str, obj.get("content_description", []))
        except:
            content_description = []
        try:
            distinguishing_features = from_list(from_str, obj.get("distinguishing_features", []))
        except:
            distinguishing_features = []

        return Item(id, created, modified, responsible_department, collection, backside_protection, acquisition_date, acquisition_date_precision, dimensions, documentation, labels, exhibitions, inscriptions, materials, object_names, production, production_date, techniques, titles, medium, notes, object_history_note, number_of_parts, object_number, object_url, frontend_url, iiif_manifest, enrichment_url, similar_images_url, production_dates_notes, public_domain, rights, on_display, has_image, image_width, image_height, image_thumbnail, image_native, colors, suggested_bg_color, entropy, contrast, saturation, colortemp, brightness, has_text, has_3_d_file, artist, content_description, distinguishing_features)

    def to_dict(self) -> dict:
        result: dict = {}
        result["id"] = from_str(self.id)
        result["created"] = self.created.isoformat()
        result["modified"] = self.modified.isoformat()
        result["responsible_department"] = from_str(self.responsible_department)
        result["collection"] = from_str(self.collection)
        result["backside_protection"] = from_bool(self.backside_protection)
        result["acquisition_date"] = self.acquisition_date.isoformat()
        result["acquisition_date_precision"] = self.acquisition_date_precision.isoformat()
        result["dimensions"] = from_list(lambda x: to_class(Dimension, x), self.dimensions)
        result["documentation"] = from_list(lambda x: to_class(Documentation, x), self.documentation)
        result["labels"] = from_list(lambda x: to_class(Labels, x), self.labels)
        result["exhibitions"] = from_list(lambda x: to_class(Exhibition, x), self.exhibitions)
        result["inscriptions"] = from_list(lambda x: to_class(Inscription, x), self.inscriptions)
        result["materials"] = from_list(from_str, self.materials)
        result["object_names"] = from_list(lambda x: to_class(ObjectName, x), self.object_names)
        result["production"] = from_list(lambda x: to_class(Production, x), self.production)
        result["production_date"] = from_list(lambda x: to_class(ProductionDate, x), self.production_date)
        result["techniques"] = from_list(from_str, self.techniques)
        result["titles"] = from_list(lambda x: to_class(Title, x), self.titles)
        result["medium"] = from_list(from_str, self.medium)
        result["notes"] = from_list(from_str, self.notes)
        result["object_history_note"] = from_list(from_str, self.object_history_note)
        result["number_of_parts"] = from_int(self.number_of_parts)
        result["object_number"] = from_str(self.object_number)
        result["object_url"] = from_str(self.object_url)
        result["frontend_url"] = from_str(self.frontend_url)
        result["iiif_manifest"] = from_str(self.iiif_manifest)
        result["enrichment_url"] = from_str(self.enrichment_url)
        result["similar_images_url"] = from_str(self.similar_images_url)
        result["production_dates_notes"] = from_list(from_str, self.production_dates_notes)
        result["public_domain"] = from_bool(self.public_domain)
        result["rights"] = from_str(self.rights)
        result["on_display"] = from_bool(self.on_display)
        result["has_image"] = from_bool(self.has_image)
        result["image_width"] = from_int(self.image_width)
        result["image_height"] = from_int(self.image_height)
        result["image_thumbnail"] = from_str(self.image_thumbnail)
        result["image_native"] = from_str(self.image_native)
        result["colors"] = from_list(from_str, self.colors)
        result["suggested_bg_color"] = from_list(from_str, self.suggested_bg_color)
        result["entropy"] = to_float(self.entropy)
        result["contrast"] = to_float(self.contrast)
        result["saturation"] = to_float(self.saturation)
        result["colortemp"] = to_float(self.colortemp)
        result["brightness"] = to_float(self.brightness)
        result["has_text"] = from_bool(self.has_text)
        result["has_3d_file"] = from_bool(self.has_3_d_file)
        result["artist"] = from_list(from_str, self.artist)
        result["content_description"] = from_list(from_str, self.content_description)
        result["distinguishing_features"] = from_list(from_str, self.distinguishing_features)
        return result

    def production_csvheader(self,delimiter=";"):
        csv_str = "timestamp" + delimiter
        csv_str = csv_str + "id" + delimiter
        csv_str = csv_str + "frontend_url"
        csv_str = csv_str + delimiter + Production.csv_header(delimiter)
        return csv_str

    def production_csv(self,production,delimiter=";"):
        csv_str = datetime.now().strftime("%Y-%m-%dT%H:%M:%SZ") + delimiter
        csv_str = csv_str + self.id + delimiter
        csv_str = csv_str + self.frontend_url
        csv_str = csv_str + delimiter + production.csv_line(delimiter)
        return csv_str

class SMKItem:
    items: List[Item]

    def __init__(self, items: List[Item]) -> None:
        self.items = items

    @staticmethod
    def from_dict(obj: Any) -> 'SMKItem':
        assert isinstance(obj, dict)
        items = from_list(Item.from_dict, obj.get("items", []))
        return SMKItem(items)

    def to_dict(self) -> dict:
        result: dict = {}
        result["items"] = from_list(lambda x: to_class(Item, x), self.items)
        return result


def smk_item_from_dict(s: Any) -> SMKItem:
    return SMKItem.from_dict(s)


def smk_item_to_dict(x: SMKItem) -> Any:
    return to_class(SMKItem, x)

# Example Usage

#jsonobject=json.loads(jsonstring)
#result = welcome_from_dict(jsonobject)
#print (result)

def test():

    # Set up logging
    artwork_error_log = "artwork_error.log"
    logging.basicConfig(filename=artwork_error_log,level=logging.ERROR,format='%(asctime)s %(message)s', datefmt='%Y-%m-%d %H:%M:%S')

    #smk_number_list = ["KKSgb29511","KMS8469"]
    smk_number_list = None
    smk_filter_list = [["public_domain","true"],
        ["has_image", "true"],
        ["creator_gender", "kvinde"],
        ["creator_nationality", "dansk"]]
    smk_filter_list = [["public_domain","true"],
        ["has_image", "true"]]
    smk_filter_list = ""

    # Generate SMK API filters from filter list
    smk_filter=smkapi.generate_smk_filter(smk_filter_list)
    #url='https://api.smk.dk/api/v1/art/search/?keys=*&filters=%5Bpublic_domain%3Atrue%5D,%5Bhas_image%3Atrue%5D,%5Bcreator_gender%3Akvinde%5D,%5Bcreator_nationality%3Adansk&offset='+str(offset)+'&rows='+str(rows)
    offset=0
    rows=1
    items = 0

    output_filename = "all_artists"
    #f_csv = open(output_filename+'.csv', 'w')
    #f_csv.write(Item.production_csvheader(";") + '\n')
    while True:
        if smk_number_list==None:
            try:
                smk_json=smkapi.get_smk_objects(smk_filter,offset, rows)
                smk_objects=json.loads(smk_json)
                smk_object_model = smk_item_from_dict(smk_objects)
                for item in smk_object_model.items:
                    #for production in item.production:
                    #    csv_str = item.production_csv(production, ";")
                    #    f_csv.write(csv_str + '\n')
                    # for object_name in item.object_names:
                    #     f_object_names = open(output_filename+'_object_names.csv', 'a')
                    #     f_object_names.write(object_name.name + '\n')
                    #     f_object_names.close()
                        
                    # for material in item.materials:
                    #     f_material = open(output_filename+'_materials.csv', 'a')
                    #     f_material.write(material + '\n')
                    #     f_material.close()
                        
                    # for technique in item.techniques:
                    #     f_techniques = open(output_filename+'_techniques.csv', 'a')
                    #     f_techniques.write(technique + '\n')
                    #     f_techniques.close()
                    
                    # for medium in item.medium:
                    #     f_media = open(output_filename+'_media.csv', 'a')
                    #     f_media.write(medium + '\n')
                    #     f_media.close()
                    
                    # for color in item.colors:
                    #     f_colors = open(output_filename+'_colors.csv', 'a')
                    #     f_colors.write(color + '\n')
                    #     f_colors.close()

                    # for suggested_bg_color in item.suggested_bg_color:
                    #     f_suggested_bg_colors = open(output_filename+'_colors.csv', 'a')
                    #     f_suggested_bg_colors.write(suggested_bg_color + '\n')
                    #     f_suggested_bg_colors.close()

                    for exhibition in item.exhibitions:
                        f_exhibitions = open(output_filename+'_exhibitions.txt', 'a')
                        f_exhibitions.write(exhibition.exhibition + '\n')
                        f_exhibitions.close()
                        f_venues = open(output_filename+'_venues.txt', 'a')
                        f_venues.write(exhibition.venue + '\n')
                        f_venues.close()

                offset=offset+1
                found=smk_objects['found']
                if offset>found:
                    break
                print('\r' + str(items), end='', flush=True)
                items = items + 1
            except Exception as e:
                print('\nException: '+str(datetime.now())+': ' + str(e)+'\n')
                logging.exception(e)
        else:
            if len(smk_number_list)==0:
                break
            else:
                current_number=smk_number_list[0]
                smk_number_list.remove(current_number)
                smk_json=smkapi.get_smk_object(current_number)
                smk_objects=json.loads(smk_json)
                
                smk_object_model = smk_item_from_dict(smk_objects)
                
                for item in smk_object_model.items:
                    for production in item.production:
                        csv_str = item.production_csv(production, ";")
                        #f_csv.write(csv_str + '\n')
                        print(production.csv_line())
    #f_csv.close()

#test()