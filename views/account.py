# coding:utf-8
from functools import wraps
from flask import abort,Blueprint,render_template,redirect,request,url_for,flash
from config import login_manager
from flask.ext.login import current_user,login_user,login_required,logout_user
from kutoto.models import User,Profile
from kutoto.form import RegisterForm,LoginForm,ProfileForm

bp = Blueprint('account',__name__)

def admin_required(func):
    @wraps(func)
    def decorated_view(*args,**kwargs):
        try:
            if not current_user.id == 1:
                abort(403)
            return func(*args,**kwargs)
        except AttributeError:
            abort(403)
    return decorated_view

@login_manager.user_loader
def load_user(userid):
    return User.query.get_or_404(userid)

@bp.route('/signup',methods=["GET","POST"])
def signup():
    if current_user is not None and current_user.is_authenticated():
        return redirect(url_for('.profile',uid = current_user.id))
    form = RegisterForm()
    if form.validate_on_submit():
        user = form.save()
        login_user(user)
        flash(("Thanks for your registering"),"success")
        return redirect(url_for('index'))
    return render_template('account/signup.html',form=form)

@bp.route('/signin',methods=["GET","POST"])
def signin():
    if current_user is not None and current_user.is_authenticated():
        return redirect(url_for('.profile',uid=current_user.id))
    form = LoginForm()
    if form.validate_on_submit():
        user,authenticated=User.authenticate(form.account.data,form.password.data)
        if user and authenticated:
            login_user(user,remember = form.remember_me.data)
            return redirect(request.args.get("next") or url_for('index'))
    return render_template("account/signin.html",form=form)

@bp.route('/logout')
@login_required
def logout():
    logout_user()
    flash(("Logged out"),"success")
    return redirect(url_for('index'))

@bp.route('/profile/uid=<int:uid>',methods=['GET','POST'])
@login_required
def profile(uid):
    user = current_user
    profile = Profile.get_or_create(uid)

    form = ProfileForm(obj=profile)
    #next_url = request.args.get('next',url_for('.setting')) 
    if form.validate_on_submit():
        user = User.query.get_or_404(current_user.id)
        form.populate_obj(user)
        form.populate_obj(profile)
        profile.save()
        user.save()
        return redirect(url_for('index'))
    return render_template('account/profile.html',form=form,profile=profile)
