import bpy
import json
import os
import random
import uuid

plane = bpy.data.objects['Plane']
scene_name = bpy.path.basename(bpy.context.blend_data.filepath)[:-6]

#Get info from user and generate JSON files
print("Scene: " + scene_name)
model_name = input("Enter model name: ")
num = int(input("Number of locations to randomly generate: "))

#Create folder to store inputs
try:
    os.makedirs("./input/" + scene_name)
except FileExistsError:
    pass

#Get outer edges of plane
bounds = {                                      
    "xmax" : plane.location.x + plane.scale.x,
    "xmin" : plane.location.x - plane.scale.x,
    "ymax" : plane.location.y + plane.scale.y,
    "ymin" : plane.location.y - plane.scale.y
}
#Write many JSON files with random x/y in bounds
for f in range(num):
    info = {
        "x" : random.uniform(bounds['xmin'], bounds['xmax']),
        "y" : random.uniform(bounds['ymin'], bounds['ymax']),
        "model" : model_name,
        "scene" : scene_name
    }
    with open("./input/" + scene_name + "/" + scene_name + "-" + model_name + "-" + uuid.uuid4().hex + ".json", "w") as outfile:
            outfile.write(json.dumps(info, indent=4))
            outfile.close()