from flask import Blueprint, render_template, redirect, url_for, request, flash, jsonify
from flask_login import login_required, current_user
from ..models import Post
from ..forms import CreatePostForm, LikeForm
from ..extensions import db
from sqlalchemy import func

home_bp = Blueprint('home', __name__)

@home_bp.route('/posts')
@login_required
def posts():
    form = LikeForm()
    posts = Post.query.order_by(func.random()).limit(10).all()
    return render_template('home/posts.html', posts=posts, form=form)

@home_bp.route('/create-post', methods=['GET', 'POST'])
@login_required
def create_post():
    form = CreatePostForm()

    if form.validate_on_submit():
        post = Post(
            title=form.title.data,
            content=form.content.data
        )
        current_user.created_posts.append(post)
        db.session.commit()
        flash('post created successfully', category='success')
        return redirect(url_for('home.posts'))
    elif request.method == 'POST':
        for field, errors in form.errors.items():
            for error in errors:
                flash(f'Error in field {field}: {error}', category='error')
    
    return render_template('home/create-post.html', form=form)

@home_bp.route('/like-post', methods=['POST'])
@login_required
def like_post():
    data = request.json
    post = Post.query.filter_by(id=data['post_id']).first()
    response = {}
    if post:
        if not current_user in post.liked_users:
            post.liked_users.append(current_user)
            response['result'] = 'liked'
        else:
            post.liked_users.remove(current_user)
            response['result'] = 'unliked'
        response['likes'] = len(post.liked_users)

        db.session.commit()
    
    return jsonify(response)
