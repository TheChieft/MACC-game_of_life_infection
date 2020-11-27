from game_prueba import GAME

game=GAME()

while game.running:
    game.menu_inicial.display_menu()
    game.run()