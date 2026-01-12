import pygame
import os
#привіт
# --- CONFIGURATION ---
FRAME_WIDTH = 32
FRAME_HEIGHT = 32
SCALE_FACTOR = 1 # How much to enlarge the 16x16 sprite

# Define the layout of your spritesheet (in 16x16 frames)
# Spritesheet layout estimate:
# Row 0: RUN (4 frames), IDLE (4 frames)
# Row 1: IDLE (4 frames - repeated?), RUN (4 frames - repeated?)
# Row 2: ROLL (3 frames), HIT (2 frames), DEATH (4 frames)
# We'll stick to the clearest ones for the example.

SPRITE_MAP = {
    'idle': (0, 0, 4),    # Row 0, Frames 0-3
    'run': (0, 2, 8),   # Row 0, Frames 4-7
    'roll': (0, 5, 8),   # Row 2, Frames 0-2 (Used for jump/fall in this code)
    'coin': (0, 0, 12),   # Row 2, Frames 3-5
}

def get_frame(sheet, x, y, width, height, scale):
    """Cuts a single frame from the spritesheet."""
    frame = pygame.Surface((width, height), pygame.SRCALPHA)
    frame.blit(sheet, (0, 0), (x * width, y * height, width, height)) # Use frame indices for x,y
    return pygame.transform.scale(frame, (width * scale, height * scale))

def get_frames_from_sheet(sheet_path):
    """Loads the sheet and returns a dictionary of all animation frames."""
    if not os.path.exists(sheet_path):
        print(f"Error: Spritesheet not found at {sheet_path}")
        return None
        
    try:
        sheet = pygame.image.load(sheet_path).convert_alpha()
    except pygame.error as e:
        print(f"Error loading spritesheet: {e}")
        return None
    
    animations = {}
    for name, (start_x_frame, start_y_frame, count) in SPRITE_MAP.items():
        frames = []
        for i in range(count):
            # Calculate frame coordinates
            x_frame = start_x_frame + i
            y_frame = start_y_frame
            
            frame = get_frame(sheet, x_frame, y_frame, FRAME_WIDTH, FRAME_HEIGHT, SCALE_FACTOR)
            frames.append(frame)
        animations[name] = frames
    
    return animations

def get_frames_from_sheet_coins(sheet_path):
    """Loads the sheet and returns a dictionary of all animation frames."""
    if not os.path.exists(sheet_path):
        print(f"Error: Spritesheet not found at {sheet_path}")
        return None
        
    try:
        sheet = pygame.image.load(sheet_path).convert_alpha()
    except pygame.error as e:
        print(f"Error loading spritesheet: {e}")
        return None
    
    animations = {}
    for name, (start_x_frame, start_y_frame, count) in SPRITE_MAP.items():
        frames = []
        for i in range(count):
            # Calculate frame coordinates
            x_frame = start_x_frame + i
            y_frame = start_y_frame
            
            frame = get_frame(sheet, x_frame, y_frame, 16, 16, SCALE_FACTOR)
            frames.append(frame)
        animations[name] = frames
    
    return animations


