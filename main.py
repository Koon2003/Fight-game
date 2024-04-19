import pygame, sys
from pygame import mixer
from button import ButtonText, Button, ButtonChoose
from herofighter import HeroFighter
from hunter import Hunter
from samurai import Samurai
from king import King

mixer.init()
pygame.init()

# Tạo cửa sổ hiển thị
SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

# Icon and Caption
pygame.display.set_caption("Game Fighter")
icon = pygame.image.load("image/icon/helmet.ico")
pygame.display.set_icon(icon)

# Đặt tốc độ khung hình
clock = pygame.time.Clock()
FPS = 60

# Âm thanh
volume_sound = 0.25
pygame.mixer.music.load('sound/soundtrack/play game music.mp3')
pygame.mixer.music.set_volume(0.25)
pygame.mixer.music.play(-1, 0.0, 500)
sound_list = [pygame.mixer.Sound("sound/motion sound/fast_sword.wav"), pygame.mixer.Sound("sound/motion sound/jump.wav"), pygame.mixer.Sound("sound/motion sound/take_hit.wav")]
for sound in sound_list:
	sound.set_volume(volume_sound)

# Màu sắc
WHITE = (255, 255, 255)
DARK_CYAN = (0, 139, 139)
DARK_RED = (139, 0, 0)
DARK_GREEN = (0, 100, 0)
SILVER = (192, 192, 192)
BLACK = (0, 0, 0)
GRAY = (128, 128, 128)

# Tải Background Home
BG_home_images = []
image_collidepoint = pygame.image.load("image/icon/swords.png").convert_alpha()
BG_play_game = pygame.transform.scale(pygame.image.load("image/background home/bg_play_game.png").convert_alpha(), (SCREEN_WIDTH, SCREEN_HEIGHT))
# Loop load images
for i in range(11, -1, -1):
	bg_image = pygame.image.load(f"image/background home/Layer_{i}.png").convert_alpha()
	bg_image_scale = pygame.transform.scale(bg_image, (SCREEN_WIDTH, SCREEN_HEIGHT))
	temp_image = bg_image_scale.subsurface(0, 180, SCREEN_WIDTH, SCREEN_HEIGHT - 180)
	temp_image_scale = pygame.transform.scale(temp_image, (SCREEN_WIDTH, SCREEN_HEIGHT))
	BG_home_images.append(temp_image_scale)

# Xác định biến Home
bg_home_width = BG_home_images[0].get_width()
scroll = 0

# Hàm vẽ Background Home
def draw_bg_home():
	global scroll
	for x in range(5):
		speed = 0.001
		for image in BG_home_images:
			screen.blit(image, ((x * bg_home_width) - scroll * speed, 0))
			scroll += 5
			speed += 0.001
	if scroll > 300000:
		scroll = 0

# Hàm tạo phông chữ với kích thước
def get_font(size, type):
	if type == 1:
		return pygame.font.Font("font/8-BIT WONDER.TTF", size)
	if type == 2:
		return pygame.font.Font("font/KOMIKAX_.ttf", size)

#---------------------------------------Play_game--------------------------------------------------
# Xác định các biến giá trị của các nhân vật
# kích thước, tỷ lệ, offset
KNIGHT_DATA = [140, 4.6, [60, 43]]
knight_sheet = pygame.image.load("image/Hero Knight 2/Sprites/hero knight 2.png").convert_alpha()
KNIGHT_ANIMATIONS = [11, 8, 4, 4, 4, 9, 6, 4]

HUNTER_DATA = [150, 4.6, [67, 57]]
hunter_sheet = pygame.image.load("image/Hunter/Sprites/huntress.png").convert_alpha()
HUNTER_ANIMATIONS = [8, 8, 2, 2, 3, 8, 5, 5, 7]

SAMURAI_DATA = [200, 3.6, [93, 73]]
samurai_sheet = pygame.image.load("image/Samurai/Sprites/samurai.png").convert_alpha()
SAMURAI_ANIMATIONS = [4, 8, 2, 2, 3, 7, 4, 4]

