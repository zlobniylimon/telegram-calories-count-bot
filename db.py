import sqlite3
import time

con = sqlite3.connect('calories.db')
cur = con.cursor()

def _get_formated_time():
	return time.strftime("%Y-%m-%d")

def insert(calories, food_name):
	cur.execute(
				f"INSERT INTO food_eated "
				f"(name, calories, created) "
				f"VALUES ('{food_name}', {int(calories)}, '{_get_formated_time()}');"
		)
	con.commit()

def _init_db():
	cur.execute("""
				CREATE table food_eated (
					id integer not null PRIMARY KEY,
					name text,
					calories integer,
					created text
				);
				""")
	con.commit()

def fetch_all():
	cur.execute("SELECT * from food_eated;")
	data = cur.fetchall()

	return data

def check_db_exist():
	cur.execute("SELECT name from sqlite_master "
				"WHERE type='table' and name='food_eated'")
	table_exist = cur.fetchall()
	if table_exist:
		return
	_init_db()

check_db_exist()