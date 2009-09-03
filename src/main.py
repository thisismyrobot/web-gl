import urllib2
import pyglet.gl
import pyglet.text
import pyglet.window
import math


class Page(object):
    """ Represents a remotely loaded page
    """
    
    page_width = 1600 #visible text area width
    page_height = 2000 #visible text area height
    page_distance = 2000 #from user
    page_border = 50 #spacing around text
    page_font_size = 14
    
    page_alpha_focussed = 1.0
    page_alpha_unfocussed = 0.25

    page_alpha = page_alpha_unfocussed
    
    def __init__(self):
        self.document = pyglet.text.decode_text('No Page Loaded')
        self.update_document_style()
        self.layout = pyglet.text.layout.IncrementalTextLayout(
            self.document,
            self.page_width, 
            self.page_height,
            dpi=200,
            multiline=True)
        self.layout.anchor_x='center' 
        self.layout.anchor_y='center'
    
    def set_focussed(self, focussed):
        if focussed is True:
            self.page_alpha = self.page_alpha_focussed
        else:
            self.page_alpha = self.page_alpha_unfocussed
        self.update_document_style()

    def update_document_style(self):
        style = {'font-size':self.page_font_size, 'color':(0, 255, 0, int(self.page_alpha*255))}
        self.document.set_style(0, 50, style)
            
    def load_url(self, url):
        """Updates the self.text with the contents of a url
        """
        request = urllib2.Request(url)
        connection = urllib2.urlopen(request)
        data = connection.read()
        connection.close()
        self.layout.document.text = data
 
    def draw_background(self):
        """ draw text background
        """
        pyglet.gl.glTranslatef(0.0, 0.0, -self.page_distance)
        pyglet.gl.glColor4f(0, 1.0, 0, self.page_alpha)
        pyglet.gl.glLineWidth(1.5);
        pyglet.gl.glBegin(pyglet.gl.GL_LINE_LOOP)
        pyglet.gl.glVertex3f((-self.page_width/2)-self.page_border, (-self.page_height/2)-self.page_border, 0.0)
        pyglet.gl.glVertex3f((-self.page_width/2)-self.page_border, (self.page_height/2)+self.page_border, 0.0)
        pyglet.gl.glVertex3f((self.page_width/2)+self.page_border, (self.page_height/2)+self.page_border, 0.0)
        pyglet.gl.glVertex3f((self.page_width/2)+self.page_border, (-self.page_height/2)-self.page_border, 0.0)
        pyglet.gl.glEnd()

    def draw_text(self):
        """ draw text
        """
        pyglet.gl.glPushMatrix()
        pyglet.gl.glTranslatef(0.0, 0.0, 1.0)
        self.layout.draw()
        pyglet.gl.glPopMatrix()

    def draw_slider(self):
        """ draw slider position
        """
        pyglet.gl.glTranslatef((self.page_width/2)+self.page_border, (self.page_height/2)+self.page_border, 0.0)
        scroll_pos = (float(self.layout.view_y) / float(self.layout.content_height - self.page_height)) * (self.page_height + self.page_border * 2)
        pyglet.gl.glTranslatef(0.0, scroll_pos, 0.0)
        pyglet.gl.glLineWidth(1.5)
        pyglet.gl.glColor4f(0, 1.0, 0, self.page_alpha)
        pyglet.gl.glBegin(pyglet.gl.GL_LINE_LOOP)
        pyglet.gl.glVertex3f(-10.0, -10.0, 0.0)
        pyglet.gl.glVertex3f(-10.0, 10.0, 0.0)
        pyglet.gl.glVertex3f(10.0, 10.0, 0.0)
        pyglet.gl.glVertex3f(10.0, -10.0, 0.0)
        pyglet.gl.glEnd()

    def scroll(self, s):
        self.layout.view_y += s

    def draw(self):
        pyglet.gl.glPushMatrix()
        self.draw_background()
        self.draw_text()
        self.draw_slider()
        pyglet.gl.glPopMatrix()


class Environment(object):

    def draw(self):
        #self.draw_base()
        pass

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


class Camera(object):

    rx,ry,rz=0,0,0
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
        if button==4:
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

    def apply(self):
        pyglet.gl.glLoadIdentity()
        pyglet.gl.glRotatef(self.rx,1,0,0)
        pyglet.gl.glRotatef(self.ry,0,1,0)
        pyglet.gl.glRotatef(self.rz,0,0,1)

    def map_to_page(self, x, y):
        """ Maps a screen click xy to a page xy
        """
        tx, ty = 0, 0

        #fix origin based on screen size
        tx = x - self.window.width/2
        ty = y - self.window.height/2
        
        #map to height/width ratios
        tx = ((tx/(self.window.width/2.)) * 1850)
        ty = ((ty/(self.window.height/2.)) * 1150) - 250
        
        return tx, ty


class Pages(object):
    """ Represents the loaded pages
    """
    pages = []

    def add_page(self, url):
        new_page = Page()
        new_page.load_url(url)
        self.pages.append(new_page)

    def draw(self):
        pyglet.gl.glPushMatrix()
        
        self.focussed_page.set_focussed(True)
        self.focussed_page.draw()
        
        for page in self.pages[1:]:
            pyglet.gl.glTranslatef(0.0, 0.0, -100)
            page.set_focussed(False)
            page.draw()
        
        pyglet.gl.glPopMatrix()
        
    @property
    def focussed_page(self):
        return self.pages[0]


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
        self.environment = Environment()
        self.pages = Pages()
        self.pages.add_page("http://www.mightyseek.com/wp-content/plugins/podpress/readme.txt")
        self.pages.add_page("http://wordpress.org/extend/plugins/about/readme.txt")
        self.opengl_init()
        self.render()

    def set_up_window(self):
        #self.window = pyglet.window.Window(fullscreen=True, resizable=True)
        
        self.window = pyglet.window.Window(fullscreen=False, resizable=True)
        self.window.width=1280
        self.window.height=800
        
        self.window.on_resize=self.camera.view
        #self.window.on_mouse_drag=self.camera.drag
        self.window.on_mouse_scroll=self.scroll_page
        #self.window.on_mouse_release=self.handle_mouse_up
        #self.window.on_mouse_motion=self.handle_mouse_up
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
            self.pages.draw()
            self.window.flip()

    def scroll_page(self, x, y, dx, dy):
        k = 100
        self.pages.focussed_page.scroll(dy*k)
        
#    def handle_mouse_up(self, x, y, button, modifiers):
#    def handle_mouse_up(self, x, y, dx, dy):
#        if button == 1:
#            x, y = self.camera.map_to_page(x, y)
#            line = self.page.layout.get_line_from_point(x, y)
#            char = self.page.layout.get_position_on_line(line, x)
#            self.page.layout.selection_background_color = (255, 0, 0, 255)
#            self.page.layout.set_selection(char, char+1)

Desktop()



