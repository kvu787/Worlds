import bpy

ValidZHeights = [
    0.0,
    0.00390625,
    0.0078125,
    0.01171875,
    0.015625,
    0.01953125,
    0.0234375,
    0.02734375,
    0.03125,
    0.03515625,
]

if __name__ == "__main__":
    print("BEGIN -----------------------------------")
    objects = [obj for obj in bpy.context.selected_objects if obj.type == "MESH"]
    objects.sort(key=lambda obj: obj.name)
    if len(objects) > 0:
        for obj in objects:
            if obj.location.z not in ValidZHeights:
                print(f"Name: {obj.name}")
                print("Origin ERROR")
                print(f"Origin: z={repr(obj.location.z)}")
            for vertex in obj.data.vertices:
                if vertex.co.z != 0.0:
                    print(f"Name: {obj.name}")
                    print("Vertex ERROR")
                    print(f"Vertex {vertex.index}: x={repr(vertex.co.x)}, y={repr(vertex.co.y)}, z={repr(vertex.co.z)}")
    else:
        print("No mesh objects found in selection")
    print("END -------------------------------------")
