# csvlookup
import csv
from operator import truediv
from warnings import catch_warnings
from datetime import datetime
import urllib.parse
import json
import requests
import os
import smkpersonmodel
from quickstatement import quickstatement
import wikidata
import smkapi
import logging

wikidata_items={}
f_artists_items={}
all_artists_items={}
artists_items={}
wikidata_worksby_items={}
person_wikidata_items={}
all_creator_lref_to_wikidata_items={}
smk_materials_to_wikidata_items={}
smk_object_names_to_wikidata_items={}
smk_artwork_types_to_wikidata_items={}
smk_artwork_types_labels_items={}

def load_wikidata_items():
    with open('wikidata_smk.csv', 'r') as file:
        reader = csv.DictReader(file, quoting=csv.QUOTE_NONE, delimiter = ';')
        for row in reader:
            wikidata_items[row["inventorynumber"].lower()] = row["wikidataitem"]

def load_person_wikidata_items():
    with open('SMK_person_to_wikidata.csv', 'r') as file:
        reader = csv.DictReader(file, quoting=csv.QUOTE_NONE, delimiter = ';')
        for row in reader:
            person_wikidata_items[row["creator_lref"].lower()] = row["wikidata"]

def load_wikidata_worksby_items():
    reader = csv.reader(open('wikidata_worksby_smk.csv'), quoting=csv.QUOTE_NONE, delimiter = ';')

    for row in reader:
        try:
            key = row[0]
            if key in wikidata_worksby_items:
                # implement your duplicate row handling here
                pass
            wikidata_worksby_items[key] = row[1:]
        except:
            print("Error:")
    
    print(wikidata_worksby_items)

def load_f_artists_items():
    reader = csv.reader(open('f_artists.csv'), quoting=csv.QUOTE_NONE, delimiter = ';')

    for row in reader:
        key = row[10]
        if key in f_artists_items:
            # implement your duplicate row handling here
            pass
        f_artists_items[key] = row[1:]
    print(f_artists_items)

def load_all_artists_items():
    reader = csv.reader(open('all_artists.csv'), quoting=csv.QUOTE_NONE, delimiter = ';')

    for row in reader:
        key = row[11]
        if key in all_artists_items:
            # implement your duplicate row handling here
            pass
        #all_artists_items[key] = row[0:]
        all_artists_items[key] = row
    print(all_artists_items)

def load_all_creator_lref_to_wikidata_items():
    reader = csv.reader(open('creator_lref_to_wikidata.csv'), quoting=csv.QUOTE_NONE, delimiter = ',')

    for row in reader:
        key = row[2].lower()
        if key in all_creator_lref_to_wikidata_items:
            # implement your duplicate row handling here
            pass
        #all_artists_items[key] = row[0:]
        all_creator_lref_to_wikidata_items[key] = row
    print(all_creator_lref_to_wikidata_items)

def load_smk_materials_to_wikidata_items():
    reader = csv.reader(open('smk_materials_to_wikidata.csv'), quoting=csv.QUOTE_NONE, delimiter = ',')

    for row in reader:
        key = row[0].lower()
        if key in smk_materials_to_wikidata_items:
            # implement your duplicate row handling here
            pass
        #all_artists_items[key] = row[0:]
        smk_materials_to_wikidata_items[key] = row
    print(smk_materials_to_wikidata_items)

smk_object_names_to_wikidata_items={}

def load_smk_object_names_to_wikidata_items():
    reader = csv.reader(open('smk_object_names_to_wikidata.csv'), quoting=csv.QUOTE_NONE, delimiter = ',')

    for row in reader:
        key = row[0].lower()
        if key in smk_object_names_to_wikidata_items:
            # implement your duplicate row handling here
            pass
        #all_artists_items[key] = row[0:]
        smk_object_names_to_wikidata_items[key] = row
    print(smk_object_names_to_wikidata_items)

def load_smk_artwork_types_to_wikidata_items():
    reader = csv.reader(open('smk_artwork_types_to_wikidata.csv'), quoting=csv.QUOTE_NONE, delimiter = ',')

    for row in reader:
        key = row[0].lower()
        if key in smk_artwork_types_to_wikidata_items:
            # implement your duplicate row handling here
            pass
        #all_artists_items[key] = row[0:]
        smk_artwork_types_to_wikidata_items[key] = row
    print(smk_artwork_types_to_wikidata_items)

