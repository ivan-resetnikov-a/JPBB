import pygame as pg

import core



class Game :
	def __init__ (self) :
		#### config
		self.size, self.title = (600, 900), 'FnF | V 1.0'
		self.fps, self.timeMult = 60, 1

		#### window
		self.window = pg.display.set_mode(self.size)
		self.clock  = pg.time.Clock()


	def update (self) :
		self.song.update(self.timeMult)


	def render (self) :
		self.window.fill((0, 0, 0))
		#### render

		self.song.render(self.window)

		#### refresh
		self.clock.tick(self.fps)
		pg.display.flip()


	def run (self) :
		self.onStart()

		self.running = 1
		while self.running :
			for event in pg.event.get() :
				if event.type == pg.QUIT :
					self.running = 0

			self.update()
			self.render()

		pg.mixer.quit()
		pg.font.quit()
		pg.quit()


	def onStart (self) :
		self.song = core.Song('test.zip')



if __name__ == '__main__' :
	Game().run()

	for song in core.filesAndFolders('songs/temp/'):
		core.deleteFolder(f'songs/temp/{song}')