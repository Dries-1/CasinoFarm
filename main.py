from player import Player
from roulette import Roulette


if __name__ == "__main__":
    player = Player()
    roulette = Roulette(player)
    roulette.start_game()