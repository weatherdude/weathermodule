import requests
from PIL import Image
from io import BytesIO
import time
import os
from config.definitions import ROOT_DIR

zoom_level = 5
tiles_xy = 2**zoom_level
for x in range(0,tiles_xy):
    for y in range(0,tiles_xy):
        print('x: '+str(x))
        print('y: '+str(y))
        url = "https://tile.openweathermap.org/map/temp_new/"+str(zoom_level)+"/"+str(x)+"/"+str(y)+".png?appid=4fe62e7b73e91da6cadffd2bf815fd91"
        print(url)
        r = requests.get(url)

        i = Image.open(BytesIO(r.content))
        path = os.path.join(ROOT_DIR, "tiles", "tile_"+str(x)+"_"+str(y)+".png")
        picture = i.save(path)

        time.sleep(1)
