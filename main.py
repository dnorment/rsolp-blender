import os
import subprocess

ROOT_PATH = "D:/CS/rsolp-blender/"
BLENDER_PATH = "C:/Program Files/Blender Foundation/Blender 2.82/blender.exe"
SCENES_PATH = ROOT_PATH + "input/"

#Get list of all scenes saved as .blend in /input
scenes = [f[:-6] for f in os.listdir(SCENES_PATH) if f.endswith('.blend')]

for scene in scenes:
    #Open the scene and ask user to generate inputs
    print("Scene: " + scene)
    subprocess.run([BLENDER_PATH,
                    "--background",
                    SCENES_PATH + scene + ".blend",
                    "--python",
                    ROOT_PATH + "generate_points.py"],
                    stdout=subprocess.DEVNULL)

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
        print("Rendering from JSON: " + jsonfile)
        subprocess.run([BLENDER_PATH,
                        "--background",
                        SCENES_PATH + scene + ".blend",
                        "--python",
                        ROOT_PATH + "render.py",
                        "--debug-value", jsonfile],
                        stdout=subprocess.DEVNULL)