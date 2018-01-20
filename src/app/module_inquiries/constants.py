from sqlalchemy.sql import text



SELECT_INQUIRIES_LIST_ALL = text('''
	SELECT t.id, t.time_issued, t.time_responded, t.email, COUNT(inquiry_item.inquiry_id), SUM(inquiry_item.amount * inquiry_item.price) 
	FROM ( 
		SELECT id, time_issued, time_responded, email 
		FROM inquiry 
		ORDER BY time_issued DESC 
		LIMIT :limit 
		OFFSET :offset 
		) t 
	LEFT JOIN inquiry_item ON t.id=inquiry_item.inquiry_id 
	GROUP BY t.id, t.time_issued, t.time_responded, t.email 
	ORDER BY t.time_issued DESC 
	;''')

SELECT_INQUIRIES_LIST_NOT_RESPONDED = text('''
	SELECT t.id, t.time_issued, t.time_responded, t.email, COUNT(inquiry_item.inquiry_id), SUM(inquiry_item.amount * inquiry_item.price) 
	FROM ( 
		SELECT id, time_issued, time_responded, email 
		FROM inquiry 
		WHERE time_responded IS NULL 
		ORDER BY time_issued DESC 
		LIMIT :limit 
		OFFSET :offset 
		) t 
	LEFT JOIN inquiry_item ON t.id=inquiry_item.inquiry_id 
	GROUP BY t.id, t.time_issued, t.time_responded, t.email 
	ORDER BY t.time_issued DESC 
	;''')

SELECT_INQUIRIES_LIST_MIN_TOTAL_PRICE_SMALL = text('''
	SELECT t.id, t.time_issued, t.time_responded, t.email, COUNT(inquiry_item.inquiry_id), SUM(inquiry_item.amount * inquiry_item.price) 
	FROM ( 
		SELECT id, time_issued, time_responded, email 
		FROM inquiry 
		WHERE ( 
			SELECT SUM(inquiry_item.amount * inquiry_item.price) 
			FROM inquiry_item 
			WHERE inquiry_item.inquiry_id = inquiry.id 
			) >= :minTotalPrice 
		ORDER BY time_issued DESC 
		LIMIT :limit 
		OFFSET :offset 
		) t 
	LEFT JOIN inquiry_item ON t.id=inquiry_item.inquiry_id 
	GROUP BY t.id, t.time_issued, t.time_responded, t.email 
	ORDER BY t.time_issued DESC 
	;''')

SELECT_INQUIRIES_LIST_MIN_TOTAL_PRICE_BIG = text('''
	SELECT t.id, t.time_issued, t.time_responded, t.email, COUNT(inquiry_item.inquiry_id), SUM(inquiry_item.amount * inquiry_item.price) 
	FROM ( 
		SELECT id, time_issued, time_responded, email 
		FROM inquiry 
		WHERE time_responded IS NOT NULL 
		ORDER BY time_issued DESC 
		LIMIT :limit 
		OFFSET :offset 
		) t 
	LEFT JOIN inquiry_item ON t.id=inquiry_item.inquiry_id 
	GROUP BY t.id, t.time_issued, t.time_responded, t.email 
	HAVING SUM(inquiry_item.amount * inquiry_item.price) > :minTotalPrice 
	ORDER BY t.time_issued DESC 
	;''')

SELECT_INQUIRY_WITH_ITEMS = text('''
	SELECT inquiry.id, inquiry.time_issued, inquiry.time_responded, inquiry.email, 
			inquiry_item.id, inquiry_item.amount, inquiry_item.price, 
	        product.code, product.title, product.price 
	FROM inquiry 
	JOIN inquiry_item ON inquiry.id=inquiry_item.inquiry_id 
	JOIN product ON inquiry_item.product_id=product.id 
	WHERE inquiry.id=:inquiry_id 
	;''')

SELECT_CATEGORY_ALL = text('''
	SELECT id, name 
	FROM category 
	;''')



INSERT_INQUIRY = text('''
	INSERT INTO inquiry (email, time_issued, auth_id) 
	VALUES ( :email, date_trunc('second', CURRENT_TIMESTAMP), (SELECT id FROM auth WHERE email=:email) ) 
	RETURNING id 
	;''')

INSERT_INQUIRY_ITEM = text('''
	INSERT INTO inquiry_item (amount, product_id, inquiry_id) 
	VALUES ( :amount, :product_id, :inquiry_id ) 
	;''')



UPDATE_INQUIRY = text('''
	UPDATE inquiry 
	SET time_responded=date_trunc('second', CURRENT_TIMESTAMP) 
	WHERE id=:inquiry_id 
	;''')

UPDATE_INQUIRY_ITEM = text('''
	UPDATE inquiry_item 
	SET amount=:amount, price=:price 
	WHERE id=:item_id 
	;''')



DELETE_INQUIRY_WITH_ITEMS = text('''
	DELETE FROM inquiry 
	WHERE id=:inquiry_id 
	RETURNING * 
	;''')

DELETE_INQUIRY_ITEM = text('''
	DELETE FROM inquiry_item 
	WHERE id=:item_id 
	;''')


