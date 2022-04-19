from dream_game import DreamGame

PLAYERS_NUM = 4

PLAYERS = ["ds", "Хай", "Бай", "Hello"]


def play_game():
    game = DreamGame()
    while True:

        game.prepare_game()
        for player in PLAYERS:
            game.join_player(player)
        start_message = game.start_game()
        print(start_message)
        while True:

            print(game.display_player_message())
            print("Вращайте барабан")
            repeat, message = game.spin_drum()
            print(f"Счёт игрока  {game.current_player_name}: {game.cur_player_score}")
            print(message)
            print(f"Слово{game.display_word}")
            if not repeat:
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

            if game.is_over():
                print(game.victory_message())
                break


# def test():
#     for _ in range(10000):
#         game = DreamGame()
#         game.prepare_game(PLAYERS)
#         start_message = game.start_game()
#         is_player_turn, need_update,  message = game.spin_drum()

# test()
play_game()
