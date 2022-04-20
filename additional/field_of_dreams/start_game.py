from dream_game import DreamGame

PLAYERS_NUM = 4

PLAYERS = ["Петр", "Василий", "Сергей", "Андрей"]


def play_game():
    game = DreamGame()
    while True:

        game.prepare_game()
        for player in PLAYERS:
            game.join_player(player)
        game.start_game()
        while True:

            print(game.turn_info, end="\n\n")
            repeat = game.spin_drum()
            print(repeat)
            if game.has_bonus:
                print(game.turn_bonus.message)
            else:
                print(game.score_message)
            if repeat:
                # print(game.turn_bonus.message)
                ...
            elif not repeat:
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

            if game.check_over():
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
