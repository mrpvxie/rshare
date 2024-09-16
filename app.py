from flask import Flask, render_template,request,url_for,redirect,jsonify
from flask_login import LoginManager,UserMixin,login_user,logout_user,current_user


from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase,Mapped,mapped_column
from sqlalchemy import Integer,String

from functools import wraps

from datetime import datetime
import re

# import pandas as pd


#FUNCTIONS

def remove_tags(text):
    clean_text = re.sub(r'<.*?>', '', text)
    clean_text = re.sub(r'&nbsp;|&quot;', ' ', clean_text)
    clean_text = re.sub(r'\s+', ' ', clean_text).strip()
    return clean_text

def current_time():
    current_date = datetime.now()
    day = current_date.day
    month = current_date.strftime("%B")  
    year = current_date.year
    return f"{day}/{month}/{year}"

# def read_csv_to_dict_list(csv_file_path):
#     df = pd.read_csv(csv_file_path)
    
#     data_list = df.to_dict(orient='records')
    
#     return data_list

#GLOBAL VARIABLES
is_admin = 0
current_user = None
app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///data.db"
app.config['SECRET_KEY']="rahulsharma122703"


login_manager =  LoginManager()
login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):
    return database.session.get(User,user_id)

#GLOBAL VARIABLES
current_page = None
small_upload_button_page = None

#TABLES 
class Base(DeclarativeBase):
    pass
database = SQLAlchemy(model_class = Base)
database.init_app(app)


class Content(database.Model):
    id : Mapped[int] = mapped_column(Integer, primary_key=True)
    content: Mapped[str] = mapped_column(String)
    time: Mapped[str] = mapped_column(String)
    
class User(UserMixin,database.Model):
    id:Mapped[int] = mapped_column(Integer, primary_key=True)
    username:Mapped[str] = mapped_column(String)
    created_on:Mapped[str] = mapped_column(String)
    email:Mapped[str] = mapped_column(String)
    password:Mapped[str] = mapped_column(String)
    
   
with app.app_context():
    database.create_all()


#RTG_FUNCTIONS
def admin_only(function):
    @wraps(function)
    def wrapper(*args,**kwargs):
        if (not is_admin):
            return render_template("admin_only.html")   
        return function(*args,**kwargs)
    return wrapper    
    

@app.context_processor
def common_variable():
    global current_user
    return dict(current_user = current_user,wrong_password = 0)

@app.route("/")
def index():
    global is_admin,current_page
    current_page = "index"
    is_admin = 0
    print("--------------index route is running---------")
    return render_template("index.html")

@app.route("/upload",methods = ['POST','GET'])
def upload():
    print("--------------upload route is running---------")
    
    if request.method == "POST":
        content = request.form.get("summernote1")
        if content:   
            new_content = Content(
                content = content,
                time = current_time()
            )
            
            database.session.add(new_content)
            database.session.commit()
            return render_template("index.html")

        else:
            return render_template("index.html")
    return render_template("index.html")

@app.route("/receive",methods = ['POST','GET'])
def receive():
    print("--------------receive route is running---------")
    content_object = database.session.execute(database.select(Content)).scalars().all()[-1]
    return render_template("index.html",render_content = content_object.content)



@app.route("/table_data")
@admin_only
def table_data():
    print("--------------table_data route is running---------")
    global current_page,small_upload_button_page
    current_page = "index"
    small_upload_button_page = "table_data"
    content_data = Content.query.all()
    json_data = [
        {
            'id': content.id,
            'content': remove_tags(content.content),
            'time': content.time  
        } for content in content_data
    ]
    return render_template("table_data.html", data = json_data)


@app.route("/check_for_admin")
def check_for_admin():
    print("--------------check_for_admin route is running---------")
    global is_admin
    is_admin = 1
    return redirect(url_for("table_data")) 

@app.route("/delete_content/<int:content_id>")
@admin_only
def delete_content(content_id):
    print("--------------delete_content route is running---------")
    content_to_delete = database.get_or_404(Content,content_id)
    database.session.delete(content_to_delete)
    database.session.commit()
    content_data = Content.query.all()
    json_data = [
        {
            'id': content.id,
            'content': remove_tags(content.content),
            'time': content.time  
        } for content in content_data
    ]
    return render_template("table_data.html", data = json_data)


