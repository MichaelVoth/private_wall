from flask import render_template, redirect, request, session, flash
from flask_app import app
from flask_app.models.users import User
from flask_app.models.messages import Message
from datetime import datetime


def time_since_posted(created_at):
    now = datetime.datetime.now()
    posted_time = datetime.datetime.strptime(created_at, '%Y-%m-%d %H:%M:%S.%f')
    time_since = now - posted_time
    days = time_since.days
    hours, remainder = divmod(time_since.seconds, 3600)
    minutes, seconds = divmod(remainder, 60)
    if days > 0:
        return f'{days} days, {hours} hours ago'
    elif hours > 0:
        return f'{hours} hours, {minutes} minutes ago'
    else:
        return f'{minutes} minutes, {seconds} seconds ago'


@app.route('/wall')
def show_wall():
    #Checks if user id is logged in.
    if session.get('user_id') is None:
        return redirect('/')
    #Gets user info by id in session.
    messages = Message.get_messages_by_recipient({'id': session['user_id']})
    users = User.get_all_users()
    count = Message.get_messages_sent({'id': session['user_id']})
    recieved_count = Message.get_message_recieved_count({'id': session['user_id']})

    return render_template('wall.html', users=users, messages=messages, count=count, recieved_count=recieved_count)



@app.route('/send', methods=['POST'])
def send_message():
        #Checks if user id is logged in.
    if session.get('user_id') is None:
        return redirect('/')
    if not Message.validate_message(request.form):
        return redirect('/wall')
    
    Message.save(request.form)

    return redirect('/wall')


@app.route('/delete', methods=['POST'])
def delete_message():
        #Checks if user id is logged in.
    if session.get('user_id') is None:
        return redirect('/')
    Message.delete_message(request.form['id'])

    return redirect('/wall')

