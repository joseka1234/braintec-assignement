from rodriguez_cortes_jose_carlos.models.contact import load_xml_contact
from rodriguez_cortes_jose_carlos.db import get_db

from flask import (
    Blueprint, redirect, request, url_for
)

xml_blueprint = Blueprint('upload_xml', __name__, url_prefix="/upload_xml")

ALLOWED_EXTENSIONS = { 'xml' }

def allowed_file(filename):
    return "." in filename and filename.split('.')[1].lower() in ALLOWED_EXTENSIONS

@xml_blueprint.route('/upload_xml', methods=('GET', 'POST'))
def upload_xml():
    if request.method == "POST":
        db = get_db()
        cr = db.cursor()
        file = request.files['xml_file']
        if allowed_file(file.filename):
            xml_text = file.read().decode('utf8')
            for contact in load_xml_contact(xml_text):
                contact.write_to_db(db = db, cr = cr)
        else:
            return redirect(url_for('contacts.contact_form'))

    return redirect(url_for('contacts.contact_list'))