KING_DATA = [160, 4, [73, 53]]
king_sheet = pygame.image.load("image/King/Sprites/king.png").convert_alpha()
KING_ANIMATIONS = [8, 8, 2, 2, 4, 6, 4, 4, 4]

#1:hero_knight #2:hunter #3:samurai   #4:king
PLAYER = [0, 0]
player_name = ["KNIGHT", "HUNTER", "SAMURAI", "KING"]

# Hàm xác định người chơi
def define_player(number_player, flip, x, y):
	if PLAYER[number_player - 1] == 1:
		return HeroFighter(x, y, flip, KNIGHT_DATA, knight_sheet, KNIGHT_ANIMATIONS, number_player, sound_list)
	elif PLAYER[number_player - 1] == 2:
		return Hunter(x, y, flip, HUNTER_DATA, hunter_sheet, HUNTER_ANIMATIONS, number_player, sound_list)
	elif PLAYER[number_player - 1] == 3:
		return Samurai(x, y, flip, SAMURAI_DATA, samurai_sheet, SAMURAI_ANIMATIONS, number_player, sound_list)
	elif PLAYER[number_player - 1] == 4:
		return King(x, y, flip, KING_DATA, king_sheet, KING_ANIMATIONS, number_player, sound_list)
# Hàm vẽ thanh máu
def draw_health_bar(health, x, y):
	ratio = health / 100
	pygame.draw.rect(screen, SILVER, (x - 2, y - 2, 404, 34))
	pygame.draw.rect(screen, DARK_RED, (x, y, 400, 30))
	pygame.draw.rect(screen, DARK_GREEN, (x, y, ratio * 400, 30))
# Hàm hiển thị chữ
def draw_text(text, font, color, x, y):
	text = font.render(text, True, color)
	text_rect = text.get_rect()
	text_rect.center = (x, y)
	screen.blit(text, text_rect) 

