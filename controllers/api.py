# Here go your api methods.

def register_student():
    email = request.vars.email
    cruzid = email.split('@')[0]
    ucsc_user = db((db.ucsc_user.cruz_id == cruzid)).select()[0]
    first_name = ucsc_user.first_name + " " + ucsc_user.middle_name
    last_name = ucsc_user.last_name
 
    user_id = db.post.insert(
        post_title=request.vars.post_title,
        post_content=request.vars.post_content,
        thumb=None,
        score=0
    )
    # We return the id of the new post, so we can insert it along all the others.
    return response.json(dict(post_id=post_id))




@auth.requires_signature()
def add_post():
    post_id = db.post.insert(
        post_title=request.vars.post_title,
        post_content=request.vars.post_content,
        post_department=request.vars.post_department,
        post_tags=request.vars.get('post_tags[]',None),
        thumb=None,
        score=0
    )
    # We return the id of the new post, so we can insert it along all the others.
    return response.json(dict(post_id=post_id))


# def get_score():
#     """Gets the score of the current post."""
#     post_id = int(request.vars.post_id)
#     thumbs_up = len(db((db.thumbs.post_id == post_id) & (db.thumbs.thumb_state == "u")).select())
#     thumbs_down = len(db((db.thumbs.post_id == post_id) & (db.thumbs.thumb_state == "d")).select())
#     score = thumbs_up - thumbs_down
#     return response.json(score=score)


def get_post_list():
    results = []
    if auth.user is None:
        # Not logged in.
        rows = db().select(db.post.ALL,orderby=~db.post.post_time)
        for row in rows:
            results.append(dict(
                id=row.id,
                post_title=row.post_title,
                post_content=row.post_content,
                post_author=row.post_author,
                post_author_name=row.post.post_author_name,
                post_department=row.post.post_department,
                post_tags=row.post.post_tags,
                post_status=row.post.post_status,
                thumb = None,
                score=0
            ))
    else:
        # Logged in.
        rows = db().select(db.post.ALL, db.thumb.ALL,
                            left=[
                                db.thumb.on((db.thumb.post_id == db.post.id) & (db.thumb.user_email == auth.user.email)),
                            ],
                            orderby=~db.post.post_time)
        for row in rows:
            thumbs_up=len(db((db.thumb.post_id == row.post.id) & (db.thumb.thumb_state == "u")).select())
            thumbs_down=len(db((db.thumb.post_id == row.post.id) & (db.thumb.thumb_state == "d")).select())
            post_score=thumbs_up - thumbs_down
            results.append(dict(
                id=row.post.id,
                post_title=row.post.post_title,
                post_content=row.post.post_content,
                post_author=row.post.post_author,
                post_author_name=row.post.post_author_name,
                post_department=row.post.post_department,
                post_tags=row.post.post_tags,
                post_status=row.post.post_status,
                thumb = None if row.thumb.id is None else row.thumb.thumb_state,
                score=post_score
            ))
    # For homogeneity, we always return a dictionary.
    return response.json(dict(post_list=results))


