import bpy

TEMPLATE_OBJECT_NAME = 'K12_Material_Template_Sphere'
MATERIAL_NAME = 'K12_Material'

PROPERTY_NAMES = [
    '1_BaseColor',
    '2_Brightness',
    '3_Shift',
    '4_Rotation',
    '5_DarkPoint',
    '6_LightPoint',
]

def ValidateTemplate():
    templateObject = bpy.data.objects.get(TEMPLATE_OBJECT_NAME)
    if templateObject is None:
        raise RuntimeError(f'Template object with name "{TEMPLATE_OBJECT_NAME}" not found')
    if MATERIAL_NAME not in bpy.data.materials.keys():
        raise RuntimeError(f'Material with name "{MATERIAL_NAME}" not found')
    return templateObject

if __name__ == '__main__':
    templateObject = ValidateTemplate()

    for obj in bpy.context.selected_objects:
        if obj == templateObject:
            continue
        if obj.type == 'MESH':
            obj.data.materials.clear()
            for propertyName in PROPERTY_NAMES:
                if propertyName in obj.keys():
                    del obj[propertyName]
            # Hack to force Blender to update stuff immediately:
            obj.location.x += 0.0
