import gmsh
import sys

def create_transfinite_rectangular_mesh():
    gmsh.initialize()
    gmsh.model.add("rectangle_mesh")

    lc = 1.0  # Characteristic length
    
    # Define rectangle corner points
    p1 = gmsh.model.geo.addPoint(0, 0, 0, lc)
    p2 = gmsh.model.geo.addPoint(2, 0, 0, lc)
    p3 = gmsh.model.geo.addPoint(2, 1, 0, lc)
    p4 = gmsh.model.geo.addPoint(0, 1, 0, lc)

    # Define edges
    l1 = gmsh.model.geo.addLine(p1, p2)
    l2 = gmsh.model.geo.addLine(p2, p3)
    l3 = gmsh.model.geo.addLine(p3, p4)
    l4 = gmsh.model.geo.addLine(p4, p1)

    # Define surface
    loop = gmsh.model.geo.addCurveLoop([l1, l2, l3, l4])
    surface = gmsh.model.geo.addPlaneSurface([loop])
    
    # Synchronize
    gmsh.model.geo.synchronize()

    # Apply transfinite meshing
    gmsh.model.mesh.setTransfiniteCurve(l1, 10)
    gmsh.model.mesh.setTransfiniteCurve(l2, 5)
    gmsh.model.mesh.setTransfiniteCurve(l3, 10)
    gmsh.model.mesh.setTransfiniteCurve(l4, 5)
    
    gmsh.model.mesh.setTransfiniteSurface(surface)

    # Recombine to get quadrilateral elements
    gmsh.model.mesh.recombine()
    
    # Define physical entities
    gmsh.model.addPhysicalGroup(1, [l1], 1)
    gmsh.model.addPhysicalGroup(1, [l2], 2)
    gmsh.model.addPhysicalGroup(1, [l3], 3)
    gmsh.model.addPhysicalGroup(1, [l4], 4)
    gmsh.model.addPhysicalGroup(2, [surface], 5)
    
    # Generate mesh
    gmsh.model.mesh.generate(2)
    
    # Save and visualize
    gmsh.write("rectangle_mesh.msh")
    gmsh.fltk.run()

    gmsh.finalize()

if __name__ == "__main__":
    create_transfinite_rectangular_mesh()

