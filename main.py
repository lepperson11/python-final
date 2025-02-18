from flask import Flask, render_template, request, url_for, redirect, session
from bson import ObjectId
from pymongo import MongoClient
import bcrypt
from dotenv import load_dotenv
import os
import certifi

load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv('SECRETKEY')

client = MongoClient(os.getenv('MONGODB_URI'), tlsCAFile=certifi.where())
db = client.get_database('pythonfinal')
users = db.users
accessoriesdb = db.accessories
computersdb = db.computers
consolesdb = db.consoles
gamesdb = db.games
monitorsdb = db.monitors

# class Base(DeclarativeBase):
#     pass
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
# db = SQLAlchemy(model_class=Base)
# db.init_app(app)

# login_manager = LoginManager()
# login_manager.init_app(app)

# @login_manager.user_loader
# def load_user(user_id):
#     return db.get_or_404(User, user_id)

# class User(UserMixin, db.Model):
#     id: Mapped[int] = mapped_column(Integer, primary_key=True)
#     email: Mapped[str] = mapped_column(String(100), unique=True)
#     password: Mapped[str] = mapped_column(String(100))

# with app.app_context():
#     db.create_all()

@app.route('/')
def home():
    return render_template("index.html")

@app.route('/games')
def games():
    game_row = list(db.games.find({}))
    game_name_list = []
    game_description_list = []
    game_image_list = []
    game_alt_list = []
    id_list = []
    type_list = []
    row(game_row, game_name_list, game_description_list, game_image_list, game_alt_list, id_list, type_list)
    count = len(game_name_list)
    return render_template("games.html", game_name_list = game_name_list, game_description_list = game_description_list, game_image_list = game_image_list, game_alt_list = game_alt_list, count = count)

@app.route('/consoles')
def consoles():
    console_row = list(db.consoles.find({}))
    console_name_list = []
    console_description_list = []
    console_image_list = []
    console_alt_list = []
    id_list = []
    type_list = []
    row(console_row, console_name_list, console_description_list, console_image_list, console_alt_list, id_list, type_list)
    count = len(console_name_list)
    return render_template("consoles.html", console_name_list = console_name_list, console_description_list = console_description_list, console_image_list = console_image_list, console_alt_list = console_alt_list, count = count)

@app.route('/accessories')
def accessories():
    accessories_row = list(db.accessories.find({}))
    accessories_name_list = []
    accessories_description_list = []
    accessories_image_list = []
    accessories_alt_list = []
    id_list = []
    type_list = []
    row(accessories_row, accessories_name_list, accessories_description_list, accessories_image_list, accessories_alt_list, id_list, type_list)
    count = len(accessories_name_list)
    return render_template("accessories.html", accessories_name_list = accessories_name_list, accessories_description_list = accessories_description_list, accessories_image_list = accessories_image_list, accessories_alt_list = accessories_alt_list, count = count)

@app.route('/computers')
def computers():
    computer_row = list(db.computers.find({}))
    computer_name_list = []
    computer_description_list = []
    computer_image_list = []
    computer_alt_list = []
    id_list = []
    type_list = []
    row(computer_row, computer_name_list, computer_description_list, computer_image_list, computer_alt_list, id_list, type_list)
    count = len(computer_name_list)
    return render_template("computers.html", computer_name_list = computer_name_list, computer_description_list = computer_description_list, computer_image_list = computer_image_list, computer_alt_list = computer_alt_list, count = count)

@app.route('/monitors')
def monitors():
    monitors_row = list(db.monitors.find({}))
    monitor_name_list = []
    monitor_description_list = []
    monitor_image_list = []
    monitor_alt_list = []
    id_list = []
    type_list = []
    row(monitors_row, monitor_name_list, monitor_description_list, monitor_image_list, monitor_alt_list, id_list, type_list)
    count = len(monitor_name_list)
    return render_template("monitors.html", monitor_name_list = monitor_name_list, monitor_description_list = monitor_description_list, monitor_image_list = monitor_image_list, monitor_alt_list = monitor_alt_list, count = count)


