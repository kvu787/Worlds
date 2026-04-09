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
