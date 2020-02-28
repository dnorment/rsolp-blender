import bpy

#Filepath containing the name of the fSpy file and background
INPUT_PATH = "D:\\CS\\rsolp-blender\\input\\"
#Name of scene
SCENE_NAME = "background502"
#Filepath containing model folders
MODEL_PATH = "D:\\CS\\rsolp-blender\\models\\"
#Name of model
MODEL_NAME = "spam"
#Path of output
OUTPUT_PATH = "D:\\CS\\rsolp-blender\\output\\"


#Set renderer to Cycles Render for shadow catching feature and use GPU as rendering device
bpy.context.scene.render.engine = 'CYCLES'
bpy.context.scene.cycles.device = 'GPU'

#Import fSpy file
def import_fSpy(filename):
    bpy.ops.fspy_blender.import_project(filepath=filename, update_existing_camera=True)
    

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
