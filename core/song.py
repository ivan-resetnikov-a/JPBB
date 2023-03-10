import pygame as pg

from .file import unZip, loadFromJSON, writeToJSON, newFolder, loadFromINI
from .note import Note

settings = loadFromINI('settings.ini')
darkenBackground = float(settings['RENDER']['darken_background'])

bigFont = pg.font.Font('font.ttf', 30)
smallFont = pg.font.Font('font.ttf', 17)


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
		self.author = content['author']
		self.difficulty = content['difficulty']

		self.noteSpeed = content['speed']

		self.icon = pg.image.load(f'{songPath}/icon.png').convert_alpha()
		self.bg   = pg.image.load(f'{songPath}/bg.png').convert_alpha()

		#### get color palette from background
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

		#### song banner
		# darken layer
		self.banner = pg.Surface((426, 132))

		self.bannerDarkenLayer = pg.Surface((426, 132))
		self.bannerDarkenLayer.fill((0, 0, 0))
		self.bannerDarkenLayer.set_alpha(128)

		# banner outline
		pg.draw.rect(self.banner, self.bgColor, (2, 2, 426, 128), 2)

		# banner icon
		self.banner.blit(self.icon, (2, 2))

		# banner title & author
		self.banner.blit(bigFont.render(self.name, 1, self.bgColor), (138, 10))
		self.banner.blit(smallFont.render(f'by {self.author}', 1, self.bgColor), (138, 40))

		# banner difficulty
		self.banner.blit(smallFont.render('difficulty', 1, self.bgColor), (138, 75))

		[pg.draw.circle(self.banner, self.bgColor, (128 + 10 + 8 + (20 * x), 112), 8) for x in range(self.difficulty)]

		#### song
		self.board = pg.Surface((500, 900))

		self.progress = 0

		self.time = 0
		self.notes = []

		#### sound
		self.hitSound = pg.mixer.Sound(f'{songPath}/hit.wav')
		self.hitSound.set_volume(content['hit_sound_volume'])

		pg.mixer.music.load(f'{songPath}/music.mp3')
		pg.mixer.music.set_volume(content['music_volume'])


	def play (self) :
		pg.mixer.music.play()


	def update (self, dt) :
		self.time += 1

		#### add notes to scene
		if len(self.song) > self.progress :
			note = self.song[self.progress]

			if note['time'] == self.time :
				self.progress += 1

				# custom note speed
				if 'speed' in note : noteSpeed = note['speed']
				else : noteSpeed = self.noteSpeed

				self.notes.append(Note(self.bgColor, note['side'], noteSpeed, self.hitSound))

		#### update each note
		toRemove = [] # used to fix skiped iteration issue
		for note in self.notes :
			note.update(dt)
			if note.hit :
				toRemove.append(note)

		#### remove notes
		for note in toRemove : self.notes.remove(note)


	def render (self, frame) :
		#### fill with average color
		frame.fill(self.bgColor)

		#### render background image
		self.board.blit(self.bg, (0, 0))

		#### draw border lines
		for x in range(1, 4) : pg.draw.line(self.board, self.bgColor, (125 * x, 0), (125 * x, 900), 1)

		pg.draw.line(self.board, self.bgColor, (0, 800), (500, 800), 5)

		#### render notes
		for note in self.notes[::-1] : note.render(self.board)

		frame.blit(self.board, (50, 0))