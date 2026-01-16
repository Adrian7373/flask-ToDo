from ToDo import app
from flask import render_template, flash, redirect, url_for, request
from ToDo import forms
from ToDo.models import *
from flask_login import login_user, login_required, logout_user, current_user
from datetime import datetime

@app.route("/", methods=['POST','GET'])
@app.route("/dashboard", methods=['POST','GET'])
@login_required
def home_page():
    folder_list = current_user.owned_folders
    counts = [f.tasks.filter_by(is_completed=False).count() for f in folder_list]
    zipped_data = zip(folder_list, counts)
    if request.method == "POST":
        new_folder = request.form.get('new_list')
        if new_folder:
            folder = Folder(name=new_folder,
                            owner=current_user.id)
            db.session.add(folder)
            db.session.commit()
            return redirect(url_for('home_page'))
    return render_template('homepage.html', data=zipped_data)

@app.route("/delete/<int:folder_id>", methods=['POST', 'GET'])
def delete_folder(folder_id):
    folder = Folder.query.get(folder_id)
    db.session.delete(folder)
    db.session.commit()
    return redirect(url_for('home_page'))

@app.route("/register", methods=['POST', 'GET'])
def register_page():
    register_form = forms.RegisterForm()
    if register_form.validate_on_submit():
        user_to_create = User(username=register_form.username.data,
                              email=register_form.username.data,
                              password=register_form.password.data)
        db.session.add(user_to_create)
        db.session.commit()
        login_user(user_to_create)
        flash(f"Account successfully created!. You are logged in as {user_to_create.username}")
        return redirect(url_for('home_page'))
    if register_form.errors != {}:
        for err_msg in register_form.errors.values():
            flash(err_msg)
    return render_template('register.html', register_form=register_form)

@app.route("/login", methods=['POST', 'GET'])
def login_page():
    login_form = forms.LoginForm()
    if login_form.validate_on_submit():
        user_to_login = User.query.filter_by(username=login_form.username.data).first()
        if user_to_login and user_to_login.check_password_correction(login_form.password.data):
            login_user(user_to_login)
            flash(f"Success! You are logged in as {user_to_login.username}")
            return redirect(url_for('home_page'))

    return render_template('login.html', login_form=login_form)

@app.route("/logout")
@login_required
def logout_page():
    logout_user()
    return redirect(url_for('login_page'))

@app.route("/folder/<int:folder_id>", methods=['POST','GET'])
def view_folder_task(folder_id):
    folder = Folder.query.get(folder_id)
    tasks = folder.tasks.filter(Task.is_completed == False).all()
    completed_tasks = folder.tasks.filter(Task.is_completed == True).all()

    if request.method == "POST":
        new_task = request.form.get('new_task')
        date = request.form.get('date')
        task = Task(name=new_task,
                    dueDate=date,
                    folder_id=folder_id)
        db.session.add(task)
        db.session.commit()
        return redirect(url_for('view_folder_task', folder_id=folder_id))

    return render_template("tasks_view.html", tasks=tasks, folder=folder, completed_tasks=completed_tasks)

@app.route("/delete/<int:folder_id>/<int:task_id>", methods=['POST','GET'])
def delete_task(folder_id, task_id):
    task = Task.query.get(task_id)
    db.session.delete(task)
    db.session.commit()
    return redirect(url_for('view_folder_task', folder_id=folder_id))

@app.route("/complete/<int:folder_id>/<int:task_id>", methods=['POST','GET'])
def complete_task(folder_id, task_id):
    task = Task.query.get(task_id)
    task.is_completed = True
    task.datetime_completed = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    db.session.commit()
    return redirect(url_for('view_folder_task', folder_id=folder_id))

@app.route("/folder/<int:folder_id>/<int:task_id>", methods=['POST','GET'])
def view_task_details(folder_id, task_id):
    folder = Folder.query.get(folder_id)
    task = Task.query.get(task_id)
    subtasks = task.subtasks.filter(Subtask.is_completed == False).all()
    completed_subtasks = task.subtasks.filter(Subtask.is_completed == True).all()

    if request.method == "POST":
        new_subtask = request.form.get('new_subtask')
        if new_subtask:
            subtask = Subtask(name=new_subtask,
                              task_id=task_id)
            db.session.add(subtask)
            db.session.commit()
            return redirect(url_for('view_task_details', folder_id=folder_id, task_id=task_id))

    return render_template('task_detail.html', subtasks=subtasks, folder=folder,
                           task=task, completed_subtasks=completed_subtasks)

@app.route("/delete/<int:folder_id>/<int:task_id>/<int:subtask_id>", methods=['POST','GET'])
def delete_subtask(folder_id,task_id,subtask_id):
    subtask = Subtask.query.get(subtask_id)
    db.session.delete(subtask)
    db.session.commit()
    return redirect(url_for('view_task_details', folder_id=folder_id, task_id=task_id))

@app.route("/complete/<int:folder_id>/<int:task_id>/<int:subtask_id>")
def complete_subtask(folder_id,task_id,subtask_id):
    subtask = Subtask.query.get(subtask_id)
    subtask.is_completed = True
    subtask.datetime_completed = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    db.session.commit()
    return redirect(url_for('view_task_details', folder_id=folder_id, task_id=task_id, subtask_id=subtask_id))

@app.route("/restore/<int:folder_id>/<int:task_id>/<int:completed_subtask_id>")
def restore_complete_subtask(folder_id, task_id, completed_subtask_id):
    subtask = Subtask.query.get(completed_subtask_id)
    subtask.is_completed = False
    db.session.commit()
    return redirect(url_for('view_task_details', folder_id=folder_id, task_id=task_id, subtask_id=subtask.id))

@app.route("/restore/<int:folder_id>/<int:completed_task_id>")
def restore_complete_task(folder_id, completed_task_id):
    task = Task.query.get(completed_task_id)
    task.is_completed = False
    db.session.commit()
    return redirect(url_for('view_folder_task', folder_id=folder_id))

@app.route("/delete/<int:folder_id>/<int:task_id>/<int:completed_subtask_id>", methods=['POST','GET'])
def perm_delete_subtask(folder_id,task_id,completed_subtask_id):
    subtask = Subtask.query.get(completed_subtask_id)
    db.session.delete(subtask)
    db.session.commit()
    return redirect(url_for('view_task_details', folder_id=folder_id, task_id=task_id))

@app.route("/delete/<int:folder_id>/<int:completed_task_id>", methods=['POST','GET'])
def perm_delete_task(folder_id, completed_task_id):
    task = Task.query.get(completed_task_id)
    db.session.delete(task)
    db.session.commit()
    return redirect(url_for('view_folder_task', folder_id=folder_id))