import scene.infrastructure

class ApplicationState(object):
    """ Represents the different states that the application can be in.
    """
    states = ('fps', 'edit')
    current_state = 0

    @classmethod
    def get_state(self):
        return self.states[self.current_state]

    @classmethod
    def set_state(self, new_state):
        """ Sets the state using the string state name.
        """
        self.current_state = self.states.index(new_state)

    @classmethod
    def handle_state_changes(self):
        """ Changes the state as necessary, based on input
        """
        #SPACE key = enter edit mode if focussed on a page
        if (32 in scene.infrastructure.Keys.keys and 
            scene.infrastructure.PageManager.get_focussed_page() and
            self.get_state() != 'edit'):
            self.set_state('edit')
            scene.infrastructure.Keys.clear_buffer()

        #CTRL key = exit edit mode 
        if (65507 in scene.infrastructure.Keys.keys and
            self.get_state() == 'edit'):
            self.set_state('fps')

        