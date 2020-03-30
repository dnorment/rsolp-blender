import json
import os
import random
import subprocess
import uuid

ROOT_PATH = "D:/CS/rsolp-blender/"
BLENDER_PATH = "C:/Program Files/Blender Foundation/Blender 2.82/blender.exe"
SCENES_PATH = "D:/CS/rsolp-blender/input/"

#Get list of all scenes saved as .blend in /input
scenes = [f[:-6] for f in os.listdir(SCENES_PATH) if f.endswith('.blend')]

for scene in scenes:
    #Save the size of the plane as a JSON file for limiting input locations
    subprocess.run([BLENDER_PATH,
                    "--background",
                    SCENES_PATH + scene + ".blend",
                    "--python",
                    ROOT_PATH + "get_plane_bounds.py"])

for scene in scenes:
    #Read in the bounds of the plane
    bounds = {}
    with open("./input/" + scene + ".json", "r") as boundfile:
        bounds = json.load(boundfile)
        boundfile.close()
    
    #
    print("Scene: " + scene)
    model_name = input("Enter model name: ")
    num = int(input("Number of locations to randomly generate: "))

    
    #Create folder to store inputs
    try:
        os.makedirs("./input/" + scene)
    except FileExistsError:
        pass

    #Write many JSON files with random x/y in bounds
    for f in range(num):
        info = {
            "x" : random.uniform(bounds['xmin'], bounds['xmax']),
            "y" : random.uniform(bounds['ymin'], bounds['ymax']),
            "model" : model_name,
            "scene" : scene
        }
        with open("./input/" + scene + "/" + scene + "-" + model_name + "-" + uuid.uuid4().hex + ".json", "w") as outfile:
                outfile.write(json.dumps(info, indent=4))
                outfile.close()

#Render the frames with given input data from each JSON file
for scene in scenes:
    #Get list of input JSON files in scene's input folder
    input_files = []
    for root, dirs, files in os.walk("./input/" + scene):
        for file in files:
            if file.endswith('.json'):
                input_files.append(os.path.abspath(os.path.join(root, file)))

    #Render using info from each JSON
    for jsonfile in input_files:
        #Run the main rendering process script
        subprocess.run([BLENDER_PATH,
                        "--background",
                        SCENES_PATH + scene + ".blend",
                        "--python",
                        ROOT_PATH + "render.py",
                        "--debug-value", jsonfile])