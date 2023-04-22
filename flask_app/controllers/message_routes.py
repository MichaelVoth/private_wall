from flask import render_template, redirect, request, session, flash
from flask_app import app
from flask_app.models.users import User
from flask_app.models.messages import Message


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
        return redirect('/report')
    Message.delete_message(request.form['id'])

    return redirect('/wall')


@app.route('/report')
def report_user():
    user_ip = request.remote_addr
    session.clear()

    return render_template('report.html', ip=user_ip)

