import pymysql
from flask import Flask, request, session, g, redirect, url_for, abort, \
     render_template, flash
from flask_bootstrap import Bootstrap
from form import Register_form,Login_form
import hashlib
#from flask.ext.script import Manager

# create our little application :)
app = Flask(__name__)
bootstrap=Bootstrap(app)
#设置默认的环境变量
app.config.update(dict(LOGIN_NAME='admin',LOGIN_PASSWD='default',SECRET_KEY='hello world'))
def get_cursor():
    #连接mysql数据库
    cur=pymysql.connect(db='hello',user='root',port=3306,host='localhost',passwd='huanghu')
    return cur
#检查登录的用户的用户名与密码是否正确
def is_true(username,password):
    with get_cursor() as cur:
        if cur.execute('select * from users where username=%s and md5_password=%s',[username,password]):
            return True
        return False

def generate_md5_password(username,password):
    md5=hashlib.md5()
    md5.update((password+'salt'+username).encode('utf-8'))
    return md5.hexdigest()

@app.route('/')
def show_entries():
    with get_cursor() as cur:
        cur.execute('select title, content from entries order by id desc limit 3')
        entries = cur.fetchall()
    return render_template('show_entries.html', entries=entries)

@app.route('/add',methods=['POST'])
def add_entry():
    title=request.form['title']
    content=request.form['content']
    with get_cursor() as cur:
        cur.execute('insert into entries(title,content) values(%s,%s)',[title,content])
    return redirect(url_for('show_entries'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    form=Login_form()
    if form.validate_on_submit():
        if is_true(request.form['username'],generate_md5_password(request.form['username'],\
                                                                  request.form['password'])):
            session['logged_in'] = True
            flash('You were logged in')
            return redirect(url_for('show_entries'))
        else:
            error='username or password is Error'
    return render_template('login.html',form=form,error=error)

@app.route('/logout')
def logout():
    session.pop('logged_in',None)
    return redirect(url_for('show_entries'))

@app.route('/register',methods=['GET','POST'])
def register_user():
    form=Register_form()
    if form.validate_on_submit():
        username=request.form['username']
        md5_password=generate_md5_password(request.form['username'],request.form['password'])
        with get_cursor() as cur:
            if cur.execute('select id from users where username=%s and md5_password=%s',[username,md5_password]):
                flash('the usename and password has existed')
                return redirect(url_for('register_user'))
            else:
                cur.execute('insert into users(username,md5_password) values(%s,%s)',[username,md5_password])
                flash('you have register successfully,and now will redirect to index page')
                return redirect('login')
#    flash('you has successful register')
    return render_template('register.html',form=form)
#    return redirect('login')




if __name__=='__main__':
    app.run(debug=True)
