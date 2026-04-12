def inspect_stuff():
   print(bpy.context.active_object)
   print(type(bpy.context.active_object.keys()))
   print(list(bpy.context.active_object.keys()))
   print(type(bpy.context.active_object['1_BaseColor']))
   print(list(bpy.context.active_object['1_BaseColor']))
   print(dict(bpy.context.active_object))
   print(bpy.context.active_object)
   print(type(bpy.context.active_object.id_properties_ui('1_BaseColor')))
   print(bpy.context.active_object.id_properties_ui('1_BaseColor').as_dict())
   print(inspect.getmembers(bpy.context.active_object.id_properties_ui('1_BaseColor')))
   print(dir(bpy.context.active_object.id_properties_ui('1_BaseColor')))
   for x in dir(bpy.context.active_object):
       print(x)
   print(type(bpy.context.active_object.id_properties_ui('1_BaseColor')))
   for x in dir(bpy.context.active_object.id_properties_ui('1_BaseColor')):
       print(x)
   print('=====')
   print(bpy.context.active_object.id_properties_ui('1_BaseColor').as_dict())

import bpy
import inspect
print('=======================')
#src = bpy.data.objects.get('K12_Material_Template_Sphere')
#print(src)

#print(dir(bpy.data.objects.get('K12_Material_Template_Sphere').id_properties_ui('1_BaseColor')))
#print(src.keys())
#print(list(src.keys()))
##for name, value in inspect.getmembers(src):
##    print(name, "=", value)
##print(bpy.data.objects.get('Sphere').id_properties_ui('1_BaseColor').as_dict())

src = bpy.data.objects.get('K12_Material_Template_Sphere')
del src['1_BaseColor']
print(list(src.keys()))
print(src.id_properties_ui('1_BaseColor').as_dict())

def validate_object(obj):
    if obj is None:
        raise RuntimeError('Object is None')
    if obj.type != 'MESH':
        raise RuntimeError('Object is not a mesh')
    if not (len(obj.data.materials) == 1 and obj.data.materials[0].name == MATERIAL_NAME):
        raise RuntimeError('Object has incorrect material')
    if len(obj.keys()) != len(PROPERTY_NAMES):
        raise RuntimeError('Object has incorrect number of custom properties')
    for name in PROPERTY_NAMES:
        if name not in obj.keys():
            raise RuntimeError('Object has incorrect custom property names')

import bpy

print('----------------------')
material_name = "Headlights"
material = bpy.data.materials.get(material_name)
#print(material)
#print(material.use_nodes)
#print(material.node_tree.nodes)
#print(material.node_tree.nodes.get("K12_Shader"))
#print(type(material.node_tree.nodes))
#for e in list(material.node_tree.nodes):
#    print(e)
#print(material.node_tree.nodes.keys())
#print(material.node_tree.nodes.values())
for e in material.node_tree.nodes['K12_Shader'].inputs:
    print(f'name = {e.name}')
    print(f'label = {e.label}')
    print(f'identifier = {e.identifier}')
    print(f'default_value = {e.default_value}')
    print()

###########################################################################
# print any objects that share a data
import bpy
from collections import defaultdict

# Group objects by the datablock they use
groups = defaultdict(list)

for obj in bpy.data.objects:
    if obj.data is not None:
        groups[obj.data].append(obj)

# Print only objects that share the same data
print(len(groups))
for data_block, objects in groups.items():
    if len(objects) > 1:
        print(f"Shared data: {data_block.name} ({type(data_block).__name__})")
        for obj in objects:
            print(f"  - {obj.name}")
        print()

#########################################################################
import bpy

PROPERTY_NAMES = [
    '1_BaseColor',
    '2_Brightness',
    '3_Shift',
    '4_Rotation',
    '5_DarkPoint',
    '6_LightPoint',
]

if __name__ == '__main__':
    for obj in bpy.context.scene.objects:
        if not (obj.type == 'MESH' or obj.type == 'CURVE' or obj.type == 'SURFACE'):
            continue
        if len(obj.material_slots) == 0:
            print(obj.name)
#        print(list(obj.material_slots))
        # for material_slot in obj.material_slots:
        #     for node in material_slot.material.node_tree.nodes:
        #         print(node.label)
        #         print(node.name)
        #         print(node.identifier)

