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
from datetime import datetime
import dateutil.parser


T = TypeVar("T")


def from_str(x: Any) -> str:
    assert isinstance(x, str)
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


def from_int(x: Any) -> int:
    assert isinstance(x, int) and not isinstance(x, bool)
    return x


def is_type(t: Type[T], x: Any) -> T:
    assert isinstance(x, t)
    return x


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
    mime_type: Optional[str] = None
    iiif_id: Optional[str] = None
    iiif_info: Optional[str] = None
    width: Optional[int] = None
    height: Optional[int] = None
    size: Optional[int] = None
    thumbnail: Optional[str] = None
    native: Optional[str] = None
    orientation: Optional[str] = None

    @staticmethod
    def from_dict(obj: Any) -> 'AlternativeImage':
        assert isinstance(obj, dict)
        mime_type = from_union([from_str, from_none], obj.get("mime_type"))
        iiif_id = from_union([from_str, from_none], obj.get("iiif_id"))
        iiif_info = from_union([from_str, from_none], obj.get("iiif_info"))
        width = from_union([from_int, from_none], obj.get("width"))
        height = from_union([from_int, from_none], obj.get("height"))
        size = from_union([from_int, from_none], obj.get("size"))
        thumbnail = from_union([from_str, from_none], obj.get("thumbnail"))
        native = from_union([from_str, from_none], obj.get("native"))
        orientation = from_union([from_str, from_none], obj.get("orientation"))
        return AlternativeImage(mime_type, iiif_id, iiif_info, width, height, size, thumbnail, native, orientation)

    def to_dict(self) -> dict:
        result: dict = {}
        result["mime_type"] = from_union([from_str, from_none], self.mime_type)
        result["iiif_id"] = from_union([from_str, from_none], self.iiif_id)
        result["iiif_info"] = from_union([from_str, from_none], self.iiif_info)
        result["width"] = from_union([from_int, from_none], self.width)
        result["height"] = from_union([from_int, from_none], self.height)
        result["size"] = from_union([from_int, from_none], self.size)
        result["thumbnail"] = from_union([from_str, from_none], self.thumbnail)
        result["native"] = from_union([from_str, from_none], self.native)
        result["orientation"] = from_union([from_str, from_none], self.orientation)
        return result


@dataclass
class Dimension:
    value: Optional[int] = None
    notes: Optional[str] = None
    part: Optional[str] = None
    type: Optional[str] = None
    unit: Optional[str] = None

    @staticmethod
    def from_dict(obj: Any) -> 'Dimension':
        assert isinstance(obj, dict)
        value = from_union([from_none, lambda x: int(from_str(x))], obj.get("value"))
        notes = from_union([from_str, from_none], obj.get("notes"))
        part = from_union([from_str, from_none], obj.get("part"))
        type = from_union([from_str, from_none], obj.get("type"))
        unit = from_union([from_str, from_none], obj.get("unit"))
        return Dimension(value, notes, part, type, unit)

    def to_dict(self) -> dict:
        result: dict = {}
        result["value"] = from_union([lambda x: from_none((lambda x: is_type(type(None), x))(x)), lambda x: from_str((lambda x: str((lambda x: is_type(int, x))(x)))(x))], self.value)
        result["notes"] = from_union([from_str, from_none], self.notes)
        result["part"] = from_union([from_str, from_none], self.part)
        result["type"] = from_union([from_str, from_none], self.type)
        result["unit"] = from_union([from_str, from_none], self.unit)
        return result


@dataclass
class Documentation:
    title: Optional[str] = None
    author: Optional[str] = None
    notes: Optional[str] = None
    shelfmark: Optional[str] = None

    @staticmethod
    def from_dict(obj: Any) -> 'Documentation':
        assert isinstance(obj, dict)
        title = from_union([from_str, from_none], obj.get("title"))
        author = from_union([from_str, from_none], obj.get("author"))
        notes = from_union([from_str, from_none], obj.get("notes"))
        shelfmark = from_union([from_str, from_none], obj.get("shelfmark"))
        return Documentation(title, author, notes, shelfmark)

    def to_dict(self) -> dict:
        result: dict = {}
        result["title"] = from_union([from_str, from_none], self.title)
        result["author"] = from_union([from_str, from_none], self.author)
        result["notes"] = from_union([from_str, from_none], self.notes)
        result["shelfmark"] = from_union([from_str, from_none], self.shelfmark)
        return result