def load_smk_artwork_types_labels_items():
    reader = csv.reader(open('artwork_types_labels.csv'), quoting=csv.QUOTE_NONE, delimiter = ';')

    for row in reader:
        key = row[0].lower()
        if key in smk_artwork_types_labels_items:
            # implement your duplicate row handling here
            pass
        #all_artists_items[key] = row[0:]
        smk_artwork_types_labels_items[key] = row
    print(smk_artwork_types_labels_items)

def save_all_artists_items():
    all_unique_artists=open('all_unique_artists.csv', 'w+')
    print("artists:")

    #for k,v in all_artists_items.items():
    #    print(k, 'corresponds to', v)

    for key, artist in all_artists_items.items():
        print(artist)
        all_artist_line=''
        for x in range(len(artist)):
            print(artist[x])
            all_artist_line=all_artist_line+artist[x]
            if x<len(artist) - 1:
                all_artist_line=all_artist_line+';'
        all_artist_line=all_artist_line+'\n'
        all_unique_artists.write(all_artist_line)
    all_unique_artists.close()

def find_wikidata_item(object_id):
    # Usage:
    #  wikidata_item = find_wikidata_item(commons_row[17])
    #  if wikidata_item != '':
    #      print(wikidata_item)
    if len(wikidata_items) == 0:
        load_wikidata_items()
    if object_id.lower() in wikidata_items: 
        wikidata_item = wikidata_items[object_id.lower()]
    else:
        wikidata_item = ''

    return(wikidata_item)

def find_person_wikidata_item(object_id):
    # Usage:
    #  person_wikidata_item = find_person_wikidata_item(commons_row[17])
    #  if person_wikidata_item != '':
    #      print(person_wikidata_item)
    if len(person_wikidata_items) == 0:
        load_person_wikidata_items()
    if object_id.lower() in person_wikidata_items: 
        person_wikidata_item = person_wikidata_items[object_id.lower()]
    else:
        person_wikidata_item = ''

    return(person_wikidata_item)

# Generate lists of unique artwork types, nationalities and creators from SMK import csv
# and filter on specific artists
def generate_lists():
    notes=[]
    nationalities=[]
    creators=[]
    artists=[]
    #with open('commons_smk_total.csv', 'r') as file:
    with open('2022-07-07_all_works.csv', 'r') as file:
        reader = csv.reader(file, quoting=csv.QUOTE_NONE, delimiter = ';')
        items=1
        for commons_row in reader:
            note_found = False 
            for note in notes:
                if commons_row[19]==note:
                    #print(commons_row[16] +' FOUND:')
                    note_found = True 
                    break
            if note_found == False:
                notes.append(commons_row[19]) 
            
            #nationalities[nationality] = commons_row[1] 
            nationality_found = False 
            for nationality in nationalities:
                if commons_row[4]==nationality:
                    #print(commons_row[16] +' FOUND:')
                    nationality_found = True 
                    break
            if nationality_found == False:
                nationalities.append(commons_row[4]) 
            
            creator_found = False 
            for creator in creators:
                if commons_row[43]==creator:
                    #print(commons_row[16] +' FOUND:')
                    creator_found = True 
                    break
            if creator_found == False:
                creators.append(commons_row[43]) 
                artists.append(commons_row)

            # Joakim Skovgaard
            # Viggo Pedersen
            # Theodor Philipsen
            # Edvard Petersen
            # Kristian Zahrtmann

            # if commons_row[0]=='Joakim Skovgaard':
            #     artists.append(commons_row) 
            # elif commons_row[0]=='Viggo Pedersen':
            #     artists.append(commons_row) 
            # elif commons_row[0]=='Theodor Philipsen':
            #     artists.append(commons_row)
            # elif commons_row[0]=='Edvard Petersen':
            #     artists.append(commons_row)
            # elif commons_row[0]=='Kristian Zahrtmann':
            #     artists.append(commons_row)
                            #debug_msg('items='+str(items))
            print('\r' + str(items) + ':' + commons_row[20], end='', flush=True)

            items=items+1

    f_type=open('type_smk.csv', 'w+')
    print("type:")
    for note in notes:
        f_type.write(note + '\n')
        print(note)
    f_type.close()

    f_nationalities=open('nationalities_smk.csv', 'w+')
    print("nationalities:")
    for nationality in nationalities:
        f_nationalities.write(nationality + '\n')
        print(nationality)
    f_nationalities.close()

    f_creators=open('creators_smk.csv', 'w+')
    print("creators:")
    for creator in creators:
        f_creators.write(creator + '\n')
        print(creator)
    f_creators.close()

    f_artists=open('f_artists.csv', 'w+')
    print("artists:")
    f_artists.write('id;created;modified;artist;nationality;author;title;description;depicted_people;date;medium;dimensions;institution;department;place_of_discovery;object_history;exhibition_history;credit_line;inscriptions;notes;accession_number;place_of_creation;source;permission;other_versions;references;depicted_place;categories;wikidata;image_height;image_width;imageurl;object_type;location;medium;public_domain;has_image;file_hash;creator_forename;creator_surname;creator_date_of_death;creator_date_of_birth;creator_gender;creator_lref\n')

    for artist in artists:
        print(artist)
        f_artist_line=''
        for f_artists_item in artist:
            f_artist_line=f_artist_line+f_artists_item+';'
        f_artist_line=f_artist_line+'\n'
        f_artists.write(f_artist_line)


    f_artists.close()

