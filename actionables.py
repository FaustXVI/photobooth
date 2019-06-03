class Actionables:
    def __init__(self, actionables):
        self.actionables = actionables

    def wait_for_event(self):
        action = None
        while action is None:
            actions = [e for e in [a.next_action() for a in self.actionables] if e is not None]
            action = (actions or [None])[0]
        return action
