import time
import sys
import random


def slow_print(text):
    for letter in text:
        sys.stdout.write(letter)
        sys.stdout.flush()
        time.sleep(0.05)
    sys.stdout.write("\n")


def print_pause(text, delay=1.5):
    print(text)
    time.sleep(delay)


def color_print_pause(text, color, delay=1.5):
    print(f"{color}{text}{color_end}")
    time.sleep(delay)


def valid_choice_input(prompt, minimum, maximum):
    while True:
        choice = input(f"{prompt}\n")
        if choice.isnumeric():
            choice = int(choice)
            if minimum <= choice <= maximum:
                return choice
            else:
                print(f"Choice must be >= {minimum} and <= {maximum}.")
        else:
            print("Your input must be natural number(non-negative integer).")


class Color:
    global red, green, yellow, blue, color_end
    red = "\033[1;31;40m"
    green = "\033[1;32;40m"
    yellow = "\033[1;33;40m"
    blue = "\033[1;34;40m"
    color_end = "\033[0m"


def gender():
    gender_choice = valid_choice_input(
        """
Are you a lady or gentleman?  1. Lady  2. Gentleman
Please input the serial number of your choice and press enter""", 1, 2)
    if gender_choice == 1:
        return "Lady"
    elif gender_choice == 2:
        return "Gentleman"


def introduction():
    global Gender
    slow_print(f"Rock, paper, scissors.{blue}(Best of Seven sets){color_end}")
    Gender = gender()
    strategy_print_choice()
    color_print_pause("Ready", red)
    color_print_pause("Go! Go! Go!", red)


class Player:
    global trick_dictionary, trick_list
    trick_dictionary = {1: "Rock", 2: "Paper", 3: "Scissors"}
    trick_list = ["Rock", "Paper", "Scissors"]

    def move(self):
        return random.choice(trick_list)

    def learn(self, last_player_move, last_robot_move):
        global player_last_move, robot_last_move
        player_last_move = last_player_move
        robot_last_move = last_robot_move

    def robot_last_move_print(self):
        color_print_pause(f"(opponent last move:{robot_last_move})",
                          green,
                          delay=0.5)


class HumanPlayer(Player):

    def player_move(self):
        return trick_dictionary[valid_choice_input(
            """\
1. Rock  2. Paper  3. Scissors
Please input the serial number you choose and press enter.""", 1, 3)]


def strategy_print_choice():
    global strategy_choice
    strategy_dic = {
        1: ComprehensivePlayer(),
        2: GenderReflectPlayer(),
        3: ReflectPlayer(),
        4: RandomPlayer(),
        5: WordsPlayer(),
        6: RockPlayer(),
        7: CyclePlayer()
    }
    strategy_choice_number = valid_choice_input(
        """
Please choose your opponent:
1: ComprehensivePlayer
2: GenderReflectPlayer
3: ReflectPlayer
4: RandomPlayer
5: WordsPlayer
6: RockPlayer
7: CyclePlayer
Please input the serial number you choose and press enter.""", 1, 7)
    strategy_choice = strategy_dic[strategy_choice_number]


class ComprehensivePlayer(Player):

    def robot_move(self):
        gender_reflect_player = GenderReflectPlayer()
        more_complicated_random_reflect_player \
            = ReflectPlayer()
        random_reflect_player = RandomPlayer()
        words_player \
            = WordsPlayer()

        if score_dic["player_score"] == 0:
            return gender_reflect_player.robot_move()
        elif score_dic["player_score"] == 1:
            return more_complicated_random_reflect_player\
                    .robot_move()
        elif score_dic["player_score"] == 2:
            return random_reflect_player.robot_move()
        elif score_dic["player_score"] == 3:
            return words_player.robot_move()


class GenderReflectPlayer(Player):

    def robot_move(self):
        if turn == 1:
            if Gender == "Lady":
                return random.choices(trick_list, weights=[8, 3, 2], k=1)[0]
            elif Gender == "Gentleman":
                return random.choices(trick_list, weights=[2, 8, 3], k=1)[0]
        elif turn > 1:
            if player_last_move == "Rock":
                return random.choices(trick_list, weights=[8, 2, 3], k=1)[0]
            elif player_last_move == "Paper":
                return random.choices(trick_list, weights=[3, 8, 2], k=1)[0]
            elif player_last_move == "Scissors":
                return random.choices(trick_list, weights=[2, 3, 8], k=1)[0]


