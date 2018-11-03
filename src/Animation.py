class Animation:

    def __init__(self, sprites, speed):
        self.speed = speed
        self.counter = 0
        self.current_image = 0
        self.animation = sprites

    def update(self):
        self.counter += 1
        if self.counter >= self.speed:
            self.current_image += 1
            self.counter = 0
            self.current_image = self.current_image % len(self.animation)

    def get_current_image(self):
        return self.animation[self.current_image]
