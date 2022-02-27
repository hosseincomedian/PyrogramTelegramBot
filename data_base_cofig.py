import psycopg2
from psycopg2 import Error 
connection = psycopg2.connect( host="", 
                                        port = 0000, 
                                        database="", 
                                        user="", 
                                        password="")
cursor = connection.cursor()
cursor.execute(
	'CREATE TABLE gp( '+
	"gp_id BIGSERIAL PRIMARY KEY,"+
	"channel_id BIGSERIAL,"+
	"days int ,"+
	"owner_id BIGSERIAL,"+
	"check_gif BOOLEAN NOT NULL DEFAULT 'f',"+
	"check_stick BOOLEAN NOT NULL DEFAULT 'f',"+
	"check_text BOOLEAN NOT NULL DEFAULT 'f',"+
	"check_video BOOLEAN NOT NULL DEFAULT 'f',"+
	"check_voice BOOLEAN NOT NULL DEFAULT 'f' ,"+
	"check_photo BOOLEAN NOT NULL DEFAULT 'f' ,"+
	"check_id BOOLEAN NOT NULL DEFAULT 'f',"+
	"check_link BOOLEAN NOT NULL DEFAULT 'f',"+
	"check_all BOOLEAN NOT NULL DEFAULT 'f',"+
	"check_hashtag BOOLEAN NOT NULL DEFAULT 'f',"+
    "date_start DATE"+
	");"
		
	)
connection.commit()

cursor.execute(
	"CREATE TABLE gp_ad("+  
	"admin_id BIGSERIAL,"+
	"gp_id BIGSERIAL,"+
	"FOREIGN KEY(gp_id) "+
    "REFERENCES gp(gp_id) on delete cascade,"+
	"PRIMARY KEY (admin_id, gp_id));"
	
	)
connection.commit()

cursor.execute(
	"CREATE TABLE vizir("+  
	"admin_id BIGSERIAL,"+
	"gp_id BIGSERIAL,"+
	"FOREIGN KEY(gp_id) "+
    "REFERENCES gp(gp_id) on delete cascade,"+
	"PRIMARY KEY (admin_id, gp_id));"
	
	)
connection.commit()

cursor.execute("CREATE TABLE gp_lock_word("+
	"word VARCHAR(15),"+
	"gp_id BIGSERIAL,"+
	
	"FOREIGN KEY(gp_id) "+ 
    "REFERENCES gp(gp_id) on delete cascade,"+
	"PRIMARY KEY (word, gp_id));")
connection.commit()

cursor.execute("CREATE TABLE gp_lock_user("+
	"person_id BIGSERIAL,"+
	"gp_id BIGSERIAL,"+
	
	"FOREIGN KEY(gp_id)" + 
    "REFERENCES gp(gp_id) on delete cascade,"+
	"PRIMARY KEY (person_id, gp_id));")
connection.commit()

cursor.execute("CREATE TABLE warning_member ("+
	"person_id BIGSERIAL,"+
	"gp_id BIGSERIAL,"+
	"count INT DEFAULT 0,"+

	"FOREIGN KEY(gp_id) "+
    "REFERENCES gp(gp_id) on delete cascade,"+
	"PRIMARY KEY (person_id, gp_id));")
connection.commit()

cursor.execute("CREATE TABLE gp_vip("+
	"person_id BIGSERIAL,"+
	"gp_id BIGSERIAL,"+
	
	"FOREIGN KEY(gp_id) "+
    "REFERENCES gp(gp_id) on delete cascade,"+
	"PRIMARY KEY (person_id, gp_id));")
connection.commit()

cursor.execute("CREATE TABLE gp_tabchi("+
	"person_id BIGSERIAL,"+
	"admin_id BIGSERIAL,"+
	"gp_id BIGSERIAL,"+
	
	"FOREIGN KEY(gp_id) "+
    "REFERENCES gp(gp_id) on delete cascade,"+
	"PRIMARY KEY (person_id));")
connection.commit()

cursor.execute("CREATE TABLE kings(" +  
	    "admin_id BIGSERIAL,"+
	    "PRIMARY KEY (admin_id));")
connection.commit()

cursor.execute("CREATE VIEW vips AS "+  	
	"select owner_id,gp_id from gp "+
	"UNION "+
	"select admin_id,gp_id from gp_ad "+
	"UNION "+
	"select person_id,gp_id from gp_vip "+
	"UNION "+
	"select admin_id,gp_id from vizir "+
	"UNION "+
	"select admin_id,NULL from kings;")
connection.commit()
