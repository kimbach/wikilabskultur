# csvlookup
import csv

wikidata_items={}

def load_wikidata_items():
    with open('wikidata_smk.csv', 'r') as file:
        reader = csv.DictReader(file, quoting=csv.QUOTE_NONE, delimiter = ';')
        for row in reader:
            wikidata_items[row["inventorynumber"].lower()] = row["wikidataitem"]

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

# Generate lists of unique artwork types, nationalities and creators from SMK import csv
# and filter on specific artists
def generate_lists():
    notes=[]
    nationalities=[]
    creators=[]
    artists=[]
    with open('commons_smk_total.csv', 'r') as file:
        reader = csv.reader(file, quoting=csv.QUOTE_NONE, delimiter = ';')
        for commons_row in reader:
            note_found = False 
            for note in notes:
                if commons_row[16]==note:
                    #print(commons_row[16] +' FOUND:')
                    note_found = True 
                    break
            if note_found == False:
                notes.append(commons_row[16]) 
            
            nationalities[nationality] = commons_row[1] 
            nationality_found = False 
            for nationality in nationalities:
                if commons_row[1]==nationality:
                    #print(commons_row[16] +' FOUND:')
                    nationality_found = True 
                    break
            if nationality_found == False:
                nationalities.append(commons_row[1]) 
            
            creator_found = False 
            for creator in creators:
                if commons_row[0] + ';' + commons_row[1]==creator:
                    #print(commons_row[16] +' FOUND:')
                    creator_found = True 
                    break
            if creator_found == False:
                creators.append(commons_row[0] + ';' + commons_row[1]) 

            # Joakim Skovgaard
            # Viggo Pedersen
            # Theodor Philipsen
            # Edvard Petersen
            # Kristian Zahrtmann

            if commons_row[0]=='Joakim Skovgaard':
                artists.append(commons_row) 
            elif commons_row[0]=='Viggo Pedersen':
                artists.append(commons_row) 
            elif commons_row[0]=='Theodor Philipsen':
                artists.append(commons_row)
            elif commons_row[0]=='Edvard Petersen':
                artists.append(commons_row)
            elif commons_row[0]=='Kristian Zahrtmann':
                artists.append(commons_row)

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
    f_artists.write('artist;title;accession_number;imageurl;public_domain;has_image\n')

    for artist in artists:
        f_artists.write(artist[0] + ';' + artist[3] + ';' + artist[17] + ';' + artist[28] + ';' + artist[29] + ';' + artist[30] + '\n')
        print(artist)
    f_artists.close()

#print(find_wikidata_item("123"))