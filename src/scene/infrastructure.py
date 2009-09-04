import math
import pyglet.gl
import scene.infrastructure


class Camera(object):
    rx,ry,rz=0,0,0
    w,h=640,480
    far=8192
    fov=60
    x,y,z=0,0,0
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
    def update(self, x, y, dx, dy):
        self.update_r(dx, dy)

    @classmethod
    def update_r(self, dx, dy):
        new_rx = self.rx-(dy/4.0)
        new_ry = self.ry+(dx/4.0)

        if new_rx < -30:
            new_rx = -30

        if new_rx > 30:
            new_rx = 30

        self.rx=new_rx
        self.ry=new_ry

    @classmethod
    def move(self):
        """ Iterates the key states, applying movement transforms as needed.
        """
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