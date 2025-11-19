Notes on workflow:
1. Run the `generate_hfun.py` script to generate an `HFUN.msh` file
2. Run `jigsaw` to produce a `MESH.msh` file
3. Run `convert_jigsaw_msh.py` to produce `SaveVertices` and `SaveTriangles` files from the `MESH.msh` file
4. Run `create_SaveDensity.py` to produce a `SaveDensity` file
5. Run `mkgrid <nPoints> <maxEdges>` to produce `grid.nc` and `graph.info` files
