import pygame_shaders.texture as texture
import pygame_shaders.screen_rect as screen_rect
import pygame_shaders.shader_utils as shader_utils

import moderngl
import pygame

ctx = None

def clear(color):
    ctx.clear(color=(color[0]/255, color[1]/255, color[2]/255))

class Shader:
    def __init__(self, rect, display, vertex_path, fragment_path, target_texture=None):
        global ctx
        if ctx is None:
            ctx = moderngl.create_context()

        self.ctx = ctx
        ctx.enable(moderngl.BLEND)
        ctx.blend_func = ctx.SRC_ALPHA, ctx.ONE_MINUS_SRC_ALPHA
        
        self.display = display
        self.shader_data = {}
        if target_texture is not None:
            self.shader_data["u_texSize"] = [float(target_texture.get_width()), float(target_texture.get_height())]
        self.shader = shader_utils.create_shader(vertex_path, fragment_path, self.ctx)
        self.render_rect = screen_rect.ScreenRect(rect, display, self.ctx, self.shader)
        self.tex_id = 1

        if target_texture is not None:
            s = pygame.Surface(target_texture.get_size())
            self.screen_texture = texture.Texture(s, self.ctx)
        
    def send(self, name, data):
        if name in self.shader_data:
            if not isinstance(data[0], pygame.Surface) and [float(x) for x in data] == self.shader_data[name]:
                return
        if isinstance(data[0], pygame.Surface):
            texture.Texture(data[0], self.ctx).use(self.tex_id)
            self.shader_data[name] = [self.tex_id]
            self.tex_id += 1
            return
        self.shader_data[name] = [float(x) for x in data]

    def render(self, surface=None):
        if surface is not None:
            self.screen_texture.update(surface)
            self.screen_texture.use(0)

        for key in self.shader_data.keys():
            data = self.shader_data[key]
            if len(data) == 1:
                self.shader[key].value = data[0]

            elif len(data) == 2:
                try:
                    self.shader[key].value = (data[0], data[1])
                except KeyError:
                    pass

        self.render_rect.vao.render()

    def update_rect(self, rect):
        self.render_rect = screen_rect.ScreenRect(rect, self.display, self.ctx, self.shader)