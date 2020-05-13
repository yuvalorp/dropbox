from flask import Flask, request, make_response
from server import *



s=Server('C:\\Users\\yuval\\projects\\drop_box\\clients_files.db','C:\\Users\\yuval\\projects\\drop_box\\client_files')
app = Flask(__name__)



@app.route('/get_file/<username>/<path:filename>')
def get_file(username, filename):
    '''
    take a path of file or directory
    if it directory return a list of the files inside
    if it file it returns the file body
    '''

    #http://localhost:5000/get_file/yuval/Themes/aero/he-IL/aerolite.msstyles.mui
    file_id=s.get_id(username,filename)
    if file_id==s.exists_eror:return('the file didnt found')
    file_type=s.check_type(file_id )
    if file_type=='file':
        r=make_response({'file_list':s.get_file_list(username,file_id)})
        return (r)
    else:
        if s.get_file(username,file_id)=='ok':
            return(str(file_id))
        else:
            return('')


@app.route('/<username>/<path:dirname>', methods=["POST"])
def put_file(username, dirname):
    '''
    get a file and save it in the server
    '''
    #http://localhost:5000/yuval/Themes/aero/he-IL?name=http_put_file_test&type=my_type
    name = request.args.get('name')
    Type = request.args.get('type')
    if type(name) is not unicode or type(Type) is not unicode:
        r = make_response('the parameters mast be string')
        r.status_code = 400
        return r
    dir_id=s.get_id(username,dirname)
    if dir_id==s.exists_eror:return('the file didnt found')
    dir_type=s.check_type(dir_id )
    if dir_type=='file':
        q=s.put_file(str(username),str(name),dir_id,str(Type))
        if type(q) is int:
            return ''
        else:
            return q
    else:
        r = make_response('the path mast be a directory')
        r.status_code = 400
        return r


@app.route('/add_permition/<username>/<path:dirname>', methods=["POST"])
def add_permition(username, dirname):
    '''
    add permition to a file
    '''

    names = request.args.getlist('names')
    dir_id=s.get_id(username,dirname)
    if dir_id==s.exists_eror:return('the file didnt found')
    if type(names) is  list :
        s.add_permition(username,dir_id,names)
    elif type(names) is not unicode:
        s.add_permition(username,dir_id,[names])
    else:
        r = make_response('the parameters mast be string')
        r.status_code = 400
        return r


@app.route('/remove_permition/<username>/<path:dirname>', methods=["POST"])
def remove_permition(username, dirname):
    '''
    add permition to a file
    '''

    names = request.args.getlist('names')
    dir_id=s.get_id(username,dirname)
    if dir_id==s.exists_eror:return('the file didnt found')
    if type(names) is  list :
        s.remove_permition(username,dir_id,names)
    elif type(names) is not unicode:
        s.remove_permition(username,dir_id,[names])
    else:
        r = make_response('the parameters mast be string')
        r.status_code = 400
        return r


@app.route('/del_file/<username>/<path:dirname>', methods=["DEL"])
def del_file(username, dirname):
    '''
    delete a file from the server
    '''
    #http://localhost:5000/yuval/Themes/aero/he-IL
    dir_id=s.get_id(username,dirname)

    if dir_id==s.exists_eror:return('the file didnt found')
    q=s.del_file(username,dir_id)
    if type(q) is list:
        return ''
    else:
        return q


@app.route('/rename_file/<username>/<path:dirname>', methods=["POST"])
def rename_file(username, dirname):
    '''
    rename file
    '''
    #http://localhost:5000/yuval/Themes/aero/he-IL?new_name=moshe
    new_name = request.args.get('new_name')
    #print(new_name,username,dirname)
    if type(new_name) is not unicode :
        r = make_response('the parameters mast be string')
        r.status_code = 400
        return r
    dir_id=s.get_id(username,dirname)
    if dir_id==s.exists_eror:return('the file didnt found')
    q=s.rename_file(username,dir_id,new_name)
    if q =='ok':
        return ''
    else:
        return q


@app.route('/check_pasward')
def check_pasward():
    pasward = request.args.get('pasward')
    user = request.args.get('user')
    if type(pasward) is not unicode or type(user) is not unicode:
        r = make_response('the parameters mast be string')
        r.status_code = 400
        return r
    return (str(s.check_pasward(user,pasward)))


@app.route('/create_user', methods=["POST"])
def create_user():
    pasward = request.args.get('pasward')
    user = request.args.get('user')
    if type(pasward) is not unicode or type(user) is not unicode:
        r = make_response('the parameters mast be string')
        r.status_code = 400
        return r
    return(s.create_user(user,pasward))


@app.route('/who_can_see/<path:dirname>')
def who_can_see(dirname):
    dir_id=s.get_id('',dirname)
    if dir_id==s.exists_eror:return('the file didnt found')
    return (s.who_can_see(dir_id))


@app.route('/files_can_see/<username>')
def files_can_see(username):
    return (s.files_can_see(username))


@app.route('/who_in_group/<groupp>')
def who_in_group(groupp):
    return (s.who_in_group(groupp))


@app.route('/groups_user_in/<username>')
def groups_user_in(username):
    return (s.groups_user_in(username))




if __name__ == '__main__':app.run(threaded=False)