

class DrawObject:
    initial_x:int
    initial_y:int
    final_x:int
    final_y:int
    is_ready: bool = False

    def __init__(self):
        self.is_drawing = True

    def set_initial(self, x, y):
        self.initial_x = x
        self.initial_y = y

        if self.is_ready:
            self.is_ready = False

    def set_final(self, x, y):
        self.final_x = x
        self.final_y = y
        self.is_ready = True

    def reset(self):
        self.initial_x = 0
        self.initial_y = 0
        self.final_x = 0
        self.final_y = 0
        self.is_ready = False
