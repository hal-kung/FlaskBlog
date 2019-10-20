from flask import request, redirect, url_for, render_template, flash, session
from flask_blog import app
from flask_blog import db
from flask_blog.models.entries import Entry
from flask_blog.views.views import login_required
from flask import Blueprint

entry = Blueprint('entry', __name__)

@entry.route('/')
@login_required
def show_entries():
# トップページにアクセスしたときに全てのブログ記事をデータベースから取得
    entries = Entry.query.order_by(Entry.id.desc()).all()
    return render_template('entries/index.html', entries=entries)

# 投稿内容を受信してデータベースに保存する処理
@entry.route('/entries', methods=['POST'])
@login_required
def add_entry():
    # 送られてきた記事タイトルと内容についてのモデルインスタンス作成
    entry = Entry(
            title=request.form['title'],
            text=request.form['text']
            )
    # 新しい内容を追加
    db.session.add(entry)
    # データベースにデータを書き込み
    db.session.commit()
    flash('新しく記事が作成されました')
    return redirect(url_for('entry.show_entries'))

#「新規投稿」のリンク、/new_entryにアクセスしたときにブログ投稿フォームを返す
@entry.route('/entries/new', methods=['GET'])
@login_required
def new_entry():
    return render_template('entries/new.html')

# idに整数以外の値が渡された時にエラー
@entry.route('/entries/<int:id>', methods=['GET'])
@login_required
def show_entry(id):
    # 渡されたidの記事をデータベースから取得
    entry = Entry.query.get(id)
    return render_template('entries/show.html', entry=entry)

@entry.route('/entries/<int:id>/edit', methods=['GET'])
@login_required
def edit_entry(id):
    entry = Entry.query.get(id)
    return render_template('entries/edit.html', entry=entry)

# フォームに入力された編集内容を受け取りデータベースを更新
@entry.route('/entries/<int:id>/update', methods=['POST'])
@login_required
def update_entry(id):
    entry = Entry.query.get(id)
    entry.title = request.form['title']
    entry.text = request.form['text']
    # 更新処理
    db.session.merge(entry)
    db.session.commit()
    flash('記事が更新されました')
    return redirect(url_for('entry.show_entries'))

@entry.route('/entries/<int:id>/delete', methods=['POST'])
@login_required
def delete_entry(id):
    entry = Entry.query.get(id)
    db.session.delete(entry)
    db.session.commit()
    flash('投稿が削除されました')
    return redirect(url_for('entry.show_entries'))
