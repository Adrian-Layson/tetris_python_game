import pygame
from colors import Colors

class Grid:
    def __init__(self):
        self.num_rows = 20
        self.num_cols = 10
        self.cell_size = 30
        self.grid = [[0 for j in range(self.num_cols)] for i in range(self.num_rows)]
        self.colors = Colors.get_cell_colors()
        self.ghost_alpha = 80  # Transparency for ghost/column highlight
        
    def get_column_heights(self):
        """Returns a list with the height of each column (how many blocks are stacked)"""
        heights = [0] * self.num_cols
        for col in range(self.num_cols):
            for row in range(self.num_rows):
                if self.grid[row][col] != 0:
                    heights[col] = self.num_rows - row
                    break
        return heights
    
    def draw(self, screen):
        # Draw column highlights first (background)
        heights = self.get_column_heights()
        for col in range(self.num_cols):
            if heights[col] > 0:
                highlight_rect = pygame.Rect(
                    col * self.cell_size + 11,
                    (self.num_rows - heights[col]) * self.cell_size + 11,
                    self.cell_size - 1,
                    heights[col] * self.cell_size - 1
                )
                # Create a semi-transparent surface for the highlight
                highlight_surface = pygame.Surface((self.cell_size - 1, heights[col] * self.cell_size - 1), pygame.SRCALPHA)
                highlight_surface.fill((255, 255, 255, self.ghost_alpha))
                screen.blit(highlight_surface, highlight_rect)
        
        # Then draw the normal grid cells on top
        for row in range(self.num_rows):
            for column in range(self.num_cols):
                cell_value = self.grid[row][column]
                cell_rect = pygame.Rect(
                    column * self.cell_size + 11,
                    row * self.cell_size + 11,
                    self.cell_size - 1,
                    self.cell_size - 1
                )
                pygame.draw.rect(screen, self.colors[cell_value], cell_rect)