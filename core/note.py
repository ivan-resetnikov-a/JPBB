import pygame as pg
pg.font.init()
pg.mixer.init()

try :
	import pygame.gfxdraw

	def draw_aacircle(surface, color, pos, radius):
		# using gfxdraw to draw anti-anialised shapes
		pg.gfxdraw.aacircle(surface, round(pos[0]), round(pos[1]), radius, color)
		pg.gfxdraw.filled_circle(surface, round(pos[0]), round(pos[1]), radius, color)
except ImportError :
	def draw_aacircle(surface, color, pos, radius):
		# using gfxdraw to draw anti-anialised shapes
		pg.draw.circle(surface, color, pos, radius)

from .file import loadFromINI


config = loadFromINI('settings.ini')

koyotTime = float(config['GAMEPLAY']['coyote_time_gap'])

font = pg.font.SysFont('Arial', 100)




class Note :
	def __init__ (self, color, side, speed, hitSound) :
		### image
		self.color = [color[0], color[1], color[2]]

		color = [color[0], color[1], color[2]]

		color[0] -= 80
		color[1] -= 80
		color[2] -= 80
		if color[0] < 0 : color[0] = 0
		if color[1] < 0 : color[1] = 0
		if color[2] < 0 : color[2] = 0

		self.outline = color

		self.letter = {0: 'D', 1: 'F', 2: 'J', 3: 'K'}[side - 1]
		self.letter = font.render(self.letter, 1, self.outline)

		### sound
		self.hitSound = hitSound

		### stats
		self.key = {0: pg.K_d, 1: pg.K_f, 2: pg.K_j, 3: pg.K_k}[side - 1]
		self.hit = 0

		self.side = side - 1

		self.noteSpeed = speed
		self.y = -120


	def update (self, dt) :
		self.y += self.noteSpeed * dt

		keys = pg.key.get_pressed()

		if keys[self.key] and (self.y > (800 - koyotTime) and self.y < (800 + koyotTime)) :
			self.hit = 1
			self.hitSound.play()


	def render (self, frame) :
		draw_aacircle(frame, self.outline, (125 * (self.side + 0.5), self.y), 60)
		draw_aacircle(frame, self.color,   (125 * (self.side + 0.5), self.y), 55)

		frame.blit(self.letter, ((125 * (self.side + 0.5)) - 25, self.y - 55))