def FindSMKArtistWikidata():
    if len(f_artists_items) == 0:
        load_f_artists_items()
    if len(wikidata_worksby_items) == 0:
        load_wikidata_worksby_items()

    smk_artists_wikidata=open('smk_artists_wikidata.csv', 'w')
    smk_artists_wikidata.write('id;created;modified;artist;nationality;author;title;description;depicted_people;date;medium;dimensions;institution;department;place_of_discovery;object_history;exhibition_history;credit_line;inscriptions;notes;accession_number;place_of_creation;source;permission;other_versions;references;depicted_place;categories;wikidata;image_height;image_width;imageurl;object_type;location;medium;public_domain;has_image;file_hash;creator_forename;creator_surname;creator_date_of_death;creator_date_of_birth;creator_gender;creator_lref;wikidata\n')

        #print(key, ':', wikidata_worksby_items[key])
    for key2 in f_artists_items:
        wikidata_number=''
        for key in wikidata_worksby_items:
            #print(key2, ':', f_artists_items[key2])
            if f_artists_items[key2][37]==wikidata_worksby_items[key][0] and f_artists_items[key2][38]==wikidata_worksby_items[key][1]:
                print('Found! ' + key + ':' + f_artists_items[key2][37] + ':' + f_artists_items[key2][38] + " " + f_artists_items[key2][9])
                wikidata_number=key
                break

        f_artist_line=key2+';'
        for f_artists_item in f_artists_items[key2]:
            f_artist_line=f_artist_line+f_artists_item+';'
        f_artist_line=f_artist_line+wikidata_number+'\n'
        smk_artists_wikidata.write(f_artist_line)

    smk_artists_wikidata.close()

"""     for dic in f_artists_items:
        for key in dic:
            print ('Book Name: %s' % (key))
            for value in dic[key]:
                print ('\t%s: %s' % (value, dic[key][value]))
    for wikidata_worksby in wikidata_worksby_items[0].keys():
        print(wikidata_worksby[0] + ':' + wikidata_worksby[1] + " " + wikidata_worksby[2])
        for f_artists in f_artists_items.items:
            if f_artists[5]==wikidata_worksby[1] and f_artists[6]==wikidata_worksby[2]:
                print(wikidata_worksby[0] + ':' + f_artists[5] + " " + f_artists[6])
 """

