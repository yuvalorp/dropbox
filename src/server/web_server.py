from flask import Flask, request, make_response,send_file
from server import *
from werkzeug.utils import secure_filename
from json import dumps,loads

import os

cwd=os.getcwd()
if not os.path.exists(cwd+'\\client_files'):os.mkdir(cwd+'\\client_files')
s=Server(cwd+'\\db_files.db',cwd+'\\client_files')
app = Flask(__name__)



@app.route('/get_file/<username>/<path:filename>')
def get_file(username, filename):
    '''
    take a path of file or directory
    if it directory return a list of the files inside
    if it file it returns the file body
    '''

    #http://localhost:5000/get_file/yuval/Themes/aero/he-IL/aerolite.msstyles.mui
    file_id=s.get_id(filename)
    s.add_to_log("asked for file username: "+str(username)+"  filename: "+ filename)
    if file_id==s.exists_eror:return('the file didnt found')
    file_type=s.check_type(file_id )
    if file_type=='file':
        r=make_response({'file_list':s.get_file_list(username,file_id)})
        return (r)
    else:
        if s.get_file(username,file_id)=='ok':
            #return(str(file_id))
            return send_file(s.data_dir+'/'+str(file_id))
        else:
            return('')

@app.route('/put_dir/<username>/<path:dirname>', methods=["POST"])
def put_dir(username, dirname):
    '''
    get a directory and save it in the server
    '''

    name = request.args.get('name')
    print(type(name))


    s.add_to_log("user send file username: "+str(username)+"  directory name: "+ dirname)
    if type(name) is not unicode:
        r = make_response('the parameters mast be string')
        r.status_code = 400
        return r
    dir_id=s.get_id(dirname)
    print (username,dir_id,name)
    if dir_id==s.exists_eror:
        return('the file didnt found')
    dir_type=s.check_type(dir_id )
    if dir_type=='file':

        q=s.put_file(str(username),str(name),dir_id,'file')
        if type(q) is int:
            return ''
        else:
            return q

    else:
        r = make_response('the path mast be a directory')
        r.status_code = 400
        return r

@app.route('/put_file/<username>/<path:dirname>', methods=["POST"])
def put_file(username, dirname):
    '''
    get a file and save it in the server
    '''
    #http://localhost:5000/yuval/Themes/aero/he-IL?name=http_put_file_test&type=my_type

    s.add_to_log("user send file username: "+str(username)+"  directory name: "+ dirname)
    dir_id=s.get_id(dirname)
    if dir_id==s.exists_eror:
        return('the file didnt found')
    dir_type=s.check_type(dir_id )
    if dir_type=='file':
        if ('content-type' in request.headers) and (request.headers['content-type'].startswith('multipart/form-data')):

            if ('file' in request.files):
                fo = request.files['file']

                print(fo)
                print('filename ' + fo.filename)

                q=s.put_file(str(username),fo.filename,dir_id,'txt')

                if type(q) is int:

                    print(s.data_dir+'/'+str(q))
                    fo.save(s.data_dir+'\\'+str(q))
                    return ''
                else:
                    return q
            return ''

    else:
        r = make_response('the path mast be a directory')
        r.status_code = 400
        return r

@app.route('/test', methods=["POST"])
def testx():
    print(request.headers)
    print(request.headers['host'])
    print(request.headers['xxxx'])
    return ''

@app.route('/change_per/<username>/<path:dirname>', methods=["POST"])
def change_permition(username, dirname):
    '''
    change permition to a file
    '''

    names = request.args.get('names')
    s.add_to_log("asked for change permition for file username: "+str(username)+"  dirname: "+ dirname)
    dir_id=s.get_id(dirname)
    if dir_id==s.exists_eror:return('the file didnt found')
    if type(names) is  list :
        s.change_per(username,dir_id,names)
    elif type(names) is not unicode:
        s.change_per(username,dir_id,[names])
    else:
        r = make_response('the parameters mast be string')
        r.status_code = 400
        return r
@app.route('/get_per/<username>/<path:dirname>')
def get_per(username,dirname):
    dir_id=s.get_id(dirname)
    if dir_id==s.exists_eror:return('the file didnt found')
    files_list=s.who_can_see(dir_id)
    group_files_list=s.who_group_can_see(dir_id)
    x=''
    for i in group_files_list:
        x='group '+i
        files_list.append(x)
    return (dumps(files_list))






@app.route('/del_file/<username>/<path:dirname>', methods=["DEL"])
def del_file(username, dirname):
    '''
    delete a file from the server
    '''
    #http://localhost:5000/yuval/Themes/aero/he-IL
    dir_id=s.get_id(dirname)
    s.add_to_log("asked for delete file username: "+str(username)+"  dirname: "+ dirname)

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
    s.add_to_log("asked for rename file username: "+str(username)+"  dirname: "+ dirname+"  new name: "+ new_name)
    if type(new_name) is not unicode :
        r = make_response('the parameters mast be string')
        r.status_code = 400
        return r
    dir_id=s.get_id(dirname)
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
    s.add_to_log("asked for check pasward: "+str(user)+"  pasward: "+ pasward)
    if type(pasward) is not unicode or type(user) is not unicode:
        r = make_response('the parameters mast be string')
        r.status_code = 400
        return r
    return (str(s.check_pasward(user,pasward)))


@app.route('/create_user', methods=["POST"])
def create_user():
    pasward = request.args.get('pasward')
    user = request.args.get('user')
    groups = loads(request.args.get('groups'))
    s.add_to_log("asked for create user user: "+str(user)+"  pasward: "+ pasward)

    if type(pasward) is not unicode or type(user) is not unicode:
        r = make_response('the parameters mast be string')
        r.status_code = 400
        return r
    return(s.create_user(user,pasward,groups))


@app.route('/who_can_see/<path:dirname>')
def who_can_see(dirname):
    dir_id=s.get_id('',dirname)
    if dir_id==s.exists_eror:return('the file didnt found')
    return (s.who_can_see(dir_id))


@app.route('/files_can_see/<username>')
def files_can_see(username):
    return (s.files_can_see(username))

'''
@app.route('/who_in_group/<groupp>')
def who_in_group(groupp):
    return (s.who_in_group(groupp))
'''

@app.route('/groups_user_in/<username>')
def groups_user_in(username):
    return (s.groups_user_in(username))

@app.route('/replace/<username>/<path:dirname>')
def replace(username,dirname):

    new_place = request.args.get('new_place')

    if type(new_place) != unicode:
        r = make_response('the parameters mast be string')
        r.status_code = 400
        return r
    file_id=s.get_id(dirname)

    if file_id==s.exists_eror:

        r = make_response(s.exists_eror)
        r.status_code = 400
        return r
    new_place=s.get_id(new_place)
    s.add_to_log("asked for replace file id: "+str(file_id)+"  new place: "+ str(new_place))
    print(username,file_id,new_place)


    ans=s.replace_file(username,file_id,new_place)
    if ans=="ok":
        return ("ok")
    else:
        r = make_response(ans)
        r.status_code = 400
        return r
'''
@app.route('/check_type/<path:dirname>')
def check_type(userame,dirname):
    file_id=s.get_id(dirname)
    file_id=s.get_id(dirname)
    if file_id==s.exists_eror:
        r = make_response(s.exists_eror)
        r.status_code = 400
        return r
    else:
        file_type=s.check_type(file_id)
        return file_type
'''

@app.route('/get_log')
def get_log():
    r=make_response({'log':s.get_log()})
    return(r)

if __name__ == '__main__':app.run(threaded=False)