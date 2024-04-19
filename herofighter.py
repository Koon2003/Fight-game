import pygame
from player import Player

class HeroFighter(Player):
	def __init__(self, x, y, flip, data, sprite_sheet, animation_steps, player, sound_list):
		super().__init__(x, y, flip, data, sprite_sheet, animation_steps, player, sound_list)
		self.dashing = False
		self.attack_width = 2.2

	def move(self, screen, screen_width, screen_height, target, round_over):
		SPEED = 15
		GRAVITY = 2
		dx = 0
		dy = 0
		self.running = False
		self.dashing = False
		self.attack_type = 0

		# Get keypresses
		key = pygame.key.get_pressed()
		if self.attacking == False and self.alive == True and round_over == False:
			# Kiểm tra người chơi
			if self.player == 1:
				# Move
				if key[pygame.K_a]:
					dx = -SPEED
					self.running = True
				if key[pygame.K_d]:
					dx = SPEED
					self.running = True
				# Jump
				if key[pygame.K_w] and self.jumping == False:
					self.sound_list[1].play()
					self.vel_y = -25
					self.jumping = True
				# Attack
				if key[pygame.K_j]:
					self.attack(screen, target)
				# Dash
				if key[pygame.K_k]:
					if self.flip == False:
						dx = SPEED * 2
					else:
						dx = -(SPEED * 2)
					self.dashing = True
			if self.player == 2:
				# Move
				if key[pygame.K_LEFT]:
					dx = -SPEED
					self.running = True
				if key[pygame.K_RIGHT]:
					dx = SPEED
					self.running = True
				# Jump
				if key[pygame.K_UP] and self.jumping == False:
					self.sound_list[1].play()
					self.vel_y = -25
					self.jumping = True
				# Attack
				if key[pygame.K_KP_1]:
					self.attack(screen, target)
				# Dash
				if key[pygame.K_KP2]:
					if self.flip == False:
						dx = SPEED * 2
					else:
						dx = -(SPEED * 2)
					self.dashing = True

		# Cập nhật vel_y và dy
		self.vel_y += GRAVITY
		dy += self.vel_y

		# Đảm bảo người  không ra khỏi màn 
		if self.rect.left + dx < 0:
			dx = -self.rect.left
		if self.rect.right + dx > screen_width:
			dx = screen_width - self.rect.right
		if self.rect.bottom + dy > screen_height - 60:
			self.vel_y = 0
			self.jumping = False
			dy = screen_height - 60 - self.rect.bottom

		# Đảm bảo người chơi đối mặt với nhau
		if target.rect.centerx > self.rect.centerx:
			self.flip = False
		else:
			self.flip = True

		# Cập nhật attack cooldown
		if self.attack_cooldown > 0:
			self.attack_cooldown -= 1

		# Cập nhật vị trí người chơi
		self.rect.x += dx
		self.rect.y += dy

	def update(self):
		if self.health <= 0:
			self.health = 0
			self.alive = False
			self.update_action(5)
		elif self.dashing == True:
			self.update_action(7)
		elif self.hit == True:
			self.update_action(4)
		elif self.attacking == True:
			self.update_action(6)
		elif self.jumping == True:
			if self.vel_y <= 0:
				self.update_action(2)
			else:
				self.update_action(3)
		elif self.running == True:
			self.update_action(1)
		else:
			self.update_action(0)
		animation_cooldown = 50
		self.image = self.animation_list[self.action][self.frame_index]
		if pygame.time.get_ticks() - self.update_time > animation_cooldown:
			self.frame_index += 1
			self.update_time = pygame.time.get_ticks()
		if self.frame_index >= len(self.animation_list[self.action]) - 1:
			if self.alive == False:
				self.frame_index = len(self.animation_list[self.action]) - 1
			else:
				self.frame_index = 0
				if self.action == 6:
					self.attacking = False
					self.attack_cooldown = 20
				if self.action == 4:
					self.hit = False
					self.attacking = False
					self.attack_cooldown = 5

	def draw(self, screen):
		img = pygame.transform.flip(self.image, self.flip,False)
		#pygame.draw.rect(screen, (255, 0, 0), self.rect)
		screen.blit(img, (self.rect.x - (self.offset[0] * self.image_scale), self.rect.y - (self.offset[1] * self.image_scale)))		
