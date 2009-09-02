import pyglet
import pyglet.window
import pyglet.graphics
import pyglet.sprite
import pyglet.gl
import pyglet.font


class Page:
    """Represents a page loaded remotely.
    """

    def __init__(self, text):
        self.text = text
        self.label = pyglet.text.Label(self.text, 
                                  font_name='Times New Roman', 
                                  font_size=10,
                                  anchor_x='center', anchor_y='center')
        arial = pyglet.font.load('Arial', 11, bold=False, italic=False)
        self.page = pyglet.font.Text(arial, 
                                     text='aslkdjalsd', 
                                     valign=pyglet.font.Text.CENTER, 
                                     halign=pyglet.font.Text.CENTER)
        #import pdb; pdb.set_trace()

    def draw(self):
#        self.page.draw()
        self.label.draw()

        
#setup
window = pyglet.window.Window()
site1 = Page("baaaaa")

pyglet.gl.glShadeModel(pyglet.gl.GL_SMOOTH)
pyglet.gl.glClearColor(0.0, 0.0, 0.0,0.0)
pyglet.gl.glClearDepth(1.0)
pyglet.gl.glEnable(pyglet.gl.GL_DEPTH_TEST)
pyglet.gl.glDepthFunc(pyglet.gl.GL_LEQUAL)
pyglet.gl.glHint(pyglet.gl.GL_PERSPECTIVE_CORRECTION_HINT,pyglet.gl.GL_NICEST)     

@window.event
def on_draw():
    window.clear()
    pyglet.gl.glLoadIdentity()
    
    #fix origin - this has to be easier...
    pyglet.gl.glTranslatef(window.width//2, window.height//2, 0.0)
    
    pyglet.gl.glPushMatrix()
    pyglet.gl.glTranslatef(0.0, 0.0, 1)
    site1.draw()
    pyglet.gl.glPopMatrix()

    pyglet.gl.glPushMatrix()    
    pyglet.gl.glRotatef(1, 0.0, 1.0, 0.0)
    pyglet.gl.glColor3f(0.5,0.5,1.0)
    pyglet.gl.glBegin(pyglet.gl.GL_QUADS)
    pyglet.gl.glVertex3f(-100.0, 100.0, 0.0)
    pyglet.gl.glVertex3f(100.0, 100.0, 0.0)
    pyglet.gl.glVertex3f(100.0, -100.0, 0.0)
    pyglet.gl.glVertex3f(-100.0, -100.0, 0.0)
    pyglet.gl.glEnd()
    pyglet.gl.glPopMatrix()
    
    pyglet.gl.glPushMatrix()    
    pyglet.gl.glColor3f(1.0,0.5,0.5)
    pyglet.gl.glBegin(pyglet.gl.GL_QUADS)
    pyglet.gl.glVertex3f(-50.0, 50.0, -0.1)
    pyglet.gl.glVertex3f(50.0, 50.0, 0.1)
    pyglet.gl.glVertex3f(50.0, -50.0, -0.1)
    pyglet.gl.glVertex3f(-50.0, -50.0, 0.1)
    pyglet.gl.glEnd()
    pyglet.gl.glPopMatrix()    
    
    
    
 
@window.event
def on_mouse_press(x, y, button, modifiers):
    pass
    
pyglet.app.run()
