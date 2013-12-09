# coding:utf-8
from functools import wraps
from flask import abort,Blueprint,render_template,redirect,request,url_for,flash,current_app
from config import login_manager,MaxinObject
from flask.ext.login import current_user,login_user,login_required,logout_user
from lolipop.models import User,Profile
from lolipop.form import RegisterForm,LoginForm,ProfileForm

bp = Blueprint('account',__name__)

def permission_limit(func):
    @wraps(func)
    def decorated_view(*args,**kwargs):
        abort(404)
    return decorated_view

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
        Profile.get_or_create(user.id)
        login_user(user)
        flash(("Thanks for your registering"),"success")
        return redirect(url_for('index.index'))
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
            return redirect(request.args.get("next") or url_for('index.index'))
    return render_template("account/signin.html",form=form)

@bp.route('/logout')
@login_required
def logout():
    try:
        current_app.config['ONLINEUSERS'].remove(current_user.id)
    except KeyError:
        pass
    logout_user()
    flash(("Logged out"),"success")
    return redirect(url_for('index.index'))

@bp.route('/profile/uid=<int:uid>',methods=['GET','POST'])
@login_required
def profile(uid):
    user = current_user
    profile = Profile.get_or_create(uid)
    
    # There are some trick codes,it is ugly
    # but,it is run well
    obj = MaxinObject()
    obj_dict = {}

    profile_dict = profile.__dict__
    user_dict = user.__dict__
    obj_dict.update(profile_dict)
    obj_dict.update(user_dict)
    for key in obj_dict:
        obj.__setattr__(key,obj_dict[key])
    form = ProfileForm(obj=obj)
    #next_url = request.args.get('next',url_for('.setting')) 
    if form.validate_on_submit():
        form.populate_obj(profile)
        profile.save()
        return redirect(url_for('.profile',uid=uid))
    return render_template('account/profile.html',form=form,profile=profile)
