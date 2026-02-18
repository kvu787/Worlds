'''
Subdivision level != 3
Non uniform scale
Non (1,1,1) scale
Non default transform delta
Non identity parent inverse matrix
Unapplied modifiers other than catmull clark subd
any modifier stack other than a single unapplied cc subd modifier
Objects or collections that are hidden or unselectable
Object hierarchies that are not in the same collection
Negative scales
'''

def main():
    if len(bpy.data.scenes) != 1:
        print("Number of scenes is not 1")
    for obj in bpy.data.objects:
        
def check_modifiers(obj):
    if len(obj.modifiers) > 1:
        print("has greater than 1 modifier")
    if len(obj.modifiers) == 1:
        modifier = obj.modifiers[0]
        if type(modifier) is not bpy.types.SubsurfModifier:
            print("has modifier that isn't subsurf")
        if modifier.level != 3:
            print("subd level != 3")

# print(type(bpy.data.objects["flame.002"].modifiers[1]) is bpy.types.SubsurfModifier)
if __name__ == "__main__":
    main()