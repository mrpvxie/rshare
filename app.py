from flask import Flask, render_template,request,url_for,redirect,jsonify
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase,Mapped,mapped_column
from sqlalchemy import Integer,String

from datetime import datetime
import re
import copy

#functions
def remove_tags(text):
    clean_text = re.sub(r'<.*?>', '', text)
    clean_text = re.sub(r'&nbsp;|&quot;', ' ', clean_text)
    clean_text = re.sub(r'\s+', ' ', clean_text).strip()
    return clean_text


class Base(DeclarativeBase):
    pass

database = SQLAlchemy(model_class = Base)


app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///data.db"

database.init_app(app)

#GLOBAL VARIABLES
current_page = None
small_upload_button_page = None

#TABLES 

class Content(database.Model):
    id : Mapped[int] = mapped_column(Integer, primary_key=True)
    content: Mapped[str] = mapped_column(String)
    time: Mapped[str] = mapped_column(String)
    
with app.app_context():
    database.create_all()

@app.route("/")
def index():
    print("--------------index route is running---------")
    return render_template("index.html")

@app.route("/upload",methods = ['POST','GET'])
def upload():
    print("--------------upload route is running---------")
    
    if request.method == "POST":
        content = request.form.get("summernote1")
        if content:
            
            current_date = datetime.now()

            day = current_date.day
            month = current_date.strftime("%B") 
            year = current_date.year
            
            new_content = Content(
                content = content,
                time = f"{day}/{month}/{year}"
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



@app.route("/table_data",methods = ['POST','GET'])
def table_data():
    print("--------------table_data route is running---------")
    global current_page
    current_page = "index"
    global small_upload_button_page
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

@app.route("/delete_content/<int:content_id>")
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
def full_content(content_id):
    print("--------------full_content route is running---------")
    global current_page
    global small_upload_button_page
    small_upload_button_page = "full_content"
    current_page = "table_data"
    chosen_content = database.session.execute(database.select(Content).where(Content.id == content_id)).scalar()
    return render_template("full_content.html",content_data = chosen_content)


@app.route("/back")
def back_button():
    print("--------------back_button route is running---------")
    return redirect(url_for(current_page))


@app.route('/get_json_data', methods=['GET'])
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


@app.route("/Edit/<int:content_id>",methods = ['POST','GET'])
def edit_content(content_id):
    print("--------------edit_content route is running---------")
    chosen_content = database.session.execute(database.select(Content).where(Content.id == content_id)).scalar()
    content = request.form.get("summernote2")
    current_date = datetime.now()
    day = current_date.day
    month = current_date.strftime("%B") 
    year = current_date.year
    chosen_content.content = content
    chosen_content.time = f"{day}/{month}/{year}(edited)"
    database.session.commit()
    return render_template("full_content.html",content_data = chosen_content)

@app.route("/small_upload/<int:content_id>",methods = ['POST','GET'])
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


if __name__ == "__main__":
    app.run(debug=True,host='0.0.0.0', port=5000)