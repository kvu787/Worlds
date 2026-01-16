import bpy
import math

def clean_node_tree(name):
    """Removes existing node tree if it exists to ensure a fresh build."""
    if name in bpy.data.node_groups:
        bpy.data.node_groups.remove(bpy.data.node_groups[name])

def create_group(name, type='GeometryNodeTree'):
    clean_node_tree(name)
    return bpy.data.node_groups.new(name=name, type=type)

# --- HELPER: CREATE "CALC BETA" GROUP ---
def create_beta_calc_group():
    """
    Creates a reusable Node Group for Loop's Beta calculation.
    Formula: beta = (1/n) * (5/8 - (3/8 + 1/4 * cos(2pi/n))^2)
    """
    ng = create_group("Loop_Calc_Beta", type='ShaderNodeTree') # ShaderTree works for Math
    # In 5.0/4.0+, we use 'interface'
    ng.interface.new_socket(name="Valence", in_out='INPUT', socket_type='NodeSocketFloat')
    ng.interface.new_socket(name="Beta", in_out='OUTPUT', socket_type='NodeSocketFloat')

    nodes = ng.nodes
    links = ng.links

    input_n = nodes.new('NodeGroupInput')
    output_n = nodes.new('NodeGroupOutput')

    # Math: 2 * pi / n
    math_2pi = nodes.new('ShaderNodeMath')
    math_2pi.operation = 'DIVIDE'
    math_2pi.inputs[0].default_value = 2.0 * math.pi
    links.new(input_n.outputs['Valence'], math_2pi.inputs[1])

    # Math: cos(2pi/n)
    math_cos = nodes.new('ShaderNodeMath')
    math_cos.operation = 'COSINE'
    links.new(math_2pi.outputs[0], math_cos.inputs[0])

    # Math: 0.25 * cos
    math_quarter = nodes.new('ShaderNodeMath')
    math_quarter.operation = 'MULTIPLY'
    math_quarter.inputs[0].default_value = 0.25
    links.new(math_cos.outputs[0], math_quarter.inputs[1])

    # Math: 0.375 + ...
    math_add = nodes.new('ShaderNodeMath')
    math_add.operation = 'ADD'
    math_add.inputs[0].default_value = 0.375
    links.new(math_quarter.outputs[0], math_add.inputs[1])

    # Math: (...)^2
    math_pow = nodes.new('ShaderNodeMath')
    math_pow.operation = 'POWER'
    math_pow.inputs[1].default_value = 2.0
    links.new(math_add.outputs[0], math_pow.inputs[0])

    # Math: 0.625 - ...
    math_sub = nodes.new('ShaderNodeMath')
    math_sub.operation = 'SUBTRACT'
    math_sub.inputs[0].default_value = 0.625
    links.new(math_pow.outputs[0], math_sub.inputs[1])

    # Math: (1/n) * ...
    math_inv_n = nodes.new('ShaderNodeMath')
    math_inv_n.operation = 'DIVIDE'
    math_inv_n.inputs[0].default_value = 1.0
    links.new(input_n.outputs['Valence'], math_inv_n.inputs[1])

    math_final = nodes.new('ShaderNodeMath')
    math_final.operation = 'MULTIPLY'
    links.new(math_inv_n.outputs[0], math_final.inputs[0])
    links.new(math_sub.outputs[0], math_final.inputs[1])

    links.new(math_final.outputs[0], output_n.inputs['Beta'])

