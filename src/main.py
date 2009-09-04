import pyglet.gl
import pyglet.text
import pyglet.window
import math
import random
import datetime
import pyglet.clock

import scene.objects


class Keys(object):
    """ Stores the state of keys
    """
    keys = []

    @classmethod
    def down(self, symbol, modifiers):
        """ Adds a key to the array, signifying that it is being pressed.
        """
        self.keys.append(symbol)

    @classmethod
    def up(self, symbol, modifiers):
        """ Adds a key to the array, signifying that it is being pressed.
        """
        self.keys.remove(symbol)


class Camera(object):
    rx,ry,rz=0,0,0
    w,h=640,480
    far=8192
    fov=60
    x,y,z=0,0,0
    speed=2000

    def view(self,width,height):
        self.w,self.h=width,height
        pyglet.gl.glViewport(0, 0, width, height)
        pyglet.gl.glMatrixMode(pyglet.gl.GL_PROJECTION)
        pyglet.gl.glLoadIdentity()
        pyglet.gl.gluPerspective(self.fov, float(self.w)/self.h, 0.1, self.far)
        pyglet.gl.glMatrixMode(pyglet.gl.GL_MODELVIEW)

    def drag(self, x, y, dx, dy):
        self.update_r(dx, dy)

    def update_r(self, dx, dy):
        new_rx = self.rx-(dy/4.0)
        new_ry = self.ry+(dx/4.0)

        if new_rx < -30:
            new_rx = -30

        if new_rx > 30:
            new_rx = 30

        self.rx=new_rx
        self.ry=new_ry

    def move(self):
        """ Iterates the key states, applying movement transforms as needed.
        """
        distance = pyglet.clock.tick() * self.speed
        for key in Keys.keys:
            if key is 119: #W - forward
                self.x -= math.sin(math.radians(self.ry)) * distance
                self.z += math.cos(math.radians(self.ry)) * distance
            if key is 115: #S - backward
                self.x += math.sin(math.radians(self.ry)) * distance
                self.z -= math.cos(math.radians(self.ry)) * distance
            if key is 97: #A - strafe left
                self.x += math.cos(math.radians(self.ry)) * distance
                self.z += math.sin(math.radians(self.ry)) * distance
            if key is 100: #D - strafe right
                self.x -= math.cos(math.radians(self.ry)) * distance
                self.z -= math.sin(math.radians(self.ry)) * distance

    def apply(self):
        self.move()
        pyglet.gl.glLoadIdentity()
        pyglet.gl.glRotatef(self.rx,1,0,0)
        pyglet.gl.glRotatef(self.ry,0,1,0)
        pyglet.gl.glRotatef(self.rz,0,0,1)
        pyglet.gl.glTranslatef(self.x, self.y, self.z)


class ControlPanel(object):
    """ Represents the hovering control area
    """


class Desktop(object):
    """ Represents the app - containing pages with content
    """
    def __init__(self):
        """ sets up the the window, starts rendering the browser
        """
        self.camera = Camera()
        self.set_up_window()
        self.camera.window = self.window
        scene.objects.PageManager.add_page("http://www.mightyseek.com/wp-content/plugins/podpress/readme.txt")
        scene.objects.PageManager.add_page("http://wordpress.org/extend/plugins/about/readme.txt")
        scene.objects.PageManager.add_page("http://wordpress.org/extend/plugins/about/readme.txt")
        scene.objects.PageManager.add_page("http://wordpress.org/extend/plugins/about/readme.txt")
        scene.objects.PageManager.add_page("http://wordpress.org/extend/plugins/about/readme.txt")
        scene.objects.PageManager.add_page("http://wordpress.org/extend/plugins/about/readme.txt")
        self.opengl_init()
        self.render()

    def set_up_window(self):
        #self.window = pyglet.window.Window(fullscreen=True, resizable=True)

        #set up window
        self.window = pyglet.window.Window(fullscreen=False, resizable=True)
        self.window.width=1280
        self.window.height=800

        #handlers
        self.window.on_resize=self.camera.view
        self.window.on_mouse_motion=self.camera.drag
        self.window.on_mouse_scroll=self.scroll_page
        self.window.on_mouse_release=self.handle_mouse_up
        self.window.on_mouse_press=self.handle_mouse_down
        self.window.on_key_press=Keys.down
        self.window.on_key_release=Keys.up

        #self.window.push_handlers(pyglet.window.event.WindowEventLogger())

    def opengl_init(self):
        pyglet.gl.glEnable(pyglet.gl.GL_BLEND)
        pyglet.gl.glBlendFunc(pyglet.gl.GL_SRC_ALPHA, pyglet.gl.GL_ONE_MINUS_SRC_ALPHA)
        pyglet.gl.glDepthFunc(pyglet.gl.GL_LEQUAL)
        pyglet.gl.glEnable(pyglet.gl.GL_LINE_SMOOTH)
        pyglet.gl.glHint(pyglet.gl.GL_LINE_SMOOTH_HINT, pyglet.gl.GL_DONT_CARE)

    def render(self):
        while 65307 not in Keys.keys: #escape
            self.window.dispatch_events()
            pyglet.gl.glClear(pyglet.gl.GL_COLOR_BUFFER_BIT | pyglet.gl.GL_DEPTH_BUFFER_BIT)
            self.camera.apply()
            scene.objects.PageManager.draw()
            self.window.flip()

    def scroll_page(self, x, y, dx, dy):
        k = 100
        scene.objects.PageManager.focussed_page.scroll(dy*k)

    def handle_mouse_up(self, x, y, button, modifiers):
        if button == 1:
            x, y = self.map_to_page(x, y)
            line = scene.objects.PageManager.focussed_page.layout.get_line_from_point(x, y)
            char = scene.objects.PageManager.focussed_page.layout.get_position_on_line(line, x)
            scene.objects.PageManager.focussed_page.layout.selection_background_color = (255, 0, 0, 255)
            scene.objects.PageManager.focussed_page.layout.set_selection(char, char+1)

    def handle_mouse_down(self, x, y, button, modifiers):
        if button == 1:
            x, y = self.map_to_page(x, y)
            if x < 900 and x > -900 and y < 1050 and y > -1050:
                scene.objects.PageManager.focussed_page.r=1
                scene.objects.PageManager.focussed_page.g=0

    def map_to_page(self, x, y):
        """ Maps a screen click xy to a page xy
        """
        tx, ty = 0, 0

        #fix origin based on screen size
        tx = x - self.window.width/2
        ty = y - self.window.height/2
        
        #map to height/width ratios
        tx = (tx/(self.window.width/2.)) * 2050
        ty = (ty/(self.window.height/2.)) * 1150
        
        return tx, ty


Desktop()