@dataclass
class Exhibition:
    exhibition: Optional[str] = None
    date_start: Optional[datetime] = None
    date_end: Optional[datetime] = None
    venue: Optional[str] = None

    @staticmethod
    def from_dict(obj: Any) -> 'Exhibition':
        assert isinstance(obj, dict)
        exhibition = from_union([from_str, from_none], obj.get("exhibition"))
        date_start = from_union([from_datetime, from_none], obj.get("date_start"))
        date_end = from_union([from_datetime, from_none], obj.get("date_end"))
        venue = from_union([from_str, from_none], obj.get("venue"))
        return Exhibition(exhibition, date_start, date_end, venue)

    def to_dict(self) -> dict:
        result: dict = {}
        result["exhibition"] = from_union([from_str, from_none], self.exhibition)
        result["date_start"] = from_union([lambda x: x.isoformat(), from_none], self.date_start)
        result["date_end"] = from_union([lambda x: x.isoformat(), from_none], self.date_end)
        result["venue"] = from_union([from_str, from_none], self.venue)
        return result


@dataclass
class Label:
    text: Optional[str] = None
    type: Optional[str] = None
    source: Optional[str] = None
    date: Optional[datetime] = None

    @staticmethod
    def from_dict(obj: Any) -> 'Label':
        assert isinstance(obj, dict)
        text = from_union([from_str, from_none], obj.get("text"))
        type = from_union([from_str, from_none], obj.get("type"))
        source = from_union([from_str, from_none], obj.get("source"))
        date = from_union([from_datetime, from_none], obj.get("date"))
        return Label(text, type, source, date)

    def to_dict(self) -> dict:
        result: dict = {}
        result["text"] = from_union([from_str, from_none], self.text)
        result["type"] = from_union([from_str, from_none], self.type)
        result["source"] = from_union([from_str, from_none], self.source)
        result["date"] = from_union([lambda x: x.isoformat(), from_none], self.date)
        return result


@dataclass
class Material:
    material: Optional[str] = None

    @staticmethod
    def from_dict(obj: Any) -> 'Material':
        assert isinstance(obj, dict)
        material = from_union([from_str, from_none], obj.get("material"))
        return Material(material)

    def to_dict(self) -> dict:
        result: dict = {}
        result["material"] = from_union([from_str, from_none], self.material)
        return result


@dataclass
class ObjectName:
    name: Optional[str] = None

    @staticmethod
    def from_dict(obj: Any) -> 'ObjectName':
        assert isinstance(obj, dict)
        name = from_union([from_str, from_none], obj.get("name"))
        return ObjectName(name)

    def to_dict(self) -> dict:
        result: dict = {}
        result["name"] = from_union([from_str, from_none], self.name)
        return result


@dataclass
class Production:
    creator: Optional[str] = None
    creator_date_of_birth: Optional[datetime] = None
    creator_date_of_death: Optional[datetime] = None
    creator_nationality: Optional[str] = None
    creator_history: Optional[str] = None
    creator_lref: Optional[str] = None

    @staticmethod
    def from_dict(obj: Any) -> 'Production':
        assert isinstance(obj, dict)
        creator = from_union([from_str, from_none], obj.get("creator"))
        creator_date_of_birth = from_union([from_datetime, from_none], obj.get("creator_date_of_birth"))
        creator_date_of_death = from_union([from_datetime, from_none], obj.get("creator_date_of_death"))
        creator_nationality = from_union([from_str, from_none], obj.get("creator_nationality"))
        creator_history = from_union([from_str, from_none], obj.get("creator_history"))
        creator_lref = from_union([from_str, from_none], obj.get("creator_lref"))
        return Production(creator, creator_date_of_birth, creator_date_of_death, creator_nationality, creator_history, creator_lref)

    def to_dict(self) -> dict:
        result: dict = {}
        result["creator"] = from_union([from_str, from_none], self.creator)
        result["creator_date_of_birth"] = from_union([lambda x: x.isoformat(), from_none], self.creator_date_of_birth)
        result["creator_date_of_death"] = from_union([lambda x: x.isoformat(), from_none], self.creator_date_of_death)
        result["creator_nationality"] = from_union([from_str, from_none], self.creator_nationality)
        result["creator_history"] = from_union([from_str, from_none], self.creator_history)
        result["creator_lref"] = from_union([from_str, from_none], self.creator_lref)
        return result


