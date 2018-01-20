/* ---------------------------------------------------- */
/*  Generated by Enterprise Architect Version 13.0 		*/
/*  Created On : 25-mar-2017 19:50:20 				*/
/*  DBMS       : PostgreSQL 						*/
/* ---------------------------------------------------- */

/* Drop Sequences for Autonumber Columns */

 

 

 

 

 

 

 

 

 

 

 

/* Drop Tables */

DROP TABLE IF EXISTS public.auth CASCADE
;

DROP TABLE IF EXISTS public.card CASCADE
;

DROP TABLE IF EXISTS public.card_provider CASCADE
;

DROP TABLE IF EXISTS public.category CASCADE
;

DROP TABLE IF EXISTS public.commentary CASCADE
;

DROP TABLE IF EXISTS public.inquiry CASCADE
;

DROP TABLE IF EXISTS public.inquiry_item CASCADE
;

DROP TABLE IF EXISTS public.product CASCADE
;

DROP TABLE IF EXISTS public.ranking CASCADE
;

DROP TABLE IF EXISTS public.review CASCADE
;

DROP TABLE IF EXISTS public.subcategory CASCADE
;

/* Create Tables */

CREATE TABLE public.auth
(
	id serial NOT NULL,
	email varchar(1024) NOT NULL,
	password_hash char(40) NOT NULL
)
;

CREATE TABLE public.card
(
	id serial NOT NULL,
	number_encrypted char(32) NOT NULL,
	holder_encrypted char(32) NOT NULL,
	security_code_encrypted char(32) NOT NULL,
	expire_encrypted char(32) NOT NULL,
	auth_id integer NOT NULL,
	card_provider_id integer NOT NULL
)
;

CREATE TABLE public.card_provider
(
	id serial NOT NULL,
	provider varchar(64) NOT NULL
)
;

CREATE TABLE public.category
(
	id serial NOT NULL,
	name varchar(64) NOT NULL
)
;

CREATE TABLE public.commentary
(
	id serial NOT NULL,
	time_created timestamp without time zone NOT NULL,
	body varchar(1024) NOT NULL,
	auth_id integer NOT NULL,
	review_id integer NOT NULL
)
;

CREATE TABLE public.inquiry
(
	id serial NOT NULL,
	email varchar(1024) NOT NULL,
	time_issued timestamp without time zone NOT NULL,
	time_responded timestamp without time zone NULL,
	auth_id integer NULL
)
;

CREATE TABLE public.inquiry_item
(
	id serial NOT NULL,
	amount integer NOT NULL,
	price numeric(10,2) NOT NULL,
	inquiry_id integer NOT NULL,
	product_id integer NOT NULL
)
;

CREATE TABLE public.product
(
	id serial NOT NULL,
	code char(8) NOT NULL,
	ean char(13) NULL,
	price numeric(10,2) NOT NULL,
	available boolean NOT NULL   DEFAULT FALSE,
	thumbnail_url varchar(2048) NOT NULL,
	image_url varchar(2048) NOT NULL,
	title varchar(256) NOT NULL,
	description text NOT NULL,
	subcategory_id integer NOT NULL
)
;

CREATE TABLE public.ranking
(
	id serial NOT NULL,
	num_stars smallint NOT NULL
)
;

CREATE TABLE public.review
(
	id serial NOT NULL,
	time_created timestamp without time zone NOT NULL,
	time_updated timestamp without time zone NULL,
	title varchar(128) NOT NULL,
	body text NOT NULL,
	auth_id integer NOT NULL,
	ranking_id integer NOT NULL,
	product_id integer NOT NULL
)
;

CREATE TABLE public.subcategory
(
	id serial NOT NULL,
	name varchar(64) NOT NULL,
	category_id integer NOT NULL
)
;

/* Create Primary Keys, Indexes, Uniques, Checks */

ALTER TABLE public.auth ADD CONSTRAINT PK_Auth
	PRIMARY KEY (id)
;

ALTER TABLE public.auth 
  ADD CONSTRAINT unique_email UNIQUE (email)
;

CREATE INDEX IX_email ON public.auth (email ASC)
;

ALTER TABLE public.card ADD CONSTRAINT PK_Card
	PRIMARY KEY (id)
;

CREATE INDEX IXFK_Card_Auth ON public.card (auth_id ASC)
;

CREATE INDEX IXFK_Card_CardProvider ON public.card (card_provider_id ASC)
;

ALTER TABLE public.card_provider ADD CONSTRAINT PK_CardProvider
	PRIMARY KEY (id)
;

ALTER TABLE public.card_provider 
  ADD CONSTRAINT unique_provider UNIQUE (provider)
;

ALTER TABLE public.category ADD CONSTRAINT PK_Category
	PRIMARY KEY (id)
;

ALTER TABLE public.category 
  ADD CONSTRAINT unique_name UNIQUE (name)
;

ALTER TABLE public.commentary ADD CONSTRAINT PK_Commentary
	PRIMARY KEY (id)
;

CREATE INDEX IXFK_Commentary_Auth ON public.commentary (auth_id ASC)
;

CREATE INDEX IXFK_Commentary_Review ON public.commentary (review_id ASC)
;

ALTER TABLE public.inquiry ADD CONSTRAINT PK_Inquiry
	PRIMARY KEY (id)
;

