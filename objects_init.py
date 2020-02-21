import os
import random

import pygame
pygame.font.init()
WINDOW_WIDTH = 500
WINDOW_HEIGHT = 800
STAT_FONT = pygame.font.SysFont("comicsans", 50)

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
            self.bird_images.append(self.load_image(os.path.join(self.images_path, "birds", item), scale=True))
        return self.bird_images

    def load_pipe_image(self):
        self.pipe_image = self.load_image(os.path.join(self.images_path, "pipe.png"), scale=True)
        return self.pipe_image

    def load_background_image(self):
        self.background_image = self.load_image(os.path.join(self.images_path, "bg.png"), scale=True)
        return self.background_image

    def load_ground_image(self):
        self.ground_image = self.load_image(os.path.join(self.images_path, "base.png"), scale=True)
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
        physic_pixels = self.velocity * self.tick_count + 1.5 * self.tick_count ** 2

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
        self.image_count += 1
        if self.image_count < self.ANIMATION_TIME:
            self.image = self.bird_images[0]
        elif self.image_count < self.ANIMATION_TIME * 2:
            self.image = self.bird_images[1]
        elif self.image_count < self.ANIMATION_TIME * 3:
            self.image = self.bird_images[2]
        elif self.image_count < self.ANIMATION_TIME * 4:
            self.image = self.bird_images[1]
        elif self.image_count < self.ANIMATION_TIME * 4 + 1:
            self.image = self.bird_images[0]
            self.image_count = 0

        if self.tilt <= -90:
            self.image = self.bird_images[1]
            self.image_count = self.ANIMATION_TIME * 2

        rotated_image = pygame.transform.rotate(self.image, self.tilt)
        new_rectangle = rotated_image.get_rect(center=self.image.get_rect(topleft=(self.x, self.y)).center)
        window.blit(rotated_image, new_rectangle)

    def get_mask(self):
        return pygame.mask.from_surface(self.image)


class Pipe(Images):
    GAP = 200
    VELOCITY = 5

    def __init__(self, x):
        super().__init__()
        super().load_pipe_image()

        self.x = x
        self.height = 0
        self.gap = 100

        self.top = 0
        self.bottom = 0
        self.pipe_top = pygame.transform.flip(self.pipe_image, False, True)
        self.pipe_bottom = self.pipe_image

        self.passed = False
        self.set_height()

    def set_height(self):
        self.height = random.randrange(40, 450)
        self.top = self.height - self.pipe_top.get_height()
        self.bottom = self.height + self.GAP

    def move(self):
        self.x -= self.VELOCITY

    def draw(self, window):
        window.blit(self.pipe_top, (self.x, self.top))
        window.blit(self.pipe_bottom, (self.x, self.bottom))

    def collide(self, bird):
        bird_mask = bird.get_mask()
        top_mask = pygame.mask.from_surface(self.pipe_top)
        bottom_mask = pygame.mask.from_surface(self.pipe_bottom)

        top_offset = (self.x - bird.x, self.top - round(bird.y))
        bottom_offset = (self.x - bird.x, self.bottom - round(bird.y))

        bottom_point_of_collsion = bird_mask.overlap(bottom_mask, bottom_offset)
        top_point_of_collsion = bird_mask.overlap(top_mask, top_offset)

        if bottom_point_of_collsion or top_point_of_collsion:
            return True

        return False


class Base(Images):
    VELOCITY = 5

    def __init__(self, y):
        super().__init__()
        super().load_ground_image()
        self.width = self.ground_image.get_width()

        self.y = y
        self.x1 = 0
        self.x2 = self.width

    def move(self):

        self.x1 -= self.VELOCITY
        self.x2 -= self.VELOCITY

        if self.x1 + self.width < 0:
            self.x1 = self.x2 + self.width

        if self.x2 + self.width < 0:
            self.x2 = self.x1 + self.width

    def draw(self, window):
        window.blit(self.ground_image, (self.x1, self.y))
        window.blit(self.ground_image, (self.x2, self.y))


def draw_window(window, bird, pipes, ground, score):
    background = Images().load_background_image()
    window.blit(background, (0, 0))

    for pipe in pipes:
        pipe.draw(window)

    text = STAT_FONT.render(f"Score: {score}", 1, (0,0,0))

    window.blit(text, (WINDOW_WIDTH - 10 - text.get_width(), 10))
    ground.draw(window)
    bird.draw(window)

    pygame.display.update()


def main():
    bird = Bird(230, 350)
    ground = Base(730)
    pipes = [Pipe(600)]
    score = 0

    window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    run = True
    clock = pygame.time.Clock()
    while run:
        clock.tick(30)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    bird.jump()
        add_pipe = False
        to_remove = []
        for pipe in pipes:
            if pipe.collide(bird):
                pass
            if pipe.x + pipe.pipe_top.get_width() < 0:
                to_remove.append(pipe)

            if not pipe.passed and pipe.x < bird.x:
                pipe.passed = True
                add_pipe = True

            pipe.move()

        if add_pipe:
            score +=1
            pipes.append(Pipe(600))

        for item in to_remove:
            pipes.remove(item)

        if bird.y + bird.image.get_height() >= 730:
            pass

        bird.move()
        ground.move()
        draw_window(window, bird, pipes, ground, score)

    pygame.quit()
    quit()


if __name__ == "__main__":
    main()
    pass
