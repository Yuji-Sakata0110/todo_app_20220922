from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, date

# aplication settings including db
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///todo.db'
db = SQLAlchemy(app)


# Database Definition
class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(30), nullable=False)
    detail = db.Column(db.String(100))
    due = db.Column(db.DateTime, nullable=False)

# routing
@app.route('/', methods=['GET', 'POST'])
def index():
    # show all detaildata
    if request.method == 'GET':
        #　期限が近い順にソート
        posts = Post.query.order_by(Post.due).all()
        return render_template('index.html', posts=posts, today=date.today())
    # post function
    else:
        title = request.form.get('title')
        detail = request.form.get('detail')
        due = request.form.get('due')

        # dueを文字列に変換し、PostインスタンスにしてDBに格納する。
        due = datetime.strptime(due, '%Y-%m-%d')
        new_post = Post(title=title, detail=detail, due=due)

        db.session.add(new_post)
        db.session.commit()
        return redirect('/')

methods=['GET', 'POST']
@app.route('/create', methods=['GET', 'POST'])
def create():
    return render_template('create.html')

# show detail of posts
@app.route('/detail/<int:id>')
def read(id):
    post = Post.query.get(id)

    return render_template('detail.html', post=post)

# delete method
@app.route('/delete/<int:id>')
def delete(id):
    post = Post.query.get(id)

    db.session.delete(post)
    db.session.commit()
    return redirect('/')

# update method
@app.route('/update/<int:id>', methods=['GET', 'POST'])
def update(id):
    post = Post.query.get(id)
    if request.method == 'GET':
        return render_template('update.html', post=post)
    else:
        post.title = request.form.get('title')
        post.detail = request.form.get('detail')
        post.due = datetime.strptime(request.form.get('due'), '%Y-%m-%d')

        db.session.commit()
        return redirect('/')

# program awake
if __name__ == "__main__":
    app.run(debug=True)
