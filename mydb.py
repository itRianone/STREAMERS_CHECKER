import sqlite3
import time
import datetime
import threading
from settings import DB_USER, DB_PASSWORD, DB_HOST, DB_PORT, DB_NAME


# def init_db():
    # while True:
    #     global db, cursor
print('Start connection ', datetime.datetime.now())
db = sqlite3.connect('database.sqlite', check_same_thread=False)
    # f'postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}',keepalives=1)
cursor = db.cursor()
    # time.sleep(60)

    # print('End connection ', datetime.datetime.now())
    # try:
    #     cursor.execute('''SELECT * from streamers''')
    # except psycopg2.OperationalError:
    #     print('err')
    #     continue

cursor.execute(
    """CREATE TABLE IF NOT EXISTS streamers(
        id INTEGER PRIMARY KEY,
        streamer_name TEXT NOT NULL,
        streamer_status TEXT,
        stream_img TEXT,
        stream_title TEXT,
        streamer_username TEXT,
        channel_discription TEXT 
    );
""")
db.commit()




# init = threading.Thread(target=init_db, daemon=True)

# cursor.execute(
#     """DROP TABLE streamers;
# """)