class ReflectPlayer(Player):

    def robot_move(self):
        if turn == 1:
            return random.choice(trick_list)
        elif turn > 1:
            return player_last_move


class RandomPlayer(Player):

    def robot_move(self):
        if turn == 1:
            return random.choice(trick_list)
        elif turn > 1:
            if player_last_move == "Rock":
                return random.choices(trick_list, weights=[3, 2, 8], k=1)[0]
            elif player_last_move == "Paper":
                return random.choices(trick_list, weights=[8, 3, 2], k=1)[0]
            elif player_last_move == "Scissors":
                return random.choices(trick_list, weights=[2, 8, 3], k=1)[0]


class WordsPlayer(Player):

    def robot_move(self):
        move_word = 'Robot say,"I will use the {move}."'
        if player_last_move == "Rock":
            print(move_word.format(move="scissors"))
            if turn == 1:
                return random.choices(trick_list, weights=[3, 2, 9], k=1)[0]
            elif turn > 1:
                return random.choices(trick_list, weights=[3, 9, 2], k=1)[0]
        elif player_last_move == "Paper":
            print(move_word.format(move="rock"))
            if turn == 1:
                return random.choices(trick_list, weights=[9, 3, 2], k=1)[0]
            elif turn > 1:
                return random.choices(trick_list, weights=[2, 3, 9], k=1)[0]
        elif player_last_move == "Scissors":
            print(move_word.format(move="paper"))
            if turn == 1:
                return random.choices(trick_list, weights=[2, 9, 3], k=1)[0]
            elif turn > 1:
                return random.choices(trick_list, weights=[9, 2, 3], k=1)[0]


class RockPlayer(Player):

    def robot_move(self):
        return "Rock"


class CyclePlayer(Player):

    def robot_move(self):
        if turn == 1:
            return "Rock"
        elif turn > 1:
            if robot_last_move == "Rock":
                return "Paper"
            elif robot_last_move == "Paper":
                return "Scissors"
            elif player_last_move == "Scissors":
                return "Rock"


class Score:

    def score_print(self):
        color_print_pause(
            f"""\
player_score: {score_dic["player_score"]}   \
robot_score: {score_dic["robot_score"]}""", yellow)

    def win_mechanism(self, player_move, robot_move):
        print(f"""\
player_move:{player_move}   robot_move:{robot_move}""")
        if player_move == "Rock":
            if robot_move == "Rock":
                return "tie"
            elif robot_move == "Paper":
                return "robot_win"
            elif robot_move == "Scissors":
                return "player_win"
        elif player_move == "Paper":
            if robot_move == "Rock":
                return "player_win"
            elif robot_move == "Paper":
                return "tie"
            elif robot_move == "Scissors":
                return "robot_win"
        elif player_move == "Scissors":
            if robot_move == "Rock":
                return "robot_win"
            elif robot_move == "Paper":
                return "player_win"
            elif robot_move == "Scissors":
                return "tie"

    def score_get(self, result):
        if result == "robot_win":
            score_dic["robot_score"] += 1
        elif result == "player_win":
            score_dic["player_score"] += 1

    def score_check(self):
        if score_dic["player_score"] == 4:
            color_print_pause("\nYou win.", blue)
            return "play_again"
        elif score_dic["robot_score"] == 4:
            color_print_pause("\nYou lose.", red)
            return "play_again"


def play_again():
    choice = valid_choice_input(
        f"""
{yellow}Do you want to play again?   1.Yes    2.No
Please input the serial number to choose \
and press enter{color_end}""", 1, 2)
    if choice == 2:
        exit(0)


class Game:

    def play_round(self):
        global round, turn, score_dic
        score = Score()
        round = 1
        turn = 1
        score_dic = {"player_score": 0, "robot_score": 0}
        human_player = HumanPlayer()
        while True:
            print(f"\nRound {round}")
            while True:
                robot_move = strategy_choice.robot_move()
                player_move = human_player.player_move()
                result = score.win_mechanism(player_move, robot_move)
                color_print_pause(result, blue, delay=0.5)
                turn += 1
                strategy_choice.learn(player_move, robot_move)
                human_player.robot_last_move_print()
                if result != "tie":
                    break
            score.score_get(result)
            score.score_print()
            if score.score_check() == "play_again":
                return "play_again"
            round += 1

    def game_start(self):
        introduction()
        if self.play_round() == "play_again":
            return "play_again"

    def play_game(self):
        while True:
            if self.game_start() == "play_again":
                play_again()


if __name__ == '__main__':
    game = Game()
    game.play_game()
