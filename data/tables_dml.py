# auth
INSERT_INTO_AUTH = '''INSERT INTO 
		auth (email, password_hash) 
		VALUES ( %s, %s ) 
		ON CONFLICT DO NOTHING;'''
# card_provider
INSERT_INTO_CARD_PROVIDER = '''INSERT INTO 
		card_provider (provider) 
		VALUES ( %s );'''
# card
INSERT_INTO_CARD = '''INSERT INTO 
		card (number_encrypted, holder_encrypted, security_code_encrypted, expire_encrypted, card_provider_id, auth_id) 
		SELECT %s, %s, %s, %s, %s, id 
		FROM auth WHERE id=%s;'''
# category
INSERT_INTO_CATEGORY = '''INSERT INTO 
		category (name) 
		VALUES ( %s );'''
# subcategory
INSERT_INTO_SUBCATEGORY = '''INSERT INTO 
		subcategory (name, category_id) 
		VALUES ( %s, %s );'''
# product
INSERT_INTO_PRODUCT = '''INSERT INTO 
		product (code, ean, price, available, thumbnail_url, image_url, title, description, subcategory_id) 
		VALUES ( %s, %s, %s, %s, %s, %s, %s, %s, %s ) 
		ON CONFLICT DO NOTHING;'''
# ranking
INSERT_INTO_RANKING = '''INSERT INTO 
		ranking (num_stars) 
		VALUES ( %s );'''
# review
INSERT_INTO_REVIEW = '''INSERT INTO 
		review (time_created, time_updated, title, body, auth_id, ranking_id, product_id) 
		SELECT %s, %s, %s, %s, t.aid, %s, t.pid 
		FROM (
			SELECT auth.id AS aid, product.id AS pid 
			FROM auth, product 
			WHERE ( auth.id, product.id ) = ( %s, %s ) 
		) t
		ON CONFLICT DO NOTHING;'''
# commentary
INSERT_INTO_COMMENTARY = '''INSERT INTO 
		commentary (time_created, body, auth_id, review_id) 
		SELECT %s, %s, t.aid, t.rid 
		FROM (
			SELECT auth.id AS aid, review.id AS rid 
			FROM auth, review 
			WHERE ( auth.id, review.id ) = ( %s, %s ) 
		) t;'''
# inquiry
INSERT_INTO_INQUIRY_AUTH = '''INSERT INTO 
		inquiry (email, time_issued, time_responded, auth_id) 
		SELECT email, %s, %s, id 
		FROM auth WHERE auth.id=%s;'''
INSERT_INTO_INQUIRY_ANONYMOUS = '''INSERT INTO 
		inquiry (email, time_issued, time_responded, auth_id) 
		VALUES ( %s, %s, %s, NULL );'''
# inquiry_item
INSERT_INTO_INQUIRY_ITEM = '''INSERT INTO 
		inquiry_item (amount, price, product_id, inquiry_id) 
		SELECT %s, t.price, t.pid, t.iid 
		FROM (
			SELECT product.price, product.id AS pid, inquiry.id AS iid 
			FROM product, inquiry 
			WHERE ( product.id, inquiry.id ) = ( %s, %s ) 
		) t
		ON CONFLICT DO NOTHING;'''

DELETE_EMPTY_INQUIRY = '''DELETE 
	FROM inquiry 
	WHERE NOT EXISTS (
		SELECT * 
		FROM inquiry_item 
		WHERE inquiry_item.inquiry_id=inquiry.id 
	);'''



SELECT_CATEGORY_ID = 'SELECT id FROM category WHERE name=%s;'
SELECT_SUBCATEGORY_ID = 'SELECT id FROM subcategory WHERE name=%s;'