@dataclass
class ProductionDate:
    start: Optional[datetime] = None
    end: Optional[datetime] = None
    period: Optional[str] = None

    @staticmethod
    def from_dict(obj: Any) -> 'ProductionDate':
        assert isinstance(obj, dict)
        start = from_union([from_datetime, from_none], obj.get("start"))
        end = from_union([from_datetime, from_none], obj.get("end"))
        period = from_union([from_str, from_none], obj.get("period"))
        return ProductionDate(start, end, period)

    def to_dict(self) -> dict:
        result: dict = {}
        result["start"] = from_union([lambda x: x.isoformat(), from_none], self.start)
        result["end"] = from_union([lambda x: x.isoformat(), from_none], self.end)
        result["period"] = from_union([from_str, from_none], self.period)
        return result


@dataclass
class Technique:
    technique: Optional[str] = None

    @staticmethod
    def from_dict(obj: Any) -> 'Technique':
        assert isinstance(obj, dict)
        technique = from_union([from_str, from_none], obj.get("technique"))
        return Technique(technique)

    def to_dict(self) -> dict:
        result: dict = {}
        result["technique"] = from_union([from_str, from_none], self.technique)
        return result


@dataclass
class Title:
    title: Optional[str] = None
    language: Optional[str] = None
    type: Optional[str] = None
    translation: Optional[str] = None

    @staticmethod
    def from_dict(obj: Any) -> 'Title':
        assert isinstance(obj, dict)
        title = from_union([from_str, from_none], obj.get("title"))
        language = from_union([from_str, from_none], obj.get("language"))
        type = from_union([from_str, from_none], obj.get("type"))
        translation = from_union([from_str, from_none], obj.get("translation"))
        return Title(title, language, type, translation)

    def to_dict(self) -> dict:
        result: dict = {}
        result["title"] = from_union([from_str, from_none], self.title)
        result["language"] = from_union([from_str, from_none], self.language)
        result["type"] = from_union([from_str, from_none], self.type)
        result["translation"] = from_union([from_str, from_none], self.translation)
        return result


