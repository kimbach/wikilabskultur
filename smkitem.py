# smkitem module models the API object model from Statens Museeum for Kunst
#
# The main class: Item, was auto-generated from the API using https://app.quicktype.io
# Using this API call
# https://api.smk.dk/api/v1/art/search/?keys=*&filters=%5Bpublic_domain%3Atrue%5D,%5Bhas_image%3Atrue%5D&offset=0&rows=10
#  
# Yielding this code
# https://app.quicktype.io?share=q7q5bhqKximgfNuxroSP
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

T = TypeVar("T")
EnumT = TypeVar("EnumT", bound=Enum)

def from_str(x: Any) -> str:
    assert isinstance(x, str)
    return x


def from_int(x: Any) -> int:
    assert isinstance(x, int) and not isinstance(x, bool)
    return x


def from_none(x: Any) -> Any:
    assert x is None
    return x


def from_union(fs, x):
    for f in fs:
        try:
            return f(x)
        except:
            pass
    assert False


def to_enum(c: Type[EnumT], x: Any) -> EnumT:
    assert isinstance(x, c)
    return x.value


def from_datetime(x: Any) -> datetime:
    return dateutil.parser.parse(x)


def from_list(f: Callable[[Any], T], x: Any) -> List[T]:
    assert isinstance(x, list)
    return [f(y) for y in x]


def from_bool(x: Any) -> bool:
    assert isinstance(x, bool)
    return x


def to_class(c: Type[T], x: Any) -> dict:
    assert isinstance(x, c)
    return cast(Any, x).to_dict()


@dataclass
class Facets:
    pass

    @staticmethod
    def from_dict(obj: Any) -> 'Facets':
        assert isinstance(obj, dict)
        return Facets()

    def to_dict(self) -> dict:
        result: dict = {}
        return result


@dataclass
class AlternativeImage:
    mime_type: str
    iiif_id: str
    iiif_info: str
    width: int
    height: int
    size: int
    thumbnail: str
    native: str
    orientation: str

    @staticmethod
    def from_dict(obj: Any) -> 'AlternativeImage':
        assert isinstance(obj, dict)
        mime_type = from_str(obj.get("mime_type"))
        iiif_id = from_str(obj.get("iiif_id"))
        iiif_info = from_str(obj.get("iiif_info"))
        width = from_int(obj.get("width"))
        height = from_int(obj.get("height"))
        size = from_int(obj.get("size"))
        thumbnail = from_str(obj.get("thumbnail"))
        native = from_str(obj.get("native"))
        orientation = from_str(obj.get("orientation"))
        return AlternativeImage(mime_type, iiif_id, iiif_info, width, height, size, thumbnail, native, orientation)

    def to_dict(self) -> dict:
        result: dict = {}
        result["mime_type"] = from_str(self.mime_type)
        result["iiif_id"] = from_str(self.iiif_id)
        result["iiif_info"] = from_str(self.iiif_info)
        result["width"] = from_int(self.width)
        result["height"] = from_int(self.height)
        result["size"] = from_int(self.size)
        result["thumbnail"] = from_str(self.thumbnail)
        result["native"] = from_str(self.native)
        result["orientation"] = from_str(self.orientation)
        return result


class Part(Enum):
    BILLEDMAAL = "billedmaal"
    BLADMAAL = "bladmaal"
    PLADEMAAL = "plademaal"


class DimensionType(Enum):
    BREDDE = "bredde"
    HOJDE = "hojde"


class Unit(Enum):
    MM = "mm"


@dataclass
class Dimension:
    part: Part
    type: DimensionType
    unit: Unit
    value: int
    notes: Optional[str] = None

    @staticmethod
    def from_dict(obj: Any) -> 'Dimension':
        assert isinstance(obj, dict)
        part = Part(obj.get("part"))
        type = DimensionType(obj.get("type"))
        unit = Unit(obj.get("unit"))
        value = int(from_str(obj.get("value")))
        notes = from_union([from_str, from_none], obj.get("notes"))
        return Dimension(part, type, unit, value, notes)

    def to_dict(self) -> dict:
        result: dict = {}
        result["part"] = to_enum(Part, self.part)
        result["type"] = to_enum(DimensionType, self.type)
        result["unit"] = to_enum(Unit, self.unit)
        result["value"] = from_str(str(self.value))
        result["notes"] = from_union([from_str, from_none], self.notes)
        return result


