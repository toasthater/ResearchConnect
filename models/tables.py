# Define your tables below (or better in another model file) for example
#
# >>> db.define_table('mytable', Field('myfield', 'string'))
#
# Fields can be 'string','text','password','integer','double','boolean'
#       'date','time','datetime','blob','upload', 'reference TABLENAME'
# There is an implicit 'id integer autoincrement' field
# Consult manual for more options, validators, etc.




# after defining tables, uncomment below to enable auditing
# auth.enable_record_versioning(db)


import datetime

def get_user_email():
    return None if auth.user is None else auth.user.email

def get_current_time():
    return datetime.datetime.utcnow()

def update_values(fields, id):
    cruzid =  fields['email'].split('@')[0]
    ucsc_users = db((db.ucsc_user.cruzid == cruzid)).select()
    if len(ucsc_users) > 0:
        ucsc_user = db((db.ucsc_user.cruzid == cruzid)).select()[0]
        first_name = ucsc_user.first_name + " " + ucsc_user.middle_name
        last_name = ucsc_user.last_name
        db(db.auth_user.id == id).update(first_name=first_name, last_name=last_name)
    else:
        print "USER NOT FOUND IN UCSC USERS DB"
    return


db.define_table('post',
                Field('post_author', default=get_user_email()),
                Field('post_title'),
                Field('post_content', 'text'),
                Field('post_time', 'datetime', default=get_current_time()),
                )


# Thumbs
db.define_table('thumb',
                Field('user_email'), # The user who thumbed, easier to just write the email here.
                Field('post_id', 'reference post'), # The thumbed post
                Field('thumb_state'), # This can be 'u' for up or 'd' for down, or None for... None.
                )

# CruzIDs
db.define_table('ucsc_user',
                Field('cruzid'),
                Field('first_name'),
                Field('middle_name'),
                Field('last_name')
                )

# CruzIDs
db.define_table('ucsc_faculty_member',
                Field('cruzid'),
                Field('phone'),
                Field('name'),
                Field('department'),
                Field('title')
                )

db.auth_user.first_name.writable = False
db.auth_user.last_name.writable = False
db.auth_user._after_insert.append(lambda f, id: update_values(f, id))