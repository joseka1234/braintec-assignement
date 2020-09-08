from rodriguez_cortes_jose_carlos.db import get_db
import defusedxml.ElementTree as et
import re

ID = 0
NAME = 1
LAST_NAME = 2
ADDRESS = 3
EMAIL = 4
PHONE = 5

class Contact:
    def __init__(self, contact_id = None, first_name = None, last_name = None, email = None, phone = None, address = None):
        self.contact_id = contact_id or ""
        self.first_name = first_name or ""
        self.last_name = last_name or ""
        self.email = email or ""
        self.phone = phone or ""
        self.address = address or ""

    # Write this contact to DB
    def write_to_db(self, db = None, cr=None):
        if db == None:
            db = get_db()
        if cr == None:
            cr = db.cursor()

        if not self.contact_exists_in_database(cr=cr):
            cr.execute("USE exercise")
            cr.execute('INSERT INTO contact (firstname, lastname, address, email, phone) VALUES (%s, %s, %s, %s, %s)',
                    (self.first_name, self.last_name, self.address, self.email, self.phone)
            )
            db.commit()
    
    def contact_exists_in_database(self, cr=None):
        if cr == None:
            cr = get_db().cursor()
        cr.execute("USE exercise")
        cr.execute("SELECT * FROM contact WHERE contact_id = %s OR email = %s OR phone = %s",
                    (self.contact_id, self.email, self.phone)
        )
        return len(cr.fetchall()) > 0

    def is_valid_contact(self):
        return self._is_valid_mail() and self._is_valid_phone()

    def _is_valid_mail(self):
        return re.fullmatch(r"^.+@.+\..+$", self.email) != None

    def _is_valid_phone(self):
        return re.fullmatch(r"^\+*[-\s()0-9]+$", self.phone) != None

    def initialize_from_xml(self, xml):
        self.contact_id = 0
        self.first_name = xml.find("firstname").text
        self.last_name = xml.find("lastname").text
        self.email = xml.find("email").text
        self.phone = xml.find("phone").text
        self.address = xml.find("address").text

# Gets all the database contacts
def get_database_contacts():
    db = get_db()
    cr = db.cursor()
    cr.execute("USE exercise")
    cr.execute("SELECT * FROM contact")
    db_contacts = cr.fetchall()
    return [Contact(c[ID], c[NAME], c[LAST_NAME], c[EMAIL], c[PHONE], c[ADDRESS]) for c in db_contacts]

# Returns an array of contacts loaded from a XML file.
# If a contact is in bad format the function doesn't load anything.
# If it's impossible to load anything the function returns a void array "[]"
def load_xml_contact(xml_file):
    contacts = []
    xml_file = "<root>" + xml_file + "</root>"
    root = et.fromstring(xml_file)
    aux_contact = Contact()

    for contact_xml in root:
        aux_contact.initialize_from_xml(contact_xml)
        if aux_contact.is_valid_contact():
            contacts.append(aux_contact)
    return contacts