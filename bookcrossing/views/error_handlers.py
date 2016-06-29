from flask import render_template


def page_not_found(e):
    error = {'title': '404 Not Found',
             'message': 'Error 404, Page Not Found'}
    return render_template('error_handler.html', error=error), 404


def forbidden(e):
    error = {'title': '403 Forbidden',
             'message': 'Error 403, Forbidden'}
    return render_template('error_handler.html', error=error), 403


def gone(e):
    error = {'title': '410 Gone',
             'message': 'Error 410, Gone'}
    return render_template('error_handler.html', error=error), 410


def internal_server_error(e):
    error = {'title': '500 Internal Server Error',
             'message': 'Error 500, Forbidden'}
    return render_template('error_handler.html', error=error), 500
