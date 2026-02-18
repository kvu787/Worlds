import bpy

if __name__ == "__main__":
    # Get all currently selected objects
    selected_objs = bpy.context.selected_objects

    # Filter the selection to only include meshes
    mesh_objects = [obj for obj in selected_objs if obj.type == 'MESH']

    # Sort the objects by name alphabetically
    mesh_objects.sort(key=lambda obj: obj.name)

    if mesh_objects:
        for obj in mesh_objects:
            print(f"Local coordinates: {obj.name}")

            mesh = obj.data

            for v in mesh.vertices:
                # repr() provides the hardware-level float representation
                print(f"Vertex {v.index}: X={repr(v.co.x)}, Y={repr(v.co.y)}, Z={repr(v.co.z)}")
    else:
        print("No mesh objects found in selection.")
