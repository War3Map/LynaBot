from dream_game import DreamGame

PLAYERS_NUM = 4

PLAYERS = ["ds", "Хай", "Бай", "Hello"]
game = DreamGame()
while True:

    game.prepare_game(PLAYERS)
    start_message = game.start_game()
    print(start_message)
    while True:

        print(game.display_player_message())
        print("Вращайте барабан")
        is_player_turn, message = game.get_current_score_state()
        print(message)
        if is_player_turn:
            choice = input("Введите букву или назовёте слово целиком? (Напишите слово!")
            if choice.lower() == "слово":
                word = input("Слово:  ")
                state = game.guess_complete_word(word)
            else:
                word = input("Буква:  ")
                state = game.guess_symbol(word)

            if state:
                print("Верно!")
            else:
                print("Нет! Не верно!")
        print(game.display_word, "\n")
        if game.is_over():
            print(game.victory_message())
            break


