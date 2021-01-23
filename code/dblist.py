import sqlite3
conn = sqlite3.connect('toeic.db')
cur = conn.cursor()

def show_all_rows(columns, all_rows):
    print(columns)
    for row in all_rows:
        print(row)
    print()

def show_table(cur, table):
    cur.execute('SELECT * FROM {}'.format(table))
    columns = [description[0] for description in cur.description]
    show_all_rows(columns, cur.fetchall())
    
tables = ('WORDS', 'SETTINGS', 'EXAMINEES', 'SCORES')
for tab in tables:
    show_table(cur, tab)

conn.close()