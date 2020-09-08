import tempfile
import pytest
import os

from rodriguez_cortes_jose_carlos.models.contact import (
    Contact, get_database_contacts, load_xml_contact
)
from rodriguez_cortes_jose_carlos.db import get_db, init_db
from rodriguez_cortes_jose_carlos import create_app

app = create_app(test_config=True)

@pytest.fixture
def setup_app():
    with app.app_context():
        db_fd, app.config['DATABASE'] = tempfile.mkstemp()
        app.config['TESTING'] = True

        with app.test_client() as client:
            with app.app_context():
                init_db()
            yield client

        os.close(db_fd)
        os.unlink(app.config['DATABASE'])

def test_contact_validation():
    good_contact = Contact(0, "JOSE CARLOS", "RODRIGUEZ CORTES", "josecarlosrodriguezcortes@gmail.com", "694479093", "C\\ Nueva")
    bad_email_contact = Contact(0, "FRANCISCO", "RODRIGUEZ HERNANDEZ", "francisco.com", "694479093", "C\\ Vieja")
    bad_phone_contact = Contact(0, "PACO", "HERNANDEZ RODRIGUEZ", "paco@gmail.com", "694u479093", "C\\ Otra")
    
    #Check a valid contact
    assert good_contact.is_valid_contact() == True
    #Check no valid contact
    assert bad_email_contact.is_valid_contact() == False
    assert bad_phone_contact.is_valid_contact() == False
    #Check individual valid fields of invalid contacts
    assert bad_email_contact._is_valid_phone() == True
    assert bad_phone_contact._is_valid_mail() == True

#Test if write to DB works
def test_write_contact_db():
    with app.app_context():
        db = get_db()
        cr = db.cursor()
        
        # We check that Good Contact is in the DB.
        Contact(0, "JOSE CARLOS", "RODRIGUEZ CORTES", "josecarlosrodriguezcortes@gmail.com", "694479093", "C\\ Nueva").write_to_db(db=db, cr=cr)
        cr.execute("USE exercise")
        cr.execute("SELECT * FROM contact WHERE phone = 694479093")
        assert len(cr.fetchall()) == 1
        
        # We check that we cannot insert the same contact two times.
        cr.execute("USE exercise")
        cr.execute("SELECT * FROM contact")
        first_length = len(cr.fetchall())
        Contact(0, "JOSE CARLOS", "RODRIGUEZ CORTES", "josecarlosrodriguezcortes@gmail.com", "694479093", "C\\ Nueva").write_to_db(db=db, cr=cr)
        cr.execute("USE exercise")
        cr.execute("SELECT * FROM contact")
        new_length = len(cr.fetchall())
        assert first_length == new_length
        
#Test if get data from DB works
def test_get_database_contacts():
    with app.app_context():
        db_contacts = get_database_contacts()
        # Check if the data is retrieved
        assert len(db_contacts) > 0
        # Check if the data type is correct
        assert type(db_contacts[0]) == Contact

def test_xml_load_contact():
    with app.app_context():
        with app.open_resource(app.config['XML_TEST_FILE_GOOD']) as good_file:
            contact_good = load_xml_contact(good_file.read().decode('utf8'))
        with app.open_resource(app.config['XML_TEST_FILE_BAD']) as bad_file:
            contact_bad = load_xml_contact(bad_file.read().decode('utf8'))
        with app.open_resource(app.config['XML_TEST_FILE_MULTIPLE']) as multi_file:
            contact_multi = load_xml_contact(multi_file.read().decode('utf8'))

        assert contact_good != None and len(contact_good) == 1 and type(contact_good[0]) == Contact
        assert contact_bad == []
        assert contact_multi != None and len(contact_multi) == 2 and type(contact_multi[0]) == Contact

def test_contact_exists_in_bd():
    with app.app_context():
        db = get_db()
        cr = db.cursor()
        
        #We set the ID to -1 to ensure that the functions looks for email or phone instead of ID.
        good_contact = Contact(-1, "JOSE CARLOS", "RODRIGUEZ CORTES", "josecarlosrodriguezcortes@gmail.com", "694479093", "C\\ Nueva")
        random_contact = Contact(-1, "RANDOM", "RODRIGUEZ", "random@modnar.com", "123321123", "Aleatory 15")
        assert good_contact.contact_exists_in_database(cr) == True
        assert random_contact.contact_exists_in_database(cr) == False