import pygame as pg
pg.font.init()
pg.mixer.init()

import pygame.gfxdraw

font = pg.font.SysFont('Arial', 100)

hitSound = pg.mixer.Sound('assets/fnf/hit.wav')
hitSound.set_volume(0.2)

koyotTime = 20





class Note :
	def __init__ (self, color, side, speed) :
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
			hitSound.play()


	def render (self, frame) :
		# using gfxdraw to draw anti-anialised shapes
		pg.gfxdraw.aacircle(frame, round(125 * (self.side + 0.5)), round(self.y), 60, self.outline)
		pg.gfxdraw.filled_circle(frame, round(125 * (self.side + 0.5)), round(self.y), 60, self.outline)
		
		pg.gfxdraw.aacircle(frame, round(125 * (self.side + 0.5)), round(self.y), 55, self.color)
		pg.gfxdraw.filled_circle(frame, round(125 * (self.side + 0.5)), round(self.y), 55, self.color)

		frame.blit(self.letter, ((125 * (self.side + 0.5)) - 25, self.y - 55))