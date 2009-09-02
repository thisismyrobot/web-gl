from pyglet import window,image
from pyglet.window import key
from pyglet.gl import *

import urllib2
import pyglet.text


class Page:
    """ Represents a remotely loaded page
    """

    def __init__(self):
        self.page = pyglet.text.Label('',
                                      font_size=8,
                                      width=400, 
                                      height=300,
                                      multiline=True, 
                                      color=(0, 255, 0, 255),
                                      anchor_x='center', 
                                      anchor_y='center')

    def load_url(self, url):
        """Updates the self.text with the contents of a url
        """
        request = urllib2.Request(url)
        connection = urllib2.urlopen(request)
        data = connection.read()
        connection.close()
        self.page.text = data

    def draw(self):

        #draw text background
        pyglet.gl.glPushMatrix()
        pyglet.gl.glTranslatef(0.0, 0.0, -500)
        pyglet.gl.glColor4f(0, 1.0, 0, 1)
        pyglet.gl.glBegin(pyglet.gl.GL_LINE_STRIP)
        pyglet.gl.glVertex3f(-220.0, -170.0, 0.0)
        pyglet.gl.glVertex3f(-220.0, 170.0, 0.0)
        pyglet.gl.glVertex3f(220.0, 170.0, 0.0)
        pyglet.gl.glVertex3f(220.0, -170.0, 0.0)
        pyglet.gl.glEnd()
        
        #draw text
        pyglet.gl.glTranslatef(0.0, 0.0, 1)
        self.page.draw()
        pyglet.gl.glPopMatrix()


class Environment:

    def draw(self):
        self.draw_base()

    def draw_base(self):
        pyglet.gl.glPushMatrix()
        pyglet.gl.glColor4f(0.0, 0.0, 1.0, 0.1)
        pyglet.gl.glBegin(pyglet.gl.GL_QUADS)
        pyglet.gl.glVertex3f(-550.0, -170.0, 550.0)
        pyglet.gl.glVertex3f(550.0, -170.0, 550.0)
        pyglet.gl.glVertex3f(550.0, -170.0, -550.0)
        pyglet.gl.glVertex3f(-550.0, -170.0, -550.0)
        pyglet.gl.glEnd()
        pyglet.gl.glPopMatrix()


class Camera():
    rx,ry,rz=30,-45,0
    w,h=640,480
    far=8192
    fov=60

    def view(self,width,height):
        self.w,self.h=width,height
        glViewport(0, 0, width, height)
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        gluPerspective(self.fov, float(self.w)/self.h, 0.1, self.far)
        glMatrixMode(GL_MODELVIEW)

    def drag(self, x, y, dx, dy, button, modifiers):
        if button==4:
            self.ry+=dx/4.
            self.rx-=dy/4.

    def apply(self):
        glLoadIdentity()
        glRotatef(self.rx,1,0,0)
        glRotatef(self.ry,0,1,0)
        glRotatef(self.rz,0,0,1)


class Browser:
    """ Represents the application's main window - the browser.
    """
    
    def __init__(self):
        """ sets up the the window, starts rendering the browser
        """
        
        self.camera = Camera()
        self.set_up_window()
        self.environment = Environment()
        self.page = Page()
        self.page.load_url("http://www.mightyseek.com/wp-content/plugins/podpress/readme.txt")
        
        self.opengl_init()
        self.render()

    def set_up_window(self):
        self.window = window.Window(resizable=True, fullscreen=True)
        self.window.on_resize=self.camera.view
        self.window.on_mouse_drag=self.camera.drag
        
    def opengl_init(self):
        glEnable(GL_BLEND)
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
        glDepthFunc(GL_LEQUAL)

    def render(self):
        while not self.window.has_exit:
            self.window.dispatch_events()
            glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
            self.camera.apply()
            self.environment.draw()
            self.page.draw()
            self.window.flip()

    def add_page(self, url):
        self.page = Page()
        self.page.load_url(url)

    def draw_pages(self):
        self.page.draw()

        
Browser()


