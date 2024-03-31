import bpy
import os
import json

directory_path = "."  # Update this path


def create_collection(collection_name):
   print(collection_name)
   if collection_name not in bpy.data.collections:
       new_collection = bpy.data.collections.new(collection_name)
       bpy.context.scene.collection.children.link(new_collection)
   else:
       new_collection = bpy.data.collections[collection_name]
   return new_collection

def clear_collection(collection):
   for obj in collection.objects:
       bpy.data.objects.remove(obj, do_unlink=True)

def apply_transformations(obj, function):
   """Apply transformations based on the model's function."""
   if function == "communication":
       # Move along Z-axis by 10mm
       obj.location.z += 0.0082  # Blender uses meters as the unit
       obj.location.y -= 0.003
   elif function == "main":
       # Move along Z-axis by 10mm
       obj.location.z += 0.0055  # Blender uses meters as the unit
   elif function == "addon":
       # Move along Z-axis by 10mm
       obj.location.z += 0.0055  # Blender uses meters as the unit
       obj.location.y -= 0.006
   elif function == "interface":
       # Rotate 90 degrees along Y-axis
       obj.rotation_euler.x -= 1.5708  # 90 degrees in radians
       obj.location.z -= 0.00082
       obj.location.y -= 0.0032

   elif function == "electrode":
       # Rotate 90 degrees along Y-axis
       obj.rotation_euler.x -= 1.5708  # 90 degrees in radians
       obj.rotation_euler.z -= 2*1.5708  # 90 degrees in radians
       obj.location.y -= 0.0032
       obj.location.z -= 0.0004

def combine_objects_in_collection(collection):
   bpy.ops.object.select_all(action='DESELECT')  # Deselect all objects
   for obj in collection.objects:
       obj.select_set(True)  # Select all objects in the collection
       bpy.context.view_layer.objects.active = obj  # Make the last object the active object
   if len(collection.objects) > 0:
       bpy.ops.object.join()  # Join all selected objects into the active object
       print(f"Combined objects in collection '{collection.name}'")

def import_wrl_and_apply_transformations(file_path, collection):
   json_file_path = file_path.replace('.wrl', '.json')
   with open(json_file_path, 'r') as json_file:
       data = json.load(json_file)
   function = data.get("function", "")
   
   bpy.ops.import_scene.x3d(filepath=file_path, filter_glob="*.wrl;*.x3d")
   
   for obj in [obj for obj in bpy.context.selected_objects if obj.type == 'MESH']:
       collection.objects.link(obj)
       bpy.context.collection.objects.unlink(obj)
   if len(collection.objects) > 1:  # Only combine if there are 2 or more objects
       combine_objects_in_collection(collection)
   for obj in [obj for obj in bpy.context.selected_objects if obj.type == 'MESH']:
       apply_transformations(obj, function)
   
   
for file_name in os.listdir(directory_path):
   if file_name.endswith(".wrl"):
       
       print(file_name)
       file_path = os.path.join(directory_path, file_name)
       collection_name = os.path.splitext(file_name)[0]
       new_collection = create_collection(collection_name)
       clear_collection(new_collection)
       import_wrl_and_apply_transformations(file_path, new_collection)
       bpy.ops.object.select_all(action='DESELECT')
