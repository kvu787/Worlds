import bpy

if __name__ == "__main__":
    print('BEGIN -----------------------------------')
    objects = [obj for obj in bpy.context.selected_objects if obj.type == 'MESH']
    objects.sort(key=lambda obj: obj.name)
    if len(objects) > 0:
        for obj in objects:
            print(f"Name: {obj.name}")
            print(f"Origin: X={repr(obj.location.x)}, Y={repr(obj.location.y)}, Z={repr(obj.location.z)}")
    else:
        print("No mesh objects found in selection")
    print('END -------------------------------------')