def play_game():
	# Đếm ngược
	intro_count = 5
	last_count_update = pygame.time.get_ticks()

	# Các giá trị Game over
	game_over = False
	round_over = False
	round_over_time = 0
	round_win = [0, 0]
	round_num = 1
	ROUND_OVER_COOLDOWN = 2000

	# Thời gian của 1 round
	time_per_round = 99
	last_time_update = pygame.time.get_ticks()

	# Phông chữ 
	count_font = get_font(100, 2)
	round_num_font = get_font(70, 2)
	player_name_font = get_font(25, 2)
	time_font = get_font(50, 2)
	win_font = get_font(35, 2)
	game_win_font = get_font(65, 2)

	# Khởi tạo người chơi
	player_1 = define_player(1, False, 200, 360)
	player_2 = define_player(2, True, 700, 360)

	# Khởi tạo các nút
	HOME_BUTTON = Button(370, 310, pygame.image.load("image/button/Home.png").convert_alpha())
	REMATCH_BUTTON = Button(470, 310, pygame.image.load("image/button/Rematch.png").convert_alpha())
	OPTION_BUTTON = Button(570, 310, pygame.image.load("image/button/Settings.png").convert_alpha())

	while True:
		clock.tick(FPS)

		# Vẽ background
		screen.blit(BG_play_game, (0, 0))

		# Vị trí chuột
		MOUSE_POS = pygame.mouse.get_pos()

		# Hiển thị thanh máu của người chơi
		draw_health_bar(player_1.health, 20, 20)
		draw_health_bar(player_2.health, SCREEN_WIDTH - 420, 20) 
		# Hiển thị tên nhân vậ
		draw_text(player_name[PLAYER[0] - 1], player_name_font, WHITE, 65, 65)
		draw_text(player_name[PLAYER[1] - 1], player_name_font, WHITE, SCREEN_WIDTH - 12 * len(player_name[PLAYER[1] - 1]), 65)


		if game_over == False:
			# Đếm ngược
			if intro_count <= 0:
				# Cập nhật di chuyển người chơi
				player_1.move(screen, SCREEN_WIDTH, SCREEN_HEIGHT, player_2, round_over)
				player_2.move(screen, SCREEN_WIDTH, SCREEN_HEIGHT, player_1, round_over)
				if round_over == False:
					# Cập nhật thời gian 1 round
					draw_text(str(time_per_round), time_font, WHITE, SCREEN_WIDTH/2, 30)
					if (pygame.time.get_ticks() - last_time_update) >= 1000:
						time_per_round -= 1
						last_time_update = pygame.time.get_ticks()
				else:
					draw_text(str(time_per_round), time_font, WHITE, SCREEN_WIDTH/2, 30)
			elif intro_count == 1:
				draw_text("FIGHT", count_font, WHITE, SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)
				if (pygame.time.get_ticks() - last_count_update) >= 1000:
					intro_count -= 1
					last_count_update = pygame.time.get_ticks()
					last_time_update = pygame.time.get_ticks()
			elif intro_count == 5:
				draw_text("ROUND " + str(round_num), round_num_font, WHITE, SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)
				if (pygame.time.get_ticks() - last_count_update) >= 1000:
					intro_count -= 1
					last_count_update = pygame.time.get_ticks()
			else:
				# Cập nhật thời gian đếm ngược
				draw_text(str(intro_count - 1), count_font, WHITE, SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)
				if (pygame.time.get_ticks() - last_count_update) >= 1000:
					intro_count -= 1
					last_count_update = pygame.time.get_ticks()

		# Cập nhật người chơi
		player_1.update()
		player_2.update()
		# Hiển thị người chơi
		player_1.draw(screen)
		player_2.draw(screen)

		if game_over == False:
			# Kiểm tra người chơi đã die hay chưa
			if round_over == False:
				if player_1.alive == False:
					round_win[1] += 1
					round_over = True
					round_over_time = pygame.time.get_ticks()
				elif player_2.alive == False:
					round_win[0] += 1
					round_over = True
					round_over_time = pygame.time.get_ticks()
			else:
				# Hiển thị người chơi chiến thắng
				if player_1.alive == True:
					draw_text("victory", win_font, (255, 215 , 0), player_1.rect.centerx, player_1.rect.y - 50)
				elif player_2.alive == True:
					draw_text("victory", win_font, (255, 215 , 0), player_2.rect.centerx, player_2.rect.y - 50)
				# Cập nhật round mới
				if pygame.time.get_ticks() - round_over_time > ROUND_OVER_COOLDOWN:
					round_over = False
					intro_count = 5
					round_num += 1
					round_over_time = pygame.time.get_ticks()
					last_count_update = pygame.time.get_ticks()
					time_per_round = 99
					player_1 = define_player(1, False, 200, 360)
					player_2 = define_player(2, True, 700, 360)

		# Nếu 1 trong 2 người chơi win 2 round trước thì game over			
		if round_win[0] == 2 or round_win[1] == 2:
			game_over = True

		# Hiển thị người chơi win game và các nút 
		if game_over == True:
			pygame.draw.rect(screen, BLACK, (202, 202, 595, 195))
			pygame.draw.rect(screen, (0, 128, 128), (200, 200, 600, 200), 5, 0, 0, 6)
			if round_win[0] == 2:
				draw_text(player_name[PLAYER[0] - 1] + " WIN", game_win_font, (255, 215 , 0), 500, 250)
			if round_win[1] == 2:
				draw_text(player_name[PLAYER[1] - 1] + " WIN", game_win_font, (255, 215 , 0), 500, 250)
			# Cập nhật trạng thái các nút	
			for button in [HOME_BUTTON, REMATCH_BUTTON, OPTION_BUTTON]:
				button.changeColor(screen, MOUSE_POS)
				button.update(screen)

		for event in pygame.event.get():
			# Thoát game
			if event.type == pygame.QUIT:
				pygame.quit()
				sys.exit()
			if event.type == pygame.MOUSEBUTTONDOWN:
				if HOME_BUTTON.checkForInput(MOUSE_POS):
					home()
				if REMATCH_BUTTON.checkForInput(MOUSE_POS):
					play_game()
				if OPTION_BUTTON.checkForInput(MOUSE_POS):
					options_start()
				
		pygame.display.update()

