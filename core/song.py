import pygame as pg

from .file import unZip, loadFromJSON, writeToJSON, newFolder
from .note import Note

pg.mixer.init()

darkenBackground = 0



class Song :
	def __init__ (self, name) :
		#### unzip song archieve
		songPath = 'songs/temp/'+name[:-4:]

		newFolder(f'{songPath}/')
		unZip(f'songs/{name}', f'{songPath}/')

		#### load info
		content = loadFromJSON(f'{songPath}/song.json')

		self.name = content['name']
		self.song = content['song']
		self.noteSpeed = content['speed']

		self.icon = pg.image.load(f'{songPath}/icon.png').convert_alpha()
		self.bg   = pg.image.load(f'{songPath}/bg.png').convert_alpha()

		self.bgColor = list(pg.transform.average_color(self.bg))

		self.bgColor[0] += 30
		self.bgColor[1] += 30
		self.bgColor[2] += 30
		if self.bgColor[0] > 255 : self.bgColor[0] = 255
		if self.bgColor[1] > 255 : self.bgColor[1] = 255
		if self.bgColor[2] > 255 : self.bgColor[2] = 255

		darkenLayer = pg.Surface((500, 900))
		darkenLayer.set_alpha((255 / 100) * darkenBackground)
		self.bg.blit(darkenLayer, (0, 0))

		#### song
		self.board = pg.Surface((500, 900))

		self.notes = []
		
		self.time = 0

		#### sound
		pg.mixer.music.load(f'{songPath}/music.mp3')
		pg.mixer.music.set_volume(content['music_volume'])
		pg.mixer.music.play()

		self.hitSound = pg.mixer.Sound(f'{songPath}/hit.wav')
		self.hitSound.set_volume(content['hit_sound_volume'])


	def update (self, dt) :
		self.time += 1
		for note in self.song :
			if note['time'] == self.time :
				try : noteSpeed = note['speed']
				except KeyError : noteSpeed = self.noteSpeed

				self.notes.append(Note(self.bgColor, note['side'], noteSpeed, self.hitSound))

		toRemove = []
		for note in self.notes :
			note.update(dt)
			if note.hit :
				toRemove.append(note)

		for note in toRemove : self.notes.remove(note)


	def render (self, frame) :
		frame.fill(self.bgColor)

		self.board.blit(self.bg, (0, 0))

		x = 1
		for _ in range(4) :
			pg.draw.line(self.board, self.bgColor, (125 * x, 0), (125 * x, 900), 1)
			x += 1

		pg.draw.line(self.board, self.bgColor, (0, 800), (500, 800), 5)

		for note in self.notes[::-1] : note.render(self.board)

		frame.blit(self.board, (50, 0))