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

# Students
db.define_table('student',
                Field('student_name'),
                Field('student_major'),
                Field('student_resume'),#file upload
                Field('student_bio'),
                Field('student_skills'),#list
                Field('student_interest'),#list
                Field('student_following'),#list
                Field('student_follower'),#list 
                Field('student_accept_state')
)


# Professors
db.define_table('professor',
                Field('prof_name'),
                Field('prof_dep'),
                Field('prof_email',default=get_user_email()),
                Field('prof_hours'),#list
                Field('prof_classes'),#list
                Field('prof_research'),#list
                Field('prof_following'),#list
                Field('prof_follower'),#list
                )
# Research Oppurtunity
db.define_table('research_post',
                Field('research_topic'),
                Field('research_professor'),
                Field('research_major'),
                Field('research_req'),#list
                Field('research_tags'),#list
                Field('research_students'),#list of student objs
)
# User
