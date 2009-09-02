from pyglet import window,image
from pyglet.window import key
from pyglet.gl import *

import urllib2
import pyglet.text

class Page:
    """Represents a page loaded remotely.
    """

    def __init__(self):
        self.page = pyglet.text.Label('',
                                      font_size=8,
                                      width=200, 
                                      height=300,
                                      multiline=True, 
                                      color=(255, 255, 255, 255),
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
        pyglet.gl.glColor4f(1.0, 1.0, 1.0, 0.5)
        pyglet.gl.glBegin(pyglet.gl.GL_QUADS)
        pyglet.gl.glVertex3f(-120.0, 170.0, 0.0)
        pyglet.gl.glVertex3f(120.0, 170.0, 0.0)
        pyglet.gl.glVertex3f(120.0, -150.0, 0.0)
        pyglet.gl.glVertex3f(-120.0, -150.0, 0.0)
        pyglet.gl.glEnd()
        
        #draw text
        pyglet.gl.glTranslatef(0.0, 0.0, 1)
        self.page.draw()

        pyglet.gl.glPopMatrix()

def pages_init():
    page1.load_url("http://www.mightyseek.com/wp-content/plugins/podpress/readme.txt")

def opengl_init():
    glEnable(GL_BLEND)
    glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
    glDepthFunc(GL_LEQUAL)

def draw_pages():
    page1.draw()

def draw_base():
    pyglet.gl.glPushMatrix()
    pyglet.gl.glColor4f(0.0, 0.0, 1.0, 0.5)
    pyglet.gl.glBegin(pyglet.gl.GL_QUADS)
    pyglet.gl.glVertex3f(-550.0, -150.0, 550.0)
    pyglet.gl.glVertex3f(550.0, -150.0, 550.0)
    pyglet.gl.glVertex3f(550.0, -150.0, -550.0)
    pyglet.gl.glVertex3f(-550.0, -150.0, -550.0)
    pyglet.gl.glEnd()
    pyglet.gl.glPopMatrix()

class camera():
    x,y,z=0,0,0
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
        glTranslatef(-self.x,-self.y,-self.z)

page1 = Page()
cam=camera()
win = window.Window(resizable=True)
win.on_resize=cam.view
win.on_mouse_drag=cam.drag
opengl_init()
pages_init()

while not win.has_exit:
    win.dispatch_events()
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    cam.apply()
    draw_pages()
    draw_base()
    win.flip() 