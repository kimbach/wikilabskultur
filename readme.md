# Wiki Labs Kultur
This is the repository for Wiki Labs Kultur, a collaboration between 
- Wikimedia Danmark 
- Den Hirschsprungske Samling 
- Det Kgl. Bibliotek (KB)
- Det Danske Filminstitut (DFI) 
- AU Library Campus Emdrup
- Statens Værksteder for Kunst (SVfK)
- Statens Museum for Kunst (SMK)
- Thorvaldsens Museum

See https://www.facebook.com/groups/133970093625705

The code is utilising the Wikimedia pywikibot API

https://www.mediawiki.org/wiki/Manual:Pywikibot

- [Wiki Labs Kultur](#wiki-labs-kultur)
  - [Files](#files)
    - [smkitems.json](#smkitemsjson)
  - [Modules](#modules)
    - [smkapi.py](#smkapipy)
    - [smkitem.py](#smkitempy)
      - [Item](#item)
    - [commons.py](#commonspy)
    - [wikidata.py](#wikidatapy)
      - [BaseTemplate](#basetemplate)
      - [ArtworkTemplate](#artworktemplate)
    - [smkbatch.py](#smkbatchpy)

## Files
### smkitems.json
File containing a sample of data returned by the SMK API, using these filters:

public_domain=true
has_image=true
offset=0
rows=10 

https://api.smk.dk/api/v1/art/search/?keys=*&filters=%5Bpublic_domain%3Atrue%5D,%5Bhas_image%3Atrue%5D&offset=0&rows=10

## Modules
### smkapi.py

smkapi module contains methods to interact with API from Statens Museeum for Kunst

### smkitem.py

smkitem module models the API object model from Statens Museeum for Kunst

#### Item
Class than contains the object model

Item, was auto-generated from the API using https://app.quicktype.io

From the JSON returned by this API call
https://api.smk.dk/api/v1/art/search/?keys=*&filters=%5Bpublic_domain%3Atrue%5D,%5Bhas_image%3Atrue%5D&offset=0&rows=10
  
Yielding this code
https://app.quicktype.io?share=q7q5bhqKximgfNuxroSP

### commons.py
Helper module for Wikimedia Commons, for instance templates

### wikidata.py
Helper module for Wikidata, for instance templates

#### BaseTemplate
Abstract base class than for templates 

#### ArtworkTemplate
Class than implements the object model for the Artwork template 

### smkbatch.py
Functions for SMK Batch Upload, main function is

MapSMKAPIToCommons(batch_title,smk_filter,smk_number_list,download_images)

