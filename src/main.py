import urllib2
import pyglet.gl
import pyglet.text
import pyglet.window

class Page:
    """ Represents a remotely loaded page
    """

    def __init__(self):
        self.document = pyglet.text.decode_text('No Page Loaded')
        self.document.set_style(0, 50, {'font-size':14, 'color':(0, 255, 0, 255)})
        self.layout = pyglet.text.layout.ScrollableTextLayout(
            self.document,
            2000, 
            1400,
            dpi=200,
            multiline=True)
        self.layout.anchor_x='center' 
        self.layout.anchor_y='center'

    def load_url(self, url):
        """Updates the self.text with the contents of a url
        """
        request = urllib2.Request(url)
        connection = urllib2.urlopen(request)
        data = connection.read()
        connection.close()
        self.layout.document.text = data
 
    def draw(self):

        #draw text background
        pyglet.gl.glPushMatrix()
        pyglet.gl.glTranslatef(0.0, 0.0, -2000)
        pyglet.gl.glColor4f(0, 1.0, 0, 1)
        pyglet.gl.glLineWidth(1.5);
        pyglet.gl.glBegin(pyglet.gl.GL_LINE_STRIP)
        pyglet.gl.glVertex3f(-1050.0, -500.0, 0.0)
        pyglet.gl.glVertex3f(-1050.0, 1000.0, 0.0)
        pyglet.gl.glVertex3f(1100.0, 1000.0, 0.0)
        pyglet.gl.glVertex3f(1100.0, -500.0, 0.0)
        pyglet.gl.glEnd()
        
        #draw text
        pyglet.gl.glTranslatef(0.0, 250, 1)
        self.layout.draw()
        pyglet.gl.glPopMatrix()

    def scroll(self, s):
        self.layout.view_y += s



class Environment:

    def draw(self):
        self.draw_base()

    def draw_base(self):
        pyglet.gl.glPushMatrix()
        pyglet.gl.glLineWidth(5);
        pyglet.gl.glColor4f(0.0, 0.0, 1.0, 0.1)
        pyglet.gl.glBegin(pyglet.gl.GL_LINE_LOOP)
        pyglet.gl.glVertex3f(-2200.0, -500.0, -2200.0)
        pyglet.gl.glVertex3f(-2200.0, -500.0, 2200.0)
        pyglet.gl.glVertex3f(2200.0, -500.0, 2200.0)
        pyglet.gl.glVertex3f(2200.0, -500.0, -2200.0)
        pyglet.gl.glEnd()
        pyglet.gl.glPopMatrix()


class Camera():
    rx,ry,rz=30,-45,0
    w,h=640,480
    far=8192
    fov=60

    def view(self,width,height):
        self.w,self.h=width,height
        pyglet.gl.glViewport(0, 0, width, height)
        pyglet.gl.glMatrixMode(pyglet.gl.GL_PROJECTION)
        pyglet.gl.glLoadIdentity()
        pyglet.gl.gluPerspective(self.fov, float(self.w)/self.h, 0.1, self.far)
        pyglet.gl.glMatrixMode(pyglet.gl.GL_MODELVIEW)

    def drag(self, x, y, dx, dy, button, modifiers):
        if button==1:
            self.ry+=dx/4.
            self.rx-=dy/4.

    def apply(self):
        pyglet.gl.glLoadIdentity()
        pyglet.gl.glRotatef(self.rx,1,0,0)
        pyglet.gl.glRotatef(self.ry,0,1,0)
        pyglet.gl.glRotatef(self.rz,0,0,1)


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
        self.window = pyglet.window.Window(fullscreen=False, resizable=True)
        self.window.on_resize=self.camera.view
        self.window.on_mouse_drag=self.camera.drag
        self.window.on_mouse_scroll=self.scroll_page
        self.window.width=1280
        self.window.height=800
        #self.window.push_handlers(pyglet.window.event.WindowEventLogger())

    def opengl_init(self):
        pyglet.gl.glEnable(pyglet.gl.GL_BLEND)
        pyglet.gl.glBlendFunc(pyglet.gl.GL_SRC_ALPHA, pyglet.gl.GL_ONE_MINUS_SRC_ALPHA)
        pyglet.gl.glDepthFunc(pyglet.gl.GL_LEQUAL)
        pyglet.gl.glEnable(pyglet.gl.GL_LINE_SMOOTH)
        pyglet.gl.glHint(pyglet.gl.GL_LINE_SMOOTH_HINT, pyglet.gl.GL_DONT_CARE)

    def render(self):
        while not self.window.has_exit:
            self.window.dispatch_events()
            pyglet.gl.glClear(pyglet.gl.GL_COLOR_BUFFER_BIT | pyglet.gl.GL_DEPTH_BUFFER_BIT)
            self.camera.apply()
            self.environment.draw()
            self.page.draw()
            self.window.flip()

    def add_page(self, url):
        self.page = Page()
        self.page.load_url(url)

    def draw_pages(self):
        self.page.draw()
        
    def scroll_page(self, x, y, dx, dy):
        k = 100
        self.page.scroll(dy*k)

Browser()



