import bpy
import json
import sys
from pathlib import Path

#Set renderer to Cycles Render for shadow catching feature and use GPU as rendering device
bpy.context.scene.render.engine = 'CYCLES'
bpy.context.scene.cycles.device = 'GPU'

#Setup paths
JSON_PATH = sys.argv[-1]
ROOT_PATH = str(Path(JSON_PATH).parent.parent.parent)
MODEL_PATH = ROOT_PATH + "/models"
OUTPUT_PATH = ROOT_PATH + "/output"

#Import model
def import_model(modelpath):
    #Import model into scene
    modelobj = modelpath + "/textured_meshes/optimized_tsdf_texture_mapped_mesh.obj"
    modelpng = modelpath + "/textured_meshes/optimized_tsdf_texture_mapped_mesh.png"
    bpy.ops.import_scene.obj(filepath=modelobj)
    
    #Resize and remove rotation
    model = bpy.context.selected_objects[0]
    model.scale = (4,4,4)
    model.rotation_euler = (0,0,0)
    
    #Add material to model
    modelTexMat = bpy.data.materials.new(name="ModelTextureMaterial")
    if (model.data.materials):
        model.data.materials[0] = modelTexMat
    else:
        model.data.materials.append(modelTexMat)
    
    #Use nodes to edit material properties
    modelTexMat.use_nodes = True
    
    tree = modelTexMat.node_tree
    nodes, links = tree.nodes, tree.links
    
    #Clear tree before adding all nodes
    nodes.clear()
    
    #Add nodes to tree
    nodeImageTex = nodes.new(type="ShaderNodeTexImage")
    nodeMaterialOutput = nodes.new(type="ShaderNodeOutputMaterial")
    
    #Set node links
    links.new(nodeImageTex.outputs['Color'], nodeMaterialOutput.inputs['Surface'])
    
    #Set image from modelpath to texture
    nodeImageTex.image = bpy.data.images.load(modelpng)
    
    return model

#Set image texture as world background
def set_background(filename):
    #Use nodes to edit world properties
    world = bpy.context.scene.world
    world.use_nodes = True
    
    tree = world.node_tree
    nodes, links = tree.nodes, tree.links
    
    #Clear tree before adding all nodes
    nodes.clear()
    
    #Add nodes to tree
    nodeTexCoords = nodes.new(type="ShaderNodeTexCoord")
    nodeMapping = nodes.new(type="ShaderNodeMapping")
    nodeImageTex = nodes.new(type="ShaderNodeTexImage")
    nodeBackground = nodes.new(type="ShaderNodeBackground")
    nodeWorldOutput = nodes.new(type="ShaderNodeOutputWorld")
    
    #Set node links
    links.new(nodeTexCoords.outputs['Window'], nodeMapping.inputs['Vector'])
    links.new(nodeMapping.outputs['Vector'], nodeImageTex.inputs['Vector'])
    links.new(nodeImageTex.outputs['Color'], nodeBackground.inputs['Color'])
    links.new(nodeBackground.outputs['Background'], nodeWorldOutput.inputs['Surface'])
    
    #Set image from filepath to background
    nodeImageTex.image = bpy.data.images.load(filename)

#Set mask on model
def set_mask(model, index):
    model.pass_index = index

#Set compositor using info from json
def setup_compositor(outputPath):
    #Use nodes to edit render layers
    scene = bpy.data.scenes["Scene"]
    scene.use_nodes = True
    
    tree = scene.node_tree
    nodes, links = tree.nodes, tree.links
    
    #Clear tree before adding all nodes
    nodes.clear()
    
    #Add nodes to tree
    node_layers = nodes.new(type="CompositorNodeRLayers")
    node_alpha_convert = nodes.new(type="CompositorNodePremulKey")
    node_id_mask = nodes.new(type="CompositorNodeIDMask")
    node_id_mask.index = 1
    node_output = nodes.new(type="CompositorNodeOutputFile")
    
    #Edit output location & names
    node_output.base_path = outputPath
    node_output.file_slots.clear()
    node_output.file_slots.new("Image")
    node_output.file_slots.new("Mask")
    
    #Set node links
    links.new(node_layers.outputs['Image'], node_output.inputs['Image'])
    links.new(node_layers.outputs['IndexOB'], node_id_mask.inputs['ID value'])
    links.new(node_id_mask.outputs['Alpha'], node_alpha_convert.inputs['Image'])
    links.new(node_alpha_convert.outputs['Image'], node_output.inputs['Mask'])

#Move model to the given x/y
def move_model(model, x, y):
    pass

if __name__ == "__main__":
    #Load info from JSON file
    loc = {}
    modelname = ""
    scenename = ""
    with open(JSON_PATH) as infofile:
        info = json.load(infofile)
        infofile.close()
        loc = {
            "x" : info["x"],
            "y" : info["y"],
        }
        modelname = info["model"]
        scenename = info["scene"]
    
    #Import model
    model = import_model(MODEL_PATH + "/" + modelname)

    #Move model
    move_model(model, loc["x"], loc["y"])

    #Set background
    set_background(ROOT_PATH + "/input/" + scenename + ".png")

    #Set mask
    set_mask(model, 1)

    #Set compositor
    setup_compositor(OUTPUT_PATH + "/" + scenename)

    #Render
    bpy.ops.render.render(use_viewport=False)