import pygame
import sys
from Config import *

SCALE_FACTOR = 1
WINDOW_WIDTH, WINDOW_HEIGHT = 1280, 720
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
MAP_WIDTH = 120
MAP_HEIGHT = 67
BASE_HEIGHT = 2
TILE_SIZE = 16
GAME_SURFACE_WIDTH, GAME_SURFACE_HEIGHT = 640/2, 360/2 # Half the window size, for a 2x zoom (1280x720 -> 640x360)

popup_lifetime = 0.8

class GameState:
    """Holds global game state (counters, scores, etc.).

    Instantiate one shared GameState and pass or import it where needed.
    """
    def __init__(self):
        self.coins = 0

# single shared game state instance
game_state = GameState()


class Game:
    """Central game manager for reusable resources like sounds, music and fonts.

    Instantiate a single `game` and import it where needed.
    """
    def __init__(self):
        self.sounds = {}
        self.music_path = None
        # try load common sounds (paths are project-relative absolute paths)
        try:
            self.sounds['coin'] = pygame.mixer.Sound('brackeys_platformer_assets/sounds/coin.wav')
        except Exception:
            self.sounds['coin'] = None
        try:
            self.sounds['jump'] = pygame.mixer.Sound('brackeys_platformer_assets/sounds/jump.wav')
        except Exception:
            self.sounds['jump'] = None

        # popup font used by UI code
        try:
            self.popup_font = pygame.font.Font('brackeys_platformer_assets/fonts/PixelOperator8.ttf', 18)
        except Exception:
            self.popup_font = pygame.font.SysFont(None, 18)

    def play_sound(self, name):
        s = self.sounds.get(name)
        if s:
            s.play()

    def set_music(self, path):
        self.music_path = path

    def play_music(self, loop=True):
        if not self.music_path:
            return
        try:
            pygame.mixer.music.load(self.music_path)
            pygame.mixer.music.play(-1 if loop else 0)
        except Exception:
            pass


# shared game resource manager (created by init_game)
game = None


def init_game():
    """Initialize and return the shared Game instance.

    Call this after pygame.init() has been called by the importing module.
    """
    global game
    if game is None:
        game = Game()
    return game




class CameraGroup(pygame.sprite.Group):
    def __init__(self):
        super().__init__()
        self.display_surface = pygame.display.get_surface()


        self.offset = pygame.math.Vector2()
        self.half_w = GAME_SURFACE_WIDTH // 2
        self.half_h = GAME_SURFACE_HEIGHT // 2
        # self.lerp = 0.1  # Camera smoothing factor

    def center_target_camera(self, target):
        # target_center = pygame.math.Vector2(target.hitbox.center)
        # desired_offset = target_center - pygame.math.Vector2(self.half_w, self.half_h)
        # self.offset += (desired_offset - self.offset) * self.lerp
        self.offset.x = target.hitbox.centerx - self.half_w
        self.offset.y = target.hitbox.centery - self.half_h
        
    def custom_draw(self, player):
        self.center_target_camera(player)

        for sprite in self.sprites():
            offset_pos = sprite.rect.topleft - self.offset
            self.display_surface.blit(sprite.image, offset_pos)









sprite_group = CameraGroup()
ground_sprite_group= CameraGroup()
platform_sprite_group= CameraGroup()
coins_sprite_group= CameraGroup()
backround_sprite_group= CameraGroup()
interface_group= CameraGroup()

class Tile(pygame.sprite.Sprite):
    def __init__(self, pos, surf, groups):
        super().__init__(groups)
        self.image = surf
        self.rect = self.image.get_rect(topleft=pos)

    

def sprite_group_append(tmx_data,name,group):
    for layer in tmx_data.visible_layers:
        if layer.name == name:
            for x, y, surf in layer.tiles():
                pos = (x*TILE_SIZE, y*TILE_SIZE)
                Tile(pos=pos, surf=surf, groups=group)

# class Button:
#     def __init__(self, x, y, width, height, text, font, bg_color=(0,128,255), text_color=(255,255,255), border_radius=10):

#         self.rect = pygame.Rect(x, y, width, height)
#         self.text = text
#         self.font = font
#         self.bg_color = bg_color
#         self.text_color = text_color
#         self.border_radius = border_radius
#         self.text_surf = self.font.render(self.text, True, self.text_color)
#         self.text_rect = self.text_surf.get_rect(center=self.rect.center)

#     def draw(self, surface):
       
#         pygame.draw.rect(surface, self.bg_color, self.rect, border_radius=self.border_radius)
#         surface.blit(self.text_surf, self.text_rect)

#     def is_clicked(self, pos):
        
