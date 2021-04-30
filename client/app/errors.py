from flask import render_template
from . import bp


@bp.errorhandler(400)
def abort_error(error):
    return render_template('400.html.j2', error=error), 400
