import bpy

TEMPLATE_OBJECT_NAME = 'K10_Material_Template_Sphere'
MATERIAL_NAME = 'K10_Material'

PROPERTY_NAMES = [
    '1_BaseColor',
    '2_Brightness',
    '3_Shift',
    '4_Rotation',
    '5_DarkPoint',
    '6_LightPoint',
]

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

if __name__ == "__main__":
    if bpy.data.objects.get(TEMPLATE_OBJECT_NAME) is None:
        raise RuntimeError(f'Template object with name "{TEMPLATE_OBJECT_NAME}" not found')
    if MATERIAL_NAME not in bpy.data.materials.keys():
        raise RuntimeError(f'Material with name "{MATERIAL_NAME}" not found')

    src = bpy.context.active_object
    print('Validating active object...')
    validate_object(src)
    print('done')

    template_object = bpy.data.objects.get(TEMPLATE_OBJECT_NAME)

    for dst in bpy.context.selected_objects:
        if dst == template_object or dst == src:
            continue
        if dst.type == 'MESH':
            print(f'Validating selected object "{dst.name}"...')
            validate_object(dst)
            print('done')

    for dst in bpy.context.selected_objects:
        if dst == template_object or dst == src:
            continue
        if dst.type == 'MESH':
            for name in PROPERTY_NAMES:
                dst[name] = src[name]
            # Hack to force Blender to update stuff immediately:
            dst.location.x += 0.0
