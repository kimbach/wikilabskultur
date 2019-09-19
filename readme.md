# Wiki Labs Kultur
This is the repository for Wiki Labs Kultur

## Modules:
### smkitem.py - implements the object model for the SMK API Items
smkitem module models the API object model from Statens Museeum for Kunst

The main class: Item, was auto-generated from the API using https://app.quicktype.io
Using this API call
https://api.smk.dk/api/v1/art/search/?keys=*&filters=%5Bpublic_domain%3Atrue%5D,%5Bhas_image%3Atrue%5D&offset=0&rows=10
  
Yielding this code
https://app.quicktype.io?share=q7q5bhqKximgfNuxroSP

#### Item - class than contains the object model

### wikimedia.py - helper module for Wikimedia projects, for instance templates
#### BaseTemplate - abstract base class than for templates 
#### ArtworkTemplate - class than contains the object model for the Artwork template 

### SMKBatchUpload.py - unit test for SMK Batch Upload
