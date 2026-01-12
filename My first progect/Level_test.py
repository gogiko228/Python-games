import pygame, sys, random, pygame.transform
from pytmx.util_pygame import load_pygame
from Config import *
import Main
pygame.init()
# initialize Main's shared game resources (fonts/sounds) now that pygame is initialized
Main.init_game()
from Main import *
game = Main.game
game_state = Main.game_state
pygame.display.set_caption("Tiny platformer")


screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))


game_surface = pygame.Surface((GAME_SURFACE_WIDTH, GAME_SURFACE_HEIGHT))

clock = pygame.time.Clock()
tmx_data = load_pygame("m.tmx")

ALL_KNIGHT_FRAMES = get_frames_from_sheet('brackeys_platformer_assets/sprites/knight.png')
player = Knight((80*16),(800),all_frames=ALL_KNIGHT_FRAMES)
player_group = CameraGroup()
player_group.add(player)

ALL_COIN_FRAMES = get_frames_from_sheet_coins('brackeys_platformer_assets/sprites/coin.png')
coin_popups = []  # active floating +1 popups

# start looping background music if present
game.set_music('brackeys_platformer_assets/music/time_for_adventure.mp3')
game.play_music(loop=True)


#Шари з плитками
#if hasattr(tmx_data, 'data'):
#Шари за іменем
#if layer.name == "Test":
sprite_group_append(tmx_data,"Test",sprite_group)
sprite_group_append(tmx_data, "Ground", ground_sprite_group)
sprite_group_append(tmx_data, "Platforms", platform_sprite_group)
sprite_group_append(tmx_data, "Backround2", backround_sprite_group)



counter = Count(10,0,50,30, groups=interface_group)


for layer in tmx_data.visible_layers:
    if layer.name == "Coins":
        for x, y, surf in layer.tiles():
            # layer.tiles() gives tile coordinates; convert to pixels
            px, py = x * TILE_SIZE, y * TILE_SIZE
            coin = Coin(px, py, ALL_COIN_FRAMES)
            coins_sprite_group.add(coin)
            



def _hitbox_collision(a, b):
        return a.hitbox.colliderect(b.hitbox)


# Make all CameraGroup instances draw onto the small game_surface
# instead of the main display. We render everything to game_surface
# then scale that surface up to the window each frame.
sprite_group.display_surface = game_surface
ground_sprite_group.display_surface = game_surface
platform_sprite_group.display_surface = game_surface
player_group.display_surface = game_surface
coins_sprite_group.display_surface = game_surface
backround_sprite_group.display_surface = game_surface

# for layer in tmx_data.visible_layers:
#     if layer.name == "Platforms":
#         for x, y, surf in layer.tiles():
#             pos = (x*16, y*16)
#             Tile(pos=pos, surf=surf, groups=ground_sprite_group)
    
running = True
while running:
    dt = clock.tick(60) / 1000.0
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
    
    

    # --- LOGIC UPDATE ---
    player.update(dt)
    coins_sprite_group.update(dt)
    counter.set_text(f"Coins: {game_state.coins}")

    # --- DRAW TO THE SMALL CANVAS (game_surface) ---
    game_surface.fill((20, 152, 220)) # Clear the small surface

    # Draw everything onto the small game_surface, NOT the screen
    sprite_group.custom_draw(player)
    backround_sprite_group.custom_draw(player)
    platform_sprite_group.custom_draw(player)
    ground_sprite_group.custom_draw(player)
    player_group.custom_draw(player)
    coins_sprite_group.custom_draw(player)
    counter.draw(game_surface)
    
    # Check for collisions between the player and coins using spritecollide.
    # We use a custom collision function so the player's hitbox is used instead of rect.
    
    hits = pygame.sprite.spritecollide(player, coins_sprite_group, dokill=True, collided=_hitbox_collision)
    if hits:
        for coin in hits:
            # increment by one per coin
            game_state.coins += 1
            # play coin sound and create a floating +1 popup at the coin's world position
            game.play_sound('coin')
            popup_surf = game.popup_font.render("+1", True, (255, 215, 0))
            coin_pos = pygame.math.Vector2(coin.rect.center)
            coin_popups.append({
                'surf': popup_surf,
                'pos': coin_pos,
                'time': 0.0,
            })
        

    # update and draw coin popups (they are in world coordinates; apply camera offset)
    
    for p in coin_popups[:]:
        p['time'] += dt
        # float upward
        p['pos'].y -= 40 * dt
        alpha = max(0, 255 - int(255 * (p['time'] / popup_lifetime)))
        surf = p['surf'].copy()
        surf.set_alpha(alpha)
        # apply camera offset from player_group so popup moves with world
        draw_pos = p['pos'] - player_group.offset
        game_surface.blit(surf, surf.get_rect(center=(int(draw_pos.x), int(draw_pos.y))))
        if p['time'] >= popup_lifetime:
            coin_popups.remove(p)
            
    

    # --- SCALE THE CANVAS AND DRAW TO THE SCREEN ---
    # Scale the small surface up to the full window size
    scaled_surface = pygame.transform.scale(game_surface, (WINDOW_WIDTH, WINDOW_HEIGHT))
    screen.blit(scaled_surface, (0, 0)) # Draw the single scaled surface

    # --- UPDATE DISPLAY ---
    pygame.display.flip() # Use flip() for better performance
    