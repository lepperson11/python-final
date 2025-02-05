from flask import Flask, render_template, request, url_for, redirect, flash, send_from_directory
from werkzeug.security import generate_password_hash, check_password_hash
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import Integer, String
from flask_login import UserMixin, login_user, LoginManager, login_required, current_user, logout_user
import json

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret-key-goes-here'

class Base(DeclarativeBase):
    pass
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
db = SQLAlchemy(model_class=Base)
db.init_app(app)

login_manager = LoginManager()
login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):
    return db.get_or_404(User, user_id)

class User(UserMixin, db.Model):
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    email: Mapped[str] = mapped_column(String(100), unique=True)
    password: Mapped[str] = mapped_column(String(100))

with app.app_context():
    db.create_all()

@app.route('/')
def home():
    return render_template("index.html")

@app.route('/games')
def games():
    with open("./static/json/products.json") as data_file:
        data = json.load(data_file)
        game_row = data["products"]["video_games"]
        game_name_list = []
        game_description_list = []
        game_image_list = []
        game_alt_list = []
        row(game_row, game_name_list, game_description_list, game_image_list, game_alt_list)
        count = len(game_name_list)
    return render_template("games.html", game_name_list = game_name_list, game_description_list = game_description_list, game_image_list = game_image_list, game_alt_list = game_alt_list, count = count)

@app.route('/consoles')
def consoles():
    with open("./static/json/products.json") as data_file:
        data = json.load(data_file)
        console_row = data["products"]["game_consoles"]
        console_name_list = []
        console_description_list = []
        console_image_list = []
        console_alt_list = []
        row(console_row, console_name_list, console_description_list, console_image_list, console_alt_list)
        count = len(console_name_list)
    return render_template("consoles.html", console_name_list = console_name_list, console_description_list = console_description_list, console_image_list = console_image_list, console_alt_list = console_alt_list, count = count)

@app.route('/accessories')
def accessories():
    with open("./static/json/products.json") as data_file:
        data = json.load(data_file)
        accessories_row = data["products"]["accessories"]
        accessories_name_list = []
        accessories_description_list = []
        accessories_image_list = []
        accessories_alt_list = []
        row(accessories_row, accessories_name_list, accessories_description_list, accessories_image_list, accessories_alt_list)
        count = len(accessories_name_list)
    return render_template("accessories.html", accessories_name_list = accessories_name_list, accessories_description_list = accessories_description_list, accessories_image_list = accessories_image_list, accessories_alt_list = accessories_alt_list, count = count)

@app.route('/computers')
def computers():
    with open("./static/json/products.json") as data_file:
        data = json.load(data_file)
        computer_row = data["products"]["computers"]
        computer_name_list = []
        computer_description_list = []
        computer_image_list = []
        computer_alt_list = []
        row(computer_row, computer_name_list, computer_description_list, computer_image_list, computer_alt_list)
        count = len(computer_name_list)
    return render_template("computers.html", computer_name_list = computer_name_list, computer_description_list = computer_description_list, computer_image_list = computer_image_list, computer_alt_list = computer_alt_list, count = count)

@app.route('/monitors')
def monitors():
    with open("./static/json/products.json") as data_file:
        data = json.load(data_file)
        monitors_row = data["products"]["monitors"]
        monitor_name_list = []
        monitor_description_list = []
        monitor_image_list = []
        monitor_alt_list = []
        row(monitors_row, monitor_name_list, monitor_description_list, monitor_image_list, monitor_alt_list)
        count = len(monitor_name_list)
    return render_template("monitors.html", monitor_name_list = monitor_name_list, monitor_description_list = monitor_description_list, monitor_image_list = monitor_image_list, monitor_alt_list = monitor_alt_list, count = count)


@app.route('/login', methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form.get('email')
        password = request.form.get('password')

        result = db.session.execute(db.select(User).where(User.email == email))
        user = result.scalar()

        if not user:
            flash("The email or password is incorrect or does not exist")
            return redirect(url_for('login'))
        elif not check_password_hash(user.password, password):
            flash("The email or password is incorrect or does not exist")
            return redirect(url_for('login'))
        else:
            login_user(user)
            return redirect(url_for('admin'))

    return render_template("login.html", logged_in=current_user.is_authenticated)

@app.route('/register', methods=["GET", "POST"])
def register():
    if request.method == "POST":
        email = request.form.get('email')
        result = db.session.execute(db.select(User).where(User.email == email))
        user = result.scalar()
        if user:
            flash("You already have an account with that email, use log in instead!")
            return redirect(url_for('login'))
        hash_salt_pass = generate_password_hash(request.form.get('password'), method="pbkdf2:sha256", salt_length=9)
        new_user = User(
            email=request.form.get('email'),
            password=hash_salt_pass
        )
        
        db.session.add(new_user)
        db.session.commit()

        login_user(new_user)
        
        return redirect(url_for("admin"))

    return render_template("register.html", logged_in=current_user.is_authenticated)

def row(row_list, name, description, image, alt):
    for row in row_list:
            name.append(row["name"])
            description.append(row["description"])
            image.append(row["image"])
            alt.append(row["alt"])
    return name, description, image, alt

@app.route('/admin')
@login_required
def admin():
    with open("./static/json/products.json") as data_file:
        data = json.load(data_file)
        accessories_row = data["products"]["accessories"]
        consoles_row = data["products"]["game_consoles"]
        computers_row = data["products"]["computers"]
        games_row = data["products"]["video_games"]
        monitors_row = data["products"]["monitors"]
        name_list = []
        description_list = []
        image_list = []
        alt_list = []
        row(accessories_row, name_list, description_list, image_list, alt_list)
        row(consoles_row, name_list, description_list, image_list, alt_list)
        row(computers_row, name_list, description_list, image_list, alt_list)
        row(games_row, name_list, description_list, image_list, alt_list)
        row(monitors_row, name_list, description_list, image_list, alt_list)
        count = len(name_list)
    return render_template("admin.html", name_list = name_list, description_list = description_list, image_list = image_list, alt_list = alt_list, count = count, logged_in=True)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('home'))

if __name__ == "__main__":
    app.run(debug=True)