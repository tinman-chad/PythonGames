import pygame, sys 
from settings import *
from components.player import Player
from components.car import Car
from random import choice, randint
from components.sprite import SimpleSprite, LongSprite
from os import walk
from pathlib import Path
from utils.scorekeeper import ScoreKeeper

class AllSprites(pygame.sprite.Group):
	def __init__(self):
		super().__init__()
		self.offset = pygame.math.Vector2()
		self.bg = pygame.image.load('./graphics/main/map.png').convert()
		self.fg = pygame.image.load('./graphics/main/overlay.png').convert_alpha()

	def customize_draw(self):

		# change the offset vector
		self.offset.x = player.rect.centerx - WINDOW_WIDTH / 2
		self.offset.y = player.rect.centery - WINDOW_HEIGHT / 2

		# blit the bg
		display_surface.blit(self.bg,-self.offset)

		for sprite in sorted(self.sprites(), key = lambda sprite: sprite.rect.centery):
			offset_pos = sprite.rect.topleft - self.offset
			display_surface.blit(sprite.image, offset_pos)

		display_surface.blit(self.fg,-self.offset)
		
# basic setup
pygame.init()
display_surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption('Road Kill')
clock = pygame.time.Clock()

scores_font = pygame.font.Font(None, 20)
scorekeeper = ScoreKeeper('RoadKill', True, Path('./scores.db'), scores_font, (125, 125, 125), 'Press Space Key For New Game')
# groups 
all_sprites = AllSprites()
obstacle_sprites = pygame.sprite.Group()

# sprites 
player = Player((2062,3274),all_sprites,obstacle_sprites)

# timer 
car_timer = pygame.event.custom_type()
pygame.time.set_timer(car_timer, 100)

pos_list = []

# font 
font = pygame.font.Font(None, 50)
text_surf = font.render('Level Completed!',True,'White')
text_rect = text_surf.get_rect(center = (WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2))
game_over = font.render('Press Space Key For New Game', True, 'White')
game_over_rect = game_over.get_rect(center = (WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2))

# music
#music = pygame.mixer.Sound('./audio/music.mp3')
#music.play(loops = -1)

# sprite setup

for file_name, pos_list in SIMPLE_OBJECTS.items():
	for pos in pos_list:
		SimpleSprite(pygame.image.load(f'./graphics/objects/simple/{file_name}.png').convert_alpha(),pos,[all_sprites,obstacle_sprites])

for file_name, pos_list in LONG_OBJECTS.items():
	for pos in pos_list:
		LongSprite(pygame.image.load(f'./graphics/objects/long/{file_name}.png').convert_alpha(),pos,[all_sprites,obstacle_sprites])

game_state = 0
player_score = 0
paging_direction = 0
key_pressed = ''
has_new_life = False
new_game_state = game_state
# game loop
while True:
	# event loop 
	for event in pygame.event.get():
		if event.type == pygame.QUIT or (event.type == pygame.KEYUP and event.key == pygame.K_ESCAPE):
			pygame.quit()
			sys.exit()

		if event.type == pygame.TEXTINPUT:
			if game_state == 4:
				key_pressed = event.text
		elif event.type == pygame.KEYUP and event.key == pygame.K_BACKSPACE:
			if game_state == 4:
				key_pressed = '\b'
		elif event.type == pygame.KEYUP and event.key == pygame.K_RETURN:
			if game_state == 4:
				key_pressed = '\r'
		elif event.type == pygame.KEYUP and event.key == pygame.K_F10:
			if game_state == 0 or game_state == 2:
				game_state = 5
			elif game_state == 5:
				game_state = 0
		elif game_state in [0, 2, 5] and event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
			if game_state in [0, 5]: #new game
				player.lives = 3
				player.score = 0
				player_score = 0
				scorekeeper.current_page = 0
			player.pos.x = 2062
			player.pos.y = 3274
			game_state = 1
		elif event.type == pygame.MOUSEWHEEL:
			if game_state == 5:
				paging_direction = event.y
		
		if event.type == car_timer and game_state == 1:
			random_pos = choice(CAR_START_POSITIONS)
			if random_pos not in pos_list:
				pos_list.append(random_pos)
				pos = (random_pos[0],random_pos[1] + randint(-8,8))
				Car(pos,[all_sprites,obstacle_sprites], 1 if pos[0] < 200 else -1, int(300 + round(10 * player.level * 0.49)))
			if len(pos_list) > 5:
				del pos_list[0]
	# delta time 
	dt = clock.tick(120) / 1000

	# draw a bg
	display_surface.fill('black')
	if game_state == 1:
		if player.pos.y >= 1180:
			level_score = player.level * (3274 - int(player.pos.y))
			player.score = player_score + level_score
			# update 
			all_sprites.update(dt)

			# draw
			all_sprites.customize_draw()
			score = font.render(f'Score: {player.score}', True, 'White')
			score_rect = score.get_rect(bottomleft = (20, WINDOW_HEIGHT-20))
			display_surface.blit(score,score_rect)

			level = font.render(f'Level: {player.level}', True, 'White')
			level_rect = level.get_rect(bottomleft = (WINDOW_WIDTH/2, WINDOW_HEIGHT-20))
			display_surface.blit(level, level_rect)

			lives = font.render(f'Lives: {player.lives}', True, 'White')
			lives_rect = lives.get_rect(bottomright = (WINDOW_WIDTH-20, WINDOW_HEIGHT-20))
			display_surface.blit(lives, lives_rect)
		else: 
			game_state = 2
			player.level += 1
			player_score = player.score
			has_new_life = True
		
		if player.lives <= 0:
			game_state = 4

	elif game_state == 2:
		display_surface.blit(text_surf,text_rect)
		if player.level % 3 == 1 and has_new_life:
			player.lives += 1
			has_new_life = False
			pygame.time.set_timer(car_timer, 100-player.level)
			
	elif game_state == 0:
		display_surface.blit(game_over,game_over_rect)
	elif game_state == 4:
		if scorekeeper.draw_input(display_surface, current_score=player.score, key_pressed=key_pressed):
			game_state = 5
		key_pressed = ''
	elif game_state == 5:
		scorekeeper.draw_scores(display_surface, page=paging_direction, current_score=player.score)
		paging_direction = 0

	# update the display surface
	pygame.display.update()