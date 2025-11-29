from flask import Blueprint, request, jsonify
from flask_login import login_required, current_user
from ..models import User
from ..extensions import db

followers_bp = Blueprint('followers', __name__)

@followers_bp.route('/follow', methods=['POST'])
@login_required
def follow_user():
    data = request.json
    id = data['user_id']
    user_to_follow = User.query.filter_by(id=id).first_or_404()
    if user_to_follow == current_user:
        return jsonify({
            'error': 'Bad request',
            'message': 'you cannot follow yourself'
        }), 400
    if current_user in user_to_follow.followers:
        user_to_follow.followers.remove(current_user)
        db.session.commit()
        return jsonify({
            'result': 'unfollowed',
            'user_followers': len(user_to_follow.followers),
        })
    else:
        user_to_follow.followers.append(current_user)
        db.session.commit()
        return jsonify({
            'result': 'followed',
            'user_followers': len(user_to_follow.followers),
        })
