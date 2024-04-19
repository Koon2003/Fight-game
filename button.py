import pygame

class ButtonText():
	def __init__(self, x, y, text_input, font, base_color, hovering_color, image_colllidepoint):
		self.font = font
		self.base_color, self.hovering_color = base_color, hovering_color
		self.text_input = text_input
		self.text = self.font.render(self.text_input, True, self.base_color)
		self.rect = self.text.get_rect()
		self.rect.center = (x, y)
		self.image_colllidepoint = pygame.transform.scale(image_colllidepoint, (self.rect.height - 10, self.rect.height - 10))

	def update(self, screen):
		#pygame.draw.rect(screen, (0, 0, 0), self.rect)
		screen.blit(self.text, self.rect)

	def checkForInput(self, pos):
		if self.rect.collidepoint(pos):
			return True
		return False

	def changeColor(self, screen, pos):
		if self.rect.collidepoint(pos):
			self.text = self.font.render(self.text_input, True, self.hovering_color)
			screen.blit(self.image_colllidepoint, (self.rect.x - self.rect.height + 5, self.rect.y + 10))
		else:
			self.text = self.font.render(self.text_input, True, self.base_color)

class Button():
	def __init__(self, x, y, image, image_X=None):
		self.image_base = image
		self.image = pygame.transform.scale(self.image_base, (55, 55))
		self.rect = self.image.get_rect()
		self.rect.topleft = (x, y)
		self.image_V, self.image_X = image, None
		if image_X is not None:
			self.image_X = image_X
			self.choose = True

	def update(self, screen):
		#pygame.draw.rect(screen, (255, 255, 255), self.rect)
		screen.blit(self.image, self.rect)

	def checkForInput(self, pos):
		if self.rect.collidepoint(pos):
			if self.image_X is not None:
				if self.choose == True:
					self.choose = False
					self.image_base = self.image_X
				else:
					self.choose = True
					self.image_base = self.image_V
			return True
		return False

	def changeColor(self, screen, pos):
		if self.rect.collidepoint(pos):
			self.image = pygame.transform.scale(self.image_base, (50, 50))
		else:
			self.image = pygame.transform.scale(self.image_base, (55, 55))			

class ButtonChoose():
	def __init__(self, x, y, image, base_color, hovering_color, data, number_player, font):
		self.image = image
		self.rect = pygame.Rect(x, y, 200, 320)
		self.base_color, self.hovering_color = base_color, hovering_color
		self.color = self.base_color
		self.scale = data[1]
		self.offset = data[2]
		self.choose = False
		self.font = font
		self.player = number_player

	def draw_text(self, text, font, x, y, screen):
		img = font.render(text, True, self.hovering_color)
		screen.blit(img, (x, y)) 

	def update(self, screen):
		pygame.draw.rect(screen, self.color, self.rect, 3, 0, 0, 4)
		screen.blit(self.image, (self.rect.x - (self.offset[0] * self.scale) + 60, self.rect.y - (self.offset[1] * self.scale) + 60))
		if self.choose == True:
			self.draw_text("Player " + str(self.player), self.font, self.rect.x + 15, self.rect.y + self.rect.height + 10, screen)

	def checkForInput(self, pos):
		if self.choose == False:
			if self.rect.collidepoint(pos):
				self.choose = True
				return True
		return False

	def changeColor(self, screen, pos):
		if self.choose == False:
			if self.rect.collidepoint(pos):
				self.color = self.hovering_color
				self.draw_text("Player " + str(self.player), self.font, self.rect.x + 15, self.rect.y + self.rect.height + 10, screen)
			else:
				self.color = self.base_color