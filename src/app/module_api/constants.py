from sqlalchemy.sql import text



SELECT_PRODUCT_BY_CODE = text('''
	SELECT id, code, ean, title, description 
	FROM product 
	WHERE code=:code 
	;''')

SELECT_PRODUCT_BY_TITLE = text('''
	SELECT id, code, ean, title, description 
	FROM product 
	WHERE subcategory_id=:subcategory_id AND title ILIKE :expr_title 
	LIMIT 50 
	;''')

SELECT_SUBCATEGORY_BY_CATEGORY = text('''
	SELECT id, name 
	FROM subcategory 
	WHERE category_id=:category_id 
	;''')


