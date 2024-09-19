from flask import Flask, render_template, redirect, url_for, request
from flask_sqlalchemy import SQLAlchemy

# Flask uygulamasını oluşturuyoruz
app = Flask(__name__)

# Veritabanı bağlantı ayarını yapıyoruz
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///C:/Users/enssn/Desktop/todo_app/todo.db'
db = SQLAlchemy(app)

# Todo modelini tanımlıyoruz
class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    tittle = db.Column(db.String(80))
    complete = db.Column(db.Boolean)

@app.route("/")
def index():
    todos=Todo.query.all()
    return render_template('index.html',todos=todos)

@app.route("/add", methods=["POST"])
def addTodo():
    tittle = request.form.get("tittle")
    newTodo = Todo(tittle=tittle, complete=False)
    db.session.add(newTodo)
    db.session.commit()
    return redirect(url_for("index"))
@app.route("/complete/<string:id>")
def completeTodo(id):
    todo=Todo.query.filter_by(id=id).first()
    """if todo.complete==True:
        todo.complete=False
    else:
        todo.complete=True """
    todo.complete =not todo.complete   
    db.session.commit()
    return redirect(url_for("index"))
@app.route("/delete/<string:id>")
def deleteTodo(id):
    todo=Todo.query.filter_by(id=id).first()
    db.session.delete(todo)
    db.session.commit()
    return redirect(url_for("index"))
# Eğer bu dosya doğrudan çalıştırılıyorsa
if __name__ == "__main__":
    # Uygulama bağlamını başlatıyoruz
    with app.app_context():
        db.create_all()  # Veritabanı tablolarını oluşturuyoruz
    # Uygulamayı çalıştırıyoruz
    app.run(debug=True)