def query_all_artists():
    folder = './artists/'

    reader = csv.reader(open('all_unique_artists.csv'), quoting=csv.QUOTE_NONE, delimiter = ';')
    
    linenumber = 1
    path_bookmark = folder + "bookmark.txt"
    if os.path.exists(path_bookmark):
        with open(path_bookmark,"r") as bookmark:
            try:
                linenumber = int(bookmark.read())
            except:
                linenumber = 1
        bookmark.close()
    else:
        linenumber = 1


    max_searches = 1000
    count = 0
    path_csv = folder + "artists_wikidata" + '.csv'
    if not os.path.exists(path_csv):
        csv_header = "creator_lref;creator;id;title;label;description;wikidata_dob;creator_dob;value_occupation_id;value_occupation_label_en;value_field_of_work;value_commons_category\n"
        with open(path_csv, 'w') as artists_wikidata:
            artists_wikidata.write(csv_header)
        artists_wikidata.close()

    skip = 0
    for row in reader:

        skip = skip + 1
        if linenumber>skip:
            continue

        count = count + 1
        
        creator = ((row[4] + " " + row[5]).replace('"', '')).strip()
        creator_lref = row[11]
        creator_date_of_birth = row[6]
        # attempt a search in wikidata
        creator_encoded = urllib.parse.quote_plus(creator)
        url = 'https://www.wikidata.org/w/api.php?action=wbsearchentities&format=json&language=en&type=item&continue=0&search=' + creator_encoded

        # Save RAW json

        path_json = folder + creator_lref + '.json'

        # Only create new file if it doesn't exist
        artists_wikidata_line_prefix = creator_lref+";"+creator+";"
        if not os.path.exists(path_json):
            creator_json=requests.get(url).text
            creator_objects=json.loads(creator_json)


            # open(path_json, 'w').write(creator_json)

            if creator_objects.get("search") != None:
                if len(creator_objects.get("search"))>0:
                    for search in creator_objects.get("search"):
                        try:
                            id = search.get("id")
                            if id==None:
                                id = ""
                        except:
                            id = ""
                        try:
                            title = search.get("title")
                            if title==None:
                                title = ""
                        except:
                            title = ""
                        try:
                            label = search.get("label")
                            if label==None:
                                label = ""
                        except:
                            label = ""
                        try:
                            description = search.get("description")
                            if description==None:
                                description = ""
                        except:
                            description = ""
                        print (id)
                        print (title)
                        print (label)
                        print (description)
                        instance_of_human = False
                        date_of_birth_match = False
                        value_time = ""
                        value_occupation_label_en = ""
                        value_occupation_id = ""

                        value_field_of_work = ""

                        claimsurl="https://www.wikidata.org/w/api.php?action=wbgetclaims&entity=" + id + "&formatversion=2" + "&format=json"
                        claims_json=requests.get(claimsurl).text
                        claims_objects=json.loads(claims_json)
                        if len(claims_objects.get("claims"))>0:
                            for claims in claims_objects.get("claims").values():
                                for claim in claims:
                                    mainsnaks = claim.get("mainsnak")
                                    property = mainsnaks.get("property")
                                    if property == "P31":
                                        datavalue = mainsnaks.get("datavalue")
                                        value = datavalue.get("value")
                                        value_id = value.get("id")
                                        if value_id == "Q5":
                                            print("instance of human")
                                            instance_of_human = True
                                    if property == "P569":
                                        # Date of birth                            
                                        try:
                                            datavalue = mainsnaks.get("datavalue")
                                            value = datavalue.get("value")
                                            value_time = value.get("time")
                                        except:
                                            value_time = ""
                                    if property == "P106":
                                        # ocupation                            
                                        try:
                                            datavalue = mainsnaks.get("datavalue")
                                            value = datavalue.get("value")
                                            value_occupation_id = value.get("id")
                                            occupationurl="https://www.wikidata.org/wiki/Special:EntityData/" + value_occupation_id + ".json"
                                            occupation_json=requests.get(occupationurl).text
                                            occupation_objects=json.loads(occupation_json)
                                            if len(occupation_objects.get("entities"))>0:
                                                entities = occupation_objects.get("entities")
                                                occupation_item = entities.get(value_occupation_id)
                                                occupation_labels = occupation_item.get("labels")
                                                label_en = occupation_labels.get("en")
                                                value_occupation_label_en = label_en.get("value")
                                                print(value_occupation_label_en)
                                        except:
                                            value_occupation_id = ""
                                    if property == "P373":
                                        # commons category                            
                                        try:
                                            datavalue = mainsnaks.get("datavalue")
                                            value_commons_category = datavalue.get("value")
                                            if value_commons_category=="Anonymous work":
                                                value_commons_category = ""
                                        except:
                                            value_commons_category = ""
                                    if property == "P101":
                                        # field of work                            
                                        try:
                                            datavalue = mainsnaks.get("datavalue")
                                            value = datavalue.get("value")
                                            value_field_of_work = value.get("id")
                                        except:
                                            value_field_of_work = ""
                        if instance_of_human:                          
                            with open(path_csv, 'a') as artists_wikidata:
                                artists_wikidata_line=artists_wikidata_line_prefix + id + ";" + '"' + title + '"' + ";" + '"' + label + '"' +  ";" + '"' + description + '"' + ";" + value_time + ";" + creator_date_of_birth  + ";" + value_occupation_id + ";" + '"' + value_occupation_label_en + '"' + ";" +  '"' + value_commons_category + '"'
                                artists_wikidata.write(artists_wikidata_line + '\n')
                                artists_wikidata.close()

                else:
                    with open(path_csv, 'a') as artists_wikidata:
                        artists_wikidata_line=artists_wikidata_line_prefix + ";" + '"' + '"' + ";" + '"' + '"' +  ";" + '"' + '"' + ";" + ";" + ";"
                        artists_wikidata.write(artists_wikidata_line + '\n')
                    artists_wikidata.close()
            else:
                with open(path_csv, 'a') as artists_wikidata:
                    artists_wikidata_line=artists_wikidata_line_prefix + ";" + '"' + '"' + ";" + '"' + '"' +  ";" + '"' + '"' + ";" + ";"  + ";"
                    artists_wikidata.write(artists_wikidata_line + '\n')
                artists_wikidata.close()

            print('\r' + str(count), end='', flush=True)

            if count >= max_searches:
                linenumber = linenumber + count
                with open(path_bookmark, 'w') as bookmark:
                    bookmark.write(str(linenumber) + "\n")

                bookmark.close()

                break

