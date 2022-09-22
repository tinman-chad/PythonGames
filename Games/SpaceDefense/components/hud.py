from pygame.draw import rect
from pygame import Surface
from pygame.font import Font


class HUD:
    def __init__(self, font : str, lives_image : Surface, pos : tuple[int, int], draw_surface : Surface):
        self.font = Font(font, 50)
        self.hs_font = Font(font,20)
        self.lives = lives_image
        self.lives_rect = self.lives.get_rect(topleft = (10, pos[1]))
        self.life_size = lives_image.get_size()
        self.draw_surface = draw_surface
        self.pos = pos
        self.high_score = 0
        


    def display(self, lives : int, score : int):
		# exercise: recreate the original display_score function inside of a class
		# actually call it in the game loop
        if score > self.high_score:
            self.high_score = score

        score_text = f'Score: {score}'
        text_surf = self.font.render(score_text,True,(255,255,255))
        text_rect = text_surf.get_rect(midbottom = self.pos)
        self.draw_surface.blit(text_surf,text_rect)
        rect(
			self.draw_surface, 
			(255,255,255),
			text_rect.inflate(30,30), 
			width = 8, 
			border_radius = 5
		)
        for life in range(1, lives+1):
            self.draw_surface.blit(self.lives,((10 + self.life_size[0])*life, self.pos[1]))

        hs_surf = self.hs_font.render(f'High Score: {self.high_score}', True, (200, 200, 200))
        hs_rect = hs_surf.get_rect(topleft = (10, 10))
        self.draw_surface.blit(hs_surf, hs_rect)
