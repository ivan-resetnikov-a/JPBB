import pygame as pg
pg.mixer.init()
pg.font.init()
pg.init()

import core



class Game :
	def __init__ (self) :
		#### config
		self.size, self.title = (600, 900), 'FnF | V 1.0'
		self.fps, self.timeMult = 60, 1

		#### window
		self.window = pg.display.set_mode(self.size)
		self.clock  = pg.time.Clock()

		#### gameplay
		self.state = 'song_menu'


	def update (self) :
		#### song selection menu
		if self.state == 'song_menu' :
			pass

		#### plaing song
		if self.state == 'playing_song' :
			self.song.update(self.timeMult)


	def render (self) :
		self.window.fill((0, 0, 0))
		#### render

		#### song selection menu
		if self.state == 'song_menu' :
			pass

		#### plaing song
		if self.state == 'playing_song' :
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

		self.onExit()


	def onStart (self) :
		#### load songs
		self.songs = []
		for song in core.filesAndFolders('songs/') :
			if song != 'temp' :
				self.songs.append(core.Song(song))

		self.state = 'playing_song'
		self.song = self.songs[0]

		self.song.play()


	def onExit (self) :
		#### clear cache
		for song in core.filesAndFolders('songs/temp/') :
			core.deleteFolder(f'songs/temp/{song}')



if __name__ == '__main__' :
	Game().run()