# -*- coding: utf-8 -*-
# this file is released under public domain and you can use without limitations

# -------------------------------------------------------------------------
# This is a sample controller
# - index is the default action of any application
# - user is required for authentication and authorization
# - download is for downloading files uploaded in the db (does streaming)
# -------------------------------------------------------------------------


def index():
    # We just want to expand the template.
    return dict()

def search():
    # We just want to expand the template.
    return dict()


def main():
    # We just want to expand the template.
    return dict()

def profile():
    # To redirect to specific profile use the following:
    # href="{{=URL('default', 'profile',  args='desired_user_id')}}
    # We initialize the user at the current user
    user = auth.user
    # If a user id is specified -> we set the user to the requested user
    if request.args(0) != None:
        id = int(request.args(0))
        users = db((db.auth_user.id == id)).select()
        if len(users) > 0:
            user = users[0]
        else:
            print "Error: user not found"
    return dict(user=user)

def research():
    # To redirect to specific profile use the following:
    # href="{{=URL('default', 'profile',  args='desired_user_id')}}
    # We initialize the user at the current user
    # If a user id is specified -> we set the user to the requested user
    if request.args(0) != None:
        id = int(request.args(0))
        posts = db((db.post.id == id)).select()
        if len(posts) > 0:
            post = posts[0]
        else:
            print "Error: post not found"
    return dict(post=post)

def settings():
    # We just want to expand the template.
    return dict()

def user():
    """
    exposes:
    http://..../[app]/default/user/login
    http://..../[app]/default/user/logout
    http://..../[app]/default/user/register
    http://..../[app]/default/user/profile
    http://..../[app]/default/user/retrieve_password
    http://..../[app]/default/user/change_password
    http://..../[app]/default/user/bulk_register
    use @auth.requires_login()
        @auth.requires_membership('group name')
        @auth.requires_permission('read','table name',record_id)
    to decorate functions that need access control
    also notice there is http://..../[app]/appadmin/manage/auth to allow administrator to manage users
    """
    if request.args(0) == 'register':
        form = auth.register(next=auth.settings.register_next)
    elif request.args(0) == 'login':
        form = auth.login(next=auth.settings.login_next)
    else:
        form = auth()
    return dict(form=form)

# def register():
#     form = SQLFORM(db.auth_user)
#     if form.validate():
#         auth.get_or_create_user(form.vars)
#         # cruzid = auth.email.split('@')[0]
#         # ucsc_user = db((db.ucsc_user.cruz_id == cruzid)).select()[0]
#         # auth.first_name = ucsc_user.first_name + " " + ucsc_user.middle_name
#         # auth.last_name = ucsc_user.last_name
#         # auth.user = admin_user
#     return dict(form=form)



@cache.action()
def download():
    """
    allows downloading of uploaded files
    http://..../[app]/default/download/[filename]
    """
    return response.download(request, db)


def call():
    """
    exposes services. for example:
    http://..../[app]/default/call/jsonrpc
    decorate with @services.jsonrpc the functions to expose
    supports xml, json, xmlrpc, jsonrpc, amfrpc, rss, csv
    """
    return service()

import os
def serve_file():
    filename = request.args(0)
    path = os.path.join(request.folder, 'private', 'file_subfolder',filename)
    return response.stream(path)
