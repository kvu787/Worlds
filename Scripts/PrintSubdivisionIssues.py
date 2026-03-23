import bpy

def check_subd_modifiers():
    for obj in bpy.data.objects:
        subd_modifiers = [m for m in obj.modifiers if type(m) is bpy.types.SubsurfModifier]
        if len(subd_modifiers) > 0:
            # if any(m.levels > 4 for m in subd_modifiers):
            #     print("-----")
            #     print(obj.name)
            # if any(not m.show_only_control_edges for m in subd_modifiers):
            #     print("-----")
            #     print(obj.name)
            for m in subd_modifiers:
                m.show_only_control_edges = True

if __name__ == "__main__":
    print("######### BEGIN")
    check_subd_modifiers()
    print("######### END")
