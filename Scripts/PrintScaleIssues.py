import bpy

def check_exact_scales():
    print("=" * 40)
    print("EXACT SCALE CHECK (No Rounding)")
    print("=" * 40)
    
    found_any_not_one = False
    found_any_not_uniform = False

    for obj in bpy.data.objects:
        s = obj.scale
        
        # Exact comparison against 1.0 and against each other
        is_not_one = (s.x != 1.0 or s.y != 1.0 or s.z != 1.0)
        is_not_uniform = (s.x != s.y or s.y != s.z or s.x != s.z)

        if is_not_one or is_not_uniform:
            print(f"Object: {obj.name}")
            print(f"  X: {s.x!r}")
            print(f"  Y: {s.y!r}")
            print(f"  Z: {s.z!r}")

            if is_not_one:
                found_any_not_one = True
                print("NOT 1,1,1")

            if is_not_uniform:
                found_any_not_uniform = True
                print("NON-UNIFORM")

            print("-" * 20)

    if found_any_not_one:
        print("Found non 1,1,1 objects")

    if found_any_not_uniform:
        print("Found non uniform objects")

    if not found_any_not_one and not found_any_not_uniform:
        print("No issues found")

if __name__ == "__main__":
    check_exact_scales()