#---------------------------------------Choose_player-------------------------------------------------
def choose_player():
	number_player = 1

	# Hình ảnh nhân vật
	knight_image = pygame.transform.scale(knight_sheet.subsurface(0, 0, KNIGHT_DATA[0], KNIGHT_DATA[0]),(KNIGHT_DATA[0]*4.6, KNIGHT_DATA[0]*4.6))
	hunter_image = pygame.transform.scale(hunter_sheet.subsurface(0, 0, HUNTER_DATA[0], HUNTER_DATA[0]), (HUNTER_DATA[0]*4.6, HUNTER_DATA[0]*4.6))
	samurai_image = pygame.transform.scale(samurai_sheet.subsurface(0, 0, SAMURAI_DATA[0], SAMURAI_DATA[0]), (SAMURAI_DATA[0]*3.6, SAMURAI_DATA[0]*3.6))
	king_image = pygame.transform.scale(king_sheet.subsurface(0, 0, KING_DATA[0], KING_DATA[0]), (KING_DATA[0]*4.1, KING_DATA[0]*4.1))

	# khởi tạo các nút
	START_BUTTON = ButtonText(500, 535, "START", get_font(50, 1), WHITE, DARK_CYAN, image_collidepoint)
	BACK_BUTTON = Button(40, 30, pygame.image.load("image/button/Back.png").convert_alpha())

	KNIGHT_BUTTON = ButtonChoose(100, 130, knight_image, WHITE, DARK_CYAN, KNIGHT_DATA, number_player, get_font(25, 1))
	HUNTER_BUTTON = ButtonChoose(310, 130, hunter_image, WHITE, DARK_CYAN, HUNTER_DATA, number_player, get_font(25, 1))
	SAMURAI_BUTTON = ButtonChoose(520, 130, samurai_image, WHITE, DARK_CYAN, SAMURAI_DATA, number_player, get_font(25, 1))
	KING_BUTTON = ButtonChoose(730, 130, king_image, WHITE, DARK_CYAN, KING_DATA, number_player, get_font(25, 1))
	
	while True:
		# Hiển thị background 
		screen.fill((0, 0, 0))
		draw_text("CHOOSE FIGHTER", get_font(65, 1), DARK_CYAN, 540, 50)

		# Vị trí chuột
		MOUSE_POS = pygame.mouse.get_pos()

		# Cập nhật trạng thái các nút 
		for button in [START_BUTTON, BACK_BUTTON]:
			button.changeColor(screen, MOUSE_POS)
			button.update(screen)

		for button_choose_player in [KNIGHT_BUTTON, HUNTER_BUTTON, SAMURAI_BUTTON, KING_BUTTON]:
			if number_player <= 2:
				button_choose_player.changeColor(screen, MOUSE_POS)
			button_choose_player.update(screen)

		for event in pygame.event.get():
			# Thoát game
			if event.type == pygame.QUIT:
				pygame.quit()
				sys.exit()
			if event.type == pygame.MOUSEBUTTONDOWN:
				# Quay lại Home
				if BACK_BUTTON.checkForInput(MOUSE_POS):
					home()
				# Bắt đầu chơi 
				if START_BUTTON.checkForInput(MOUSE_POS) and number_player == 3:
					play_game()
				# Xác định người chơi
				if number_player <= 2:
					if KNIGHT_BUTTON.checkForInput(MOUSE_POS):
						PLAYER[number_player - 1] = 1
						number_player += 1
						# kiểm tra nhân vật dã chọn hay chưa 
						if HUNTER_BUTTON.choose == False:
							HUNTER_BUTTON = ButtonChoose(310, 130, hunter_image, WHITE, DARK_CYAN, HUNTER_DATA, number_player, get_font(25, 1))
						if SAMURAI_BUTTON.choose == False:
							SAMURAI_BUTTON = ButtonChoose(520, 130, samurai_image, WHITE, DARK_CYAN, SAMURAI_DATA, number_player, get_font(25, 1))
						if KING_BUTTON.choose == False:
							KING_BUTTON = ButtonChoose(730, 130, king_image, WHITE, DARK_CYAN, KING_DATA, number_player, get_font(25, 1))

					if HUNTER_BUTTON.checkForInput(MOUSE_POS):
						PLAYER[number_player - 1] = 2
						number_player += 1
						# kiểm tra nhân vật dã chọn hay chưa 
						if KNIGHT_BUTTON.choose == False:
							KNIGHT_BUTTON = ButtonChoose(100, 130, knight_image, WHITE, DARK_CYAN, KNIGHT_DATA, number_player, get_font(25, 1))
						if SAMURAI_BUTTON.choose == False:
							SAMURAI_BUTTON = ButtonChoose(520, 130, samurai_image, WHITE, DARK_CYAN, SAMURAI_DATA, number_player, get_font(25, 1))
						if KING_BUTTON.choose == False:
							KING_BUTTON = ButtonChoose(730, 130, king_image, WHITE, DARK_CYAN, KING_DATA, number_player, get_font(25, 1))

					if SAMURAI_BUTTON.checkForInput(MOUSE_POS):
						PLAYER[number_player - 1] = 3
						number_player += 1
						# kiểm tra nhân vật dã chọn hay chưa 
						if KNIGHT_BUTTON.choose == False:
							KNIGHT_BUTTON = ButtonChoose(100, 130, knight_image, WHITE, DARK_CYAN, KNIGHT_DATA, number_player, get_font(25, 1))
						if HUNTER_BUTTON.choose == False:
							HUNTER_BUTTON = ButtonChoose(310, 130, hunter_image, WHITE, DARK_CYAN, HUNTER_DATA, number_player, get_font(25, 1))	
						if KING_BUTTON.choose == False:
							KING_BUTTON = ButtonChoose(730, 130, king_image, WHITE, DARK_CYAN, KING_DATA, number_player, get_font(25, 1))

					if KING_BUTTON.checkForInput(MOUSE_POS):
						PLAYER[number_player - 1] = 4
						number_player += 1
						# kiểm tra nhân vật dã chọn hay chưa 
						if KNIGHT_BUTTON.choose == False:
							KNIGHT_BUTTON = ButtonChoose(100, 130, knight_image, WHITE, DARK_CYAN, KNIGHT_DATA, number_player, get_font(25, 1))
						if HUNTER_BUTTON.choose == False:
							HUNTER_BUTTON = ButtonChoose(310, 130, hunter_image, WHITE, DARK_CYAN, HUNTER_DATA, number_player, get_font(25, 1))
						if SAMURAI_BUTTON.choose == False:
							SAMURAI_BUTTON = ButtonChoose(520, 130, samurai_image, WHITE, DARK_CYAN, SAMURAI_DATA, number_player, get_font(25, 1))	

		pygame.display.update()

