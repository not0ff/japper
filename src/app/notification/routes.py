from flask import jsonify, render_template, request
from flask.typing import ResponseReturnValue
from flask_login import current_user, login_required

from app.extensions import db
from app.models import Notification

from . import notification


@notification.route('/get')
@login_required
def get_notifications() -> ResponseReturnValue:
    since = request.args.get('since', 0.0, type=float)
    unread_only = request.args.get('unread_only', False, type=lambda x: x.lower() == 'true')
    autoread = request.args.get('autoread', False, type=lambda x: x.lower() == 'true')

    notifications = Notification.query.filter(
        Notification.user_id == current_user.id,
        Notification.timestamp > since)
    
    if unread_only:
        notifications = notifications.filter(Notification.read == False)
    
    notifications = notifications.all()
    if autoread:
        for notif in notifications:
            notif.display_unread = True if not notif.read else False
            notif.mark_read()
        db.session.commit()
    
    return jsonify([render_template('components/notification.html', notification=notif) for notif in notifications])


@notification.route('/unread_count')
@login_required
def count_unread_notifications() -> ResponseReturnValue:
    since = request.args.get('since', 0.0, type=float)
    
    notif_count = Notification.query.filter(
        Notification.user_id == current_user.id,
        Notification.read == False,
        Notification.timestamp > since).count()
    
    return jsonify({'count': notif_count}), 200