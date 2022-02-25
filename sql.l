sql query:





-- gp
CREATE TABLE gp(
	gp_id BIGSERIAL PRIMARY KEY,
	owner_id BIGSERIAL,
	check_gif BOOLEAN NOT NULL DEFAULT 'f',
	check_stick BOOLEAN NOT NULL DEFAULT 'f',
	check_text BOOLEAN NOT NULL DEFAULT 'f',
	check_video BOOLEAN NOT NULL DEFAULT 'f',
	check_voice BOOLEAN NOT NULL DEFAULT 'f' ,
	check_photo BOOLEAN NOT NULL DEFAULT 'f',
	check_id BOOLEAN NOT NULL DEFAULT 'f',
	check_link BOOLEAN NOT NULL DEFAULT 'f',
	check_all BOOLEAN NOT NULL DEFAULT 'f',
	check_hashtag BOOLEAN NOT NULL DEFAULT 'f',
	date_start DATE
);


-- gp admin
CREATE TABLE gp_ad(   
	admin_id BIGSERIAL,
	gp_id BIGSERIAL,
	

	FOREIGN KEY(gp_id) 
    REFERENCES gp(gp_id) on delete cascade,
	PRIMARY KEY (admin_id, gp_id)
);


CREATE TABLE gp_lock_word(
	word VARCHAR(15),
	gp_id BIGSERIAL,
	
	FOREIGN KEY(gp_id) 
    REFERENCES gp(gp_id) on delete cascade,
	PRIMARY KEY (word, gp_id)
);


--gp lock
CREATE TABLE gp_lock_user(
	person_id BIGSERIAL,
	gp_id BIGSERIAL,
	
	FOREIGN KEY(gp_id) 
    REFERENCES gp(gp_id) on delete cascade,
	PRIMARY KEY (person_id, gp_id)
);


CREATE TABLE warning_member (
	person_id BIGSERIAL,
	gp_id BIGSERIAL,
	count INT DEFAULT 0,

	FOREIGN KEY(gp_id) 
    REFERENCES gp(gp_id) on delete cascade,
	PRIMARY KEY (person_id, gp_id)
);

CREATE TABLE gp_vip(
	person_id BIGSERIAL,
	gp_id BIGSERIAL,
	
	FOREIGN KEY(gp_id) 
    REFERENCES gp(gp_id) on delete cascade,
	PRIMARY KEY (person_id, gp_id)
);

CREATE TABLE gp_tabchi(
	person_id BIGSERIAL,
	admin_id BIGSERIAL,
	gp_id BIGSERIAL,
	
	FOREIGN KEY(gp_id) 
    REFERENCES gp(gp_id) on delete cascade,
	PRIMARY KEY (person_id)
);

CREATE TABLE kings(   
	admin_id BIGSERIAL,
	
	PRIMARY KEY (admin_id)
);

CREATE VIEW vips AS   	
	select owner_id,gp_id from gp
	UNION
	select admin_id,gp_id from gp_ad
	UNION
	select person_id,gp_id from gp_vip
	UNION 
	select admin_id,NULL from kings;
	
https://www.digitalocean.com/community/tutorials/how-to-install-and-use-postgresql-on-ubuntu-18-04