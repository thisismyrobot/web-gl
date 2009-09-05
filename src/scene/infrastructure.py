import math
import pyglet.gl
import scene.infrastructure
import scene.pages
import scene.state


class Camera(object):
    rx,ry,rz=0,0,0
    w,h=640,480
    far=10000
    fov=60
    x,y,z=0,0,-2000
    speed=2000

    @classmethod
    def view(self,width,height):
        self.w,self.h=width,height
        pyglet.gl.glViewport(0, 0, width, height)
        pyglet.gl.glMatrixMode(pyglet.gl.GL_PROJECTION)
        pyglet.gl.glLoadIdentity()
        pyglet.gl.gluPerspective(self.fov, float(self.w)/self.h, 0.1, self.far)
        pyglet.gl.glMatrixMode(pyglet.gl.GL_MODELVIEW)

    @classmethod
    def snap_focussed_page(self):
        """ will position camera in front of focussed page
        """
        target_page = PageManager.get_focussed_page()
        if target_page:
            page_x = target_page.x
            page_z = target_page.z
        self.x = -page_x
        self.z = -page_z - 2000
        self.ry, self.rx = 0, 0

    @classmethod
    def update_r(self, dx, dy):
        new_rx = self.rx-(dy/4.0)
        new_ry = self.ry+(dx/4.0)

        if new_rx < -30:
            new_rx = -30

        if new_rx > 30:
            new_rx = 30

        new_ry = new_ry % 360
        if new_ry > 180:
            new_ry = new_ry - 360
        
        self.rx=new_rx
        self.ry=new_ry

    @classmethod
    def move(self):
        """ Iterates the key states, applying movement transforms as needed.
            Only moves if in "fps" state.
        """
        if scene.state.ApplicationState.get_state() == 'fps':
            distance = pyglet.clock.tick() * self.speed
            for key in scene.infrastructure.Keys.keys:
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

    @classmethod
    def apply(self):
        self.move()
        pyglet.gl.glLoadIdentity()
        pyglet.gl.glRotatef(self.rx,1,0,0)
        pyglet.gl.glRotatef(self.ry,0,1,0)
        pyglet.gl.glRotatef(self.rz,0,0,1)
        pyglet.gl.glTranslatef(self.x, self.y, self.z)


class Mouse(object):
    """ Handles mouse events
    """
    @classmethod
    def mouse_release(self, x, y, button, modifiers):
        if button == 1:
            Camera.snap_focussed_page()

    @classmethod
    def mouse_motion(self, x, y, dx, dy):
        Camera.update_r(dx, dy)


class Keys(object):
    """ Stores the state of keys
    """
    keys = []
    buffer = []

    @classmethod
    def down(self, symbol, modifiers):
        """ Adds a key to the array, signifying that it is being pressed.
        """
        self.keys.append(symbol)
        print symbol

    @classmethod
    def up(self, symbol, modifiers):
        """ Removes a key from the array, signifying that it has been released.
        """
        self.keys.remove(symbol)
        self.push_key(symbol)

    @classmethod
    def push_key(self, symbol):
        """ Creates a queue of "up" keystrokes - used for piping input to a page.
        """
        self.buffer.append(symbol)

    @classmethod
    def pop_key(self):
        """ Creates a queue of "up" keystrokes - used for piping input to a page.
        """
        if len(self.buffer) > 0:
            return self.buffer.pop(0)

    @classmethod
    def clear_buffer(self):
        """ Clears the buffer of residual keystrokes - usefull when transitioning
            from movement to piping input to a page
        """
        self.buffer = []


class PageManager(object):
    """ Represents the loaded pages
    """
    pages = []

    @classmethod
    def add_page(self, new_page):
        """ Adds a page to the front of the queue
        """
        for page in self.pages:
            page.z -= 2000
            page.x -= 1000
            page.x *= -2
        new_page.load()
        self.pages.insert(0, new_page)

    @classmethod
    def hightlight_focussed(self):
        """ sets "focussed = True" on the closest page - doesn't activate in
            edit mode
        """
        distances = []
        errors = []

        for i in range(len(self.pages)):
            page = self.pages[i]

            #get angle to page
            x_offset = -Camera.x - page.x
            z_offset = -Camera.z - page.z
            angle = math.degrees(math.atan2(x_offset, z_offset))

            #get how far off your camera is
            error = abs(-Camera.ry - angle)

            #store the error as a page-index:error dict
            errors.append((i,error))

            #unfocus all pages as a default
            page.focussed = False

        #sort the errors to put the page-index with the least error at the head
        errors.sort(cmp=lambda x,y: cmp(x[1], y[1]))

        #re-focus the page that had the least error - if within the FOV
        if errors[0][1] < 30:
            self.pages[errors[0][0]].focussed = True


    @classmethod
    def draw(self):
        if scene.state.ApplicationState.get_state() != 'edit':
            self.hightlight_focussed()
        pyglet.gl.glPushMatrix()
        for i in range(len(self.pages)):
            self.pages[i].draw()
        pyglet.gl.glPopMatrix()

    @classmethod
    def get_focussed_page(self):
        focussed_page = [page for page in self.pages if page.focussed is True]
        if focussed_page:
            return focussed_page[0]