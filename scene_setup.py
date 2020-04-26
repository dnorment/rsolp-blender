import bpy

#Name of scene to import
SCENE_NAME = "counter"
#Root path of project files
ROOT_PATH = "D:/CS/rsolp-blender/"
#Filepath containing the name of the fSpy file and background
INPUT_PATH = ROOT_PATH + "input/"

#Set renderer to Cycles Render for shadow catching feature and use GPU as rendering device
bpy.context.scene.render.engine = 'CYCLES'
bpy.context.scene.cycles.device = 'GPU'

#Import fSpy file
def import_fSpy(filename):
    bpy.ops.fspy_blender.import_project(filepath=filename, update_existing_camera=True)

if __name__ == "__main__":
    import_fSpy(INPUT_PATH + SCENE_NAME + ".fspy")
    bpy.ops.mesh.primitive_plane_add()
    bpy.context.object.cycles.is_shadow_catcher = True
    bpy.context.scene.view_layers["View Layer"].use_pass_object_index = True