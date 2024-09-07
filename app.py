from flask import Flask, render_template,request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase,Mapped,mapped_column
from sqlalchemy import Integer,String,Float

from datetime import datetime

#Tables
class Base(DeclarativeBase):
    pass

database = SQLAlchemy(model_class = Base)


app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///data.db"

database.init_app(app)

class Content(database.Model):
    id : Mapped[int] = mapped_column(Integer, primary_key=True)
    content: Mapped[str] = mapped_column(String)
    time: Mapped[str] = mapped_column(String)
    
with app.app_context():
    database.create_all()

@app.route("/")
def index():
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
            return "Content uploaded successfully!"
        else:
            return 'no content found'
    return render_template("index.html")

@app.route("/receive",methods = ['POST','GET'])
def receive():
    content_object = database.session.execute(database.select(Content)).scalars().all()[-1]
    print(content_object.content)
    return render_template("index.html",render_content = content_object.content)


if __name__ == "__main__":
    app.run(debug=True)