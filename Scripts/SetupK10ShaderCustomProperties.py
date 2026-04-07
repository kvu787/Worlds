import bpy
import inspect

SRC_OBJECT_NAME = 'K10_SHADER_TEMPLATE_SPHERE'

PROPERTY_NAMES = [
    '1_BaseColor',
    '2_Brightness',
    '3_Shift',
    '4_Rotation',
    '5_DarkPoint',
    '6_LightPoint',
]

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

if __name__ == "__main__":
    print('======== BEGIN')
    src = bpy.data.objects.get(SRC_OBJECT_NAME)
    dst = bpy.context.active_object

    for name in PROPERTY_NAMES:
        dst[name] = src[name]
        dst.id_properties_ui(name).update_from(src.id_properties_ui(name))
    print('======== END')
