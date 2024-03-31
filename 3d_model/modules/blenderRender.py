import bpy
import sys
from mathutils import Matrix
from math import radians

outputDir = "render/"
outputFormat = "png"

def render( outputDir, outputFormat):
    
    # Set the output path
    bpy.context.scene.render.filepath = outputDir + "_front." + outputFormat
    # Render the image
    bpy.ops.render.render(write_still=True)

    
    
    # Retrieve the camera object
    camera = bpy.data.objects["Camera"]
    bpy.ops.object.select_all(action='DESELECT')
    camera.select_set(True)
    bpy.context.view_layer.objects.active = camera
    pivot_point = bpy.context.scene.cursor.location
    camera_vector = camera.location - pivot_point
    rotation_matrix = Matrix.Rotation(radians(180), 4, 'Z')
    rotated_vector = rotation_matrix @ camera_vector
    new_camera_location = pivot_point + rotated_vector
    camera.location = new_camera_location
    camera.rotation_euler.z += 3.14159

    # Set the output path
    bpy.context.scene.render.filepath = outputDir + "_back." + outputFormat
    # Render the image
    bpy.ops.render.render(write_still=True)

    camera = bpy.data.objects["Camera"]
    bpy.ops.object.select_all(action='DESELECT')
    camera.select_set(True)
    bpy.context.view_layer.objects.active = camera
    pivot_point = bpy.context.scene.cursor.location
    camera_vector = camera.location - pivot_point
    rotation_matrix = Matrix.Rotation(radians(180), 4, 'Z')
    rotated_vector = rotation_matrix @ camera_vector
    new_camera_location = pivot_point + rotated_vector
    camera.location = new_camera_location
    camera.rotation_euler.z += 3.14159



#print all available collections
for collection in bpy.data.collections:
    if collection.name != "Collection":
        print(collection.name)
        #hide all collections
        for c in bpy.data.collections:
            if c.name != "Collection":
                c.hide_render = True
        #show the collection to render
        bpy.data.collections[collection.name].hide_render = False
        # Render the collection
        render(outputDir+collection.name, outputFormat)

#combinaison
combination = [["COM_MOD", "DRY_ELECTRODES", "EMG_DAQ_ADS1293"],
               ["COM_MOD", "DRY_ELECTRODES", "EMG_DAQ_ADS1298"],
                ["COM_MOD", "DRY_ELECTRODES", "EMG_INA331"],
                ["COM_MOD", "DRY_ELECTRODES", "FES_AO4882"],
                ["COM_MOD", "DRY_ELECTRODES", "IMU_ICM2094", "EMG_DAQ_ADS1293"],
                ["COM_MOD", "DRY_ELECTRODES", "JACK_CONN", "EMG_DAQ_ADS1293"]]

for i, comb in enumerate(combination):
    for c in bpy.data.collections:
        if c.name != "Collection":
            c.hide_render = True
    for collection in comb:
        bpy.data.collections[collection].hide_render = False
    render(outputDir+"combination_"+str(i), outputFormat)
                

