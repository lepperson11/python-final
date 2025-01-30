from flask import Flask, json, render_template, request, url_for, redirect, flash, send_from_directory

app = Flask(__name__)

@app.route('/')
def home():
    return render_template("index.html")

@app.route('/games')
def games():
    with open("./static/json/games.json") as data_file:
        data = json.load(data_file)
        data_row = data["video_games"]
        game_name_list = []
        game_description_list = []
        game_image_list = []
        game_alt_list = []
        for row in data_row:
            game_name_list.append(row["name"])
            game_description_list.append(row["description"])
            game_image_list.append(row["image"])
            game_alt_list.append(row["alt"])
        count = len(game_name_list)
    return render_template("games.html", game_name_list = game_name_list, game_description_list = game_description_list, game_image_list = game_image_list, game_alt_list = game_alt_list, count = count)

@app.route('/consoles')
def consoles():
    with open("./static/json/consoles.json") as data_file:
        data = json.load(data_file)
        data_row = data["game_consoles"]
        console_name_list = []
        console_description_list = []
        console_image_list = []
        console_alt_list = []
        for row in data_row:
            console_name_list.append(row["name"])
            console_description_list.append(row["description"])
            console_image_list.append(row["image"])
            console_alt_list.append(row["alt"])
        count = len(console_name_list)
    return render_template("consoles.html", console_name_list = console_name_list, console_description_list = console_description_list, console_image_list = console_image_list, console_alt_list = console_alt_list, count = count)

@app.route('/accessories')
def accessories():
    with open("./static/json/accessories.json") as data_file:
        data = json.load(data_file)
        data_row = data["accessories"]
        accessories_name_list = []
        accessories_description_list = []
        accessories_image_list = []
        accessories_alt_list = []
        for row in data_row:
            accessories_name_list.append(row["name"])
            accessories_description_list.append(row["description"])
            accessories_image_list.append(row["image"])
            accessories_alt_list.append(row["alt"])
        count = len(accessories_name_list)
    return render_template("accessories.html", accessories_name_list = accessories_name_list, accessories_description_list = accessories_description_list, accessories_image_list = accessories_image_list, accessories_alt_list = accessories_alt_list, count = count)

@app.route('/computers')
def computers():
    with open("./static/json/computers.json") as data_file:
        data = json.load(data_file)
        data_row = data["computers"]
        computer_name_list = []
        computer_description_list = []
        computer_image_list = []
        computer_alt_list = []
        for row in data_row:
            computer_name_list.append(row["name"])
            computer_description_list.append(row["description"])
            computer_image_list.append(row["image"])
            computer_alt_list.append(row["alt"])
        count = len(computer_name_list)
    return render_template("computers.html", computer_name_list = computer_name_list, computer_description_list = computer_description_list, computer_image_list = computer_image_list, computer_alt_list = computer_alt_list, count = count)

@app.route('/monitors')
def monitors():
    with open("./static/json/monitors.json") as data_file:
        data = json.load(data_file)
        data_row = data["monitors"]
        monitor_name_list = []
        monitor_description_list = []
        monitor_image_list = []
        monitor_alt_list = []
        for row in data_row:
            monitor_name_list.append(row["name"])
            monitor_description_list.append(row["description"])
            monitor_image_list.append(row["image"])
            monitor_alt_list.append(row["alt"])
        count = len(monitor_name_list)
    return render_template("monitors.html", monitor_name_list = monitor_name_list, monitor_description_list = monitor_description_list, monitor_image_list = monitor_image_list, monitor_alt_list = monitor_alt_list, count = count)



if __name__ == "__main__":
    app.run(debug=True)