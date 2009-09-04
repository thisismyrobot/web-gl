import pyglet.gl
import urllib2
import subprocess


class Page(object):
    """ Represents a remotely loaded page
    """
    page_width = 1600 #visible text area width
    page_height = 2000 #visible text area height
    page_border = 50 #spacing around text
    page_font_size = 14
    page_alpha = 1.0

    x,y,z,rz = 0,0,0,0
    r,g,b = 0.0,1.0,0.0
    r_foc,g_foc,b_foc = 1.0,0.0,0.0

    focussed = False

    def __init__(self, **kwargs):
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
        self.kwargs = kwargs


    def update_document_style(self):
        style = {'font-size':self.page_font_size, 'color':(int(self.r*255), int(self.g*255), int(self.b*255), int(self.page_alpha*255))}
        self.document.set_style(0, 50, style)

    def load(self):
        """ Marker for the code to load the page. Needs to do what ever is needed
            for an initial page load, and set "self.layout.document.text" 
            with the result.
        """

    def draw_background(self):
        """ draw text background
        """
        #border
        if self.focussed is False:
            pyglet.gl.glColor4f(self.r, self.g, self.b, self.page_alpha)
        else:
            pyglet.gl.glColor4f(self.r_foc, self.g_foc, self.b_foc, self.page_alpha)
            
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
        self.layout.draw()
        pyglet.gl.glPopMatrix()

    def draw_slider(self):
        """ draw slider position
        """
        pyglet.gl.glTranslatef((self.page_width/2)+self.page_border, (self.page_height/2)+self.page_border, 0.0)
        scroll_pos = (float(self.layout.view_y) / float(self.layout.content_height - self.page_height)) * (self.page_height + self.page_border * 2)
        pyglet.gl.glTranslatef(0.0, scroll_pos, 0.0)
        pyglet.gl.glLineWidth(1.5)
        pyglet.gl.glColor4f(self.r, self.g, self.b, self.page_alpha)
        pyglet.gl.glBegin(pyglet.gl.GL_LINE_LOOP)
        pyglet.gl.glVertex3f(-20.0, -20.0, 0.0)
        pyglet.gl.glVertex3f(-20.0, 20.0, 0.0)
        pyglet.gl.glVertex3f(20.0, 20.0, 0.0)
        pyglet.gl.glVertex3f(20.0, -20.0, 0.0)
        pyglet.gl.glEnd()

    def scroll(self, s):
        self.layout.view_y += s

    def position_page(self):
        pyglet.gl.glTranslatef(self.x, self.y, self.z)
        pyglet.gl.glRotatef(self.rz, 0, 0, 1)

    def draw(self):
        pyglet.gl.glPushMatrix()
        self.position_page()
        self.draw_background()
        self.draw_text()
        self.draw_slider()
        pyglet.gl.glPopMatrix()


class URL(Page):
    """ Creates an page from a url
    """
    def load(self, **kwargs):
        """ Updates the self.text with the contents of a url
        """
        request = urllib2.Request(self.kwargs['url'])
        connection = urllib2.urlopen(request)
        data = connection.read()
        connection.close()
        self.layout.document.text = data


class PythonConsole(Page):
    """ Creates a page with an interactive python console
    """
    def load(self, **kwargs):
        """ Updates the self.text with the contents of a url
        """
        process = subprocess.Popen(["python", "-i"], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        result = process.communicate()[1]
        result = result.replace("\r","")
        self.layout.document.text = result