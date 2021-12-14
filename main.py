#C:/Users/user1/Documents/anaconda/Scripts/activate
#from mydb import init
#init.start()
import time 
time.sleep(1)
from get_streamers_status import my_demon
my_demon.start()
from script import app
app.run()