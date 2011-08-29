import os, pygame, random, datetime
from Vector2D import Vector2D


def load_image(name, colorkey=None):
	fullname = os.path.join('data', name)
	try:
		image = pygame.image.load(fullname)
	except pygame.error, message:
		print 'Cannot load image:', fullname
		raise SystemExit, message
	image = image.convert()
	if colorkey is not None:
		if colorkey is -1:
			colorkey = image.get_at((0, 0))
		image.set_colorkey(colorkey, pygame.RLEACCEL)
	return image


class Fish(pygame.sprite.Sprite):
	def __init__(self, position, speed):
		pygame.sprite.Sprite.__init__(self)
		self.image = load_image('fish.png', -1)
		self.rect = self.image.get_rect(center=position)

		self.position = Vector2D (*position)
		self.destination = None
		self.state = "still"
		self.speed = speed

	def update(self, time_passed_seconds):
		if self.state == "move":
			travelvector = self.destination - self.position

			distance_moved = time_passed_seconds * self.speed
			self.position += travelvector * distance_moved

			self.rect = self.image.get_rect(center=(self.position.x, self.position.y))

			if self.position == self.destination:
				self.state = "still"

	def moveTo(self, destination):
		self.destination = Vector2D(*destination)
		self.state = "move"

def main():
	pygame.init()
	screen = pygame.display.set_mode((1024, 768))
	pygame.display.set_caption('Fish')
	background = load_image("sea.jpg")

	random.seed(datetime.time.microsecond)

	fishes = []
	for fish in range (10):
		fishes.append(Fish((random.randint(0, 400), random.randint(0, 400)), random.uniform(0.2, 5.5)))

	sprites = pygame.sprite.RenderUpdates((fishes))

	screen.blit(background, (0, 0))
	pygame.display.flip()

	clock = pygame.time.Clock()

	while True:
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				exit()

			if event.type == pygame.MOUSEMOTION:
				for fish in fishes:
					fish.moveTo(event.pos)

		time_passed_seconds = clock.tick() / 1000.0

		sprites.update(time_passed_seconds)
		sprites.clear(screen, background)
		changes = sprites.draw(screen)
		pygame.display.update(changes)


if __name__ == '__main__': main()
