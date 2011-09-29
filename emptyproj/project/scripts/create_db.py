"""Create the application's database.
"""

import sys
from pyramid.paster import get_app

from c2cgeoportal import schema
from c2cgeoportal import parentschema

import transaction

def main():
    if len(sys.argv) < 2:
        sys.exit("""Usage: buildout/bin/create_db INI_FILE OPTION..."

Available options:
  -d  --drop        drop the curent tables
  -p  --populate    populate the table with example data""")

    # read the configuration
    ini_file = sys.argv[1]
    app = get_app(ini_file, "c2cgeoportal")
    settings = app.registry.settings

    # sets the schema and load the database model
    schema = settings['schema']
    parentschema = settings['parentschema']
    from project import models
    from c2cgeoportal import models as c2cmodels

    if "-d" in sys.argv[2:] or '--drop' in sys.argv[2:]:
        print "Dropping tables"
        for table in reversed(Base.metadata.sorted_tables):
            if table.name != 'tsearch' and table.schema == schema: 
                print "Dropping table %s" % table.name
                table.drop(bind=DBSession.bind, checkfirst=True)

    print "Creating tables"
    for table in Base.metadata.sorted_tables:
        if table.name != 'tsearch' and table.schema == schema: 
            print "Creating table %s" % table.name
            table.create(bind=DBSession.bind, checkfirst=True)
    sess = c2cmodels.DBSession()

    admin = models.User(username=u'admin', 
                password=u'admin',
                )
    roleadmin = c2cmodels.Role(name=u'role_admin') 
    admin.role = roleadmin
    sess.add_all([admin, roleadmin])

    if "-p" in sys.argv[2:] or '--populate' in sys.argv[2:]:
        print "Populate the Database"

        # add the objects creation there

        sess.add_all([]) # add the oblect that we want to commit in the array

    transaction.commit()
    print "Commited successfully"

