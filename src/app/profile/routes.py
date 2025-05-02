from os import path, remove

import sqlalchemy as sa
from flask import (
    flash,
    jsonify,
    render_template,
    request,
    send_file,
    send_from_directory,
    url_for,
)
from flask.typing import ResponseReturnValue
from flask_login import current_user, login_required
from werkzeug.utils import secure_filename

from app.extensions import db, profile_imgs
from app.forms import EditProfileForm, FollowProfileForm
from app.models import Post, User
from app.utils import (
    add_notification,
    flash_form_errors,
    get_profile,
    optimize_img,
    redirect_to_referrer,
)

from . import profile


@profile.route("/<username>")
@login_required
def profile_page(username: str) -> ResponseReturnValue:
    profile_form: EditProfileForm = EditProfileForm()
    follow_profile_form: FollowProfileForm = FollowProfileForm()
    user = User.query.filter_by(username=username).first_or_404()
    posts = Post.query.filter_by(user_id=user.id).order_by(sa.desc(Post.timestamp))

    profile_form.bio.data = user.bio
    return render_template(
        "profile/profile.html",
        user=user,
        posts=posts,
        profile_form=profile_form,
        follow_profile_form=follow_profile_form,
    )


@profile.route("/pfp/<user_id>")
@login_required
def serve_pfp(user_id: int) -> ResponseReturnValue:
    User.query.get_or_404(user_id)
    img_name = secure_filename(f"{user_id}_pfp.webp")
    img_path = profile_imgs.path(img_name)

    if path.exists(img_path):
        return send_file(img_path)
    return send_from_directory("static", "images/default_pfp.webp")


@profile.route("/edit", methods=["POST"])
@login_required
def edit_profile() -> ResponseReturnValue:
    form: EditProfileForm = EditProfileForm()
    if form.validate_on_submit():
        if form.bio.data != current_user.bio and form.bio.data:
            current_user.bio = form.bio.data
            db.session.add(current_user)
            db.session.commit()
            flash("Profile bio changed", category="success")

        if form.image.data:
            img = optimize_img(form.image.data, resize=True)
            name = secure_filename(f"{current_user.id}_pfp.webp")

            if path.exists(img_path := profile_imgs.path(name)):
                remove(img_path)

            profile_imgs.save(img, name=name)
            flash("Profile picture updated!", category="success")
    elif form.errors:
        flash_form_errors(form)

    return redirect_to_referrer()


@profile.route("/follow", methods=["POST"])
@login_required
def follow_profile() -> ResponseReturnValue:
    form: FollowProfileForm = FollowProfileForm()
    if form.validate_on_submit():
        user: User = User.query.filter_by(id=form.profile_id.data).first_or_404()

        current_user.follow(user)
        add_notification(user=user, content=f"{current_user.username} followed you!")
        db.session.commit()

    elif form.errors:
        flash_form_errors(form)

    return redirect_to_referrer(
        fallback=url_for("profile.profile_page", username=current_user.username)
    )


@profile.route("/unfollow", methods=["POST"])
@login_required
def unfollow_profile() -> ResponseReturnValue:
    form: FollowProfileForm = FollowProfileForm()
    if form.validate_on_submit():
        user: User = User.query.filter_by(id=form.profile_id.data).first_or_404()
        current_user.unfollow(user)
        db.session.commit()

    elif form.errors:
        flash_form_errors(form)

    return redirect_to_referrer(
        fallback=url_for("profile.profile_page", username=current_user.username)
    )


@profile.route("/get_followers")
@login_required
def get_followers() -> ResponseReturnValue:
    resp, status = get_profile(request.args.to_dict())
    if status != 200:
        return jsonify(resp), status

    followers = None
    if isinstance(resp, User):
        followers = resp.followers

    return jsonify(
        {
            "status": "ok",
            "result": {
                "userList": render_template(
                    "components/user_list.html", users=followers
                )
            },
        }
    ), 200


@profile.route("/get_following")
@login_required
def get_following() -> ResponseReturnValue:
    resp, status = get_profile(request.args.to_dict())
    if status != 200:
        return jsonify(resp), status

    followers = None
    if isinstance(resp, User):
        followers = resp.following

    return jsonify(
        {
            "status": "ok",
            "result": {
                "userList": render_template(
                    "components/user_list.html", users=followers
                )
            },
        }
    ), 200