def get_creator_lref_without_q():
    try:
        folder = './artists/'
        # Set up logging
        creator_error_log = folder+"creator_error.log"
        logging.basicConfig(filename=creator_error_log,level=logging.ERROR,format='%(asctime)s %(message)s', datefmt='%Y-%m-%d %H:%M:%S')

        smk_creator_lref_retrieved=open(folder + 'get_creator_lref_without_q_retrieved.csv', 'w')
        smk_creator_lref_retrieved.write('creator_lref;created;modified;artist;nationality;creator_forename;creator_surname;creator_date_of_death;creator_date_of_birth;creator_gender\n')

        reader = csv.reader(open(folder + 'creator_lref_without_q.csv'), quoting=csv.QUOTE_NONE, delimiter = ',')

        for row in reader:
            try:
                lref_person = row[0] 
                artist = row[1]
                url = 'https://api.smk.dk/api/v1/person?id=' + lref_person
                creator_json=requests.get(url).text

                creator_objects=json.loads(creator_json)
                creator_object_model =smkpersonmodel.welcome_from_dict(creator_objects)
                print(creator_object_model)
                if len(creator_object_model.items)>0:
                    qs = None
                    publisher = wikidata.wd_statens_museum_for_kunst
                    for item in creator_object_model.items:
                        qsitem=""
                        qs = quickstatement(item.id, \
                            datetime.now(), \
                            item.created, \
                            item.modified, \
                            '', \
                            publisher, \
                            'https://api.smk.dk/api/v1/person?id=' + lref_person)
                        
                        # Labels
                        creator_name = (item.forename+' '+item.surname).strip()
                        if creator_name=='':
                            creator_name = item.name
                            if creator_name=='':
                                creator_name=item.artist
                        qsitem=qsitem+qs.label(creator_name,'da')+qs.comment('dansk label')+'\n'
                        qsitem=qsitem+qs.label(creator_name,'en')+qs.comment('English label')+'\n'

                        # Descriptions
                        desc_da ='' 
                        desc_en= '' 
                        if len(item.nationality)>0:
                            for nationality in item.nationality:
                                desc_da=nationality.lower()+'/'
                                desc_en=smkapi.smk_nationality_to_english(nationality.lower())+'/'
                            desc_da=desc_da[0:-1]+' '
                            desc_en=desc_en[0:-1]+' '

                        life=''
                        if len(item.birth_date_start)!=0:
                            life=life+' (' + str(item.birth_date_start[0].year)+'-'
                            if len(item.death_date_start)!=0:
                                life=life+ str(item.death_date_start[0].year)
                            life=life+')' 
                        qsitem=qsitem + qs.description(desc_da+'kunstner'+life, 'da')+qs.comment('beskrivelse')+'\n' 
                        qsitem=qsitem + qs.description(desc_en+'artist'+life, 'en')+qs.comment('description')+'\n' 

                        # Instance of human
                        qsitem = qsitem + qs.instance_of()+qs.comment('instance of human')+'\n'

                        # Gender
                        qsitem = qsitem + qs.gender(smkapi.smk_gender_to_wikidata_q(item.gender[0]))+qs.comment('gender')+'\n'

                        # Nationalities
                        if len(item.nationality)>0:
                            for nationality in item.nationality:
                                qsitem=qsitem+smkapi.smk_nationality_to_wikidata_q(nationality.lower())+qs.comment('nationality')+'\n'

                        # Reference URL
                        qsitem = qsitem + qs.reference_url(False)+qs.comment('reference url')+'\n'

                        # Has works in the collection of, generate reference url to artwork
                        ref_url=None
                        if len(item.works)!=0:
                            ref_url='https://api.smk.dk/api/v1/art/?object_number='+item.works[0]
                        qsitem = qsitem + qs.has_works_in_collection(ref_url)+qs.comment('has works in the collection of')+'\n'

                        # Date of birth
                        if len(item.birth_date_start)!=0:
                            precision=11
                            dob_end=None
                            if len(item.birth_date_end)!=0:
                                dob_end=item.birth_date_end[0]
                                if item.birth_date_start!=dob_end:
                                    # Date of birth start and end dates different
                                    # Assume year precision
                                    precision=9
                            qsitem = qsitem + qs.date_of_birth(item.birth_date_start[0],dob_end,precision)
                            qsitem = qsitem + qs.comment('date of birth')+'\n'

                        # Date of death
                        if len(item.death_date_start)!=0:
                            precision=11
                            dod_end=None
                            if len(item.death_date_end)!=0:
                                dod_end=item.death_date_end[0]
                                if item.death_date_start!=dod_end:
                                    # Date of birth start and end dates different
                                    # Assume year precision
                                    precision=9
                            qsitem = qsitem + qs.date_of_death(item.death_date_start[0],dod_end,precision)
                            qsitem = qsitem + qs.comment('date of death')+'\n'

                        # Occupation
                        qsitem = qsitem + qs.occupation() + qs.comment('occupation')+'\n'
                        if len(item.name_type)>0:
                            smk_occupation=open(folder + 'smk_occupation.csv', 'a')
                            smk_occupation.write(item.name_type[0]+'\n')
                            smk_occupation.close()

                        print(qsitem)
                        personfile=open(folder+item.id+'.txt','w')
                        if qs.wikidata_item=='':
                            personfile.write('CREATE\n')
                        personfile.write(qsitem)
                        personfile.close()
            except Exception as e:
                logging.exception(e)
                
        personfile.close()
    except Exception as e:
        logging.exception(e)
    finally:
        smk_creator_lref_retrieved.close()