def get_search_posts():
    results = []
    search_type = request.vars.search_type
    search_query = request.vars.search_query
    print "Search type : " + search_type
    print "Search query : " + search_query

    if auth.user is None:
        # Not logged in.
        if search_type == 'tag':
            rows = db(db.post.post_tags.contains(search_query)).select(db.post.ALL,orderby=~db.post.post_time)
            print "Found " + str(len(rows)) + " researches "
        elif search_type == 'department':
            rows = db(db.post.post_department.contains(search_query)).select(db.post.ALL,orderby=~db.post.post_time)
        elif search_type == 'title':
            rows = db(db.post.post_title.contains(search_query)).select(db.post.ALL,orderby=~db.post.post_time)
        elif search_type == 'professor' :
            rows = db(db.post.post_author_name.contains(search_query)).select(db.post.ALL,orderby=~db.post.post_time)
        else :
            rows = db().select(db.post.ALL,orderby=~db.post.post_time)
        
        for row in rows:
            results.append(dict(
                id=row.id,
                post_title=row.post_title,
                post_content=row.post_content,
                post_author=row.post_author,
                post_department=row.post.post_department,
                post_tags=row.post.post_tags,
                post_status=row.post.post_status,
                thumb = None,
                score=0
            ))
    else:
        # Logged in.
        if search_type == 'tag':
            rows = db(db.post.post_tags.contains(search_query)).select(db.post.ALL, db.thumb.ALL,
                                left=[
                                    db.thumb.on((db.thumb.post_id == db.post.id) & (db.thumb.user_email == auth.user.email)),
                                ],
                                orderby=~db.post.post_time)
            print "Found " + str(len(rows)) + " researches "
        elif search_type == 'department':
            rows = db(db.post.post_department.contains(search_query)).select(db.post.ALL, db.thumb.ALL,
                            left=[
                                db.thumb.on((db.thumb.post_id == db.post.id) & (db.thumb.user_email == auth.user.email)),
                            ],
                            orderby=~db.post.post_time)
        elif search_type == 'title':
            rows = db(db.post.post_title.contains(search_query)).select(db.post.ALL, db.thumb.ALL,
                            left=[
                                db.thumb.on((db.thumb.post_id == db.post.id) & (db.thumb.user_email == auth.user.email)),
                            ],
                            orderby=~db.post.post_time)
        elif search_type == 'professor' :
            rows = db(db.post.post_author_name.contains(search_query)).select(db.post.ALL, db.thumb.ALL,
                            left=[
                                db.thumb.on((db.thumb.post_id == db.post.id) & (db.thumb.user_email == auth.user.email)),
                            ],
                            orderby=~db.post.post_time)
        else :
            rows = db().select(db.post.ALL, db.thumb.ALL,
                            left=[
                                db.thumb.on((db.thumb.post_id == db.post.id) & (db.thumb.user_email == auth.user.email)),
                            ],
                            orderby=~db.post.post_time)
        for row in rows:
            thumbs_up=len(db((db.thumb.post_id == row.post.id) & (db.thumb.thumb_state == "u")).select())
            thumbs_down=len(db((db.thumb.post_id == row.post.id) & (db.thumb.thumb_state == "d")).select())
            post_score=thumbs_up - thumbs_down
            results.append(dict(
                id=row.post.id,
                post_title=row.post.post_title,
                post_content=row.post.post_content,
                post_author=row.post.post_author,
                post_department=row.post.post_department,
                post_tags=row.post.post_tags,
                post_status=row.post.post_status,
                thumb = None if row.thumb.id is None else row.thumb.thumb_state,
                score=post_score
            ))
    # For homogeneity, we always return a dictionary.
    return response.json(dict(post_list=results))

    

def get_filtered_post_list():
    results = []
    if auth.user is None:
        # Not logged in.
        rows = db().select(db.post.ALL,orderby=~db.post.post_time)
        for row in rows:
            results.append(dict(
                id=row.id,
                post_title=row.post_title,
                post_content=row.post_content,
                post_author=row.post_author,
                post_department=row.post.post_department,
                post_tags=row.post.post_tags,
                post_status=row.post.post_status,
                thumb = None,
                score=0
            ))
    else:
        # Logged in.
        rows = db().select(db.post.ALL, db.thumb.ALL,
                            left=[
                                db.thumb.on((db.thumb.post_id == db.post.id) & (db.thumb.user_email == auth.user.email)),
                            ],
                            orderby=~db.post.post_time)
        for row in rows:
            thumbs_up=len(db((db.thumb.post_id == row.post.id) & (db.thumb.thumb_state == "u")).select())
            thumbs_down=len(db((db.thumb.post_id == row.post.id) & (db.thumb.thumb_state == "d")).select())
            post_score=thumbs_up - thumbs_down
            results.append(dict(
                id=row.post.id,
                post_title=row.post.post_title,
                post_content=row.post.post_content,
                post_author=row.post.post_author,
                post_department=row.post.post_department,
                post_tags=row.post.post_tags,
                post_status=row.post.post_status,
                thumb = None if row.thumb.id is None else row.thumb.thumb_state,
                score=post_score
            ))
    # For homogeneity, we always return a dictionary.
    return response.json(dict(post_list=results))

@auth.requires_signature()
def set_thumb():
    post_id = int(request.vars.post_id)
    thumb_up = request.vars.thumb.lower().startswith('u')
    thumb_down = request.vars.thumb.lower().startswith('d')
    if thumb_up:
        db.thumb.update_or_insert(
            (db.thumb.post_id == post_id) & (db.thumb.user_email == auth.user.email),
            post_id = post_id,
            user_email = auth.user.email,
            thumb_state='u'
        )
    elif thumb_down:
        db.thumb.update_or_insert(
            (db.thumb.post_id == post_id) & (db.thumb.user_email == auth.user.email),
            post_id = post_id,
            user_email = auth.user.email,
            thumb_state='d'

        )
    else:
        db((db.thumb.post_id == post_id) & (db.thumb.user_email == auth.user.email)).delete()
    return "ok"