#----------------------------------Options------------------------------------------------------------
MUSIC_BUTTON = Button(650, 225, pygame.image.load("image/button/V.png").convert_alpha(), pygame.image.load("image/button/X.png").convert_alpha())
SOUND_BUTTON = Button(650, 375, pygame.image.load("image/button/V.png").convert_alpha(), pygame.image.load("image/button/X.png").convert_alpha())

def options_start():
	# Khởi tạo nút
	BACK_BUTTON = Button(40, 30, pygame.image.load("image/button/Back.png").convert_alpha())

	while True:
		# Hiển thị background
		draw_bg_home()
		draw_text("OPTIONS", get_font(70, 1), SILVER, 500, 50)
		draw_text("MUSIC", get_font(60, 1), WHITE, 430, 250)
		draw_text("SOUND", get_font(60, 1), WHITE, 430, 400)

		# Vị trí chuột
		OPTIONS_MOUSE_POS = pygame.mouse.get_pos()
		
		# Cập nhật trạng thái nút 
		for button in [BACK_BUTTON, MUSIC_BUTTON, SOUND_BUTTON]:
			button.changeColor(screen, OPTIONS_MOUSE_POS)
			button.update(screen)

		for event in pygame.event.get():
			# Thoát game
			if event.type == pygame.QUIT:
				pygame.quit()
				sys.exit()
			if event.type == pygame.MOUSEBUTTONDOWN:
				# Quay lại Home
				if BACK_BUTTON.checkForInput(OPTIONS_MOUSE_POS):
					home()
				if MUSIC_BUTTON.checkForInput(OPTIONS_MOUSE_POS):
					if MUSIC_BUTTON.choose == True: 
						pygame.mixer.music.play(-1, 0.0, 500)
					else:
						pygame.mixer.music.stop()
				if SOUND_BUTTON.checkForInput(OPTIONS_MOUSE_POS):
					sound_volume = 0.25
					if SOUND_BUTTON.choose == False:
						sound_volume = 0
					for sound in sound_list:
							sound.set_volume(sound_volume)

		pygame.display.update()

