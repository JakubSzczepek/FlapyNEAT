import os

import pygame

WINDOW_WIDTH = 600
WINDOW_HEIGHT = 800


class Images:

    def __init__(self, path):
        self.bird_images = []
        self.pipe_image = []
        self.background_image = []
        self.ground_image = []
        self.images_path = path

    def __call__(self):

        self.load_bird_images(self.images_path)
        self.load_background_image(self.images_path)
        self.load_ground_image(self.images_path)
        self.load_pipe_image(self.images_path)


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

    def load_bird_images(self, path):
        for item in os.listdir(os.path.join(path, "birds")):
            self.bird_images.append(self.load_image(os.path.join(path,"birds", item), scale=True))

    def load_pipe_image(self, path):
        self.pipe_image = self.load_image(os.path.join(path, "pipe.png"))

    def load_background_image(self, path):
        self.background_image = self.load_image(os.path.join(path, "bg.png"))

    def load_ground_image(self, path):
        self.ground_image = self.load_image(os.path.join(path, "base.png"))

class Bird(Images):

    def __init__(self):

        self.bird_images = super(Images)


if __name__ == "__main__":

    images = Images("./Images")
    images()

    pass