import json
import os
import random
import subprocess

ROOT_PATH = "D:/CS/rsolp-blender/"
BLENDER_PATH = "C:/Program Files/Blender Foundation/Blender 2.82/blender.exe"
SCENES_PATH = "D:/CS/rsolp-blender/input/"

scenes = [f[:-6] for f in os.listdir(SCENES_PATH) if f.endswith('.blend')]   #all names of .blend files in scene folder

for scene in scenes:
    #Save the size of the plane as a JSON file for limiting input locations
    subprocess.run([BLENDER_PATH,
                    "--background",
                    SCENES_PATH + scene + ".blend",
                    "--python",
                    ROOT_PATH + "get_plane_bounds.py"])
    
    num = int(input("Number of locations to randomly generate: "))

    #Read in the bounds of the plane
    bounds = {}
    with open("./input/" + scene + ".json", "r") as boundfile:
        bounds = json.load(boundfile)
        boundfile.close()
    
    #Create folder to store inputs
    os.makedirs("./input/" + scene)

    #Write many JSON files with random x/y in bounds
    for f in range(num):
        loc = {
            "x" : random.uniform(bounds['xmin'], bounds['xmax']),
            "y" : random.uniform(bounds['ymin'], bounds['ymax'])
        }
        with open("./input/" + scene + "/" + str(f) + ".json", "w") as outfile:
                outfile.write(json.dumps(loc, indent=4))
                outfile.close()