#----------------------------------Credits------------------------------------------------------------
# Hàm Credits
def credits_start():
	# Tạo credits
	text_credits = ['CODE', 'VU DUY THANH', 'DANG VAN QUANG', 'ARTIST', 'ITCH IO', 'MUSIC AND SOUND', 'PIXABAY', 'CHOSIC']

	def draw_text_credits():
		dis = 120
		for text in text_credits:
			col = WHITE
			if text == 'CODE' or text == 'ARTIST' or text == 'MUSIC AND SOUND': col = DARK_CYAN
			draw_text(text, get_font(40, 1), col, 500, dis)
			dis+=60

	# Khởi tạo nút
	BACK_BUTTON = Button(x=40, y=30, image=pygame.image.load("image/button/Back.png").convert_alpha())

	while True:
		# Hiển thị background
		draw_bg_home()
		draw_text("CREDITS", get_font(70, 1), SILVER, 500, 50)
		draw_text_credits()

		CREDITS_MOUSE_POS = pygame.mouse.get_pos()
		
		# Cập nhật trạng thái nút 
		BACK_BUTTON.changeColor(screen, CREDITS_MOUSE_POS)
		BACK_BUTTON.update(screen)

		for event in pygame.event.get():
			# Thoát game
			if event.type == pygame.QUIT:
				pygame.quit()
				sys.exit()
			if event.type == pygame.MOUSEBUTTONDOWN:
				# Quay lại Home
				if BACK_BUTTON.checkForInput(CREDITS_MOUSE_POS):
					home()

		pygame.display.update()

# --------------------------------Home----------------------------------------------------------------
# Hàm Home
def home():
	# Khởi tạo các nút hiển thị trên Home
	PLAY_BUTTON = ButtonText(500, 250, "PLAY", get_font(60, 1), WHITE, DARK_CYAN, image_collidepoint)
	OPTION_BUTTON = ButtonText(500, 330, "OPTIONS", get_font(60, 1), WHITE, DARK_CYAN, image_collidepoint)
	CREDITS_BUTTON = ButtonText(500, 410, "CREDITS", get_font(60, 1), WHITE, DARK_CYAN, image_collidepoint)
	QUIT_BUTTON = ButtonText(500, 490, "QUIT", get_font(60, 1), WHITE, DARK_CYAN, image_collidepoint)

	while True:
		clock.tick(FPS)
		# Hiển thị Background Home
		draw_bg_home()
		draw_text("GAME", get_font(80, 1), DARK_CYAN, 500, 150)
		draw_text("FIGHTER", get_font(80, 1), DARK_CYAN, 500, 50)

		# Vị trí chuột 
		HOME_MOUSE_POS = pygame.mouse.get_pos()

		# Cập nhật tình trạng các nút
		for button in [PLAY_BUTTON, OPTION_BUTTON, CREDITS_BUTTON, QUIT_BUTTON]:
			button.changeColor(screen, HOME_MOUSE_POS)
			button.update(screen)

		for event in pygame.event.get():
			# Thoát game
			if event.type == pygame.QUIT:
				pygame.quit()
				sys.exit()
			if event.type == pygame.MOUSEBUTTONDOWN:
				if PLAY_BUTTON.checkForInput(HOME_MOUSE_POS):
					choose_player()
				if OPTION_BUTTON.checkForInput(HOME_MOUSE_POS):
					options_start()
				if CREDITS_BUTTON.checkForInput(HOME_MOUSE_POS):
					credits_start()
				if QUIT_BUTTON.checkForInput(HOME_MOUSE_POS):
					pygame.quit()
					sys.exit()

		pygame.display.update()

home()