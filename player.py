import pygame

class Player():
	def __init__(self, x, y, flip, data, sprite_sheet, animation_steps, player, sound_list):
		self.player = player
		self.size = data[0]
		self.image_scale = data[1]
		self.offset = data[2]
		self.update_time = pygame.time.get_ticks()
		# Animations
		self.animation_list = self.load_images(sprite_sheet, animation_steps)
		self.action = 0
		self.frame_index = 0
		self.image = self.animation_list[self.action][self.frame_index]
		self.rect = pygame.Rect((x, y, 80, 180))
		# Action
		self.running = False
		self.jumping = False
		self.attacking = False
		self.attack_type = 0
		self.attack_cooldown = 0
		self.hit = False
		self.flip = flip
		self.alive = True
		self.health = 100
		self.vel_y = 0
		# Sound
		self.sound_list = sound_list

	def load_images(self, sprite_sheet, animation_steps):
		# Trích xuất images từ sprite sheet
		animation_list = []
		for y, animation in enumerate(animation_steps):
			temp_image_list = []
			for x in range(animation):
				temp_image = sprite_sheet.subsurface(x * self.size, y * self.size, self.size, self.size)
				temp_image_list.append(pygame.transform.scale(temp_image, (self.size * self.image_scale, self.size * self.image_scale)))
			animation_list.append(temp_image_list)
		return animation_list

	def attack(self, screen, target):
		if self.attack_cooldown == 0:
			self.attacking = True
			self.sound_list[0].play()
			if self.flip == False:
				attack_rect = pygame.Rect(self.rect.right, self.rect.y, self.rect.width * self.attack_width, self.rect.height)
			else:
				attack_rect = pygame.Rect(self.rect.x - self.rect.width * self.attack_width, self.rect.y, self.rect.width * self.attack_width, self.rect.height)
			if attack_rect.colliderect(target.rect):
				target.health -= 10
				target.hit = True
				target.sound_list[2].play()
			#pygame.draw.rect(screen, (0, 255, 0), attack_rect)

	def update_action(self, new_action):
		# Kiểm tra xem hành động mới có khác với hành động trước không
		if new_action != self.action:
			self.action = new_action
			# Cập nhật 
			self.frame_index = 0
			self.update_time = pygame.time.get_ticks()

