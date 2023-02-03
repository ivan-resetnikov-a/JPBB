import pygame.gfxdraw
import pygame as pg

from .file import loadFromINI

settings = loadFromINI('settings.ini')
koyotTime = float(settings['GAMEPLAY']['coyote_time_gap'])

font = pg.font.Font('font.ttf', 90)



def draw_aacircle(surface, color, pos, radius):
	pg.gfxdraw.aacircle(surface, round(pos[0]), round(pos[1]), radius, color)
	pg.gfxdraw.filled_circle(surface, round(pos[0]), round(pos[1]), radius, color)



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

		self.letter = {0: 'd', 1: ' f', 2: ' j', 3: 'k'}[side - 1]
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
			self.hitSound.play()
			self.hit = 1


	def render (self, frame) :
		draw_aacircle(frame, self.outline, (125 * (self.side + 0.5), self.y), 60)
		draw_aacircle(frame, self.color,   (125 * (self.side + 0.5), self.y), 55)

		frame.blit(self.letter, ((125 * (self.side + 0.5)) - 30, self.y - 70))