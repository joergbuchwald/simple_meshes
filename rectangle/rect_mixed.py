import gmsh
import sys

# Initialize gmsh
gmsh.initialize(sys.argv)

# Create a new model
model_name = "square_mixed_mesh"
gmsh.model.add(model_name)

# Define points for a 1x1 square (at z=0)
p1 = gmsh.model.occ.addPoint(0, 0, 0)  # Bottom-left
p2 = gmsh.model.occ.addPoint(1, 0, 0)  # Bottom-right
p3 = gmsh.model.occ.addPoint(1, 1, 0)  # Top-right
p4 = gmsh.model.occ.addPoint(0, 1, 0)  # Top-left
p5 = gmsh.model.occ.addPoint(0.5, 0, 0)  # Middle point at bottom
p6 = gmsh.model.occ.addPoint(0.5, 1, 0)  # Middle point at top

# Create lines for boundary and dividing line
l1 = gmsh.model.occ.addLine(p1, p5)  # Bottom edge (left half)
l2 = gmsh.model.occ.addLine(p5, p2)  # Bottom edge (right half)
l3 = gmsh.model.occ.addLine(p2, p3)  # Right edge
l4 = gmsh.model.occ.addLine(p3, p6)  # Top edge (right half)
l5 = gmsh.model.occ.addLine(p6, p4)  # Top edge (left half)
l6 = gmsh.model.occ.addLine(p4, p1)  # Left edge
l7 = gmsh.model.occ.addLine(p5, p6)  # Middle vertical line

# Create two curve loops - one for each half
curve_loop_left = gmsh.model.occ.addCurveLoop([l1, l7, l5, l6])
curve_loop_right = gmsh.model.occ.addCurveLoop([l2, l3, l4, -l7])  # Note the negative sign for l7 to match direction

# Create surfaces
surface_left = gmsh.model.occ.addPlaneSurface([curve_loop_left])   # Will be quad elements
surface_right = gmsh.model.occ.addPlaneSurface([curve_loop_right])  # Will be triangle elements

# Synchronize the model
gmsh.model.occ.synchronize()

# Create physical groups for different element types
gmsh.model.addPhysicalGroup(2, [surface_left], name="QuadRegion")
gmsh.model.addPhysicalGroup(2, [surface_right], name="TriangleRegion")

# Set element size
element_size = 0.1
gmsh.model.mesh.setSize([(0, p1), (0, p2), (0, p3), (0, p4), (0, p5), (0, p6)], element_size)

# Mesh settings for left half - quad elements
gmsh.model.mesh.setAlgorithm(2, surface_left, 8)  # Delaunay algorithm
gmsh.model.mesh.setRecombine(2, surface_left)     # Recombine triangles into quads

# Mesh settings for right half - triangle elements
gmsh.model.mesh.setAlgorithm(2, surface_right, 1)  # MeshAdapt algorithm for triangles

# Generate the mesh
gmsh.model.mesh.generate(2)  # 2D mesh

# Optional: Write mesh to file
gmsh.write("square_mixed_mesh.msh")

# Optionally display the mesh (can be commented out for headless operation)
if '-nopopup' not in sys.argv:
    gmsh.fltk.run()

# Clean up
gmsh.finalize()

print("Mixed mesh generation completed. Mesh saved to 'square_mixed_mesh.msh'")
