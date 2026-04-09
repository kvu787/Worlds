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

def setup_object(obj):
    src = bpy.data.objects.get(TEMPLATE_OBJECT_NAME)
    dst = obj

    # Setup custom properties
    for name in PROPERTY_NAMES:
        dst[name] = src[name]
        dst.id_properties_ui(name).update_from(src.id_properties_ui(name))

    # Setup material
    dst.data.materials.append(bpy.data.materials[MATERIAL_NAME])

if __name__ == "__main__":
    if bpy.data.objects.get(TEMPLATE_OBJECT_NAME) is None:
        raise RuntimeError(f'Template object with name "{TEMPLATE_OBJECT_NAME}" not found')
    if MATERIAL_NAME not in bpy.data.materials.keys():
        raise RuntimeError(f'Material with name "{MATERIAL_NAME}" not found')

    template_object = bpy.data.objects.get(TEMPLATE_OBJECT_NAME)

    for obj in bpy.context.selected_objects:
        if obj == template_object:
            continue
        if obj.type == 'MESH':
            obj.data.materials.clear()
            setup_object(obj)
            # Hack to force Blender to update stuff immediately:
            obj.location.x += 0.0
