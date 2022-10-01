from dis import dis
import pygame, sys
from pygame import Surface
from pygame.transform import scale
from random import randint, uniform
from components.ship import Ship
from components.meteor import Meteor, meteor_death_event
from components.hud import HUD
from utils.scorekeeper import ScoreKeeper
from pathlib import Path

def playGame(screen: Surface, ship: Ship) -> int:
	# update
	spaceship_group.update()
	laser_group.update()
	meteor_group.update()

	# score
	score.display(ship.lives, ship.score)

	# graphics 
	if ship.time_to_life <= 0:
		spaceship_group.draw(screen)
	laser_group.draw(screen)
	meteor_group.draw(screen)
	if ship.lives <= 0:
		if ship.score <= 0:
			return 2
		return 4 #game over save score.
	return 1

# basic setup
font_file = './graphics/subatomic.ttf'
pygame.init()

scores_font = pygame.font.Font(font_file, 20)
scorekeeper = ScoreKeeper('SpaceDefense', True, Path('./scores.db'), scores_font, (125, 125, 125), 'Press Space Key For New Game')

WINDOW_WIDTH, WINDOW_HEIGHT = 1280, 720 
display_surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption('Space shooter')
clock = pygame.time.Clock()

game_font = pygame.font.Font(font_file,50)
height = game_font.get_height() + 5
# grpahics 
background_surf = pygame.image.load('./graphics/background.png').convert()
ship_image = pygame.image.load('./graphics/ship.png').convert_alpha()
laser_image = pygame.image.load('./graphics/laser.png').convert_alpha()
meteor_image = pygame.image.load('./graphics/meteor.png').convert_alpha()
#sounds
bg_music = pygame.mixer.Sound('./sounds/music.wav')
laser_sound = pygame.mixer.Sound('./sounds/laser.ogg')
explosion_sound = pygame.mixer.Sound('./sounds/explosion.wav')

# sprite groups 
spaceship_group = pygame.sprite.GroupSingle()
laser_group = pygame.sprite.Group()
meteor_group = pygame.sprite.Group()

# sprite creation 
ship = Ship(spaceship_group, ship_image, (WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2), laser_image, laser_sound, explosion_sound, laser_group=laser_group, meteor_group=meteor_group)

# timer 
meteor_timer = pygame.event.custom_type()
pygame.time.set_timer(meteor_timer,200)

# score 
score = HUD(font = font_file, lives_image = scale(ship_image, (20,20)), pos = (WINDOW_WIDTH / 2, WINDOW_HEIGHT - 80), draw_surface = display_surface)

# music play
#bg_music.play(loops = 2, fade_ms = 50)
game_state = 0
key_pressed = ''
paging_direction = 0
# game loop
while True:
	# event loop
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			pygame.quit()
			sys.exit()

		if event.type == pygame.TEXTINPUT:
			if game_state == 4:
				print(event.__dict__)
				key_pressed = event.text
		elif event.type == pygame.KEYUP and event.key == pygame.K_BACKSPACE:
			if game_state == 4:
				key_pressed = '\b'
		elif event.type == pygame.KEYUP and event.key == pygame.K_RETURN:
			if game_state == 4:
				key_pressed = '\r'
		elif event.type == pygame.KEYUP and event.key == pygame.K_SPACE:
			if game_state == 0 or game_state == 2 or game_state == 5:
				ship.lives = 3
				ship.score = 0
				laser_group.empty()
				meteor_group.empty()
				game_state = 1
				scorekeeper.current_page = 0
			elif game_state == 1:
				game_state = 3 #pause game
			elif game_state == 3:
				game_state = 1 #resume game
		elif event.type == pygame.KEYUP and event.key == pygame.K_F10:
			if game_state == 0 or game_state == 2:
				game_state = 5
			elif game_state == 5:
				game_state = 0
		elif event.type == pygame.MOUSEWHEEL:
			if game_state == 5:
				paging_direction = event.y

		if event.type == meteor_death_event and game_state == 1:
			ship.score += 10
		if event.type == meteor_timer and game_state == 1:
			meteor_y_pos = randint(-150,-50)
			meteor_x_pos = randint(-100, WINDOW_WIDTH+100)
			Meteor(groups = meteor_group, pos = (meteor_x_pos, meteor_y_pos), image = meteor_image, speed = randint(400, 600), direction = uniform(-0.5, 0.5), size = randint(1, 3), rotation_speed = randint(20, 50), max_y = WINDOW_HEIGHT)

	# delta time 
	dt = clock.tick(120) / 1000
	#print(f'frame speed: {dt}')
	# background 
	display_surface.blit(background_surf,(0,0))

	if game_state == 1: #playing the game
		game_state = playGame(display_surface, ship)
	elif game_state == 2: #game over no high scores
		game_over_text = f'GAME OVER!'
		game_over_text_surf = game_font.render(game_over_text,True,(255,255,255))
		game_over_text_rect = game_over_text_surf.get_rect(midbottom = (WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2))
		display_surface.blit(game_over_text_surf,game_over_text_rect)
		game_over_text = 'PRESS SPACE KEY TO START'
		game_over_text_surf = game_font.render(game_over_text,True,(255,255,255))
		game_over_text_rect = game_over_text_surf.get_rect(midbottom = (WINDOW_WIDTH / 2, (WINDOW_HEIGHT / 2)+height))
		display_surface.blit(game_over_text_surf,game_over_text_rect)
		game_over_text = 'F10 FOR LEADERBOARD'
		game_over_text_surf = game_font.render(game_over_text,True,(255,255,255))
		game_over_text_rect = game_over_text_surf.get_rect(midbottom = (WINDOW_WIDTH / 2, (WINDOW_HEIGHT / 2)+(height*2)))
		display_surface.blit(game_over_text_surf,game_over_text_rect)
	elif game_state == 0: #freshly loaded game, not played yet.
		game_over_text = 'PRESS SPACE KEY TO START'
		game_over_text_surf = game_font.render(game_over_text,True,(255,255,255))
		game_over_text_rect = game_over_text_surf.get_rect(midbottom = (WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2))
		display_surface.blit(game_over_text_surf,game_over_text_rect)
		game_over_text = 'F10 FOR LEADERBOARD'
		game_over_text_surf = game_font.render(game_over_text,True,(255,255,255))
		game_over_text_rect = game_over_text_surf.get_rect(midbottom = (WINDOW_WIDTH / 2, (WINDOW_HEIGHT / 2)+height))
		display_surface.blit(game_over_text_surf,game_over_text_rect)
		
	elif game_state == 4: # high score name entry
		scorekeeper.draw_input(display_surface, ship.score, key_pressed)
		if key_pressed == '\r':
			game_state = 5
		key_pressed = ''
	elif game_state == 5: # display high score list
		scorekeeper.draw_scores(display_surface, page=paging_direction, current_score=ship.score)
		paging_direction = 0
	elif game_state == 3: 
		game_over_text = f'PRESS SPACE KEY TO RESUME!'
		game_over_text_surf = game_font.render(game_over_text,True,(255,255,255))
		game_over_text_rect = game_over_text_surf.get_rect(midbottom = (WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2))
		display_surface.blit(game_over_text_surf,game_over_text_rect)
	# draw the frame 
	pygame.display.update()
