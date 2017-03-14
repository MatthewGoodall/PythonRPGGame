import Game


def PlayGame():
    game = Game.Game()
    game.Setup()
    game.StartScreen()
    game.GameLoop()
    game.Quit()


if __name__ == "__main__":
    PlayGame()