@dataclass
class Documentation:
    title: str
    author: str
    notes: str
    shelfmark: str

    @staticmethod
    def from_dict(obj: Any) -> 'Documentation':
        assert isinstance(obj, dict)
        title = from_str(obj.get("title"))
        author = from_str(obj.get("author"))
        notes = from_str(obj.get("notes"))
        shelfmark = from_str(obj.get("shelfmark"))
        return Documentation(title, author, notes, shelfmark)

    def to_dict(self) -> dict:
        result: dict = {}
        result["title"] = from_str(self.title)
        result["author"] = from_str(self.author)
        result["notes"] = from_str(self.notes)
        result["shelfmark"] = from_str(self.shelfmark)
        return result


@dataclass
class Exhibition:
    exhibition: str
    date_start: datetime
    date_end: datetime
    venue: str

    @staticmethod
    def from_dict(obj: Any) -> 'Exhibition':
        assert isinstance(obj, dict)
        exhibition = from_str(obj.get("exhibition"))
        date_start = from_datetime(obj.get("date_start"))
        date_end = from_datetime(obj.get("date_end"))
        venue = from_str(obj.get("venue"))
        return Exhibition(exhibition, date_start, date_end, venue)

    def to_dict(self) -> dict:
        result: dict = {}
        result["exhibition"] = from_str(self.exhibition)
        result["date_start"] = self.date_start.isoformat()
        result["date_end"] = self.date_end.isoformat()
        result["venue"] = from_str(self.venue)
        return result


class FrameNote(Enum):
    BAGKLÆDNING_FALSE = "Bagklædning: false"
    MIKROKLIMARAMME_FALSE = "Mikroklimaramme: false"


@dataclass
class Inscription:
    content: str
    position: Optional[str] = None
    language: Optional[str] = None
    method: Optional[str] = None

    @staticmethod
    def from_dict(obj: Any) -> 'Inscription':
        assert isinstance(obj, dict)
        content = from_str(obj.get("content"))
        position = from_union([from_str, from_none], obj.get("position"))
        language = from_union([from_str, from_none], obj.get("language"))
        method = from_union([from_str, from_none], obj.get("method"))
        return Inscription(content, position, language, method)

    def to_dict(self) -> dict:
        result: dict = {}
        result["content"] = from_str(self.content)
        result["position"] = from_union([from_str, from_none], self.position)
        result["language"] = from_union([from_str, from_none], self.language)
        result["method"] = from_union([from_str, from_none], self.method)
        return result


@dataclass
class ObjectName:
    name: str

    @staticmethod
    def from_dict(obj: Any) -> 'ObjectName':
        assert isinstance(obj, dict)
        name = from_str(obj.get("name"))
        return ObjectName(name)

    def to_dict(self) -> dict:
        result: dict = {}
        result["name"] = from_str(self.name)
        return result


class CreatorNationality(Enum):
    DANSK = "dansk"
    HOLLANDSK = "hollandsk"
    TYSK = "tysk"