@dataclass
class Item:
    id: Optional[str] = None
    created: Optional[datetime] = None
    modified: Optional[datetime] = None
    acquisition_date_precision: Optional[datetime] = None
    responsible_department: Optional[str] = None
    content_description: Optional[List[str]] = None
    current_location_name: Optional[str] = None
    frame_notes: Optional[List[str]] = None
    dimensions: Optional[List[Dimension]] = None
    documentation: Optional[List[Documentation]] = None
    exhibitions: Optional[List[Exhibition]] = None
    labels: Optional[List[Label]] = None
    materials: Optional[List[Material]] = None
    object_names: Optional[List[ObjectName]] = None
    part_of: Optional[List[str]] = None
    parts: Optional[List[str]] = None
    production: Optional[List[Production]] = None
    production_date: Optional[List[ProductionDate]] = None
    techniques: Optional[List[Technique]] = None
    titles: Optional[List[Title]] = None
    notes: Optional[List[str]] = None
    number_of_parts: Optional[int] = None
    object_history_note: Optional[List[str]] = None
    object_number: Optional[str] = None
    iiif_manifest: Optional[str] = None
    production_dates_notes: Optional[List[str]] = None
    public_domain: Optional[bool] = None
    rights: Optional[str] = None
    on_display: Optional[bool] = None
    alternative_images: Optional[List[AlternativeImage]] = None
    image_mime_type: Optional[str] = None
    image_iiif_id: Optional[str] = None
    image_iiif_info: Optional[str] = None
    image_width: Optional[int] = None
    image_height: Optional[int] = None
    image_thumbnail: Optional[str] = None
    image_native: Optional[str] = None
    image_cropped: Optional[bool] = None
    image_orientation: Optional[str] = None
    has_image: Optional[bool] = None

    @staticmethod
    def from_dict(obj: Any) -> 'Item':
        assert isinstance(obj, dict)
        id = from_union([from_str, from_none], obj.get("id"))
        created = from_union([from_datetime, from_none], obj.get("created"))
        modified = from_union([from_datetime, from_none], obj.get("modified"))
        acquisition_date_precision = from_union([from_datetime, from_none], obj.get("acquisition_date_precision"))
        responsible_department = from_union([from_str, from_none], obj.get("responsible_department"))
        content_description = from_union([lambda x: from_list(from_str, x), from_none], obj.get("content_description"))
        current_location_name = from_union([from_str, from_none], obj.get("current_location_name"))
        frame_notes = from_union([lambda x: from_list(from_str, x), from_none], obj.get("frame_notes"))
        dimensions = from_union([lambda x: from_list(Dimension.from_dict, x), from_none], obj.get("dimensions"))
        documentation = from_union([lambda x: from_list(Documentation.from_dict, x), from_none], obj.get("documentation"))
        exhibitions = from_union([lambda x: from_list(Exhibition.from_dict, x), from_none], obj.get("exhibitions"))
        labels = from_union([lambda x: from_list(Label.from_dict, x), from_none], obj.get("labels"))
        materials = from_union([lambda x: from_list(Material.from_dict, x), from_none], obj.get("materials"))
        object_names = from_union([lambda x: from_list(ObjectName.from_dict, x), from_none], obj.get("object_names"))
        part_of = from_union([lambda x: from_list(from_str, x), from_none], obj.get("part_of"))
        parts = from_union([lambda x: from_list(from_str, x), from_none], obj.get("parts"))
        production = from_union([lambda x: from_list(Production.from_dict, x), from_none], obj.get("production"))
        production_date = from_union([lambda x: from_list(ProductionDate.from_dict, x), from_none], obj.get("production_date"))
        techniques = from_union([lambda x: from_list(Technique.from_dict, x), from_none], obj.get("techniques"))
        titles = from_union([lambda x: from_list(Title.from_dict, x), from_none], obj.get("titles"))
        notes = from_union([lambda x: from_list(from_str, x), from_none], obj.get("notes"))
        number_of_parts = from_union([from_int, from_none], obj.get("number_of_parts"))
        object_history_note = from_union([lambda x: from_list(from_str, x), from_none], obj.get("object_history_note"))
        object_number = from_union([from_str, from_none], obj.get("object_number"))
        iiif_manifest = from_union([from_str, from_none], obj.get("iiif_manifest"))
        production_dates_notes = from_union([lambda x: from_list(from_str, x), from_none], obj.get("production_dates_notes"))
        public_domain = from_union([from_bool, from_none], obj.get("public_domain"))
        rights = from_union([from_str, from_none], obj.get("rights"))
        on_display = from_union([from_bool, from_none], obj.get("on_display"))
        alternative_images = from_union([lambda x: from_list(AlternativeImage.from_dict, x), from_none], obj.get("alternative_images"))
        image_mime_type = from_union([from_str, from_none], obj.get("image_mime_type"))
        image_iiif_id = from_union([from_str, from_none], obj.get("image_iiif_id"))
        image_iiif_info = from_union([from_str, from_none], obj.get("image_iiif_info"))
        image_width = from_union([from_int, from_none], obj.get("image_width"))
        image_height = from_union([from_int, from_none], obj.get("image_height"))
        image_thumbnail = from_union([from_str, from_none], obj.get("image_thumbnail"))
        image_native = from_union([from_str, from_none], obj.get("image_native"))
        image_cropped = from_union([from_bool, from_none], obj.get("image_cropped"))
        image_orientation = from_union([from_str, from_none], obj.get("image_orientation"))
        has_image = from_union([from_bool, from_none], obj.get("has_image"))
        return Item(id, created, modified, acquisition_date_precision, responsible_department, content_description, current_location_name, frame_notes, dimensions, documentation, exhibitions, labels, materials, object_names, part_of, parts, production, production_date, techniques, titles, notes, number_of_parts, object_history_note, object_number, iiif_manifest, production_dates_notes, public_domain, rights, on_display, alternative_images, image_mime_type, image_iiif_id, image_iiif_info, image_width, image_height, image_thumbnail, image_native, image_cropped, image_orientation, has_image)

    def to_dict(self) -> dict:
        result: dict = {}
        result["id"] = from_union([from_str, from_none], self.id)
        result["created"] = from_union([lambda x: x.isoformat(), from_none], self.created)
        result["modified"] = from_union([lambda x: x.isoformat(), from_none], self.modified)
        result["acquisition_date_precision"] = from_union([lambda x: x.isoformat(), from_none], self.acquisition_date_precision)
        result["responsible_department"] = from_union([from_str, from_none], self.responsible_department)
        result["content_description"] = from_union([lambda x: from_list(from_str, x), from_none], self.content_description)
        result["current_location_name"] = from_union([from_str, from_none], self.current_location_name)
        result["frame_notes"] = from_union([lambda x: from_list(from_str, x), from_none], self.frame_notes)
        result["dimensions"] = from_union([lambda x: from_list(lambda x: to_class(Dimension, x), x), from_none], self.dimensions)
        result["documentation"] = from_union([lambda x: from_list(lambda x: to_class(Documentation, x), x), from_none], self.documentation)
        result["exhibitions"] = from_union([lambda x: from_list(lambda x: to_class(Exhibition, x), x), from_none], self.exhibitions)
        result["labels"] = from_union([lambda x: from_list(lambda x: to_class(Label, x), x), from_none], self.labels)
        result["materials"] = from_union([lambda x: from_list(lambda x: to_class(Material, x), x), from_none], self.materials)
        result["object_names"] = from_union([lambda x: from_list(lambda x: to_class(ObjectName, x), x), from_none], self.object_names)
        result["part_of"] = from_union([lambda x: from_list(from_str, x), from_none], self.part_of)
        result["parts"] = from_union([lambda x: from_list(from_str, x), from_none], self.parts)
        result["production"] = from_union([lambda x: from_list(lambda x: to_class(Production, x), x), from_none], self.production)
        result["production_date"] = from_union([lambda x: from_list(lambda x: to_class(ProductionDate, x), x), from_none], self.production_date)
        result["techniques"] = from_union([lambda x: from_list(lambda x: to_class(Technique, x), x), from_none], self.techniques)
        result["titles"] = from_union([lambda x: from_list(lambda x: to_class(Title, x), x), from_none], self.titles)
        result["notes"] = from_union([lambda x: from_list(from_str, x), from_none], self.notes)
        result["number_of_parts"] = from_union([from_int, from_none], self.number_of_parts)
        result["object_history_note"] = from_union([lambda x: from_list(from_str, x), from_none], self.object_history_note)
        result["object_number"] = from_union([from_str, from_none], self.object_number)
        result["iiif_manifest"] = from_union([from_str, from_none], self.iiif_manifest)
        result["production_dates_notes"] = from_union([lambda x: from_list(from_str, x), from_none], self.production_dates_notes)
        result["public_domain"] = from_union([from_bool, from_none], self.public_domain)
        result["rights"] = from_union([from_str, from_none], self.rights)
        result["on_display"] = from_union([from_bool, from_none], self.on_display)
        result["alternative_images"] = from_union([lambda x: from_list(lambda x: to_class(AlternativeImage, x), x), from_none], self.alternative_images)
        result["image_mime_type"] = from_union([from_str, from_none], self.image_mime_type)
        result["image_iiif_id"] = from_union([from_str, from_none], self.image_iiif_id)
        result["image_iiif_info"] = from_union([from_str, from_none], self.image_iiif_info)
        result["image_width"] = from_union([from_int, from_none], self.image_width)
        result["image_height"] = from_union([from_int, from_none], self.image_height)
        result["image_thumbnail"] = from_union([from_str, from_none], self.image_thumbnail)
        result["image_native"] = from_union([from_str, from_none], self.image_native)
        result["image_cropped"] = from_union([from_bool, from_none], self.image_cropped)
        result["image_orientation"] = from_union([from_str, from_none], self.image_orientation)
        result["has_image"] = from_union([from_bool, from_none], self.has_image)
        return result


