import bpy

def print_parent_inverse(obj):
    if obj is None:
        print("No object selected.")
        return

    print(f"\n--- Parent Inverse Matrix: {obj.name} ---")
    
    # Access the matrix_parent_inverse property
    inv_matrix = obj.matrix_parent_inverse
    
    # Print the 4x4 matrix row by row for readability
    for row in inv_matrix:
        print(f"[ {row[0]:.4f}, {row[1]:.4f}, {row[2]:.4f}, {row[3]:.4f} ]")
    
    # Check if it's an Identity Matrix (no offset)
    if inv_matrix.is_identity:
        print("Status: Identity Matrix (No offset/correction applied)")
    else:
        print("Status: Offset applied (Object was parented 'In Place')")

# Execute on the currently active object
print_parent_inverse(bpy.context.active_object)