@dataclass
class Production:
    creator: str
    creator_date_of_birth: datetime
    creator_date_of_death: datetime
    creator_lref: str
    creator_nationality: Optional[CreatorNationality] = None
    notes: Optional[str] = None
    creator_history: Optional[str] = None
    creator_qualifier: Optional[str] = None
    creator_role: Optional[str] = None

    @staticmethod
    def from_dict(obj: Any) -> 'Production':
        assert isinstance(obj, dict)
        creator = from_str(obj.get("creator"))
        creator_date_of_birth = from_datetime(obj.get("creator_date_of_birth"))
        creator_date_of_death = from_datetime(obj.get("creator_date_of_death"))
        creator_lref = from_str(obj.get("creator_lref"))
        creator_nationality = from_union([CreatorNationality, from_none], obj.get("creator_nationality"))
        notes = from_union([from_str, from_none], obj.get("notes"))
        creator_history = from_union([from_str, from_none], obj.get("creator_history"))
        creator_qualifier = from_union([from_str, from_none], obj.get("creator_qualifier"))
        creator_role = from_union([from_str, from_none], obj.get("creator_role"))
        return Production(creator, creator_date_of_birth, creator_date_of_death, creator_lref, creator_nationality, notes, creator_history, creator_qualifier, creator_role)

    def to_dict(self) -> dict:
        result: dict = {}
        result["creator"] = from_str(self.creator)
        result["creator_date_of_birth"] = self.creator_date_of_birth.isoformat()
        result["creator_date_of_death"] = self.creator_date_of_death.isoformat()
        result["creator_lref"] = from_str(self.creator_lref)
        result["creator_nationality"] = from_union([lambda x: to_enum(CreatorNationality, x), from_none], self.creator_nationality)
        result["notes"] = from_union([from_str, from_none], self.notes)
        result["creator_history"] = from_union([from_str, from_none], self.creator_history)
        result["creator_qualifier"] = from_union([from_str, from_none], self.creator_qualifier)
        result["creator_role"] = from_union([from_str, from_none], self.creator_role)
        return result


@dataclass
class ProductionDate:
    start: datetime
    end: datetime
    period: str

    @staticmethod
    def from_dict(obj: Any) -> 'ProductionDate':
        assert isinstance(obj, dict)
        start = from_datetime(obj.get("start"))
        end = from_datetime(obj.get("end"))
        period = from_str(obj.get("period"))
        return ProductionDate(start, end, period)

    def to_dict(self) -> dict:
        result: dict = {}
        result["start"] = self.start.isoformat()
        result["end"] = self.end.isoformat()
        result["period"] = from_str(self.period)
        return result


@dataclass
class RelatedObject:
    notes: str

    @staticmethod
    def from_dict(obj: Any) -> 'RelatedObject':
        assert isinstance(obj, dict)
        notes = from_str(obj.get("notes"))
        return RelatedObject(notes)

    def to_dict(self) -> dict:
        result: dict = {}
        result["notes"] = from_str(self.notes)
        return result


@dataclass
class Reproduction:
    reproduction_reference: str
    reproduction_reference_lref: int

    @staticmethod
    def from_dict(obj: Any) -> 'Reproduction':
        assert isinstance(obj, dict)
        reproduction_reference = from_str(obj.get("reproduction_reference"))
        reproduction_reference_lref = int(from_str(obj.get("reproduction_reference_lref")))
        return Reproduction(reproduction_reference, reproduction_reference_lref)

    def to_dict(self) -> dict:
        result: dict = {}
        result["reproduction_reference"] = from_str(self.reproduction_reference)
        result["reproduction_reference_lref"] = from_str(str(self.reproduction_reference_lref))
        return result


class ResponsibleDepartment(Enum):
    SAMLING_OG_FORSKNING_KKS = "Samling og Forskning (KKS)"


@dataclass
class Technique:
    technique: str

    @staticmethod
    def from_dict(obj: Any) -> 'Technique':
        assert isinstance(obj, dict)
        technique = from_str(obj.get("technique"))
        return Technique(technique)

    def to_dict(self) -> dict:
        result: dict = {}
        result["technique"] = from_str(self.technique)
        return result


class TitleType(Enum):
    DESCRIPT = "DESCRIPT"
    MUSEUM = "MUSEUM"
    OEUVRE = "OEUVRE"


