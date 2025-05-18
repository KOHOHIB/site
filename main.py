from flask_wtf import FlaskForm
from flask_login import LoginManager, login_user
from flask import Flask, request, make_response, session, render_template, redirect
from wtforms.validators import DataRequired
from data import db_session
from wtforms import EmailField, PasswordField, BooleanField, SubmitField, TextAreaField, Field
from data.users import User
from data.themes import Themes
from data.comments import Comments
import datetime


class UserData:
    username = ""
    a = 0

app = Flask(__name__)
app.config['PERMANENT_SESSION_LIFETIME'] = datetime.timedelta(
    days=365
)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'
login_manager = LoginManager()
login_manager.init_app(app)


@login_manager.user_loader
def load_user(user_id):
    db_sess = db_session.create_session()
    return db_sess.query(User).get(user_id)


class LoginForm(FlaskForm):
    email = EmailField('Почта', validators=[DataRequired()])
    password = PasswordField('Пароль', validators=[DataRequired()])
    remember_me = BooleanField('Запомнить меня')
    submit = SubmitField('Войти')


class RegisterForm(FlaskForm):
    email = EmailField('Почта', validators=[DataRequired()])
    password = PasswordField('Пароль', validators=[DataRequired()])
    id = TextAreaField("id")
    surname = TextAreaField("фамилия")
    name = TextAreaField("имя")
    age = TextAreaField("возраст")
    position = TextAreaField("позиция")
    spetiality = TextAreaField("специальность")
    address = TextAreaField("адрес")
    submit = SubmitField('Зарегистрироваться')


class ThemeForm(FlaskForm):
    id = TextAreaField("id")
    theme = TextAreaField('Theme', validators=[DataRequired()])
    text = TextAreaField('Text', validators=[DataRequired()])
    submit = SubmitField('Добавить')


class ThemeForm2(FlaskForm):
    comment = TextAreaField("Добавить комментарий")
    delete_id = TextAreaField("ID удаляемого комментария")
    submit = SubmitField('Добавить')
    submit2 = SubmitField('Удалить')


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        db_session.global_init("db/blogs.db")
        db_sess = db_session.create_session()
        user = db_sess.query(User).filter(User.email == form.email.data).first()
        print(form.email.data)
        if user and user.hashed_password == form.password.data:
            login_user(user, remember=form.remember_me.data)
            UserData.username = user.name
            return redirect("/")
        return render_template('login.html',
                               message="Неправильный логин или пароль",
                               form=form)
    return render_template('login.html', title='Авторизация', form=form)


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    db_session.global_init("db/blogs.db")
    db_sess = db_session.create_session()
    user = User()
    user.id = form.id.data
    user.surname = form.surname.data
    user.name = form.name.data
    user.age = form.age.data
    user.position = form.position.data
    user.spetiality = form.spetiality.data
    user.address = form.address.data
    user.email = form.email.data
    user.hashed_password = form.password.data
    if form.validate_on_submit():
        db_sess.add(user)
        db_sess.commit()
        db_sess.close()
        return redirect("/login")
    return render_template('register.html', title='Авторизация', form=form)


@app.route('/addtheme', methods=['GET', 'POST'])
def addtheme():
    form = ThemeForm()
    db_session.global_init("db/themes.db")
    db_sess = db_session.create_session()
    if form.validate_on_submit() and UserData.username != "":
        theme1 = Themes()
        theme1.id = form.id.data
        theme1.theme = form.theme.data
        theme1.text = form.text.data
        theme1.owner_name = UserData.username
        db_sess.add(theme1)
        db_sess.commit()
        db_sess.close()
    return render_template('job.html', form=form)


@app.route('/', methods=['GET', 'POST'])
def a():
    db_session.global_init("db/themes.db")
    db_sess = db_session.create_session()
    zzz = db_sess.query(Themes).all()
    all_themes = []
    for i in zzz:
        all_themes.append(i.theme)
        print(i.theme)
    all1 = []
    all1.append(all_themes)
    UserData.a = all1
    return render_template('main.html', name=UserData.username, all=all1)


@app.route('/theme/<name>', methods=['GET', 'POST'])
def theme(name):
    form = ThemeForm2()
    db_session.global_init("db/themes.db")
    db_sess = db_session.create_session()
    theme = db_sess.query(Themes).filter(Themes.theme == name).first()
    db_sess.close()

    db_session.global_init("db/comments.db")
    db_sess = db_session.create_session()
    if form.validate_on_submit() and UserData.username != "":
        new_comment = Comments()
        new_comment.text = form.comment.data
        new_comment.theme_id = name
        new_comment.owner_name = UserData.username
        db_sess.add(new_comment)
        db_sess.commit()
        db_sess.close()

    comments1 = db_sess.query(Comments).filter(Comments.theme_id == theme.theme).all()

    return render_template('theme.html', form=form, name=theme.theme, text=theme.text, comments=comments1)


@app.route('/delete_comment/<delete_id>', methods=['GET', 'POST'])
def delete_comment(delete_id):
    form = ThemeForm2()
    db_session.global_init("db/comments.db")
    db_sess = db_session.create_session()
    db_sess.query(Comments).filter_by(id=int(delete_id)).delete()
    print(a)
    db_sess.commit()
    db_sess.close()
    return render_template('delete.html', form=form)


def main():
    app.run()


if __name__ == '__main__':
    main()
