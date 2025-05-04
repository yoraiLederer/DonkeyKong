import pygame
from Constants import *
from Graphics import Graphics
from Human_Agent import Human_Agent
from Environment import Environment
from DQN_Agent import DQN_Agent
from State import State

def main():
    # Initialize Pygame and Mixer
    pygame.init()
    pygame.mixer.init()
    clock = pygame.time.Clock()

    graphics = Graphics(SCREEN_WIDTH, SCREEN_HEIGHT)
    env = Environment(delay=0)
    # env = Environment()      
    # path = "Data\params100"
    path = None
    player = DQN_Agent(train=True, parametes_path=path)

    # player = Human_Agent()

    # Game loop
    running = True
    while running:
        graphics.clear_screen()

        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:      
                running = False
        state=env.state.get_tensor() 
        if type(player) is DQN_Agent:
            action = player.get_action(state=state,events=events, train=True)
        else:
            action = player.get_action(events=events)
        env.move(action=action)
        
        done = env.play(graphics.game_bonus_sound, graphics.got_hit_sound)
        if done:
                graphics.game_over(env.state.score)
                if player.another_game():
                    env.state.restart()
                else:
                    break
                
        graphics.write_text(graphics.header_surf, "Lives: " + str(env.state.lives_left), (300, 10))
        graphics.write_text(graphics.header_surf, "Score: " + str(env.state.score) ,(700, 10))
        
        graphics.draw(env.state)
        pygame.display.update()
        clock.tick(FPS)

    # Quit Pygame
    pygame.quit()

    
                
if __name__ == "__main__":
    main()