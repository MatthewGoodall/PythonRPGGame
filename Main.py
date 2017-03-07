import Game

def PlayGame():
    game = Game()
    game.Setup()
    game.GameLoop()
    game.Quit()

if __name__ == "__main__":
    PlayGame()
