import pygame


def load_image(path, scale=1, animation=False, flip_x=False, flip_y=False, alpha=True, fixed_hight_pixels=None):
    if not animation:
        image = pygame.image.load(path)
        if not fixed_hight_pixels:
            image = pygame.transform.scale(image, [x * scale for x in image.get_size()])
        else:
            unscaled_width, unscaled_height = image.get_size()
            width = unscaled_width * fixed_hight_pixels / unscaled_height
            image = pygame.transform.scale(image, [int(width), int(fixed_hight_pixels)])

        image = pygame.transform.flip(image, flip_x, flip_y)
        if alpha:
            image = image.convert_alpha()
        else:
            image = image.convert()
        return image
    else:
        animation_array = []
        counter = 1
        while animation:
            try:
                image = pygame.image.load("{}{}.png".format(path, str(counter)))
                image = pygame.transform.scale(image, [x * scale for x in image.get_size()])
                image = pygame.transform.flip(image, flip_x, flip_y)
                if alpha:
                    image = image.convert_alpha()
                else:
                    image = image.convert()
                animation_array.append(image)
                counter += 1
            except pygame.error:
                if len(animation_array) > 0:
                    return animation_array
                else:
                    raise FileNotFoundError