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
    print('-------------------------------')

    for obj in bpy.context.scene.objects:
        if not (obj.type == 'MESH' or obj.type == 'CURVE' or obj.type == 'SURFACE'):
            continue

        shouldClear = False
        for material_slot in obj.material_slots:
            # print(f'material name: {material_slot.material.name}')
            if material_slot.material.name == 'K12_Material':
                shouldClear = True
                break

        if shouldClear:
            obj.data.materials.clear()
            for propertyName in PROPERTY_NAMES:
                if propertyName in obj.keys():
                    del obj[propertyName]
