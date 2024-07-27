import numpy as np

def draw_lines(window, vertices, lines, draw_line_function, screen_w, screen_h):
    for line in lines:
        point_1 = line[0]
        point_2 = line[1]
        color = line[2]
        
        vertex_1 = vertices[point_1]
        vertex_2 = vertices[point_2]

        vertex_1 += np.array([screen_w/2 + (screen_w/2 * vertex_1[0]), screen_h/2])
        vertex_2

        draw_line_function(window, color, vertices[point_1], vertices[point_2])