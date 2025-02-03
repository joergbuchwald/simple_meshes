from pathlib import Path
import gmsh
import sys

import ogstools as ot

import pyvista as pv

def create_transfinite_hexahedral_mesh(meshname):
    gmsh.initialize()
    gmsh.model.add(meshname)

    lc = 1.0  # Characteristic length
    nx = 60
    ny = 10
    nz = 5
    l = 1
    b = 0.1
    h = 0.04

    # Define cube corner points
    p1 = gmsh.model.geo.addPoint(0, 0, 0, lc)
    p2 = gmsh.model.geo.addPoint(l, 0, 0, lc)
    p3 = gmsh.model.geo.addPoint(l, b, 0, lc)
    p4 = gmsh.model.geo.addPoint(0, b, 0, lc)
    p5 = gmsh.model.geo.addPoint(0, 0, h, lc)
    p6 = gmsh.model.geo.addPoint(l, 0, h, lc)
    p7 = gmsh.model.geo.addPoint(l, b, h, lc)
    p8 = gmsh.model.geo.addPoint(0, b, h, lc)

    # Define cube edges
    lx1 = gmsh.model.geo.addLine(p1, p2)
    ly2 = gmsh.model.geo.addLine(p2, p3)
    lx3 = gmsh.model.geo.addLine(p3, p4)
    ly4 = gmsh.model.geo.addLine(p4, p1)
    lx5 = gmsh.model.geo.addLine(p5, p6)
    ly6 = gmsh.model.geo.addLine(p6, p7)
    lx7 = gmsh.model.geo.addLine(p7, p8)
    ly8 = gmsh.model.geo.addLine(p8, p5)
    lz9 = gmsh.model.geo.addLine(p1, p5)
    lz10 = gmsh.model.geo.addLine(p2, p6)
    lz11 = gmsh.model.geo.addLine(p3, p7)
    lz12 = gmsh.model.geo.addLine(p4, p8)

    # Define cube faces
    f1 = gmsh.model.geo.addCurveLoop([lx1, ly2, lx3, ly4])
    f2 = gmsh.model.geo.addCurveLoop([lx5, ly6, lx7, ly8])
    f3 = gmsh.model.geo.addCurveLoop([lx1, lz10, -lx5, -lz9])
    f4 = gmsh.model.geo.addCurveLoop([ly2, lz11, -ly6, -lz10])
    f5 = gmsh.model.geo.addCurveLoop([lx3, lz12, -lx7, -lz11])
    f6 = gmsh.model.geo.addCurveLoop([ly4, lz9, -ly8, -lz12])

    s1 = gmsh.model.geo.addPlaneSurface([f1])
    s2 = gmsh.model.geo.addPlaneSurface([f2])
    s3 = gmsh.model.geo.addPlaneSurface([f3])
    s4 = gmsh.model.geo.addPlaneSurface([f4])
    s5 = gmsh.model.geo.addPlaneSurface([f5])
    s6 = gmsh.model.geo.addPlaneSurface([f6])

    # Define the volume
    sl = gmsh.model.geo.addSurfaceLoop([s1, s2, s3, s4, s5, s6])
    vol = gmsh.model.geo.addVolume([sl])

    # Synchronize
    gmsh.model.geo.synchronize()

    # Apply transfinite meshing
    gmsh.model.mesh.setTransfiniteCurve(lx1, nx)
    gmsh.model.mesh.setTransfiniteCurve(ly2, ny)
    gmsh.model.mesh.setTransfiniteCurve(lx3, nx)
    gmsh.model.mesh.setTransfiniteCurve(ly4, ny)
    gmsh.model.mesh.setTransfiniteCurve(lx5, nx)
    gmsh.model.mesh.setTransfiniteCurve(ly6, ny)
    gmsh.model.mesh.setTransfiniteCurve(lx7, nx)
    gmsh.model.mesh.setTransfiniteCurve(ly8, ny)
    gmsh.model.mesh.setTransfiniteCurve(lz9, nz)
    gmsh.model.mesh.setTransfiniteCurve(lz10, nz)
    gmsh.model.mesh.setTransfiniteCurve(lz11, nz)
    gmsh.model.mesh.setTransfiniteCurve(lz12, nz)

    gmsh.model.mesh.setTransfiniteSurface(s1)
    gmsh.model.mesh.setTransfiniteSurface(s2)
    gmsh.model.mesh.setTransfiniteSurface(s3)
    gmsh.model.mesh.setTransfiniteSurface(s4)
    gmsh.model.mesh.setTransfiniteSurface(s5)
    gmsh.model.mesh.setTransfiniteSurface(s6)

    gmsh.model.mesh.setRecombine(2, s1)
    gmsh.model.mesh.setRecombine(2, s2)
    gmsh.model.mesh.setRecombine(2, s3)
    gmsh.model.mesh.setRecombine(2, s4)
    gmsh.model.mesh.setRecombine(2, s5)
    gmsh.model.mesh.setRecombine(2, s6)

    gmsh.model.mesh.recombine()


    gmsh.model.mesh.setRecombine(3, vol)

    gmsh.model.mesh.recombine()
    gmsh.model.mesh.setTransfiniteVolume(vol)

    # Recombine to get hexahedral elements
    gmsh.model.mesh.recombine()

    # Define physical entities
    gmsh.model.addPhysicalGroup(2, [s1], 1)
    gmsh.model.setPhysicalName(2, 1, "bottom")
    gmsh.model.addPhysicalGroup(2, [s2], 2)
    gmsh.model.setPhysicalName(2, 2, "top")
    gmsh.model.addPhysicalGroup(2, [s3], 3)
    gmsh.model.setPhysicalName(2, 3, "front")
    gmsh.model.addPhysicalGroup(2, [s4], 4)
    gmsh.model.setPhysicalName(2, 4, "left")
    gmsh.model.addPhysicalGroup(2, [s5], 5)
    gmsh.model.setPhysicalName(2, 5, "back")
    gmsh.model.addPhysicalGroup(2, [s6], 6)
    gmsh.model.setPhysicalName(2, 6, "right")
    gmsh.model.addPhysicalGroup(3, [vol], 7)
    gmsh.model.setPhysicalName(3, 7, "bulk")
    # Generate mesh
    gmsh.model.mesh.generate(3)

    # Save and visualize
    gmsh.write(f"{meshname}.msh")
    #gmsh.fltk.run()

    gmsh.finalize()

if __name__ == "__main__":
    meshname = "beam"
    create_transfinite_hexahedral_mesh(meshname)
    meshes = ot.meshes_from_gmsh(filename=f"{meshname}.msh", dim=3, reindex=True, log=False)
    print(*[f"{name}: {mesh.n_cells=}" for name, mesh in meshes.items()], sep="\n")
    for name, mesh in meshes.items():
        pv.save_meshio(Path(".", name + ".vtu"), mesh)
