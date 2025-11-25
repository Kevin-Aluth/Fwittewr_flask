from flask import Blueprint, render_template, redirect, url_for, request, flash, jsonify
from flask_login import login_required, current_user
from ..models import Post, Comment, User
from ..forms import CreatePostForm
from ..extensions import db
from sqlalchemy import func

home_bp = Blueprint('home', __name__)

@home_bp.route('/posts')
@login_required
def posts():
    posts = Post.query.filter_by(deleted=False).order_by(func.random()).limit(10).all()
    return render_template('home/posts.html', posts=posts)

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
    post = Post.query.filter_by(id=data['post_id']).first_or_404()
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

@home_bp.route('/like-comment', methods=['POST'])
@login_required
def like_comment():
    data = request.json
    comment = Comment.query.filter_by(id=data['comment_id']).first_or_404()
    response = {}
    if comment:
        if not current_user in comment.liked_users:
            comment.liked_users.append(current_user)
            response['result'] = 'liked'
        else:
            comment.liked_users.remove(current_user)
            response['result'] = 'unliked'
        response['likes'] = len(comment.liked_users)

        db.session.commit()
    
    return jsonify(response)

@home_bp.route('/post-comments/<id>', methods=['GET', 'POST'])
@login_required
def show_post_comments(id):
    form = CreatePostForm()
    post = Post.query.filter_by(id=id).first_or_404()

    if form.validate_on_submit():
        comment = Comment(content=form.content.data)
        current_user.created_comments.append(comment)
        comment.referenced_post = post
        db.session.commit()
        return redirect(url_for('home.show_post_comments', id=id))
    
    return render_template('home/comments/post-comments.html', post=post, form=form)

@home_bp.route('/comment-comments/<id>', methods=['GET', 'POST'])
@login_required
def show_comment_comments(id):
    form = CreatePostForm()
    comment = Comment.query.filter_by(id=id).first_or_404()

    if form.validate_on_submit():
        new_comment = Comment(content=form.content.data)
        current_user.created_comments.append(new_comment)
        new_comment.referenced_comment = comment
        db.session.commit()
        return redirect(url_for('home.show_comment_comments', id=id))
    
    return render_template('home/comments/comment-comments.html', post=comment, form=form)

@home_bp.route('/delete-post', methods=['POST'])
@login_required
def delete_post():
    data = request.json
    id = data['post_id']
    post = Post.query.filter_by(id=id, user_id=current_user.id).first_or_404()
    post.content = '[this post was deleted]'
    post.title = '[Deleted Post]'
    post.deleted = True
    db.session.commit()
    return jsonify({
        'result': 'deleted', 
        'title': post.title, 
        'content': post.content
    })

@home_bp.route('/delete-comment', methods=['POST'])
@login_required
def delete_comment():
    data = request.json
    id = data['comment_id']
    comment = Comment.query.filter_by(id=id, user_id=current_user.id).first_or_404()
    comment.content = '[this comment was deleted]'
    comment.deleted = True
    db.session.commit()
    return jsonify({
        'result': 'deleted',
        'content': comment.content
    })

@home_bp.route('/show-user/<id>')
@login_required
def show_user(id):
    user = User.query.filter_by(id=id).first_or_404()
    return render_template('home/user.html', user=user)
