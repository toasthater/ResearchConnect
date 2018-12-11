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
                post_department=row.post.post_department,
                post_tags=row.post.post_tags,
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
    user_email = auth.user.email

    db.resumes.update_or_insert(
        (db.resumes.user_email == user_email),
        user_email = user_email,
        file_str = file_str
    )

    return response.json(dict(file_str = file_str))

# TODO: Shold this require signature?
# @auth.requires_signature()
def get_resume():
    user_email = auth.user.email

    row = db(db.resumes.user_email == user_email).select().first()

    file_str = None
    if row is not None and row.file_str is not None:
        file_str = row.file_str
    return response.json(dict(file_str = file_str))


def get_applicants():
    post_id = int(request.vars.post_id)
    print post_id
    applicant_list = list()
    applicants = db(db.applicant.post_id == post_id).select(orderby=~db.applicant.apply_time)
    for applicant in applicants:
        applicant_list.append(dict(
            id = applicant.id,
            name = applicant.name,
            email = applicant.email,
        ))
    return response.json(dict(applicant_list = applicant_list))

#@auth.requires_signature()
def add_applicant():
    applicant_list = []
    applicant_email = request.vars.email
    pid = int(request.vars.post_id)
    full_list = db(db.applicant.post_id == pid and db.applicant.email == applicant_email).select(orderby=~db.applicant.apply_time)
    for applicant in full_list:
        applicant_list.append(dict(
            id = applicant.id,
            name = applicant.name,
            email = applicant.email,
        ))
        
    if (applicant_list == []):
        applicant_id = db.applicant.insert(
            post_id = pid,
        )
    return response.json(dict(post_id=pid))
    
    