#         return self.rect.collidepoint(pos)
#player = pygame.sprite.GroupSingle()
# class Entity(pygame.sprite.Sprite):
#     def __init__(self, x=0, y=0, width=32, height=32, image=None):
#         super().__init__()
#         self.gravity=0
#         self.x = x
#         self.y = y 
#         self.width = width
#         self.height = height
#         self.image = image
#         self.image = pygame.image.load(image).convert_alpha() if image else None
#         self.rect =  pygame.Rect(x,y, width, height)
# #self.image.get_rect(midbottom=(x, y)) if image else 

#     def draw(self, surface):
#         if self.image:
#             surface.blit(self.image, (self.x, self.y))
#         else:
#             pygame.draw.rect(surface, (255, 0, 0), self.rect)  # Draw a red rectangle if no image is provided

#     def movement(self):
#         keys = pygame.key.get_pressed()
#         if keys[pygame.K_LEFT]:
#             self.rect.x -= 5
#         if keys[pygame.K_RIGHT]:
#             self.rect.x += 5
#         # if keys[pygame.K_SPACE]:  # Jump only if on the ground
#         #     self.gravity = -20  # Jump effect


#         self.rect.y += self.gravity  # Simple gravity effect
        
#         for sprite in ground_sprite_group:
#             if sprite.rect.colliderect(self.rect):
#                 if self.gravity > 0:  # Falling
#                     self.rect.bottom = sprite.rect.top
#                     self.gravity = 0
#                     if keys[pygame.K_SPACE]:  # Jump only if on the ground
#                         self.gravity = -20
                    
#                 elif self.gravity < 0:  # Jumping
#                     self.rect.top = sprite.rect.bottom
#                     self.gravity = 1
#                 break

#         for sprite in platform_sprite_group:
#             if sprite.rect.colliderect(self.rect):
#                 if self.gravity > 0:  # Falling
#                     self.rect.bottom = sprite.rect.top
#                     self.gravity = 0
#                     if keys[pygame.K_SPACE]:  # Jump only if on the ground
#                         self.gravity = -20
                    
#                 break
        
#         else:
#             self.gravity += 1        
#           # Ground collision

#         self.y = min(self.y + self.gravity, HEIGHT - self.height)  # Prevent falling below the screen
        

        

#     def update(self):
#         self.movement()

        
    
    # def aply_gravity(self):
        
    #     self.rect.y += self.gravity  # Simple gravity effect
    #     if self.rect.bottom > HEIGHT - 32:  # Ground collision
    #         self.rect.bottom = HEIGHT - 32
    #         self.gravity = -1
    #     for sprite in ground_sprite_group:
    #         if sprite.rect.colliderect(self.rect):
    #             if self.gravity > 0:  # Falling
    #                 self.rect.bottom = sprite.rect.top
    #                 self.gravity = 0
                    
    #             elif self.gravity < 0:  # Jumping
    #                 self.rect.top = sprite.rect.bottom
    #                 self.gravity = 1
    #             break
        
    #     else:
    #         self.gravity += 1        
    #       # Ground collision
                
                


