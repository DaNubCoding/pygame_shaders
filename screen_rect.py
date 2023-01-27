import numpy as np
import moderngl

class ScreenRect:
    def __init__(self, rect, win_size, ctx, program):
        size = rect[2] / win_size[0] * 2, rect[3] / win_size[1] * 2
        pos = rect[0] / win_size[0] * 2 - 1, -rect[1] / win_size[1] * 2 + 1

        self.vertices = [
            (pos[0], pos[1] - size[1]),
            (pos[0] + size[0], pos[1] - size[1]),
            (pos[0], pos[1]),

            (pos[0], pos[1]),
            (pos[0] + size[0], pos[1] - size[1]),
            (pos[0] + size[0], pos[1]),
        ]
        self.tex_coords = [
           (0.0, 0.0),
           (1.0, 0.0),
           (0.0, 1.0),

           (0.0, 1.0),
           (1.0, 0.0),
           (1.0, 1.0),
        ]

        self.vertices = np.array(self.vertices, dtype=np.float32)
        self.tex_coords = np.array(self.tex_coords, dtype=np.float32)
        self.data = np.hstack([self.vertices, self.tex_coords])

        self.vbo = ctx.buffer(self.data)

        try:
            self.vao = ctx.vertex_array(program, [
                (self.vbo, '2f 2f', 'vertexPos', 'vertexTexCoord'),
            ])
        except moderngl.error.Error:
            self.vbo = ctx.buffer(self.vertices)
            self.vao = ctx.vertex_array(program, [
                (self.vbo, '2f', 'vertexPos'),
            ])

        self.program = program