@app.route("/full_content/<int:content_id>",methods = ['POST','GET'])
@admin_only
def full_content(content_id):
    print("--------------full_content route is running---------")
    global current_page,small_upload_button_page
    small_upload_button_page = "full_content"
    current_page = "table_data"
    chosen_content = database.session.execute(database.select(Content).where(Content.id == content_id)).scalar()
    return render_template("full_content.html",content_data = chosen_content)


@app.route("/back")
def back_button():
    print("--------------back_button route is running---------")
    return redirect(url_for(current_page))

@app.route('/get_json_data_content', methods=['GET'])
@admin_only
def get_data():
    print("--------------get_data route is running---------")
    
    contents = Content.query.all()
    data = [
        {
            'id': content.id,
            'content': content.content,
            'time': content.time  
        } for content in contents
    ]
    
    return jsonify(data)

@app.route('/get_json_data_user', methods=['GET']) #123
def get_data_user():
    print("--------------get_data_user route is running---------")
    
    users = User.query.all()
    data = [
        {
            'id': user.id,
            'username': user.username,
            'email': user.email  
        } for user in users
    ]
    
    return jsonify(data)

@app.route("/Edit/<int:content_id>",methods = ['POST','GET'])
@admin_only
def edit_content(content_id):
    print("--------------edit_content route is running---------")
    chosen_content = database.session.execute(database.select(Content).where(Content.id == content_id)).scalar()
    content = request.form.get("summernote2")
    chosen_content.content = content
    chosen_content.time = current_time()
    database.session.commit()
    return render_template("full_content.html",content_data = chosen_content)

@app.route("/small_upload/<int:content_id>",methods = ['POST','GET'])
@admin_only
def small_upload(content_id):
    global small_upload_button_page
    
    print("--------------small_upload route is running---------")
    chosen_content = database.session.execute(database.select(Content).where(Content.id == content_id)).scalar()
    
    new_content = Content(
    content = chosen_content.content,
    time = chosen_content.time
    )
    database.session.add(new_content)
    database.session.delete(chosen_content)
    database.session.commit()
    if small_upload_button_page == "table_data":
        content_data = Content.query.all()
        json_data = [
            {
                'id': content.id,
                'content': remove_tags(content.content),
                'time': content.time  
            } for content in content_data
        ]
        return render_template("table_data.html", data = json_data)
    
    return render_template("full_content.html",content_data = chosen_content)


@app.route('/register',methods = ['GET','POST'])
def register():
    print("--------------register route is running---------")
    global current_user
    all_user_data = database.session.execute(database.select(User)).scalars().all()
    emails = [user.email for user in all_user_data]
    usernames = [user.username for user in all_user_data]      
    if request.method =="POST":
        new_user = User(
            username = request.form.get("username").lower(),
            created_on = current_time(),
            email = request.form.get("email").lower(),
            password = request.form.get("password")
        )
        database.session.add(new_user)
        database.session.commit()
        login_user(new_user)
        current_user = new_user
        return render_template('index.html')
    return render_template('register.html',emails = emails,usernames = usernames)

@app.route('/login',methods = ['GET','POST'])
def login():
    print("--------------login route is running---------")
    global current_user
    if request.method == "POST":
        username_input_data = request.form.get("username_or_email").lower()
        password_input_data = request.form.get("password")
        chosen_username = None
        if("@" in username_input_data):
            chosen_username = database.session.execute(database.select(User).filter(User.email == username_input_data)).scalar()
        else:
            chosen_username = database.session.execute(database.select(User).filter(User.username == username_input_data)).scalar()
        if chosen_username.password == password_input_data:
            login_user(chosen_username)
        else:
            return render_template('index.html',wrong_password = 1)
        current_user = chosen_username
        return render_template('index.html')   
    return render_template('index.html')

@app.route('/logout')
def logout():
    print("--------------logout route is running---------")
    global current_user
    current_user = None
    logout_user()
    return redirect(url_for('index'))
# @app.route("/insert_data")
# def insert_data():
#     print("--------------insert_data route is running---------")
#     all_content = database.session.execute(database.select(Content)).scalars().all()
#     data_list = read_csv_to_dict_list("output.csv")
#     count  = 0
#     for data in all_content:
#         data.id =  data_list[count]['id']
#         data.content = data_list[count]['content']
#         data.time = data_list[count]['time']
#         count += 1
#     database.session.commit()
#     return "<h1>DATA INSERTED SUCCESSFULLY</H1>"

if __name__ == "__main__":
    app.run(debug=True,host='0.0.0.0', port=5000)