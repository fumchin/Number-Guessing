import random
import threading
import guessingMachine.timer as timer
import guessingMachine.leaderboard as GamerInfo
from operator import attrgetter


class GuessingMachine:
    def __init__(self):
        self.questionNumList = random.sample(range(10), 4)  # generate four random int without repeating
        self.roundCount = 0
        self.well_done = False   # check if the game is finished
        self.history_input = []  # check if this input has appeared before, example, input 1234 twice
        self.leaderboardList = []  # store top ten gamer information
        self.rank_num = 10  # numbers of people we put on the leaderboard

        self.stopFlag = threading.Event()  # our flag to tell thread to stop
        self.thread = timer.MyThread(self.stopFlag)

    # first, we check input format using: self.check_input_format(userInput)
    # second, if correct, we check the numbers of A and B: self.judge(userInput)
    # finally, we either return what wrong with the input or ?A?B
    def input_submit(self, userInput):
        # check input format
        result = self.check_input_format(userInput)
        if result != "":
            return result
        else:
            # compare answer and userInput
            self.roundCount += 1
            result = self.judge(userInput)
            return "round" + str(self.roundCount) + " " + userInput + " " + result + "\n"

    # we check
    # 1. length error
    # 2. character repeat error
    # 3. not int error
    # 4. same input again error
    # return string that show what's wrong with the input
    # if input is acceptable, return ""
    def check_input_format(self, userInput):
        result = ""
        repeat_check = True
        # length
        if len(userInput) != 4:
            result += (userInput + " Invalid input!! (length error) Try again!!\n")
            repeat_check = False
        # repeat
        if len(set(userInput)) != len(userInput):
            # we could use set to check repeat because there won't be same item in a set
            # so the length of set(a) and a won't be the same if a contain repeat character
            result += (userInput + " Invalid input!! (character repeat) Try again!!\n")
            repeat_check = False
        # error
        if not userInput.isdigit():
            # I use isdigit() to check if every char in the string is 0~9
            result += (userInput + " Invalid input!! (character error) Try again!!\n")
            repeat_check = False

        if repeat_check:
            # check if the input is in history_input ot not
            # and store the input into history_input
            store_or_not = True
            for item in self.history_input:
                if item == userInput:
                    result = userInput + " You've guess this number before!! Try again!!\n"
                    store_or_not = False
            if store_or_not:
                self.history_input.append(userInput)

        return result

    # come here only if the input format is correct
    # if the number and position of a digit is correct, A += 1
    # number is right, but position is wrong, B += 1
    # if the input is totally correct, set the well_done flag to True, showing that this game is finished
    def judge(self, userInput):
        a_count = 0
        b_count = 0
        for i in range(len(userInput)):
            for j in range(len(self.questionNumList)):
                if i == j and userInput[i] == str(self.questionNumList[j]):
                    a_count += 1
                else:
                    if userInput[i] == str(self.questionNumList[j]):
                        b_count += 1
        result = str(a_count) + "A" + str(b_count) + "B"
        if a_count == 4:
            self.well_done = True
        return result

    # reset everything if new_game button is pressed
    # including question, record count, time count, and history_input
    def new_game(self):
        self.questionNumList = random.sample(range(10), 4)
        self.roundCount = 0
        self.well_done = False
        self.history_input.clear()
        self.thread.restart()

    # check if this round can be written in leaderboard
    # yes if your round count is lower than others,
    # or if having same round count, we choose the one having lower time spent
    # we return T/F to indicate whether gamer is qualified to enter leaderboard
    def ranking_check(self):
        qualify = False
        if len(self.leaderboardList) < self.rank_num:
            return True
        else:
            for ls in self.leaderboardList:
                if self.roundCount < ls.get_rounds():
                    qualify = True
                elif self.roundCount == ls.get_rounds():
                    if self.thread.get_total_sec() < ls.get_total_sec():
                        qualify = True
        return qualify

    # put gamer info into the leaderboard list
    # first compare the rounds count than total time spent
    # keep the length of the list no more than 10
    def ranking(self, userName):
        # store GamerInfo() in list
        self.leaderboardList.append(GamerInfo.GamerInfo(userName, self.roundCount, self.thread.get_time(), self.thread.get_total_sec()))
        # we can use attrgetter to compare rounds first and total time spent second
        self.leaderboardList = sorted(self.leaderboardList, key=attrgetter('rounds', 'total_sec'))
        if len(self.leaderboardList) > self.rank_num:
            del self.leaderboardList[-1]

    # put leaderboard list info into s string and return it
    def get_leaderboard(self):
        record = "Rank\tName\tRounds\tTime\n"
        for i, ls in enumerate(self.leaderboardList):
            record += (str(i+1) + "\t" + ls.get_record())
        return record

    def get_ans(self):
        s = [str(i) for i in self.questionNumList]
        return "".join(s)

    def get_round_count(self):
        return self.roundCount

    def get_status(self):
        return self.well_done

    def set_time_string(self, time_string):
        self.thread.set_time_string(time_string)

    def get_stop_flag(self):
        return self.stopFlag

    def get_thread(self):
        return self.thread





