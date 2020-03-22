import json
import os
import random
import subprocess

ROOT_PATH = "D:/CS/rsolp-blender/"
BLENDER_PATH = "C:/Program Files/Blender Foundation/Blender 2.82/blender.exe"
SCENES_PATH = "D:/CS/rsolp-blender/input/"

scenes = [f[:-6] for f in os.listdir(SCENES_PATH) if f.endswith('.blend')]   #all names of .blend files in scene folder
print(scenes)


for scene in scenes:
    #Save the size of the plane as a JSON file for limiting input locations
    subprocess.run([BLENDER_PATH,
                    "--background",
                    SCENES_PATH + scene + ".blend",
                    "--python",
                    ROOT_PATH + "get_plane_bounds.py"])
