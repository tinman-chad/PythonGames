import pygame, sys
from pygame.transform import scale
from random import randint, uniform
from components.ship import Ship
from components.meteor import Meteor, meteor_death_event
from components.hud import HUD

#should probably put this in a score tracking class so I can re-use it once I get there so pass in the font path and path to sqlite3 db????
def is_high_score(score : int) -> bool:
	'''Lookup to database if this is a high score (do I want to track by user?)'''
	return False

def render_high_score_list():
	'''Need to render each high score (say limit top 5) one per line onto screen until spacebar is pressed.'''
	pass

def render_high_score_entry(score : int):
	'''Render and accept text input for user name'''
	pass

# basic setup
font_file = './graphics/subatomic.ttf'
pygame.init()
WINDOW_WIDTH, WINDOW_HEIGHT = 1280, 720 
display_surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption('Space shooter')
clock = pygame.time.Clock()

game_font = pygame.font.Font(font_file,50)
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
# game loop
while True:

	# event loop
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			pygame.quit()
			sys.exit()
		if event.type == pygame.KEYUP and event.key == pygame.K_SPACE and game_state == 0: # fresh load
			game_state = 1
		if event.type == pygame.KEYUP and event.key == pygame.K_SPACE and game_state == 2: #game over reset lives and score
			ship.lives = 3
			ship.score = 0
			laser_group.empty()
			meteor_group.empty()
			game_state = 3
		if event.type == pygame.KEYUP and game_state == 2 and event.key == pygame.K_PAUSE:
			game_state = 5
		if event.type == meteor_death_event and game_state == 1:
			ship.score += 10
		if event.type == meteor_timer and game_state == 1:
			meteor_y_pos = randint(-150,-50)
			meteor_x_pos = randint(-100, WINDOW_WIDTH+100)
			Meteor(groups = meteor_group, pos = (meteor_x_pos, meteor_y_pos), image = meteor_image, speed = randint(400, 600), direction = uniform(-0.5, 0.5), size = randint(1, 3), rotation_speed = randint(20, 50), max_y = WINDOW_HEIGHT)

	# delta time 
	dt = clock.tick(40) / 1000
	#print(f'frame speed: {dt}')
	# background 
	display_surface.blit(background_surf,(0,0))
	if game_state == 1:
		# update
		spaceship_group.update()
		laser_group.update()
		meteor_group.update()

		# score
		score.display(ship.lives, ship.score)

		# graphics 
		if ship.time_to_life <= 0:
			spaceship_group.draw(display_surface)
		laser_group.draw(display_surface)
		meteor_group.draw(display_surface)
		if ship.lives <= 0:
			if is_high_score(ship.score):
				game_state = 4
			else:
				game_state = 2
	elif game_state == 2:
		game_over_text = f'GAME OVER!'
		game_over_text_surf = game_font.render(game_over_text,True,(255,255,255))
		game_over_text_rect = game_over_text_surf.get_rect(midbottom = (WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2))
		display_surface.blit(game_over_text_surf,game_over_text_rect)
	elif game_state == 0:
		game_over_text = f'PRESS ANY KEY TO START!'
		game_over_text_surf = game_font.render(game_over_text,True,(255,255,255))
		game_over_text_rect = game_over_text_surf.get_rect(midbottom = (WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2))
		display_surface.blit(game_over_text_surf,game_over_text_rect)
	elif game_state == 4: # placeholder for high score name entry
		print('Save high score')
		game_state = 1
	elif game_state == 5: # placeholder for high score list
		print('show high score list')
		game_state = 1
	elif game_state == 3:
		game_state = 1
	# draw the frame 
	pygame.display.update()
