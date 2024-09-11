from flask import Flask, render_template,request,url_for,redirect,jsonify
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase,Mapped,mapped_column
from sqlalchemy import Integer,String,Float

from datetime import datetime
import re

#functions
def remove_tags(text):
    clean_text = re.sub(r'<.*?>', '', text)
    clean_text = re.sub(r'&nbsp;|&quot;', ' ', clean_text)
    clean_text = re.sub(r'\s+', ' ', clean_text).strip()
    return clean_text

#Tables
class Base(DeclarativeBase):
    pass

database = SQLAlchemy(model_class = Base)


app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///data.db"

database.init_app(app)

current_page = None

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
    content_object = database.session.execute(database.select(Content)).scalars().all()[-1]
    print(content_object.content)
    return render_template("index.html",render_content = content_object.content)



@app.route("/table_data",methods = ['POST','GET'])
def table_data():
    print("--------------table_data route is running---------")
    global current_page
    current_page = "index"
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
    global current_page
    current_page = "table_data"
    chosen_content = database.session.execute(database.select(Content).where(Content.id == content_id)).scalar()
    return render_template("full_content.html",content_data = chosen_content.content)


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
            'time': content.time  # Convert datetime to ISO format
        } for content in contents
    ]
    
    return jsonify(data)

if __name__ == "__main__":
    app.run(debug=True,host='0.0.0.0', port=5000)