import bpy

AIO_TEMPLATE_OBJECT_NAME = 'K12_Material_AIO_TemplateSphere'
AIO_MATERIAL_NAME = 'K12_Material_AIO'
CPI_TEMPLATE_OBJECT_NAME = 'K12_Material_CPI_TemplateSphere'
CPI_MATERIAL_NAME = 'K12_Material_CPI'

PROPERTY_NAMES = [
    '1_BaseColor',
    '2_Brightness',
    '3_Shift',
    '4_Rotation',
    '5_DarkPoint',
    '6_LightPoint',
]

def ValidateTemplates():

    templateObjectAio = bpy.data.objects.get(AIO_TEMPLATE_OBJECT_NAME)
    if templateObjectAio is None:
        raise RuntimeError(f'Template object with name "{AIO_TEMPLATE_OBJECT_NAME}" not found')
    if AIO_MATERIAL_NAME not in bpy.data.materials.keys():
        raise RuntimeError(f'Material with name "{AIO_MATERIAL_NAME}" not found')

    templateObjectCpi = bpy.data.objects.get(CPI_TEMPLATE_OBJECT_NAME)
    if templateObjectCpi is None:
        raise RuntimeError(f'Template object with name "{CPI_TEMPLATE_OBJECT_NAME}" not found')
    if CPI_MATERIAL_NAME not in bpy.data.materials.keys():
        raise RuntimeError(f'Material with name "{CPI_MATERIAL_NAME}" not found')

    return (templateObjectAio, templateObjectCpi)

if __name__ == '__main__':
    (templateObjectAio, templateObjectCpi) = ValidateTemplates()
    # for obj in bpy.context.scene.objects:
    for obj in bpy.context.selected_objects:
        if obj == templateObjectAio or obj == templateObjectCpi:
            continue
        if obj.type == 'MESH' or obj.type == 'CURVE' or obj.type == 'SURFACE':
            for material_slot in obj.material_slots:
                for node in material_slot.material.node_tree.nodes:
                    print(node.label)
                    print(node.name)
                    print(node.identifier)
                # mat = slot.material
                # if not mat or not mat.use_nodes:
                #     continue
                # nodes = mat.node_tree.nodes
                # for node in nodes:
                #     # Check node name (or label if you prefer)
                #     print(node.label)
                #     print(node.name)
                #     print(node.identifier)
                #     if node.name == 'K12_Shader':
                #         print(f"Object '{obj.name}' uses material '{mat.name}' with surface '{target_name}'")

    # for obj in bpy.context.selected_objects:
    #     if obj == templateObjectAio or obj == templateObjectCpi:
    #         continue
    #     if obj.type == 'MESH' or obj.type == 'CURVE' or obj.type == 'SURFACE':
    #         obj.data.materials.clear()
    #         for propertyName in PROPERTY_NAMES:
    #             if propertyName in obj.keys():
    #                 del obj[propertyName]
    #         # Append template material
    #         # Copy material
    #         # Set material inputs via default_value
    #         # Hack to force Blender to update stuff immediately:
    #         obj.location.x += 0.0