@app.route('/login', methods=["GET", "POST"])
def login():
    message = 'Please login to your account'
    if "email" in session:
        return redirect(url_for("admin"))

    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")

        #check if email exists in database
        email_found = users.find_one({"email": email})
        if email_found:
            email_val = email_found['email']
            passwordcheck = email_found['password']
            #encode the password and check if it matches
            if bcrypt.checkpw(password.encode('utf-8'), passwordcheck):
                session["email"] = email_val
                return redirect(url_for('admin'))
            else:
                if "email" in session:
                    return redirect(url_for("admin"))
                message = 'Wrong password'
                return render_template('login.html', message=message)
        else:
            message = 'Email not found'
            return render_template('login.html', message=message)
    # if request.method == "POST":
    #     email = request.form.get('email')
    #     password = request.form.get('password')

    #     result = db.session.execute(db.select(User).where(User.email == email))
    #     user = result.scalar()

    #     if not user:
    #         flash("The email or password is incorrect or does not exist")
    #         return redirect(url_for('login'))
    #     elif not check_password_hash(user.password, password):
    #         flash("The email or password is incorrect or does not exist")
    #         return redirect(url_for('login'))
    #     else:
    #         login_user(user)
    #         return redirect(url_for('admin'))

    return render_template("login.html", message = message)

@app.route('/register', methods=["GET", "POST"])
def register():
    message = ""

    if "email" in session:
        return redirect(url_for("login"))
    
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")

        email_found = users.find_one({"email": email})
        if email_found:
            message = "This email already exists in database"
            return render_template('register.html', message=message)
        else:
            hashed = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

            user_input = {'email': email, 'password': hashed}
            users.insert_one(user_input)
            return redirect(url_for('admin'))

    # if request.method == "POST":
    #     email = request.form.get('email')
    #     result = db.session.execute(db.select(User).where(User.email == email))
    #     user = result.scalar()
    #     if user:
    #         flash("You already have an account with that email, use log in instead!")
    #         return redirect(url_for('login'))
    #     hash_salt_pass = generate_password_hash(request.form.get('password'), method="pbkdf2:sha256", salt_length=9)
    #     new_user = User(
    #         email=request.form.get('email'),
    #         password=hash_salt_pass
    #     )
        
    #     db.session.add(new_user)
    #     db.session.commit()

    #     login_user(new_user)
        
    #     return redirect(url_for("admin"))

    return render_template("register.html")

def row(row_list, name, description, image, alt, _id, type_):
    for row in row_list:
            _id.append(row["_id"])
            name.append(row["name"])
            description.append(row["description"])
            image.append(row["image"])
            alt.append(row["alt"])
            type_.append(row["type"])
    return name, description, image, alt, _id, type_

@app.route('/admin', methods=["GET", "POST"])
def admin():
    if "email" in session:
        accessories_row = list(db.accessories.find({}))
        consoles_row = list(db.consoles.find({}))
        computers_row = list(db.computers.find({}))
        games_row = list(db.games.find({}))
        monitors_row = list(db.monitors.find({}))
        name_list = []
        description_list = []
        image_list = []
        alt_list = []
        id_list = []
        type_list = []
        row(accessories_row, name_list, description_list, image_list, alt_list, id_list, type_list)
        row(consoles_row, name_list, description_list, image_list, alt_list, id_list, type_list)
        row(computers_row, name_list, description_list, image_list, alt_list, id_list, type_list)
        row(games_row, name_list, description_list, image_list, alt_list, id_list, type_list)
        row(monitors_row, name_list, description_list, image_list, alt_list, id_list, type_list)
        count = len(name_list)
        if request.method == "POST":
            return edit(request.form.get("edit_submit"), name_list, description_list, id_list, image_list, alt_list, type_list)
        return render_template("admin.html", name_list = name_list, description_list = description_list, image_list = image_list, alt_list = alt_list, id_list = id_list, count = count, logged_in=True)
    else:
        return redirect(url_for("login"))
    
@app.route('/edit', methods=["GET", "POST"])
def edit(_id, name_list, description_list, id_list, image_list, alt_list, type_list):
    
    name = ""
    description = ""
    image = ""
    alt = ""
    type_ = ""
    count = 0
    for row in id_list:
        if str(_id) == str(row):
            name = name_list[count]
            description = description_list[count]
            image = image_list[count]
            alt = alt_list[count]
            type_ = type_list[count]
        count += 1
    
    if request.method == "POST":
        new_name = request.form.get("name")
        new_description = request.form.get("description")

        query = {"_id": ObjectId(_id)}
        product_input = {'_id': _id, 'image': image, 'alt': alt, 'name': new_name, 'description': new_description, 'type': type_}
        if type_ == "games":
            gamesdb.update_one(query, {"$set":{'image': image, 'alt': alt, 'name': new_name, 'description': new_description, 'type': type_}}, upsert=True)

        # return redirect(url_for('admin'))
    
    return render_template("edit.html", name = name, description = description)

@app.route('/logout', methods=["POST", "GET"])
def logout():
    if "email" in session:
        session.pop("email", None)
        return render_template("index.html")
    else:
        return redirect(url_for('login'))

if __name__ == "__main__":
  app.run(debug=True)