class Knight(pygame.sprite.Sprite):
    def __init__(self, x, y, all_frames):
        super().__init__()
        
        # --- Animation & State ---
        self.all_frames = all_frames
        # CHANGED: Animation speeds are now in Frames Per Second (FPS).
        self.animation_speeds = {'idle': 8, 'run': 12, 'roll': 15}
        self.current_animation = 'idle'
        self.frame_index = 0
        self.facing_right = True
        
        # --- Physics & Position ---
        # NEW: We use a velocity vector for movement.
        self.velocity = pygame.math.Vector2(0, 0)
        
        # CHANGED: All physics values are now in pixels-per-second.
        # This makes them easy to reason about and tweak!
        self.speed = 250
        self.gravity_acceleration = 800
        self.jump_strength = -450 # A single upward burst of velocity.

        
        

        #finishing config
        self.image = self.all_frames[self.current_animation][self.frame_index]
        self.rect = self.image.get_rect(topleft=(x, y))
        self.hitbox = pygame.Rect(0, 0, 16, 28)
        self.hitbox.midbottom = self.rect.midbottom
        self.on_ground = False

    def _get_current_image(self):
        frame = self.all_frames[self.current_animation][int(self.frame_index)]
        if not self.facing_right:
            return pygame.transform.flip(frame, True, False)
        return frame

    def set_animation(self, name):
        if self.current_animation != name:
            self.current_animation = name
            self.frame_index = 0

    def animate(self, dt):
        # CHANGED: Simple, clean animation update.
        speed = self.animation_speeds[self.current_animation]
        self.frame_index += speed * dt
        
        if self.frame_index >= len(self.all_frames[self.current_animation]):
            self.frame_index = 0
            
        self.image = self._get_current_image()

    def hitting_wall(self, ground_sprite_group):

        for sprite in ground_sprite_group.sprites() : #+ platform_sprite_group.sprites():
            if sprite.rect.colliderect(self.hitbox):
                if self.velocity.x > 0: 
                    self.hitbox.right = sprite.rect.left
                elif self.velocity.x < 0:
                    self.hitbox.left = sprite.rect.right

        

    def movement(self, keys, dt):
    # --- 1. HORIZONTAL MOVEMENT ---
        self.velocity.x = 0 
        if keys[pygame.K_LEFT]:
            self.velocity.x = -self.speed
            self.facing_right = False
        elif keys[pygame.K_RIGHT]:
            self.velocity.x = self.speed
            self.facing_right = True
        
        self.hitbox.x += self.velocity.x * dt

        # Check for horizontal collisions with ALL collidable sprites
        self.hitting_wall(ground_sprite_group)
        

        # --- 2. VERTICAL MOVEMENT ---
        self.velocity.y += self.gravity_acceleration * dt
        self.hitbox.y += self.velocity.y * dt

        self.on_ground = False
        
        # Check for vertical collisions with SOLID GROUND
        for sprite in ground_sprite_group.sprites():
            if sprite.rect.colliderect(self.hitbox):
                if self.velocity.y > 0:
                    self.hitbox.bottom = sprite.rect.top
                    self.on_ground = True
                    self.velocity.y = 0
                elif self.velocity.y < 0:
                    self.hitbox.top = sprite.rect.bottom
                    self.velocity.y = 0
        
        # NEW: Check for vertical collisions with ONE-WAY PLATFORMS
        for sprite in platform_sprite_group.sprites():
            # Only collide if falling down AND the player's bottom is near the platform's top
            if sprite.rect.colliderect(self.hitbox) and self.velocity.y > 0:
                # This condition checks if the player was above or at the platform's level in the previous frame.
                # It prevents snapping to the top while jumping through.
                if self.hitbox.bottom <= sprite.rect.top + self.velocity.y * dt + 1:
                    self.hitbox.bottom = sprite.rect.top
                    self.on_ground = True
                    self.velocity.y = 0
        
        

        # --- 3. JUMPING ---
        if self.on_ground and keys[pygame.K_SPACE]:
            self.velocity.y = self.jump_strength
            # play jump sound from shared game audio manager if available
            try:
                game.play_sound('jump')
            except Exception:
                # game may not be created yet in some contexts; ignore
                pass

        # --- 4. SET ANIMATION ---
        if self.on_ground:
            if self.velocity.x != 0:
                self.set_animation('run')
            else:
                self.set_animation('idle')
        else:
            self.set_animation('roll')
        
        self.rect.midbottom = self.hitbox.midbottom


    def update(self, dt):
        keys = pygame.key.get_pressed()
        self.movement(keys, dt)
        self.animate(dt)

class Count(pygame.sprite.Sprite):
    def __init__ (self, x,y,width,height, groups):
        super().__init__(groups)
        self.Rect = pygame.Rect(x,y,width,height)
    
    def set_text(self, text, font="brackeys_platformer_assets/fonts/PixelOperator8.ttf", color=(89, 89, 89)):
        self.text_surf = pygame.font.Font(font, 10).render(text, True, color)
        self.text_rect = self.text_surf.get_rect(center=self.Rect.center)
    
    def draw(self, surface):
        # pygame.draw.rect(surface, (0,0,0), self.Rect)
        surface.blit(self.text_surf, self.text_rect)





class Coin(pygame.sprite.Sprite):
    def __init__(self, x, y, all_frames):
        super().__init__()
        
        # --- Animation & State ---
        self.all_frames = all_frames
        # CHANGED: Animation speeds are now in Frames Per Second (FPS).
        self.animation_speeds = {'coin': 8}
        self.current_animation = 'coin'
        self.frame_index = 0

        
        

        #finishing config
        self.image = self.all_frames[self.current_animation][self.frame_index]
        self.rect = self.image.get_rect(topleft=(x, y))
        self.hitbox = pygame.Rect(0, 0, 20, 28)
        self.hitbox.midbottom = self.rect.midbottom
        
    
    def _get_current_image(self):
        frame = self.all_frames[self.current_animation][int(self.frame_index)]
        return frame


    def animate(self, dt):
        # CHANGED: Simple, clean animation update.
        speed = self.animation_speeds[self.current_animation]
        self.frame_index += speed * dt
        
        if self.frame_index >= len(self.all_frames[self.current_animation]):
            self.frame_index = 0
            
        self.image = self._get_current_image()

    def got_colected(self, player):
        # increment the shared game_state counter when collected
        if self.hitbox.colliderect(player.hitbox):
            from Main import game_state as _game_state  # local import to avoid circular issues
            _game_state.coins += 1
            self.kill()

    def update(self, dt):
        """Update called by sprite groups. Forward dt to animation."""
        self.animate(dt)
        
