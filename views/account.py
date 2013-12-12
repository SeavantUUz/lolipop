# coding:utf-8
from functools import wraps
from flask import abort,Blueprint,render_template,redirect,request,url_for,flash,current_app
from _helpers import login_manager,MaxinObject,cache
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
    #next_url = request.args.get('next',url_for('.profile'))
    #token = request.args.get('token')
    #if token:
    #    user = verify_auth_token(token,1)
    #    if not user:
    #        flash(u'无效用户','error')
    #        return redirect(next_url)
    #    user.save()
    #    login_user(user)
    #    return redirect(next_url)

    form = RegisterForm()
    if form.validate_on_submit():
        user = form.save()
        #profile = Profile(user.id)
        #wait_verify = redis.set(user.username,True)
        #if not wait_verify:
        #    user.save()
        #    Profile.get_or_create(user.id)
        #    login_user(user)
        #    return redirect(next_url)
        Profile.get_or_create(user.id)
        login_user(user)
        cache.clear()
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
            cache.clear()
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
