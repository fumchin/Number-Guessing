import random
import tkinter as tk
import threading
import guessingMachine.timer as timer

class GuessingMachine():
    def __init__(self):
        self.questionNumList = random.sample(range(10), 4)
        self.roundCount = 0
        self.well_done = False
        self.history_input = []
        self.leaderboard = []
        # self.timeString = tk.StringVar()

        self.stopFlag = threading.Event()
        self.thread = timer.MyThread(self.stopFlag)
        # self.thread.set_time_string(timeString)

    def click_run(self, userInput):
        # check input format
        result = self.check_input_format(userInput)
        if result != "":
            return result
        else:
            # compare answer and userInput
            self.roundCount += 1
            result = self.judge(userInput)
            return "round" + str(self.roundCount) + " " + userInput + " " + result + "\n"


    def check_input_format(self, userInput):
        result = ""
        repeat_check = True
        # length
        if len(userInput) != 4:
            result += (userInput + " Invalid input!! (length error) Try again!!\n")
            repeat_check = False
        # repeat
        if len(set(userInput)) != len(userInput):
            result += (userInput + " Invalid input!! (character repeat) Try again!!\n")
            repeat_check = False
        # error
        if not userInput.isdigit():
            result += (userInput + " Invalid input!! (character error) Try again!!\n")
            repeat_check = False

        # if repeat_check:
        #     store_or_not = True
        #     for item in self.history_input:
        #         if item == userInput:
        #             result = userInput + " You've guess this number before!! Try again!!\n"
        #             store_or_not = False
        #     if store_or_not:
        #         self.history_input.append(userInput)

        return result

    def judge(self, userInput):
        a_conut = 0
        b_count = 0
        for i in range(len(userInput)):
            for j in range(len(self.questionNumList)):
                # print(type(userInput[i]) + " and " + self.questionNumList[j])
                if i == j and userInput[i] == str(self.questionNumList[j]):
                    a_conut += 1
                else:
                    if userInput[i] == str(self.questionNumList[j]):
                        b_count += 1
        result = str(a_conut) + "A" + str(b_count) + "B"
        if a_conut == 4:
            self.well_done = True
        return result


    def new_game(self):
        self.questionNumList = random.sample(range(10), 4)
        self.roundCount = 0
        self.well_done = False

    def get_ans(self):
        s = [str(i) for i in self.questionNumList]
        return "".join(s)

    def get_round_count(self):
        return self.roundCount

    def get_status(self):
        return self.well_done

    def set_time(self, t):
        self.time = t

    def ranking_check(self):
        return True

    def ranking(self, userName):
        self.leaderboard.append([userName, self.thread.get_time()])

    def set_time_string(self, time_string):
        # self.timeString = timeString
        self.thread.set_time_string(time_string)

    def get_stop_flag(self):
        return self.stopFlag

    def get_thread(self):
        return self.thread





