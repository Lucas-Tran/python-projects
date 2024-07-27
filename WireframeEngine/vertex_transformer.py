def transform_vertices(vertices, camera):
    for i in range(len(vertices)):
        vertices[i] -= camera.position
    
    return vertices