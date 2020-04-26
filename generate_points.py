import bmesh
import bpy
import json
import os
import random
import uuid

from bpy_extras.object_utils import world_to_camera_view

#Check if given point is (mostly) inside the field of view of the camera
def check_in_view(x, y, z):
    #Get scene, camera
    scene = bpy.context.scene
    cam = scene.camera

    #Deselect all objects
    bpy.ops.object.select_all(action='DESELECT')

    #Create an icosphere at x,y,z
    bpy.ops.mesh.primitive_ico_sphere_add(location=(x,y,z))

    #Get matrix & world data from object
    obj = bpy.data.objects['Icosphere']
    obj.scale = (0.5, 0.5, 0.5)
    mesh = obj.data
    mat_world = obj.matrix_world
    cs, ce = cam.data.clip_start, cam.data.clip_end

    #Get objects mesh
    bpy.ops.object.mode_set(mode='EDIT')
    bm = bmesh.from_edit_mesh(mesh)

    #Check ratio of vertices inside frustum
    num_vertices = num_inside = 0
    for v in bm.verts:
        num_vertices += 1
        co_ndc = world_to_camera_view(scene, cam, mat_world @ v.co)
        #Check whether point is inside frustum
        if (0.0 < co_ndc.x < 1.0 and
            0.0 < co_ndc.y < 1.0 and
            cs < co_ndc.z <  ce):
            num_inside += 1

    #Return to object mode and delete the icosphere
    bpy.ops.object.mode_set(mode='OBJECT')
    bpy.ops.object.delete()

    #Return true if at least 95% of vertices are inside the camera frustum
    return num_inside / num_vertices > 0.95


if __name__ == "__main__":
    plane = bpy.data.objects['Plane']
    scene_name = bpy.path.basename(bpy.context.blend_data.filepath)[:-6]

    #Get info from user and generate JSON files
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
        #Choose random x,y
        x = random.uniform(bounds['xmin'], bounds['xmax'])
        y = random.uniform(bounds['ymin'], bounds['xmax'])
        #Check if x,y in full view of camera, otherwise regenerate point
        while not check_in_view(x, y, 0):
            x = random.uniform(bounds['xmin'], bounds['xmax'])
            y = random.uniform(bounds['ymin'], bounds['xmax'])

        info = {
            "x" : x,
            "y" : y,
            "model" : model_name,
            "scene" : scene_name
        }
        with open("./input/" + scene_name + "/" + scene_name + "-" + model_name + "-" + uuid.uuid4().hex + ".json", "w") as outfile:
                outfile.write(json.dumps(info, indent=4))
                outfile.close()