def query_all_artwork_types():
    try:
        # Set up logging
        artwork_types_log = "all_artwork_types.log"
        logging.basicConfig(filename=artwork_types_log,level=logging.ERROR,format='%(asctime)s %(message)s', datefmt='%Y-%m-%d %H:%M:%S')

        all_artwork_types_csv='all_artwork_types.csv'
        
        reader = csv.reader(open(all_artwork_types_csv), quoting=csv.QUOTE_NONE, delimiter = ';')

        artwork_types_labels=open('artwork_types_labels.csv','w')
        artwork_types_labels.write('SMK;item;LDa;LEn;DDa;DEn\n')
        
        for row in reader:
            try:
                artwork_type_item = row[1] 
                url= 'https://www.wikidata.org/w/api.php?action=wbgetentities&props=labels|descriptions&ids='+artwork_type_item+'&languages=en|da&format=json'

                artwork_type_json=requests.get(url).text
                artwork_type_objects=json.loads(artwork_type_json)

                try:
                    try:
                        LDa=artwork_type_objects['entities'][artwork_type_item]['labels']['da']['value']
                    except:
                        LDa=''
                    try:
                        LEn=artwork_type_objects['entities'][artwork_type_item]['labels']['en']['value']
                    except:
                        LEn=''
                    try:
                        DDa=artwork_type_objects['entities'][artwork_type_item]['descriptions']['da']['value']
                    except:
                        DDa=''
                    try:
                        DEn=artwork_type_objects['entities'][artwork_type_item]['descriptions']['en']['value']
                    except:
                        DEn=''

                    line=row[0]+';'+artwork_type_item+';'+LDa+';'+LEn+';'+DDa+';'+DEn
                    artwork_types_labels.write(line+'\n')
                except Exception as e:
                    logging.exception(e)
            except Exception as e:
                logging.exception(e)
    except Exception as e:
        logging.exception(e)
    finally:
        artwork_types_labels.close()

