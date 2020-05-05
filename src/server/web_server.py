from flask import Flask, request, make_response
from server import *

s=Server('C:\\Users\\yuval\\projects\\drop_box\\clients_files.db','C:\\Users\\yuval\\projects\\drop_box\\client_files')
app = Flask(__name__)


@app.route('/')
def hello():
    return "Hello World!"

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
        r=make_response(s.get_file_list(username,file_id))
        return (r)
    else:
        if s.get_file(username,file_id)=='ok':
            return(str(file_id))
        else:
            return('')

@app.route('/<username>/<path:dirname>', methods=["POST"])
def put_file(username, dirname):
    '''
    get a file and save it im=n the server
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
"""
@app.route('/<username>/<path:dirname>', methods=["POST"])
def add_permition(username, dirname):
    '''
    get a file and save it im=n the server
    '''
    #http://localhost:5000/yuval/Themes/aero/he-IL?name=http_put_file_test&type=my_type
    names = request.args.get('names')
    Type = request.args.get('type')
    if type(name) is not unicode or type(Type) is not unicode:
        r = make_response('the parameters mast be string')
        r.status_code = 400
        return r
    dir_id=s.get_id(username,dirname)
    if dir_id==s.exists_eror:return('the file didnt found')
    dir_type=s.check_type(dir_id )
"""
@app.route('/del_file/<username>/<path:dirname>')
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

if __name__ == '__main__':
    app.run(threaded=False)