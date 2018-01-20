### Setup
Change database properties in `app/properties.py`

### Launch application
Run `python run.py` for default base url `localhost:5000`

### Routes
  
Module: inquiries  
`/inquiries` (GET, POST)  
`/inquiries/detail/<int:inquiry_id>` (GET)  
`/inquiries/edit/<int:inquiry_id>` (GET, POST)  
`/inquiries/edit/<int:inquiry_id>/json` (GET)  
`/inquiries/new` (GET, POST)  
`/inquiries/delete/<int:inquiry_id>` (POST)  
`/inquiries/delete_item/<int:inquiry_id>/<int:item_id>` (POST)  
  
Module: api  
`/api/_search_by_code` (GET)  
`/api/_search_by_title` (GET)  
`/api/_subcategory_by_category` (GET)  

## Dependencies
* Python 3.6.0
* PostgreSql 9.6
* SQLAlchemy 1.1.5
* Flask 0.12
