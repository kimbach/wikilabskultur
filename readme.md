# Wiki Labs Kultur
This is the repository for Wiki Labs Kultur

- [Wiki Labs Kultur](#wiki-labs-kultur)
  - [Modules](#modules)
    - [smkitem.py](#smkitempy)
      - [Item](#item)
    - [wikimedia.py](#wikimediapy)
      - [BaseTemplate](#basetemplate)
      - [ArtworkTemplate](#artworktemplate)
    - [SMKBatchUpload.py](#smkbatchuploadpy)

## Modules
### smkitem.py

smkitem module models the API object model from Statens Museeum for Kunst

#### Item
Class than contains the object model

Item, was auto-generated from the API using https://app.quicktype.io
Using this API call
https://api.smk.dk/api/v1/art/search/?keys=*&filters=%5Bpublic_domain%3Atrue%5D,%5Bhas_image%3Atrue%5D&offset=0&rows=10
  
Yielding this code
https://app.quicktype.io?share=q7q5bhqKximgfNuxroSP


### wikimedia.py
Helper module for Wikimedia projects, for instance templates

#### BaseTemplate
Abstract base class than for templates 

#### ArtworkTemplate
Class than implements the object model for the Artwork template 

### SMKBatchUpload.py
Unit test for SMK Batch Upload
