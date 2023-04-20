from flask_app import app
import datetime


@app.template_filter('time_since')
def time_since(dt):
    time_diff = datetime.datetime.now() - dt
    if time_diff.days > 365:
        return '{} years ago'.format(time_diff.days // 365)
    elif time_diff.days > 30:
        return '{} months ago'.format(time_diff.days // 30)
    elif time_diff.days > 0:
        return '{} days ago'.format(time_diff.days)
    elif time_diff.seconds > 3600:
        return '{} hours ago'.format(time_diff.seconds // 3600)
    elif time_diff.seconds > 60:
        return '{} minutes ago'.format(time_diff.seconds // 60)
    else:
        return 'just now'
