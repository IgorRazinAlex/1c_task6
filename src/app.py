import os
import datetime

from flask import Flask, render_template, redirect
from flask_login import LoginManager, login_user, login_required, logout_user, \
    current_user

from data import db_session
from data.models.user import User
from data.models.post import Post
from data.models.subscription import Subscription
from data.models.dinner import Dinner

from forms.login import LoginForm
from forms.register import RegisterForm
from forms.add_meal import MealAddForm
from forms.change_meal import ChangeMealForm
from forms.search import MangaSearchForm
from forms.add_dinner import DinnerAddForm
from forms.check_cpfc import CheckCPFC

import matplotlib.pyplot as plt
import numpy as np

class App:
    def __init__(self, namespace):
        self.app = Flask(namespace)
        self.config()
        self.build_db_session()
        self.build_login_manager()
        self.build_app()

    def config(self):
        self.app.config["SECRET_KEY"] = "AM_AM_AM"

    def build_app(self):
        @self.app.route("/")
        @self.app.route("/meals")
        def meals():
            db_sess = db_session.create_session()
            posts = db_sess.query(Post).all()

            recent_posts = sorted(posts,
                                  key=lambda post: post.update_date)[::-1][:10]

            db_sess.close()
            return render_template("meals.html", title="Fan-Manga",
                                   recent_posts=recent_posts)

        @self.app.route("/meals/search", methods=["GET", "POST"])
        def search():
            form = MangaSearchForm()

            if not form.validate_on_submit():
                return render_template("search.html", found=True, form=form)
            
            db_sess = db_session.create_session()
            posts = db_sess.query(Post).filter(Post.name == form.name.data).all()
            db_sess.close()
            if len(posts) == 0:
                return render_template("search.html", found=False, form=form)

            return render_template("filtered_meals.html", title="Results",
                                   filter_type="Found named", posts=posts)

        @self.app.route("/meals/recent")
        def recent_meals():
            db_sess = db_session.create_session()
            posts = db_sess.query(Post).all()
            recent_posts = sorted(posts,
                                  key=lambda post: post.update_date)[::-1]

            db_sess.close()
            return render_template("filtered_meals.html", title="Recent meals",
                                   filter_type="Recent", posts=recent_posts)

        @self.app.route("/meals/<int:meal_id>", methods=["GET"])
        def meal_page(meal_id):
            db_sess = db_session.create_session()
            meal = db_sess.query(Post).filter(Post.id == meal_id).first()

            author = db_sess.query(User).filter(User.id == meal.author).first()

            db_sess.close()
            return render_template("meal_page.html", title=meal.name,
                                   meal=meal,
                                   author=author,
                                   current_user=current_user)

        @self.app.route("/meals/add_meal", methods=["GET", "POST"])
        def add_meal():
            if not current_user.is_authenticated:
                return redirect("/account/login")
            
            form = MealAddForm()

            if not form.validate_on_submit():
                return render_template("add_meal.html", title="Add meal", form=form)

            db_sess = db_session.create_session()

            post = Post(
                name=form.name.data,
                author=current_user.id,
                calories=form.calories.data,
                proteins=form.proteins.data,
                fats=form.fats.data,
                carbonades=form.carbonades.data,
                about=form.about.data
            )

            db_sess.add(post)
            db_sess.commit()

            os.makedirs(os.path.join("static", "image", "meals"))

            preview = form.preview.data
            preview.save(os.path.join("static", "image", "meals", f"{post.id}.jpg"))

            db_sess.close()

            return redirect(f"/meals/{post.id}")

        @self.app.route("/meals/<int:meal_id>/change_meal",
                        methods=["GET", "POST"])
        def change_meal(meal_id):
            if not (current_user.is_authenticated):
                return redirect(f"/meals/{meal_id}")
            
            db_sess = db_session.create_session()
            meal = db_sess.query(Post).filter(Post.id == meal_id).first()

            if not (current_user.id == meal.author):
                db_sess.close()
                return redirect(f"/meals/{meal_id}")

            form = ChangeMealForm()

            if not form.validate_on_submit():
                db_sess.close()
                return render_template("change_meal.html",
                                    title="Change meal",
                                    form=form,
                                    meal=meal)

            if not (form.name.data or form.calories.data or form.proteins.data or form.fats.data or form.carbonades.data \
                    or form.about.data or form.preview.data):
                db_sess.close()
                return render_template("change_meal.html",
                                        title="Change meal",
                                        form=form,
                                        meal=meal,
                                        message="At least something needs to be changed")

            meal.name = form.name.data if form.name.data else meal.name
            meal.calories = form.calories.data if form.calories.data else meal.calories
            meal.proteins = form.proteins.data if form.proteins.data else meal.proteins
            meal.fats = form.fats.data if form.fats.data else meal.fats
            meal.carbonades = form.carbonades.data if form.carbonades.data else meal.carbonades
            meal.about = form.about.data if form.about.data else meal.about
            meal.update_date = datetime.datetime.now()

            preview = form.preview.data
            if preview is not None:
                if not os.path.exists(os.path.join("static", "image", "meals")):
                    os.makedirs(os.path.join("static", "image", "meals"))

                preview.save(os.path.join("static", "image", "meals", f"{meal.id}.jpg"))

            db_sess.add(meal)
            db_sess.commit()
            db_sess.close()
            return redirect("/")

        @self.app.route("/meals/<int:meal_id>/sub")
        def subscribe(meal_id):
            if not current_user.is_authenticated:
                return redirect(f"/meals/{meal_id}")
            
            db_sess = db_session.create_session()
            
            sub = Subscription(
                user_id = current_user.id,
                meal_id = meal_id
            )

            db_sess.add(sub)
            db_sess.commit()
            db_sess.close()

            return redirect(f"/meals/{meal_id}")

        @self.app.route("/account")
        def access_account():
            if current_user.is_authenticated:
                return redirect("/account/page")

            return redirect("account/login")

        @self.app.route("/account/login", methods=["GET", "POST"])
        def login():
            form = LoginForm()

            if form.validate_on_submit():
                db_sess = db_session.create_session()
                user = db_sess.query(User).filter(
                    User.email == form.email.data).first()
                if user and user.check_password(form.password.data):
                    login_user(user, remember=form.remember_me.data)
                    db_sess.close()
                    return redirect("/account/page")
                db_sess.close()
                return render_template("login.html",
                                       title="Authorisation",
                                       message="Invalid login or password",
                                       form=form)

            return render_template("login.html", title="Authorisation",
                                   form=form)

        @self.app.route("/account/register", methods=["POST", "GET"])
        def register():
            form = RegisterForm()

            if form.validate_on_submit():
                if form.password.data != form.password_check.data:
                    return render_template("register.html",
                                           title="Registration",
                                           form=form,
                                           message="Passwords don`t match")
                db_sess = db_session.create_session()

                if db_sess.query(User).filter(
                        User.username == form.username.data).first():
                    db_sess.close()
                    return render_template("register.html",
                                           title="Registration",
                                           form=form,
                                           message="This username is " +
                                                   "already taken")

                if db_sess.query(User).filter(
                        User.email == form.email.data).first():
                    db_sess.close()
                    return render_template("register.html",
                                           title="Registration",
                                           form=form,
                                           message="User with this email " +
                                                   "already exists")

                user = User(
                    email=form.email.data,
                    username=form.username.data,
                    age=form.age.data
                )
                user.set_password(form.password.data)
                db_sess.add(user)
                db_sess.commit()
                db_sess.close()
                return redirect("/account/login")

            return render_template("register.html",
                                   title="Registration",
                                   form=form)

        @self.app.route("/account/logout")
        @login_required
        def logout():
            logout_user()
            return redirect("/")

        @self.app.route("/account/page")
        def account_page():
            if not current_user.is_authenticated:
                return redirect("/")
            
            db_sess = db_session.create_session()
            
            subscriptions = db_sess.query(Subscription).filter(Subscription.user_id == current_user.id).all()
            post_subs = []
            for sub in subscriptions:
                post = db_sess.query(Post).filter(Post.id == sub.meal_id).first()
                post_subs.append(post)

            db_sess.close()
            return render_template("account.html",
                                   title="Account",
                                   user=current_user,
                                   subscriptions=post_subs)
        
        @self.app.route("/account/add_dinner", methods=["POST", "GET"])
        def add_dinner():
            if not current_user.is_authenticated:
                return redirect("/login")
            
            form = DinnerAddForm()

            if not form.validate_on_submit():
                return render_template("add_dinner.html", title="Add dinner", form=form)

            db_sess = db_session.create_session()
            
            meal = db_sess.query(Post).filter(Post.name == form.name.data).first()

            if meal is None:
                db_sess.close()
                return render_template("add_dinner.html",
                                        title="Add dinner",
                                        form=form,
                                        message="No meal found with such name!")

            dinner = Dinner(
                user_id=current_user.id,
                meal_id=meal.id,
                date=datetime.date.today()
            )

            db_sess.add(dinner)
            db_sess.commit()

            db_sess.close()

            return redirect(f"/account")
        
        @self.app.route("/account/check_cpfc", methods=["POST", "GET"])
        def check_cpfc():
            if not current_user.is_authenticated:
                return redirect("/login")
            
            form = CheckCPFC()

            if not form.validate_on_submit():
                return render_template("check_cpfc.html", title="Check CPFC", form=form)
            
            from_date = form.from_date.data
            to_date = form.to_date.data

            db_sess = db_session.create_session()

            dinners = db_sess.query(Dinner).filter(Dinner.user_id == current_user.id)
            dinners = dinners.filter(Dinner.date >= from_date)
            dinners = dinners.filter(Dinner.date <= to_date).all()

            cal_stat = {}
            p_stat = {}
            f_stat = {}
            car_stat = {}
            for dinner in dinners:
                meal = db_sess.query(Post).filter(Post.id == dinner.meal_id).first()
                if str(dinner.date) not in cal_stat.keys():
                    cal_stat[str(dinner.date)] = 0
                cal_stat[str(dinner.date)] += meal.calories
                if str(dinner.date) not in p_stat.keys():
                    p_stat[str(dinner.date)] = 0
                p_stat[str(dinner.date)] += meal.proteins
                if str(dinner.date) not in f_stat.keys():
                    f_stat[str(dinner.date)] = 0
                f_stat[str(dinner.date)] += meal.fats
                if str(dinner.date) not in car_stat.keys():
                    car_stat[str(dinner.date)] = 0
                car_stat[str(dinner.date)] += meal.carbonades
            
            fig, ax = plt.subplots()
            grid = cal_stat.keys()

            ax.bar(grid, cal_stat.values(), label="Calories")
            ax.set_xlabel("Date")
            ax.set_ylabel("Amount")
            ax.set_title("Calories")

            if not os.path.exists(os.path.join("static", "image", "graphics", f"{current_user.id}")):
                os.makedirs(os.path.join("static", "image", "graphics", f"{current_user.id}"))
            
            fig.savefig(os.path.join("static", "image", "graphics", f"{current_user.id}", f'{from_date}-{to_date}.png'))
            return render_template("check_cpfc.html", title="Check CPFC", form=form, 
                                   impath=os.path.join("static", "image", "graphics", f"{current_user.id}", f'{from_date}-{to_date}.png'))


        @self.app.route("/about")
        def about():
            return render_template("about.html", title="About")

    @staticmethod
    def build_db_session():
        db_session.global_init()

    def build_login_manager(self):
        login_manager = LoginManager()
        login_manager.init_app(self.app)

        @login_manager.user_loader
        def load_user(user_id):
            db_sess = db_session.create_session()
            return db_sess.query(User).get(user_id)

    def get_app(self):
        return self.app
