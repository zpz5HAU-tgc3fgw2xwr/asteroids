import pygame

def create_game_over_surface(screen, drawable, score):
	"""Create a surface for the Game Over screen with all final positions and text."""
	final_frame = screen.copy()

	# Draw all objects in their final positions
	for obj in drawable:
		obj.draw(final_frame)

	# Add "Game Over" text
	font = pygame.font.Font(None, 74)
	text = font.render("Game Over!", True, (255, 255, 255))
	text_rect = text.get_rect(center=(screen.get_width() / 2, screen.get_height() / 2))
	final_frame.blit(text, text_rect)

	# Add final score as a sub-message
	sub_font = pygame.font.Font(None, 36)
	sub_text = sub_font.render(f"Score: {score} | Press any key to exit", True, (255, 255, 255))
	sub_text_rect = sub_text.get_rect(center=(screen.get_width() / 2, screen.get_height() / 2 + 50))
	final_frame.blit(sub_text, sub_text_rect)

	return final_frame

def display_score(screen, score):
	"""Displays the player's score at the top-left corner."""
	font = pygame.font.Font(None, 36)
	score_text = font.render(f"Score: {score}", True, (255, 255, 255))
	screen.blit(score_text, (10, 10))