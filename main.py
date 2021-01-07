import tkinter as tk
import guessingMachine.machine as guessingMachine

# ======================================================
# button function ======================================
# ======================================================

def new_game():
    outputBox.delete('1.0', "end")
    userInputBox.delete(0, "end")
    gm.new_game()
    runButton['state'] = tk.NORMAL
    thread.restart()

def finished_or_not():
    result = gm.click_run(userInput.get())
    userInputBox.delete(0, "end")
    outputBox.insert("end", result)
    if gm.get_status():
        # already finished, open new window
        thread.pause()
        # disable button
        runButton['state'] = tk.DISABLED
        if gm.ranking_check():
            # input your name
            create_leaderboard_input_window()
        create_end_window()

    elif gm.get_round_count() >= 10:
        outputBox.insert("end", "You lose!! Answer: " + gm.get_ans() + "\n")
        thread.pause()
        runButton['state'] = tk.DISABLED
        create_end_window()
        
def exit():
    stopFlag.set()
    top.destroy()

def create_end_window():
    end_window = tk.Toplevel(top)
    end_window.title("next?")
    f = tk.Frame(end_window)
    tk.Button(f, text="Leaderboard", command=show_leaderboard).grid(row=0, column=1)
    tk.Button(f, text="New Game", command=lambda: [new_game(), end_window.destroy()]).grid(row=1, column=1)
    tk.Button(f, text="exit", command=exit).grid(row=2, column=1)
    f.pack()
    end_window.mainloop()

def create_leaderboard_input_window():
    ranking_input_window = tk.Toplevel(top)
    f = tk.Frame(ranking_input_window)
    userName = tk.StringVar()
    tk.Label(f, text="congratulations! You are qualified to enter the leaderboard!").grid(row=0, column=1)
    tk.Entry(f, width=20, textvariable=userName).grid(row=1, column=1)
    tk.Button(f, text="Enter", command=lambda: [
        gm.ranking(userName.get()),
        ranking_input_window.destroy(),
        create_end_window()
    ]).grid(row=2, column=1)
    f.pack()
    ranking_input_window.mainloop()

def show_leaderboard():
    # leaderboardDF
    leaderboard_window = tk.Toplevel(top)
    leaderboard_window.title("Leaderboard")
    f = tk.Frame(leaderboard_window)
    record = tk.StringVar()
    record.set(gm.get_leaderboard())
    leaderboard_output_box = tk.Text(f)
    leaderboard_output_box.grid(row=0, column=1)
    leaderboard_output_box.insert("end", record.get())
    leaderboard_output_box['state'] = tk.DISABLED
    tk.Button(f, text="Close", command=lambda: [leaderboard_window.destroy()]).grid(row=1,column=1)
    f.pack()
    leaderboard_window.mainloop()
# ======================================================
# ======================================================
# ======================================================



# ======================================================
# layout ===============================================
# ======================================================
top = tk.Tk()
top.title("number guessing")
f1 = tk.Frame(top)

gm = guessingMachine.GuessingMachine()

time_string = tk.StringVar()
gm.set_time_string(time_string)
userInput = tk.StringVar()

timeLabel = tk.Label(f1, textvariable=time_string).grid(row=0, column=1)
welcomeLabel = tk.Label(f1, text="Welcome to Number Game~").grid(row=1, column=1)
userInputBox = tk.Entry(f1, width=20, textvariable=userInput)
userInputBox.grid(row=2, column=1)

outputBox = tk.Text(f1)
outputBox.grid(row=4, column=1)

# submit answer
runButton = tk.Button(f1, text="RUN", command=finished_or_not)
runButton.grid(row=3, column=1)

# show answer
showAnsButton = tk.Button(f1, text="Show Answer", command=lambda: (
    outputBox.insert("end", "Answer: " + gm.get_ans() + "\n")
)).grid(row=5, column=1)

# new game
newGameButton = tk.Button(f1, text="New Game", command=new_game).grid(row=6, column=1)

# show leaderboard
leaderboardButton = tk.Button(f1, text="leaderboard", command=show_leaderboard).grid(row=7,column=1)

exitButton = tk.Button(f1, text="exit", command=exit).grid(row=8, column=1)

f1.pack()
# ======================================================
# ======================================================
# ======================================================
stopFlag = gm.get_stop_flag()
thread = gm.get_thread()
thread.start()

top.mainloop()

