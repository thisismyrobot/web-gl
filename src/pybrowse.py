import pyglet.gl
import pyglet.text
import pyglet.window
import math
import random
import datetime
import pyglet.clock
import scene.pages
import scene.infrastructure


class Desktop(object):
    """ Represents the app - containing pages with content
    """
    def __init__(self):
        """ sets up the the window, starts rendering the browser
        """
        scene.infrastructure.Camera()
        self.set_up_window()

        #add some pages
        scene.infrastructure.PageManager.add_page(
            scene.pages.URL(
                url="http://www.abc.net.au/news/indexes/justin/rss.xml", 
                xpath=('//item//title/text()', '//item/description/text()', '//item/pubDate/text()')
                )
            )

        scene.infrastructure.PageManager.add_page(scene.pages.GoogleReader())

        self.opengl_init()
        self.render()

    def set_up_window(self):
        #self.window = pyglet.window.Window(fullscreen=True, resizable=True)

        #set up window
        self.window = pyglet.window.Window(fullscreen=False, resizable=True)
        self.window.width=1280
        self.window.height=800
        
        #handlers
        self.window.on_resize=scene.infrastructure.Camera.view
        self.window.on_mouse_motion=scene.infrastructure.Mouse.mouse_motion
        self.window.on_mouse_release=scene.infrastructure.Mouse.mouse_release
        self.window.on_mouse_scroll=self.scroll_page
        self.window.on_key_press=scene.infrastructure.Keys.down
        self.window.on_key_release=scene.infrastructure.Keys.up
    
        self.window.set_exclusive_mouse(True)
        #self.window.push_handlers(pyglet.window.event.WindowEventLogger())

    def opengl_init(self):
        pyglet.gl.glEnable(pyglet.gl.GL_BLEND)
        pyglet.gl.glBlendFunc(pyglet.gl.GL_SRC_ALPHA, pyglet.gl.GL_ONE_MINUS_SRC_ALPHA)
        pyglet.gl.glDepthFunc(pyglet.gl.GL_LEQUAL)
        pyglet.gl.glEnable(pyglet.gl.GL_LINE_SMOOTH)
        pyglet.gl.glHint(pyglet.gl.GL_LINE_SMOOTH_HINT, pyglet.gl.GL_DONT_CARE)

    def render(self):
        while 65307 not in scene.infrastructure.Keys.keys:
            self.window.dispatch_events()
            pyglet.gl.glClear(pyglet.gl.GL_COLOR_BUFFER_BIT | pyglet.gl.GL_DEPTH_BUFFER_BIT)
            scene.infrastructure.Camera.apply()
            scene.infrastructure.PageManager.draw()
            #scene.state.ApplicationState.handle_state_changes()
            self.window.flip()

    def scroll_page(self, x, y, dx, dy):
        k = 100
        scene.infrastructure.PageManager.get_focussed_page().scroll(dy*k)

Desktop()



