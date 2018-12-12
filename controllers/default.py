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
    return dict(type=request.vars['search_type'], content=request.vars['contains'])


def main():
    # We just want to expand the template.
    return dict()

def profile():
    if(auth.user is None):
        return redirect('../index')
    # To redirect to specific profile use the following:
    # href="{{=URL('default', 'profile',  args='desired_user_id')}}
    # We initialize the user at the current user
    user = auth.user
    #foo = api.get_user()
    # URL('api', 'get_user', args=request.args(0))
    #print(foo.user_degree)

    # If a user id is specified -> we set the user to the requested user
    if request.args(0) != None:
        id = int(request.args(0))

        users = db((db.auth_user.id == id)).select()
        if len(users) > 0:
            user = users[0]

            # attach the other data
            # user_data = db(db.users.user_id == id).select().first()
            # if user_data is not None:
            #     print "hullo"
            #     # user.append(dict(
                #     user_degree = user_data.user_degree,
                #     user_bio = user_data.user_bio,
                #     user_links = user_data.user_links
                # ))

        else:
            print "Error: user not found"
            return redirect('../main')
    return dict(user=user)

def research():
    if request.args(0) != None:
        if(auth.user is None):
                return redirect('../index')
        id = int(request.args(0))
        posts = db((db.post.id == id)).select()
        if len(posts) > 0:
            post = posts[0]
            if (len(db((db.applicant.user_id == auth.user.id)&(db.applicant.post_id == post.id)).select()) > 0):
                is_applicant = True
            else:
                is_applicant = False
            tags = post.post_tags
            tags = tags.split(',')
        else:
            print "Error: post not found"
            return redirect('../main')
    return dict(post=post, is_applicant=is_applicant, given_tags=tags)

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
    #flash = dict(register='An email verifying your registration has been sent. Follow the link to proceed.')
    #auth.messages.email_sent = flash.get(request.args(0),auth.messages.email_sent)
    if request.args(0) == 'register':
        form = auth.register(next=auth.settings.register_next)
    if request.args(0) == 'login':
        form = auth.login(next=auth.settings.login_next)
    else:
        form = auth()
    return dict(form=auth())
    
def register():
   return dict(form=auth.register())



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
