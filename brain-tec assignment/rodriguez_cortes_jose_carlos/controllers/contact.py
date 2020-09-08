from flask import (
    Blueprint, flash, redirect, render_template, request, url_for
)

from rodriguez_cortes_jose_carlos.models.contact import Contact, get_database_contacts
from rodriguez_cortes_jose_carlos.db import get_db

blueprint = Blueprint('contacts', __name__, url_prefix="/")

@blueprint.route('/', methods=('GET', 'POST'))
def contact_form():
    if request.method == 'POST':
        contact = Contact(
            None,
            request.form['firstname'],
            request.form['lastname'],
            request.form['email'],
            request.form['phone'],
            request.form['address']
        )
        
        if contact.is_valid_contact():
            contact.write_to_db()
            return redirect(url_for('contacts.contact_list'))
        else:
            flash("You've made some mistake introducing the contact data.")

    return render_template('contact/contact_form.html')

@blueprint.route('/list', methods=('GET', 'POST'))
def contact_list():
    return render_template('contact/contact_list.html', contacts = get_database_contacts())