@dataclass
class Empty:
    offset: Optional[int] = None
    rows: Optional[int] = None
    found: Optional[int] = None
    items: Optional[List[Item]] = None
    facets: Optional[Facets] = None
    facets_ranges: Optional[Facets] = None
    autocomplete: Optional[List[Any]] = None

    @staticmethod
    def from_dict(obj: Any) -> 'Empty':
        assert isinstance(obj, dict)
        offset = from_union([from_int, from_none], obj.get("offset"))
        rows = from_union([from_int, from_none], obj.get("rows"))
        found = from_union([from_int, from_none], obj.get("found"))
        items = from_union([lambda x: from_list(Item.from_dict, x), from_none], obj.get("items"))
        facets = from_union([Facets.from_dict, from_none], obj.get("facets"))
        facets_ranges = from_union([Facets.from_dict, from_none], obj.get("facets_ranges"))
        autocomplete = from_union([lambda x: from_list(lambda x: x, x), from_none], obj.get("autocomplete"))
        return Empty(offset, rows, found, items, facets, facets_ranges, autocomplete)

    def to_dict(self) -> dict:
        result: dict = {}
        result["offset"] = from_union([from_int, from_none], self.offset)
        result["rows"] = from_union([from_int, from_none], self.rows)
        result["found"] = from_union([from_int, from_none], self.found)
        result["items"] = from_union([lambda x: from_list(lambda x: to_class(Item, x), x), from_none], self.items)
        result["facets"] = from_union([lambda x: to_class(Facets, x), from_none], self.facets)
        result["facets_ranges"] = from_union([lambda x: to_class(Facets, x), from_none], self.facets_ranges)
        result["autocomplete"] = from_union([lambda x: from_list(lambda x: x, x), from_none], self.autocomplete)
        return result


def empty_from_dict(s: Any) -> Empty:
    return Empty.from_dict(s)


def empty_to_dict(x: Empty) -> Any:
    return to_class(Empty, x)