@auth.requires_signature()
def post_resume():
    file_str = request.vars.file_str
    user_id = auth.user.id

    db.resumes.update_or_insert(
        (db.resumes.user_id == user_id),
        user_id = user_id,
        file_str = file_str
    )

    return response.json(dict(file_str = file_str))


def get_resume():
    user_id = auth.user.id

    row = db(db.resumes.user_id == user_id).select().first()

    file_str = None
    if row is not None and row.file_str is not None:
        file_str = row.file_str
    return response.json(dict(file_str = file_str))

@auth.requires_signature()
def post_user():
    # file_str = request.vars.file_str
    user_id = auth.user.id
    db.users.update_or_insert(
        (db.users.user_id == user_id),
        user_degree = request.vars.user_degree,
        user_bio = request.vars.user_bio,
        user_linkedin = rrequest.vars.user_linkedin
        
    )

    return response.json(dict(file_str = file_str))

def get_user():

    user_id = request.args(0)

    row = db(db.users.user_id == user_id).select().first()

    results = None
    if row is not None:
        results = dict(
            user_degree = row.user_degree,
            user_bio = row.user_bio,
            user_linkedin = row.user_linkedin
        )

    return response.json(dict(user = results))

@auth.requires_signature()
def edit_user():
    user_id = auth.user.id

    first_name = request.vars.user_first_name
    last_name = request.vars.user_last_name
    user_bio = request.vars.user_bio
    user_degree = request.vars.user_degree
    user_linkedin = request.vars.user_linkedin

    db.users.update_or_insert(
        (db.users.user_id == user_id),
        user_id = user_id,
        user_degree = user_degree,
        user_bio = user_bio,
        user_linkedin = user_linkedin,
    )

    row = db(db.auth_user.id == user_id).select().first()
    row.update_record(first_name = first_name, last_name = last_name)

    #TODO: first and last name updating


def get_applicants():
    post_id = int(request.vars.post_id)
    print post_id
    applicant_list = list()
    applicants = db(db.applicant.post_id == post_id).select(orderby=~db.applicant.apply_time)
    for applicant in applicants:
        if(applicant.accepted == 0):
            applicant_list.append(dict(
                id = applicant.id,
                name = applicant.name,
                email = applicant.email,
                user_id = applicant.user_id
            ))
    return response.json(dict(applicant_list = applicant_list))

#@auth.requires_signature()
def add_applicant():
    pid = int(request.vars.post_id)
    applicant_id = db.applicant.insert(
        post_id = pid,
    )
    return response.json(dict(post_id=pid))

def add_participant():
    applicant_id = int(request.vars.applicant_id)
    db.applicant.update_or_insert(
            (db.applicant.id == applicant_id),
            accepted = 1
        )
    return response.json(dict(applicant_id=applicant_id))
    
def decline_participant():
    applicant_id = int(request.vars.applicant_id)
    db(db.applicant.id == applicant_id).delete()
    return response.json(dict(applicant_id=applicant_id))

def get_participants():
    post_id = int(request.vars.post_id)
    participant_list = list()
    participants = db(db.applicant.post_id == post_id).select(orderby=~db.applicant.apply_time)
    for participant in participants:
        if(participant.accepted == 1):
            participant_list.append(dict(
                id = participant.id,
                name = participant.name,
                email = participant.email,
                user_id = participant.user_id
            ))
    return response.json(dict(participant_list = participant_list))

def remove_post():
    post_id = int(request.vars.post_id)
    db(db.post.id == post_id).delete()
    db(db.applicant.post_id == post_id).delete()
    return response.json(dict(post_id=post_id))
    
def toggle_post():
    post_id = int(request.vars.post_id)
    post_status = request.vars.post_status
    if(post_status == 'Open'):
        post_status = 'Closed'
    else:
        post_status = 'Open'
    db.post.update_or_insert(
            (db.post.id == post_id),
            post_status = post_status
        )
    return response.json(dict(post_id=post_id))