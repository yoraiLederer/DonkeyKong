import pygame

class Human_Agent:
    def __init__ (self):
        self.action = 10

    def get_action(self, events=None):
    # If events is None, set it to an empty list
        if not events:
            return None
    # Handle key events
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    self.action = 1
                elif event.key == pygame.K_a:
                    self.action = 2
                elif event.key == pygame.K_d:
                    self.action = 3
                elif event.key == pygame.K_w:
                    self.action = 4
                elif event.key == pygame.K_s:
                    self.action = 5

            

            if event.type == pygame.KEYUP:
                # If no keys are pressed, reset action to 0
                temp = pygame.key.get_pressed()
                if not (temp[pygame.K_a] or temp[pygame.K_d] or temp[pygame.K_w] or temp[pygame.K_s]):
                    self.action = 0
                

        return self.action
    
    def another_game(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return False
            
            keys = pygame.key.get_pressed()
            if keys[pygame.K_y]:
                return True
            if keys[pygame.K_n]:
                return False