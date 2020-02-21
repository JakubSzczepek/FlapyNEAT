import os

import pygame

WINDOW_WIDTH = 600
WINDOW_HEIGHT = 800


class Images:

    def __init__(self):
        self.bird_images = []
        self.pipe_image = []
        self.background_image = []
        self.ground_image = []
        self.images_path = os.path.join(os.getcwd(), 'Images')

    @staticmethod
    def load_image(path, scale=False):
        image = None
        try:
            if scale:
                image = pygame.transform.scale2x(pygame.image.load(path))
            else:
                image = pygame.image.load(path)
        except (FileNotFoundError, IOError):
            print(f'Path {path} is not correct !')

        return image

    def load_bird_images(self):
        for item in os.listdir(os.path.join(self.images_path, "birds")):
            self.bird_images.append(self.load_image(os.path.join(self.images_path,"birds", item), scale=True))
        return self.bird_images

    def load_pipe_image(self):
        self.pipe_image = self.load_image(os.path.join(self.images_path, "pipe.png"))
        return self.pipe_image

    def load_background_image(self):
        self.background_image = self.load_image(os.path.join(self.images_path, "bg.png"), scale=True)
        return self.background_image

    def load_ground_image(self):
        self.ground_image = self.load_image(os.path.join(self.images_path, "base.png"))
        return self.ground_image

class Bird(Images):

    MAX_ROTATION = 25
    ROTATION_VELOCITY = 20
    ANIMATION_TIME = 5

    def __init__(self, x, y):
        super().__init__()
        super().load_bird_images()
        self.x = x
        self.y = y
        self.tilt = 0
        self.tick_count = 0
        self.velocity = 0
        self.height = y
        self.image_count = 0
        self.image = self.bird_images[0]

    def jump(self):

        self.velocity = -10.5
        self.tick_count = 0
        self.height = self.y

    def move(self):
        self.tick_count += 1
        physic_pixels = self.velocity * self.tick_count + 1.5*self.tick_count**2

        if physic_pixels >= 16:
            physic_pixels = 16

        if physic_pixels < 0:
            physic_pixels -= 2

        self.y = self.y + physic_pixels

        if physic_pixels < 0 or self.y < self.height + 50:
            if self.tilt < self.MAX_ROTATION:
                self.tilt = self.MAX_ROTATION
        else:
            if self.tilt > -90:
                self.tilt -= self.ROTATION_VELOCITY

    def draw(self, window):
        self.image_count +=1
        if self.image_count < self.ANIMATION_TIME:
            self.image = self.bird_images[0]
        elif self.image_count < self.ANIMATION_TIME *2:
            self.image = self.bird_images[1]
        elif self.image_count < self.ANIMATION_TIME *3:
            self.image = self.bird_images[2]
        elif self.image_count < self.ANIMATION_TIME *4:
            self.image = self.bird_images[1]
        elif self.image_count < self.ANIMATION_TIME *4 + 1:
            self.image = self.bird_images[0]
            self.image_count = 0

        if self.tilt <= -90:
            self.image = self.bird_images[1]
            self.image_count = self.ANIMATION_TIME * 2

        rotated_image = pygame.transform.rotate(self.image, self.tilt)
        new_rectangle = rotated_image.get_rect(center=self.image.get_rect(topleft = (self.x, self.y)).center)
        window.blit(rotated_image, new_rectangle)

    def get_mask(self):
        return pygame.mask.from_surface(self.image)



def draw_window(window, bird):
    background = Images().load_background_image()
    window.blit(background, (0,0))
    bird.draw(window)
    pygame.display.update()

def main():
    bird = Bird(200, 200)
    window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    run = True
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
        draw_window(window, bird)

    pygame.quit()
    quit()



if __name__ == "__main__":
    main()
    pass