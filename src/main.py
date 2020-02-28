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

#Import model from path
def import_model(modelpath):
    #import model into scene
    modelobj = modelpath + "\\textured_meshes\\optimized_tsdf_texture_mapped_mesh.obj"
    modelpng = modelpath + "\\textured_meshes\\optimized_tsdf_texture_mapped_mesh.png"
    bpy.ops.import_scene.obj(filepath=modelobj)
    
    #TODO: set texture on model
    
    #resize and remove rotation
    model = bpy.context.selected_objects[0]
    model.scale = (4,4,4)
    model.rotation_euler = (0,0,0)
    
    return model

#Main render process
def main_render(fSpyFile, imgFile, modelFile, orientation, position):
    #import fSpy file
    import_fSpy(fSpyFile)
    
    #set background to image
    set_background(imgFile)
    
    #import model
    model = import_model(modelFile)

main_render(INPUT_PATH + SCENE_NAME + ".fspy", 
            INPUT_PATH + SCENE_NAME + ".png", 
            MODEL_PATH + MODEL_NAME, 
            0, 
            0)
