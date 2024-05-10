import tkinter as tk
from tkinter import ttk
from nba_api.stats.static import players
from nba_api.stats.endpoints import playergamelog

nba_players = players.get_players()

# function to get player ID from name
def get_player_id(name):
    matched_names = []
    for player in nba_players:
        if player["full_name"].lower() == name.lower():
            return player["id"]
        elif player["full_name"].split() == name.split():
            return player["id"]
        elif player["first_name"].lower() == name.strip().lower() or player["last_name"].lower() == name.strip().lower():
            matched_names.append(player["full_name"])

    if matched_names:
        return matched_names
    else:
        return None

def calculate_stat(name, stat, amount, over_under):
    player_id = get_player_id(name)
    if player_id:
        game_log = playergamelog.PlayerGameLog(player_id=player_id, season="2022-23")
        game_log_df = game_log.get_data_frames()[0]
        point_totals = game_log_df.loc[0:4, stat.upper()].tolist()
        if over_under == 'Over':
            hit_times = sum(1 for x in point_totals if x > amount)
        else:
            hit_times = sum(1 for x in point_totals if x < amount)
        return hit_times
    else:
        return None


# Tkinter app
class NBAStatsApp:
    def __init__(self, master):
        self.master = master
        master.title("NBA Stats Calculator")

        self.label_name = tk.Label(master, text="Enter Player Name:")
        self.label_name.grid(row=0, column=0, padx=10, pady=5)

        self.player_name_entry = tk.Entry(master)
        self.player_name_entry.grid(row=0, column=1, padx=10, pady=5)

        self.label_stat = tk.Label(master, text="Select Stat:")
        self.label_stat.grid(row=1, column=0, padx=10, pady=5)

        self.stat_var = tk.StringVar()
        self.stat_combobox = ttk.Combobox(master, textvariable=self.stat_var)
        self.stat_combobox['values'] = ('PTS', 'AST', 'STL', 'TOV', 'REB')
        self.stat_combobox.grid(row=1, column=1, padx=10, pady=5)

        self.label_amount = tk.Label(master, text="Enter Amount:")
        self.label_amount.grid(row=2, column=0, padx=10, pady=5)

        self.amount_entry = tk.Entry(master)
        self.amount_entry.grid(row=2, column=1, padx=10, pady=5)

        self.over_under_var = tk.StringVar(value='Over')
        self.over_radio_over = tk.Radiobutton(master, text="Over", variable=self.over_under_var, value='Over')
        self.over_radio_over.grid(row=3, column=0, padx=5, pady=5)
        self.over_radio_under = tk.Radiobutton(master, text="Under", variable=self.over_under_var, value='Under')
        self.over_radio_under.grid(row=3, column=1, padx=5, pady=5)

        self.calculate_button = tk.Button(master, text="Calculate", command=self.calculate)
        self.calculate_button.grid(row=4, column=0, columnspan=2, padx=10, pady=5)

        self.result_label = tk.Label(master, text="")
        self.result_label.grid(row=5, column=0, columnspan=2, padx=10, pady=5)

    def calculate(self):
        player_name = self.player_name_entry.get().strip()
        stat = self.stat_var.get()
        amount = int(self.amount_entry.get().strip()) if self.amount_entry.get().strip() else None
        over_under = self.over_under_var.get()

        if player_name and stat and amount and over_under:
            hits = calculate_stat(player_name, stat, amount, over_under)
            if hits is not None:
                self.result_label.config(text=f"{player_name} hit the {stat} {over_under} {amount} {hits} times.")
            else:
                self.result_label.config(text=f"Player '{player_name}' not found.")
        else:
            self.result_label.config(text="Please fill in all fields.")


root = tk.Tk()
app = NBAStatsApp(root)
root.mainloop()
