from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///todos.db'
db = SQLAlchemy(app)

class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(250), nullable=False)
    is_done = db.Column(db.Boolean, nullable=False, default=False)

    def __repr__(self):
        return self.title

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        title = request.form['title']
        if title:
            todo = Todo(title=title)
            db.session.add(todo)
            db.session.commit()
        return redirect(url_for('index'))
    else:
        todos = Todo.query.all()[::-1]
        return render_template('index.html', todos=todos)

@app.route('/del/<int:id>')
def delete(id):
    db.session.delete(Todo.query.get(id))
    db.session.commit()
    return redirect(url_for('index'))

@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit(id):
    todo = Todo.query.get(id)
    if request.method == 'POST':
        title = request.form['title']
        todo.title = title
        db.session.add(todo)
        db.session.commit()
        return redirect(url_for('index'))
    return render_template('edit.html', todo=todo)

@app.route('/update/<int:id>', methods=['GET', 'POST'])
def update(id):
    todo = Todo.query.get(id)
    status = todo.is_done
    todo.is_done = not status
    db.session.add(todo)
    db.session.commit()
    return redirect(url_for('index'))


if __name__ == '__main__':
    app.run(debug=True)
