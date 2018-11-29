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
        post_tags=request.vars.post_tags,
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