ALTER TABLE public.inquiry ADD CONSTRAINT check_time_responded CHECK (time_issued < time_responded)
;

CREATE INDEX IX_time_issued ON public.inquiry (time_issued DESC)
;

ALTER TABLE public.inquiry_item ADD CONSTRAINT PK_InquiryItem
	PRIMARY KEY (id)
;

ALTER TABLE public.inquiry_item 
  ADD CONSTRAINT unique_inquiry_and_product UNIQUE (inquiry_id,product_id)
;

ALTER TABLE public.inquiry_item ADD CONSTRAINT check_price CHECK (price > 0)
;

ALTER TABLE public.inquiry_item ADD CONSTRAINT check_amount CHECK (amount > 0)
;

CREATE INDEX IXFK_InquiryItem_Inquiry ON public.inquiry_item (inquiry_id ASC)
;

ALTER TABLE public.product ADD CONSTRAINT PK_Product
	PRIMARY KEY (id)
;

ALTER TABLE public.product 
  ADD CONSTRAINT unique_code UNIQUE (code)
;

ALTER TABLE public.product ADD CONSTRAINT check_price CHECK (price > 0)
;

CREATE INDEX IXFK_Product_Subcategory ON public.product (subcategory_id ASC)
;

CREATE INDEX IX_code ON public.product (code ASC)
;

ALTER TABLE public.ranking ADD CONSTRAINT PK_Ranking
	PRIMARY KEY (id)
;

ALTER TABLE public.ranking 
  ADD CONSTRAINT unique_num_stars UNIQUE (num_stars)
;

ALTER TABLE public.review ADD CONSTRAINT PK_Review
	PRIMARY KEY (id)
;

ALTER TABLE public.review 
  ADD CONSTRAINT unique_auth_and_product UNIQUE (auth_id,product_id)
;

ALTER TABLE public.review ADD CONSTRAINT check_time_updated CHECK (time_created < time_updated)
;

CREATE INDEX IXFK_Review_Auth ON public.review (auth_id ASC)
;

CREATE INDEX IXFK_Review_Product ON public.review (product_id ASC)
;

CREATE INDEX IXFK_Review_Ranking ON public.review (ranking_id ASC)
;

ALTER TABLE public.subcategory ADD CONSTRAINT PK_Subcategory
	PRIMARY KEY (id)
;

ALTER TABLE public.subcategory 
  ADD CONSTRAINT unique_name_and_category UNIQUE (category_id,name)
;

CREATE INDEX IXFK_Subcategory_Category ON public.subcategory (category_id ASC)
;

/* Create Foreign Key Constraints */

ALTER TABLE public.card ADD CONSTRAINT FK_Card_Auth
	FOREIGN KEY (auth_id) REFERENCES public.auth (id) ON DELETE Cascade ON UPDATE No Action
;

ALTER TABLE public.card ADD CONSTRAINT FK_Card_CardProvider
	FOREIGN KEY (card_provider_id) REFERENCES public.card_provider (id) ON DELETE No Action ON UPDATE No Action
;

ALTER TABLE public.commentary ADD CONSTRAINT FK_Commentary_Auth
	FOREIGN KEY (auth_id) REFERENCES public.auth (id) ON DELETE Cascade ON UPDATE No Action
;

ALTER TABLE public.commentary ADD CONSTRAINT FK_Commentary_Review
	FOREIGN KEY (review_id) REFERENCES public.review (id) ON DELETE Cascade ON UPDATE No Action
;

ALTER TABLE public.inquiry ADD CONSTRAINT FK_Inquiry_Auth
	FOREIGN KEY (auth_id) REFERENCES public.auth (id) ON DELETE Set Null ON UPDATE No Action
;

ALTER TABLE public.inquiry_item ADD CONSTRAINT FK_InquiryItem_Inquiry
	FOREIGN KEY (inquiry_id) REFERENCES public.inquiry (id) ON DELETE Cascade ON UPDATE No Action
;

ALTER TABLE public.inquiry_item ADD CONSTRAINT FK_InquiryItem_Product
	FOREIGN KEY (product_id) REFERENCES public.product (id) ON DELETE Set Null ON UPDATE No Action
;

ALTER TABLE public.product ADD CONSTRAINT FK_Product_Subcategory
	FOREIGN KEY (subcategory_id) REFERENCES public.subcategory (id) ON DELETE No Action ON UPDATE No Action
;

ALTER TABLE public.review ADD CONSTRAINT FK_Review_Auth
	FOREIGN KEY (auth_id) REFERENCES public.auth (id) ON DELETE Cascade ON UPDATE No Action
;

ALTER TABLE public.review ADD CONSTRAINT FK_Review_Product
	FOREIGN KEY (product_id) REFERENCES public.product (id) ON DELETE Cascade ON UPDATE No Action
;

ALTER TABLE public.review ADD CONSTRAINT FK_Review_Ranking
	FOREIGN KEY (ranking_id) REFERENCES public.ranking (id) ON DELETE No Action ON UPDATE No Action
;

ALTER TABLE public.subcategory ADD CONSTRAINT FK_Subcategory_Category
	FOREIGN KEY (category_id) REFERENCES public.category (id) ON DELETE No Action ON UPDATE No Action
;

/* Create Table Comments, Sequences for Autonumber Columns */

 

 

 

 

 

 

 

 

 

 

 