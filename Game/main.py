#FINAL_CODE

from game import GAME

game=GAME()

while game.running:
    game.menu_inicial.display_menu()
    game.run()