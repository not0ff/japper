from flask import Response, jsonify, render_template, request
from flask.typing import ResponseReturnValue
from flask_login import current_user, login_required

from app import db
from app.utils import get_post

from . import api


@api.route('/fetch_post', methods=['POST'])
@login_required
def fetch_post() -> ResponseReturnValue:
    status, resp = get_post(request.json)
    if status != 200:
        return Response(
            response=jsonify(resp).get_data(
                as_text=True),
            status=status,
            mimetype='application/json'
        )
        
    return render_template('components/post.html', post=resp)

@api.route('/add_like', methods=['POST'])
@login_required
def like_post() -> Response:
    status, resp = get_post(request.json)
    if status != 200:
        return Response(
            response=jsonify(resp).get_data(
                as_text=True),
            status=status,
            mimetype='application/json'
        )

    current_user.add_like(resp)
    db.session.commit()

    return Response(
        response=jsonify(
            {'status': 'success', 'message': 'Like added successfully'}).get_data(as_text=True),
        status=200,
        mimetype='application/json'
    )

@api.route('/remove_like', methods=['POST'])
@login_required
def remove_post() -> Response:
    status, resp = get_post(request.json)
    if status != 200:
        return Response(
            response=jsonify(resp).get_data(
                as_text=True),
            status=status,
            mimetype='application/json'
        )

    current_user.remove_like(resp)
    db.session.commit()

    return Response(
        response=jsonify(
            {'status': 'success', 'message': 'Like removed successfully'}).get_data(as_text=True),
        status=200,
        mimetype='application/json'
    )