@dataclass
class Title:
    title: Optional[str] = None
    language: Optional[str] = None
    type: Optional[TitleType] = None
    notes: Optional[str] = None

    @staticmethod
    def from_dict(obj: Any) -> 'Title':
        assert isinstance(obj, dict)
        title = from_union([from_str, from_none], obj.get("title"))
        language = from_union([from_str, from_none], obj.get("language"))
        type = from_union([TitleType, from_none], obj.get("type"))
        notes = from_union([from_str, from_none], obj.get("notes"))
        return Title(title, language, type, notes)

    def to_dict(self) -> dict:
        result: dict = {}
        result["title"] = from_union([from_str, from_none], self.title)
        result["language"] = from_union([from_str, from_none], self.language)
        result["type"] = from_union([lambda x: to_enum(TitleType, x), from_none], self.type)
        result["notes"] = from_union([from_str, from_none], self.notes)
        return result


@dataclass
class Item:
    id: str
    modified: datetime
    acquisition_date_precision: datetime
    responsible_department: ResponsibleDepartment
    frame_notes: List[FrameNote]
    dimensions: List[Dimension]
    object_names: List[ObjectName]
    production: List[Production]
    production_date: List[ProductionDate]
    techniques: List[Technique]
    titles: List[Title]
    object_number: str
    iiif_manifest: str
    public_domain: bool
    rights: str
    on_display: bool
    image_thumbnail: str
    image_native: str
    has_image: bool
    collection: Optional[List[str]] = None
    content_description: Optional[List[str]] = None
    distinguishing_features: Optional[List[str]] = None
    reproduction: Optional[List[Reproduction]] = None
    number_of_parts: Optional[int] = None
    production_dates_notes: Optional[List[str]] = None
    alternative_images: Optional[List[AlternativeImage]] = None
    image_mime_type: Optional[str] = None
    image_iiif_id: Optional[str] = None
    image_iiif_info: Optional[str] = None
    image_width: Optional[int] = None
    image_height: Optional[int] = None
    image_size: Optional[int] = None
    image_cropped: Optional[bool] = None
    image_orientation: Optional[str] = None
    documentation: Optional[List[Documentation]] = None
    inscriptions: Optional[List[Inscription]] = None
    part_of: Optional[List[str]] = None
    parts: Optional[List[str]] = None
    related_objects: Optional[List[RelatedObject]] = None
    notes: Optional[List[str]] = None
    object_history_note: Optional[List[str]] = None
    work_status: Optional[List[str]] = None
    content_person: Optional[List[str]] = None
    exhibitions: Optional[List[Exhibition]] = None

    @staticmethod
    def from_dict(obj: Any) -> 'Item':
        assert isinstance(obj, dict)
        id = from_str(obj.get("id"))
        modified = from_datetime(obj.get("modified"))
        acquisition_date_precision = from_datetime(obj.get("acquisition_date_precision"))
        responsible_department = ResponsibleDepartment(obj.get("responsible_department"))
        frame_notes = from_list(FrameNote, obj.get("frame_notes"))
        dimensions = from_list(Dimension.from_dict, obj.get("dimensions"))
        object_names = from_list(ObjectName.from_dict, obj.get("object_names"))
        production = from_list(Production.from_dict, obj.get("production"))
        production_date = from_list(ProductionDate.from_dict, obj.get("production_date"))
        techniques = from_list(Technique.from_dict, obj.get("techniques"))
        titles = from_list(Title.from_dict, obj.get("titles"))
        object_number = from_str(obj.get("object_number"))
        iiif_manifest = from_str(obj.get("iiif_manifest"))
        public_domain = from_bool(obj.get("public_domain"))
        rights = from_str(obj.get("rights"))
        on_display = from_bool(obj.get("on_display"))
        image_thumbnail = from_str(obj.get("image_thumbnail"))
        image_native = from_str(obj.get("image_native"))
        has_image = from_bool(obj.get("has_image"))
        collection = from_union([lambda x: from_list(from_str, x), from_none], obj.get("collection"))
        content_description = from_union([lambda x: from_list(from_str, x), from_none], obj.get("content_description"))
        distinguishing_features = from_union([lambda x: from_list(from_str, x), from_none], obj.get("distinguishing_features"))
        reproduction = from_union([lambda x: from_list(Reproduction.from_dict, x), from_none], obj.get("reproduction"))
        number_of_parts = from_union([from_int, from_none], obj.get("number_of_parts"))
        production_dates_notes = from_union([lambda x: from_list(from_str, x), from_none], obj.get("production_dates_notes"))
        alternative_images = from_union([lambda x: from_list(AlternativeImage.from_dict, x), from_none], obj.get("alternative_images"))
        image_mime_type = from_union([from_str, from_none], obj.get("image_mime_type"))
        image_iiif_id = from_union([from_str, from_none], obj.get("image_iiif_id"))
        image_iiif_info = from_union([from_str, from_none], obj.get("image_iiif_info"))
        image_width = from_union([from_int, from_none], obj.get("image_width"))
        image_height = from_union([from_int, from_none], obj.get("image_height"))
        image_size = from_union([from_int, from_none], obj.get("image_size"))
        image_cropped = from_union([from_bool, from_none], obj.get("image_cropped"))
        image_orientation = from_union([from_str, from_none], obj.get("image_orientation"))
        documentation = from_union([lambda x: from_list(Documentation.from_dict, x), from_none], obj.get("documentation"))
        inscriptions = from_union([lambda x: from_list(Inscription.from_dict, x), from_none], obj.get("inscriptions"))
        part_of = from_union([lambda x: from_list(from_str, x), from_none], obj.get("part_of"))
        parts = from_union([lambda x: from_list(from_str, x), from_none], obj.get("parts"))
        related_objects = from_union([lambda x: from_list(RelatedObject.from_dict, x), from_none], obj.get("related_objects"))
        notes = from_union([lambda x: from_list(from_str, x), from_none], obj.get("notes"))
        object_history_note = from_union([lambda x: from_list(from_str, x), from_none], obj.get("object_history_note"))
        work_status = from_union([lambda x: from_list(from_str, x), from_none], obj.get("work_status"))
        content_person = from_union([lambda x: from_list(from_str, x), from_none], obj.get("content_person"))
        exhibitions = from_union([lambda x: from_list(Exhibition.from_dict, x), from_none], obj.get("exhibitions"))
        return Item(id, modified, acquisition_date_precision, responsible_department, frame_notes, dimensions, object_names, production, production_date, techniques, titles, object_number, iiif_manifest, public_domain, rights, on_display, image_thumbnail, image_native, has_image, collection, content_description, distinguishing_features, reproduction, number_of_parts, production_dates_notes, alternative_images, image_mime_type, image_iiif_id, image_iiif_info, image_width, image_height, image_size, image_cropped, image_orientation, documentation, inscriptions, part_of, parts, related_objects, notes, object_history_note, work_status, content_person, exhibitions)

    def to_dict(self) -> dict:
        result: dict = {}
        result["id"] = from_str(self.id)
        result["modified"] = self.modified.isoformat()
        result["acquisition_date_precision"] = self.acquisition_date_precision.isoformat()
        result["responsible_department"] = to_enum(ResponsibleDepartment, self.responsible_department)
        result["frame_notes"] = from_list(lambda x: to_enum(FrameNote, x), self.frame_notes)
        result["dimensions"] = from_list(lambda x: to_class(Dimension, x), self.dimensions)
        result["object_names"] = from_list(lambda x: to_class(ObjectName, x), self.object_names)
        result["production"] = from_list(lambda x: to_class(Production, x), self.production)
        result["production_date"] = from_list(lambda x: to_class(ProductionDate, x), self.production_date)
        result["techniques"] = from_list(lambda x: to_class(Technique, x), self.techniques)
        result["titles"] = from_list(lambda x: to_class(Title, x), self.titles)
        result["object_number"] = from_str(self.object_number)
        result["iiif_manifest"] = from_str(self.iiif_manifest)
        result["public_domain"] = from_bool(self.public_domain)
        result["rights"] = from_str(self.rights)
        result["on_display"] = from_bool(self.on_display)
        result["image_thumbnail"] = from_str(self.image_thumbnail)
        result["image_native"] = from_str(self.image_native)
        result["has_image"] = from_bool(self.has_image)
        result["collection"] = from_union([lambda x: from_list(from_str, x), from_none], self.collection)
        result["content_description"] = from_union([lambda x: from_list(from_str, x), from_none], self.content_description)
        result["distinguishing_features"] = from_union([lambda x: from_list(from_str, x), from_none], self.distinguishing_features)
        result["reproduction"] = from_union([lambda x: from_list(lambda x: to_class(Reproduction, x), x), from_none], self.reproduction)
        result["number_of_parts"] = from_union([from_int, from_none], self.number_of_parts)
        result["production_dates_notes"] = from_union([lambda x: from_list(from_str, x), from_none], self.production_dates_notes)
        result["alternative_images"] = from_union([lambda x: from_list(lambda x: to_class(AlternativeImage, x), x), from_none], self.alternative_images)
        result["image_mime_type"] = from_union([from_str, from_none], self.image_mime_type)
        result["image_iiif_id"] = from_union([from_str, from_none], self.image_iiif_id)
        result["image_iiif_info"] = from_union([from_str, from_none], self.image_iiif_info)
        result["image_width"] = from_union([from_int, from_none], self.image_width)
        result["image_height"] = from_union([from_int, from_none], self.image_height)
        result["image_size"] = from_union([from_int, from_none], self.image_size)
        result["image_cropped"] = from_union([from_bool, from_none], self.image_cropped)
        result["image_orientation"] = from_union([from_str, from_none], self.image_orientation)
        result["documentation"] = from_union([lambda x: from_list(lambda x: to_class(Documentation, x), x), from_none], self.documentation)
        result["inscriptions"] = from_union([lambda x: from_list(lambda x: to_class(Inscription, x), x), from_none], self.inscriptions)
        result["part_of"] = from_union([lambda x: from_list(from_str, x), from_none], self.part_of)
        result["parts"] = from_union([lambda x: from_list(from_str, x), from_none], self.parts)
        result["related_objects"] = from_union([lambda x: from_list(lambda x: to_class(RelatedObject, x), x), from_none], self.related_objects)
        result["notes"] = from_union([lambda x: from_list(from_str, x), from_none], self.notes)
        result["object_history_note"] = from_union([lambda x: from_list(from_str, x), from_none], self.object_history_note)
        result["work_status"] = from_union([lambda x: from_list(from_str, x), from_none], self.work_status)
        result["content_person"] = from_union([lambda x: from_list(from_str, x), from_none], self.content_person)
        result["exhibitions"] = from_union([lambda x: from_list(lambda x: to_class(Exhibition, x), x), from_none], self.exhibitions)
        return result


@dataclass
class Empty:
    offset: int
    rows: int
    found: int
    items: List[Item]
    facets: Facets
    facets_ranges: Facets

    @staticmethod
    def from_dict(obj: Any) -> 'Empty':
        assert isinstance(obj, dict)
        offset = from_int(obj.get("offset"))
        rows = from_int(obj.get("rows"))
        found = from_int(obj.get("found"))
        items = from_list(Item.from_dict, obj.get("items"))
        facets = Facets.from_dict(obj.get("facets"))
        facets_ranges = Facets.from_dict(obj.get("facets_ranges"))
        return Empty(offset, rows, found, items, facets, facets_ranges)

    def to_dict(self) -> dict:
        result: dict = {}
        result["offset"] = from_int(self.offset)
        result["rows"] = from_int(self.rows)
        result["found"] = from_int(self.found)
        result["items"] = from_list(lambda x: to_class(Item, x), self.items)
        result["facets"] = to_class(Facets, self.facets)
        result["facets_ranges"] = to_class(Facets, self.facets_ranges)
        return result


def empty_from_dict(s: Any) -> Empty:
    return Empty.from_dict(s)


def empty_to_dict(x: Empty) -> Any:
    return to_class(Empty, x)
