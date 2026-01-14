import bpy
import bmesh
import math
from mathutils import Vector

# todo: use limit surface positions
# todo: use limit surface tangents/normals
# todo: use lookup table for get_loop_beta if this is too slow
# todo: investigate paper for limiting bounding curvature for extraordinary vertices
#   Triangle Mesh Subdivision with Bounded Curvature and the Convex Hull Property, Charles Loop, 2001
#   https://www.microsoft.com/en-us/research/wp-content/uploads/2016/02/tr-2001-24.pdf

def get_loop_beta(n):
    """
    Calculates the beta weight for a vertex with n neighbors
    based on Charles Loop's original formula.
    """
    # Loop's formula
    val = 3.0/8.0 + (1.0/4.0) * math.cos(2.0 * math.pi / n)
    beta = (1.0 / n) * (5.0/8.0 - val**2)
    return beta

def loop_subdivision(obj, iterations=1):
    """
    Applies Loop Subdivision to the provided object.
    """
    me = obj.data

    # Ensure we are in Object mode to modify mesh data
    bpy.ops.object.mode_set(mode='OBJECT')

    for _ in range(iterations):
        # Create a BMesh from the mesh data
        bm = bmesh.new()
        bm.from_mesh(me)

        # Loop subdivision requires a triangulated mesh
        bmesh.ops.triangulate(bm, faces=bm.faces)

        # Prepare dictionaries to store new coordinates
        # Map: old_vert_index -> new_coordinates (Vector)
        even_verts_coords = {}
        # Map: old_edge_index -> new_coordinates (Vector)
        odd_verts_coords = {}

        # --- STEP 1: Calculate 'Even' Vertices (Update old vertices) ---
        bm.verts.ensure_lookup_table()
        for v in bm.verts:
            if v.is_boundary:
                # Boundary Case:
                # 3/4 * v + 1/8 * (boundary neighbors)
                boundary_neighbors = []
                for e in v.link_edges:
                    if e.is_boundary:
                        boundary_neighbors.append(e.other_vert(v))

                if len(boundary_neighbors) != 2:
                    # Corner case or non-manifold, just keep original
                    even_verts_coords[v.index] = v.co
                else:
                    new_co = 0.75 * v.co + 0.125 * (boundary_neighbors[0].co + boundary_neighbors[1].co)
                    even_verts_coords[v.index] = new_co
            else:
                # Interior Case:
                # (1 - n*beta) * v + beta * sum(neighbors)
                neighbors = [e.other_vert(v) for e in v.link_edges]
                n = len(neighbors)
                beta = get_loop_beta(n)

                sum_neighbors = Vector((0,0,0))
                for neighbor in neighbors:
                    sum_neighbors += neighbor.co

                new_co = (1 - n * beta) * v.co + beta * sum_neighbors
                even_verts_coords[v.index] = new_co

        # --- STEP 2: Calculate 'Odd' Vertices (New edge vertices) ---
        bm.edges.ensure_lookup_table()
        for e in bm.edges:
            v1 = e.verts[0]
            v2 = e.verts[1]

            if e.is_boundary:
                # Boundary Edge: Midpoint
                odd_verts_coords[e.index] = (v1.co + v2.co) * 0.5
            else:
                # Interior Edge: 3/8*(v1+v2) + 1/8*(opposing_v1 + opposing_v2)
                # Find the two faces sharing this edge
                f1 = e.link_faces[0]
                f2 = e.link_faces[1]

                # Find the vertex in the face that is NOT part of the edge
                v_opp1 = [v for v in f1.verts if v not in e.verts][0]
                v_opp2 = [v for v in f2.verts if v not in e.verts][0]

                new_co = (3.0/8.0)*(v1.co + v2.co) + (1.0/8.0)*(v_opp1.co + v_opp2.co)
                odd_verts_coords[e.index] = new_co

        # --- STEP 3: Reconstruct Mesh ---
        # We build a new BMesh to avoid topology pointer issues during splitting
        new_bm = bmesh.new()

        # 3a. Add Updated Old Vertices
        old_idx_to_new_vert = {}
        for old_idx, co in even_verts_coords.items():
            new_v = new_bm.verts.new(co)
            old_idx_to_new_vert[old_idx] = new_v

        # 3b. Add New Edge Vertices
        old_edge_idx_to_new_vert = {}
        for old_idx, co in odd_verts_coords.items():
            new_v = new_bm.verts.new(co)
            old_edge_idx_to_new_vert[old_idx] = new_v

        new_bm.verts.ensure_lookup_table()

        # 3c. Create Faces
        # Each old triangle (v1, v2, v3) splits into 4 new triangles
        for f in bm.faces:
            v1, v2, v3 = f.verts

            # Look up the new "even" vertices
            new_v1 = old_idx_to_new_vert[v1.index]
            new_v2 = old_idx_to_new_vert[v2.index]
            new_v3 = old_idx_to_new_vert[v3.index]

            # Look up the new "odd" vertices (on the edges)
            # We need to find the edge connecting the specific pair of verts
            e1 = bm.edges.get([v1, v2])
            e2 = bm.edges.get([v2, v3])
            e3 = bm.edges.get([v3, v1])

            new_e1 = old_edge_idx_to_new_vert[e1.index]
            new_e2 = old_edge_idx_to_new_vert[e2.index]
            new_e3 = old_edge_idx_to_new_vert[e3.index]

            # Create the 4 new faces
            # Corner 1
            new_bm.faces.new((new_v1, new_e1, new_e3))
            # Corner 2
            new_bm.faces.new((new_e1, new_v2, new_e2))
            # Corner 3
            new_bm.faces.new((new_e2, new_v3, new_e3))
            # Center
            new_bm.faces.new((new_e1, new_e2, new_e3))

        # Write the new bmesh back to the mesh data
        new_bm.to_mesh(me)
        new_bm.free()
        bm.free()

        # Update mesh geometry
        me.update()

# --- Execution ---
active_obj = bpy.context.active_object

ITERATIONS=3

if active_obj and active_obj.type == 'MESH':
    print(f"Applying Loop Subdivision to {active_obj.name}...")
    loop_subdivision(active_obj, ITERATIONS)
    print("Done.")
else:
    print("Please select a mesh object.")