def find_wikidata_from_creator_lref(creator_lref):
    if len(all_creator_lref_to_wikidata_items) == 0:
        load_all_creator_lref_to_wikidata_items()
    if creator_lref.lower() in all_creator_lref_to_wikidata_items: 
        wikidata_item = all_creator_lref_to_wikidata_items[creator_lref.lower()][1]
    else:
        wikidata_item = ''

    return(wikidata_item)

def find_wikidata_from_creator_name(creator_name):
    if len(all_creator_lref_to_wikidata_items) == 0:
        load_all_creator_lref_to_wikidata_items()
    if creator_name.lower() in all_creator_lref_to_wikidata_items: 
        wikidata_item = all_creator_lref_to_wikidata_items[creator_name.lower()][1]
    else:
        wikidata_item = ''

    return(wikidata_item)

def find_wikidata_from_smk_material(smk_material):
    if len(smk_materials_to_wikidata_items) == 0:
        load_smk_materials_to_wikidata_items()
    if smk_material.lower() in smk_materials_to_wikidata_items: 
        wikidata_item = smk_materials_to_wikidata_items[smk_material.lower()][1]
    else:
        wikidata_item = ''

    return(wikidata_item)

def find_wikidata_from_object_name(smk_object_name):
    if len(smk_object_names_to_wikidata_items) == 0:
        load_smk_object_names_to_wikidata_items()
    if smk_object_name.lower() in smk_object_names_to_wikidata_items: 
        wikidata_item = smk_object_names_to_wikidata_items[smk_object_name.lower()][1]
    else:
        wikidata_item = ''

    return(wikidata_item)

def find_wikidata_from_artwork_type(smk_artwork_type):
    if len(smk_artwork_types_to_wikidata_items) == 0:
        load_smk_artwork_types_to_wikidata_items()
    if smk_artwork_type.lower() in smk_object_names_to_wikidata_items: 
        wikidata_item = smk_object_names_to_wikidata_items[smk_artwork_type.lower()][1]
    else:
        wikidata_item = ''

    return(wikidata_item)

def find_english_label_from_artwork_type(smk_artwork_types_label):
    if len(smk_artwork_types_labels_items) == 0:
        load_smk_artwork_types_labels_items()
    if smk_artwork_types_label.lower() in smk_artwork_types_labels_items: 
        english_label = smk_artwork_types_labels_items[smk_artwork_types_label.lower()][3]
    else:
        english_label = ''

    return(english_label)

def Test():
    #print(find_wikidata_item("123"))
    #generate_lists()
    #load_f_artists_items()
    #load_all_artists_items()
    #save_all_artists_items()
    #load_wikidata_worksby_items()
    #FindSMKArtistWikidata()
    #print(find_person_wikidata_item('244_person'))
    query_all_artists()
    #get_creator_lref_without_q()
    #query_all_artwork_types()
    # creator_lref="1039_person"
    # creator_wikidata=find_wikidata_from_creator_lref(creator_lref)
    # print(creator_wikidata)

    # smk_material="Æg"
    # smk_material_wikidata=find_wikidata_from_smk_material(smk_material)
    # print(smk_material_wikidata)

    # smk_object_name="Collage"
    # smk_object_name_wikidata=find_wikidata_from_object_name(smk_object_name)
    # print(smk_object_name_wikidata)

    # smk_artwork_type="kobberstik"
    # smk_artwork_type_wikidata=find_wikidata_from_artwork_type(smk_artwork_type)
    # print(smk_artwork_type_wikidata)

#Test()
