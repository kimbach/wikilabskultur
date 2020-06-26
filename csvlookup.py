# csvlookup
import csv

def find_wikidata_item(object_id):
    # Usage:
    #  wikidata_item = find_wikidata_item(commons_row[17])
    #  if wikidata_item != '':
    #      print(wikidata_item)

    wikidata_item = ''
    with open('wikidata_smk.csv', 'r') as file:
        reader = csv.reader(file, quoting=csv.QUOTE_NONE, delimiter = ';')
        for row in reader:
            if row[0]==object_id:
                print('FOUND:')
                print(row)
                wikidata_item = row[1]
                break
    return(wikidata_item)

# Generate lists of unique artwork types and nationalities 
notes=[]
nationalities=[]
with open('commons_smk_total.csv', 'r') as file:
    reader = csv.reader(file, quoting=csv.QUOTE_NONE, delimiter = ';')
    for commons_row in reader:
        notes_found = False 
        for note in notes:
            if commons_row[16]==note:
                #print(commons_row[16] +' FOUND:')
                notes_found = True 
                break
        if notes_found == False:
            notes.append(commons_row[16]) 
        nationality_found = False 
        for nationality in nationalities:
            if commons_row[1]==nationality:
                #print(commons_row[16] +' FOUND:')
                nationality_found = True 
                break
        if nationality_found == False:
            nationalities.append(commons_row[1]) 
        
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


