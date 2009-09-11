import zope.interface


class IPage(zope.interface.Interface):
    """ This is the interface for all the pages
    """

    def load():
        """ This method performs the initial load of a page's content.
            Sets the value of self.layout.document.text
        """

    def handle_input():
        """ Is called when there is the need for use-input to be piped
            to the page - in an "edit" mode for instance.
        """

    def draw():
        """ Renders the page in space.
        """

    def scroll(s):
        """ Updates the vertical scroll position of the page by s.
        """

    def draw_slider():
        """ Draws the scroll-slider
        """

    def draw_text():
        """ Renders the actual text
        """

    def draw_background():
        """ Renders the visuals of the page that do not include the
            actual text.
        """

    def position_page():
        """ Performs the gl translations/rotations to before rendering.
            Recommend pushing matrix before calling and popping maxtrix
            after all elements rendered. Is called by draw() method.
        """