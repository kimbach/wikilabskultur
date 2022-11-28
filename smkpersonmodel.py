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
#     result = welcome_from_dict(json.loads(json_string))

from datetime import datetime
from typing import List, Any, TypeVar, Callable, Type, cast
import dateutil.parser
import json
import requests

T = TypeVar("T")


def from_str(x: Any) -> str:
    assert isinstance(x, str)
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


class Item:
    id: str
    created: datetime
    modified: datetime
    works: List[str]
    birth_date_end: List[datetime]
    birth_date_prec: List[str]
    birth_date_start: List[datetime]
    birth_place: List[str]
    death_date_end: List[datetime]
    death_date_prec: List[str]
    death_date_start: List[datetime]
    forename: str
    gender: List[str]
    name: str
    name_type: List[str]
    nationality: List[str]
    surname: str
    has_image: bool
    has_3_d_file: bool
    artist: List[str]
    retrieved_date: datetime

    def __init__(self, id: str, created: datetime, modified: datetime, works: List[str], birth_date_end: List[datetime], birth_date_prec: List[str], birth_date_start: List[datetime], birth_place: List[str], death_date_end: List[datetime], death_date_prec: List[str], death_date_start: List[datetime], forename: str, gender: List[str], name: str, name_type: List[str], nationality: List[str], surname: str, has_image: bool, has_3_d_file: bool, artist: List[str]) -> None:
        self.id = id
        self.created = created
        self.modified = modified
        self.works = works
        self.birth_date_end = birth_date_end
        self.birth_date_prec = birth_date_prec
        self.birth_date_start = birth_date_start
        self.birth_place = birth_place
        self.death_date_end = death_date_end
        self.death_date_prec = death_date_prec
        self.death_date_start = death_date_start
        self.forename = forename
        self.gender = gender
        self.name = name
        self.name_type = name_type
        self.nationality = nationality
        self.surname = surname
        self.has_image = has_image
        self.has_3_d_file = has_3_d_file
        self.artist = artist

    @staticmethod
    def from_dict(obj: Any) -> 'Item':
        assert isinstance(obj, dict)
        try:
            id = from_str(obj.get("id"))
        except:
            id = ""
        try:
            created = from_datetime(obj.get("created"))
        except:
            created = ""
        try:
            modified = from_datetime(obj.get("modified"))
        except:
            modified = ""
        try:
            works = from_list(from_str, obj.get("works"))
        except:
            works = []
        try:
            birth_date_end = from_list(from_datetime, obj.get("birth_date_end"))
        except:
            birth_date_end = []
        try:
            birth_date_prec = from_list(from_str, obj.get("birth_date_prec"))
        except:
            birth_date_prec = []
        try:
            birth_date_start = from_list(from_datetime, obj.get("birth_date_start"))
        except:
            birth_date_start = []
        try:
            birth_place = from_list(from_str, obj.get("birth_place"))
        except:
            birth_place = []
        try:
            death_date_end = from_list(from_datetime, obj.get("death_date_end"))
        except:
            death_date_end = []
        try:
            death_date_prec = from_list(from_str, obj.get("death_date_prec"))
        except:
            death_date_prec = []
        try:
            death_date_start = from_list(from_datetime, obj.get("death_date_start"))
        except:
            death_date_start = []
        try:
            forename = from_str(obj.get("forename"))
        except:
            forename = ""
        try:
            gender = from_list(from_str, obj.get("gender"))
        except:
            gender = []
        try:
            name = from_str(obj.get("name"))
        except:
            name = ""
        try:
            name_type = from_list(from_str, obj.get("name_type"))
        except:
            name_type = []
        try:
            nationality = from_list(from_str, obj.get("nationality"))
        except:
            nationality = []
        try:
            surname = from_str(obj.get("surname"))
        except:
            surname = ""
        try:
            has_image = from_bool(obj.get("has_image"))
        except:
            has_image = ""
        try:
            has_3_d_file = from_bool(obj.get("has_3d_file"))
        except:
            has_3_d_file = ""
        try:
            artist = from_list(from_str, obj.get("artist"))
        except:
            artist = []
        return Item(id, created, modified, works, birth_date_end, birth_date_prec, birth_date_start, birth_place, death_date_end, death_date_prec, death_date_start, forename, gender, name, name_type, nationality, surname, has_image, has_3_d_file, artist)

    def to_dict(self) -> dict:
        result: dict = {}
        result["id"] = from_str(self.id)
        result["created"] = self.created.isoformat()
        result["modified"] = self.modified.isoformat()
        result["works"] = from_list(from_str, self.works)
        result["birth_date_end"] = from_list(lambda x: x.isoformat(), self.birth_date_end)
        result["birth_date_prec"] = from_list(from_str, self.birth_date_prec)
        result["birth_date_start"] = from_list(lambda x: x.isoformat(), self.birth_date_start)
        result["birth_place"] = from_list(from_str, self.birth_place)
        result["death_date_end"] = from_list(lambda x: x.isoformat(), self.death_date_end)
        result["death_date_prec"] = from_list(from_str, self.death_date_prec)
        result["death_date_start"] = from_list(lambda x: x.isoformat(), self.death_date_start)
        result["forename"] = from_str(self.forename)
        result["gender"] = from_list(from_str, self.gender)
        result["name"] = from_str(self.name)
        result["name_type"] = from_list(from_str, self.name_type)
        result["nationality"] = from_list(from_str, self.nationality)
        result["surname"] = from_str(self.surname)
        result["has_image"] = from_bool(self.has_image)
        result["has_3d_file"] = from_bool(self.has_3_d_file)
        result["artist"] = from_list(from_str, self.artist)
        return result

class Welcome:
    items: List[Item]

    def __init__(self, items: List[Item]) -> None:
        self.items = items

    @staticmethod
    def from_dict(obj: Any) -> 'Welcome':
        assert isinstance(obj, dict)
        items = from_list(Item.from_dict, obj.get("items"))
        return Welcome(items)

    def to_dict(self) -> dict:
        result: dict = {}
        result["items"] = from_list(lambda x: to_class(Item, x), self.items)
        return result

def welcome_from_dict(s: Any) -> Welcome:
    return Welcome.from_dict(s)

def welcome_to_dict(x: Welcome) -> Any:
    return to_class(Welcome, x)

def test(lref_person):
    url = 'https://api.smk.dk/api/v1/person?id=' + lref_person
    creator_json=requests.get(url).text
    creator_objects=json.loads(creator_json)
    creator_object_model = welcome_from_dict(creator_objects)
    print(creator_object_model)
