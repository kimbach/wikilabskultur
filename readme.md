# Wiki Labs Kultur
This is the repository for Wiki Labs Kultur

Modules:
- smkitem.py - implements the object model for the SMK API Items
-- Item - class than contains the object model
--- To use, make sure you
---     import json
---
--- and then, to convert JSON from a string, do
---
---     result = empty_from_dict(json.loads(json_string))

- wikimedia.py - helper module for Wikimedia projects, for instance templates
-- BaseTemplate - abstract base class than for templates 
-- ArtworkTemplate - class than contains the object model for the Artwork template 
--- To use this code, make sure you

-SMKBatchUpload.py - unit test for SMK Batch Upload