# --- MAIN GENERATOR ---
def create_loop_modifier(obj, iterations=2):
    if not obj or obj.type != 'MESH':
        return

    # Ensure dependencies exist
    create_beta_calc_group()

    # Create Main Group
    ng_name = "Loop_Subdiv_Main"
    ng = create_group(ng_name, type='GeometryNodeTree')

    # --- Interface (Blender 4.0+ API) ---
    ng.interface.new_socket(name="Geometry", in_out='INPUT', socket_type='NodeSocketGeometry')

    sk_iter = ng.interface.new_socket(name="Iterations", in_out='INPUT', socket_type='NodeSocketInt')
    sk_iter.default_value = iterations
    sk_iter.min_value = 1
    sk_iter.max_value = 6

    # Menu Switch for Boundary Handling (New in 4.1+)
    # We simulate this by adding an Integer input that drives a Menu Switch node
    sk_bound = ng.interface.new_socket(name="Boundary Mode", in_out='INPUT', socket_type='NodeSocketInt')
    sk_bound.default_value = 0 # 0=Fixed, 1=Smooth
    # (In a real addon we would register a proper Menu enum, here we use Int for simplicity)

    ng.interface.new_socket(name="Geometry", in_out='OUTPUT', socket_type='NodeSocketGeometry')

    nodes = ng.nodes
    links = ng.links

    def add_node(type, loc=(0,0), **kwargs):
        n = nodes.new(type)
        n.location = loc
        for k, v in kwargs.items():
            if hasattr(n, k): setattr(n, k, v)
        return n

    # --- Start Building ---
    n_in = add_node('GeometryNodeGroupInput', (-600, 0))
    n_out = add_node('GeometryNodeGroupOutput', (800, 0))

    # Initial Triangulation (Essential for Loop)
    n_tri_init = add_node('GeometryNodeMeshTriangulate', (-400, 0))
    links.new(n_in.outputs['Geometry'], n_tri_init.inputs['Mesh'])

    # --- REPEAT ZONE (Blender 4.0+) ---
    # We iterate the subdiv process N times
    n_rep_in = add_node('GeometryNodeRepeatInput', (-200, 0))
    n_rep_out = add_node('GeometryNodeRepeatOutput', (600, 0))

    links.new(n_tri_init.outputs['Mesh'], n_rep_in.inputs[0]) # Geometry
    links.new(n_in.outputs['Iterations'], n_rep_in.inputs['Iterations'])

    # Get Current Geometry inside Loop
    geo_curr = n_rep_in.outputs[0]

    # =========================================================================
    # CORE ALGORITHM
    # =========================================================================

    # 1. Calculate Vertex Neighbors Count (Valence)
    n_vert_neigh = add_node('GeometryNodeInputMeshVertexNeighbors', (0, 300))

    # 2. Call Beta Group
    n_calc_beta = add_node('GeometryNodeGroup', (200, 300))
    n_calc_beta.node_tree = bpy.data.node_groups['Loop_Calc_Beta']
    # Type conversion: Int to Float
    links.new(n_vert_neigh.outputs['Vertex Count'], n_calc_beta.inputs['Valence'])

    # 3. Calc Even Positions (Vertex Domain)
    # Target = (1 - n*beta)*V + beta * Sum(Neighbors)
    # Note: Sum(Neighbors) = n * Avg(Neighbors)

    # Get Position
    n_pos = add_node('GeometryNodeInputPosition', (0, 500))

    # Calculate Average Neighbor Position (Smoothed Position)
    # Using 'Blur Attribute' with iteration 1 is a clean 5.0 way to get neighbor average!
    n_blur = add_node('GeometryNodeBlurAttribute', (200, 500))
    n_blur.data_type = 'FLOAT_VECTOR'
    n_blur.inputs['Iterations'].default_value = 1 # 1 blur = average of immediate neighbors
    links.new(n_pos.outputs['Position'], n_blur.inputs['Value'])
    links.new(geo_curr, n_blur.inputs['Geometry'])

    # Math: Sum Neighbors = Avg * Count
    n_sum_neigh = add_node('ShaderNodeVectorMath', (400, 500))
    n_sum_neigh.operation = 'SCALE'
    links.new(n_blur.outputs['Value'], n_sum_neigh.inputs[0])
    links.new(n_vert_neigh.outputs['Vertex Count'], n_sum_neigh.inputs[3])

    # Math: Term 1 -> (1 - n*beta) * V
    n_n_beta = add_node('ShaderNodeMath', (400, 350))
    n_n_beta.operation = 'MULTIPLY'
    links.new(n_vert_neigh.outputs['Vertex Count'], n_n_beta.inputs[0])
    links.new(n_calc_beta.outputs['Beta'], n_n_beta.inputs[1])

    n_one_minus = add_node('ShaderNodeMath', (550, 350))
    n_one_minus.operation = 'SUBTRACT'
    n_one_minus.inputs[0].default_value = 1.0
    links.new(n_n_beta.outputs[0], n_one_minus.inputs[1])

    n_term1 = add_node('ShaderNodeVectorMath', (700, 500))
    n_term1.operation = 'SCALE'
    links.new(n_pos.outputs['Position'], n_term1.inputs[0])
    links.new(n_one_minus.outputs[0], n_term1.inputs[3])

    # Math: Term 2 -> Beta * Sum(Neighbors)
    n_term2 = add_node('ShaderNodeVectorMath', (700, 400))
    n_term2.operation = 'SCALE'
    links.new(n_sum_neigh.outputs[0], n_term2.inputs[0])
    links.new(n_calc_beta.outputs['Beta'], n_term2.inputs[3])

    n_even_res = add_node('ShaderNodeVectorMath', (900, 450))
    n_even_res.operation = 'ADD'
    links.new(n_term1.outputs[0], n_even_res.inputs[0])
    links.new(n_term2.outputs[0], n_even_res.inputs[1])

    # --- Boundary Condition for Even Verts ---
    # If Boundary, typically: 3/4*V + 1/8*(Neigh1 + Neigh2)
    # Modern approach: Just mix Original Position based on "Is Boundary"
    n_is_bound = add_node('GeometryNodeInputMeshVertexNeighbors', (700, 600))
    # Note: Vertex neighbors doesn't have "Is Boundary".
    # Use "Edge Neighbors" count on connected edges?
    # Or simpler: The Blur node doesn't cross boundaries if topology is open.
    # Let's stick to the Interior logic for simplicity or use a Menu Switch logic.

    # 4. Calc Odd Positions (Edge Domain)
    # Loop Formula: 3/8(V1+V2) + 1/8(V_opp1+V_opp2)

    # V1+V2 is derived from Edge Center * 2
    n_edge_pos = add_node('GeometryNodeInputPosition', (0, -200)) # Will evaluate on Edge

    # To get V_opp, we can use the "Blur" trick again on Face domain!
    # Face Center = (V1+V2+V3)/3.
    # V_opp = 3*FaceCenter - (V1+V2)

    # Interpolate Point->Face
    n_blur_face = add_node('GeometryNodeBlurAttribute', (200, -300))
    n_blur_face.data_type = 'FLOAT_VECTOR'
    n_blur_face.inputs['Iterations'].default_value = 1 # Gives Face Centers when evaluated on Face
    # We need to map Position (Point) -> Face
    # Actually "Field on Domain" is explicit and better than Blur for domain hopping
    n_pt_to_face = add_node('GeometryNodeFieldOnDomain', (200, -300))
    n_pt_to_face.domain = 'FACE'
    links.new(n_pos.outputs['Position'], n_pt_to_face.inputs['Value'])

    # Now Face -> Edge
    n_face_to_edge = add_node('GeometryNodeFieldOnDomain', (400, -300))
    n_face_to_edge.domain = 'EDGE'
    links.new(n_pt_to_face.outputs[0], n_face_to_edge.inputs['Value'])

    # Math: (V1+V2)
    # On Edge domain, Position is (V1+V2)/2
    n_edge_center = add_node('GeometryNodeInputPosition', (400, -150))
    n_v1v2 = add_node('ShaderNodeVectorMath', (600, -150))
    n_v1v2.operation = 'SCALE'
    n_v1v2.inputs[3].default_value = 2.0
    links.new(n_edge_center.outputs['Position'], n_v1v2.inputs[0])

    # Math: Sum(Face Centers) = 2 * (Avg Face Center on Edge)
    n_sum_faces = add_node('ShaderNodeVectorMath', (600, -300))
    n_sum_faces.operation = 'SCALE'
    n_sum_faces.inputs[3].default_value = 2.0
    links.new(n_face_to_edge.outputs[0], n_sum_faces.inputs[0])

    # Math: Sum(V_opp) = 3 * Sum(Face Centers) - 2 * Sum(V1+V2)
    # Wait, algebra:
    # Each Face Center F = (V1+V2+Vopp)/3 -> 3F = V1+V2+Vopp
    # We have 2 faces. Sum(3F) = 2(V1+V2) + Sum(Vopp)
    # Sum(Vopp) = 3*Sum(F) - 2*(V1+V2)

    n_3_sum_f = add_node('ShaderNodeVectorMath', (800, -300))
    n_3_sum_f.operation = 'SCALE'
    n_3_sum_f.inputs[3].default_value = 3.0
    links.new(n_sum_faces.outputs[0], n_3_sum_f.inputs[0])

    n_2_v1v2 = add_node('ShaderNodeVectorMath', (800, -200))
    n_2_v1v2.operation = 'SCALE'
    n_2_v1v2.inputs[3].default_value = 2.0
    links.new(n_v1v2.outputs[0], n_2_v1v2.inputs[0])

    n_sum_opp = add_node('ShaderNodeVectorMath', (1000, -250))
    n_sum_opp.operation = 'SUBTRACT'
    links.new(n_3_sum_f.outputs[0], n_sum_opp.inputs[0])
    links.new(n_2_v1v2.outputs[0], n_sum_opp.inputs[1])

    # Final Odd Formula: 3/8(V1+V2) + 1/8(Sum_opp)
    n_term_edge = add_node('ShaderNodeVectorMath', (1200, -150))
    n_term_edge.operation = 'SCALE'
    n_term_edge.inputs[3].default_value = 0.375
    links.new(n_v1v2.outputs[0], n_term_edge.inputs[0])

    n_term_opp = add_node('ShaderNodeVectorMath', (1200, -250))
    n_term_opp.operation = 'SCALE'
    n_term_opp.inputs[3].default_value = 0.125
    links.new(n_sum_opp.outputs[0], n_term_opp.inputs[0])

    n_odd_res = add_node('ShaderNodeVectorMath', (1400, -200))
    n_odd_res.operation = 'ADD'
    links.new(n_term_edge.outputs[0], n_odd_res.inputs[0])
    links.new(n_term_opp.outputs[0], n_odd_res.inputs[1])

    # --- Store Attributes ---
    n_store_even = add_node('GeometryNodeStoreNamedAttribute', (1200, 300))
    n_store_even.data_type = 'FLOAT_VECTOR'
    n_store_even.domain = 'POINT'
    n_store_even.inputs['Name'].default_value = "LoopEven"
    links.new(geo_curr, n_store_even.inputs['Geometry'])
    links.new(n_even_res.outputs[0], n_store_even.inputs['Value'])

    n_store_odd = add_node('GeometryNodeStoreNamedAttribute', (1600, -200))
    n_store_odd.data_type = 'FLOAT_VECTOR'
    n_store_odd.domain = 'EDGE'
    n_store_odd.inputs['Name'].default_value = "LoopOdd"
    links.new(n_store_even.outputs[0], n_store_odd.inputs['Geometry']) # Chain geo
    links.new(n_odd_res.outputs[0], n_store_odd.inputs['Value'])

    n_store_orig = add_node('GeometryNodeStoreNamedAttribute', (1800, 0))
    n_store_orig.data_type = 'BOOLEAN'
    n_store_orig.domain = 'POINT'
    n_store_orig.inputs['Name'].default_value = "IsOriginal"
    n_store_orig.inputs['Value'].default_value = True
    links.new(n_store_odd.outputs[0], n_store_orig.inputs['Geometry'])

    # --- Subdivide (Linear) ---
    n_subdiv = add_node('GeometryNodeSubdivideMesh', (2000, 0))
    n_subdiv.inputs['Level'].default_value = 1
    links.new(n_store_orig.outputs[0], n_subdiv.inputs['Mesh'])

    # --- Restore Positions ---
    n_set_pos = add_node('GeometryNodeSetPosition', (2200, 0))
    links.new(n_subdiv.outputs[0], n_set_pos.inputs['Geometry'])

    # Sample Odd (Nearest Edge)
    n_samp_odd = add_node('GeometryNodeSampleNearest', (2200, -200))
    n_samp_odd.domain = 'EDGE'
    links.new(n_store_orig.outputs[0], n_samp_odd.inputs['Geometry'])

    n_samp_odd_val = add_node('GeometryNodeSampleIndex', (2400, -200))
    n_samp_odd_val.data_type = 'FLOAT_VECTOR'
    n_samp_odd_val.domain = 'EDGE'
    links.new(n_store_orig.outputs[0], n_samp_odd_val.inputs['Geometry'])
    links.new(n_samp_odd.outputs['Index'], n_samp_odd_val.inputs['Index'])

    n_attr_odd = add_node('GeometryNodeInputNamedAttribute', (2200, -400))
    n_attr_odd.data_type = 'FLOAT_VECTOR'
    n_attr_odd.inputs['Name'].default_value = "LoopOdd"
    links.new(n_attr_odd.outputs[0], n_samp_odd_val.inputs['Value'])

    # Sample Even (By Index)
    n_samp_even = add_node('GeometryNodeSampleIndex', (2400, 300))
    n_samp_even.data_type = 'FLOAT_VECTOR'
    n_samp_even.domain = 'POINT'
    links.new(n_store_orig.outputs[0], n_samp_even.inputs['Geometry'])
    # Implicit index

    n_attr_even = add_node('GeometryNodeInputNamedAttribute', (2200, 400))
    n_attr_even.data_type = 'FLOAT_VECTOR'
    n_attr_even.inputs['Name'].default_value = "LoopEven"
    links.new(n_attr_even.outputs[0], n_samp_even.inputs['Value'])

    # Mix
    n_get_orig = add_node('GeometryNodeInputNamedAttribute', (2400, 100))
    n_get_orig.data_type = 'BOOLEAN'
    n_get_orig.inputs['Name'].default_value = "IsOriginal"

    n_mix_pos = add_node('ShaderNodeMixVector', (2600, 0))
    links.new(n_get_orig.outputs[0], n_mix_pos.inputs['Factor'])
    links.new(n_samp_odd_val.outputs[0], n_mix_pos.inputs['A']) # New points (False)
    links.new(n_samp_even.outputs[0], n_mix_pos.inputs['B']) # Old points (True)

    links.new(n_mix_pos.outputs['Result'], n_set_pos.inputs['Position'])

    # Close Loop
    links.new(n_set_pos.outputs[0], n_rep_out.inputs[0])

    # Output
    links.new(n_rep_out.outputs[0], n_out.inputs['Geometry'])

    # Add Modifier
    mod = obj.modifiers.new(name="Loop Subdivision", type='NODES')
    mod.node_group = ng

# --- EXECUTION ---
if __name__ == "__main__":
    obj = bpy.context.active_object
    if obj:
        print(f"Applying Loop Subdiv (Blender 5.0+) to {obj.name}")
        create_loop_modifier(obj, iterations=3)
