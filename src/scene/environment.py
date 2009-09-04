class Floor(object):

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


class ControlPanel(object):
    """ Represents the hovering control area
    """
