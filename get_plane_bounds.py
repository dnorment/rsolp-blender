import bpy
import json
import sys

plane = bpy.data.objects['Plane']

bounds = {                                      #get outer edges of plane as dict
    "xmax" : plane.location.x + plane.scale.x,
    "xmin" : plane.location.x - plane.scale.x,
    "ymax" : plane.location.y + plane.scale.y,
    "ymin" : plane.location.y - plane.scale.y
}
json_obj = json.dumps(bounds, indent=4)         #parse into JSON object

name = sys.argv[2].split("/")[-1][:-6]          #get name of scene from CLargs

with open("./input/" + name + ".json", "w") as outfile:     #write json to input folder
    outfile.write(json_obj)
    outfile.close()
