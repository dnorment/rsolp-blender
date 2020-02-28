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
    #Import model into scene
    modelobj = modelpath + "\\textured_meshes\\optimized_tsdf_texture_mapped_mesh.obj"
    modelpng = modelpath + "\\textured_meshes\\optimized_tsdf_texture_mapped_mesh.png"
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

#Sets object ID 1 to the model for masking
def set_mask(model):
    model.pass_index = 1

#Setup compositor for output and masks
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
    node_output.base_path = outputPath + "\\"
    node_output.file_slots.clear()
    node_output.file_slots.new("Image")
    node_output.file_slots.new("Mask")
    
    #Set node links
    links.new(node_layers.outputs['Image'], node_output.inputs['Image'])
    links.new(node_layers.outputs['IndexOB'], node_id_mask.inputs['ID value'])
    links.new(node_id_mask.outputs['Alpha'], node_alpha_convert.inputs['Image'])
    links.new(node_alpha_convert.outputs['Image'], node_output.inputs['Mask'])

#Main render process
def main_render(fSpyFile, imgFile, modelFile, outputPath, orientation, position):
    #Import fSpy file
    import_fSpy(fSpyFile)
    
    #Set background to image
    set_background(imgFile)
    
    #Import model
    model = import_model(modelFile)
    
    #Set mask on model
    set_mask(model)
    
    #Setup compositor for mask image
    setup_compositor(outputPath)
    

main_render(INPUT_PATH + SCENE_NAME + ".fspy", 
            INPUT_PATH + SCENE_NAME + ".png", 
            MODEL_PATH + MODEL_NAME, 
            OUTPUT_PATH, 
            0, 
            0)
