from flask import request, redirect, url_for, render_template, flash, session
from flask_blog import app
from functools import wraps

def login_required(view):
    @wraps(view)
    def inner(*args, **kwargs):
        if not session.get('logged_in'):
            return redirect(url_for('login'))
        return view(*args, **kwargs)
    return inner


#methodsを指定することで、このURLに対するHTTPメソッドを制限
#指定しない場合はGETメソッドのみ許可
@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    #POSTメソッドでリクエストがあった場合の処理
    if request.method == 'POST':
        if request.form['username'] != app.config['USERNAME']:
            flash('ユーザ名が異なります')
        elif request.form['password'] != app.config['PASSWORD']:
            flash('パスワードが異なります')
        #正しい場合は、/にリダイレクトさせる
        else:
            session['logged_in'] = True
            flash('ログインしました')
            return redirect(url_for('entry.show_entries'))
    #GETメソッドでリクエストがあった場合、ログインフォームが表示
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    flash('ログアウトしました')
    return redirect(url_for('entry.show_entries'))

@app.errorhandler(404)
def non_existant_route(error):
   return redirect(url_for('login'))
