from json import  loads,dumps
def check_pasward(name,pas,conection):
    conection.request("GET", "/check_pasward?pasward="+pas+"&user="+name)

    res = conection.getresponse()
    if res.status==200:
        data = res.read()
        return (data=="True")
    else:
        return ("there was a conection eror")

def create_user(name,pas,conection):
    conection.request("POST", "/create_user?pasward="+pas+"&user="+name)
    res = conection.getresponse()
    if res.status==200:
        return (res.read())
    else:
        return ("there was a conection eror")

#/get_file/<username>/<path:filename>
def get_file_list(username,path,conection):
    conection.request("GET", "/get_file/"+username+path)

    res=conection.getresponse()
    if res.status==200:

        return (loads(res.read()))
    else:
        return ("there was a conection eror")

def rename_file(username,path,new_name,conection):
    conection.request("POST", "/rename_file/"+username+path+"?new_name="+new_name)
    res=conection.getresponse()
    if res.status==200:

        return (res.read())
    else:
        return ("there was a conection eror")

def delete_file(username,path,conection):
    conection.request("DEL", "/del_file/"+username+path)
    res=conection.getresponse()
    if res.status==200:

        return (res.read())
    else:
        return ("there was a conection eror")

def replace(username,path,new_path,conn):
    print(username,path,new_path)
    conn.request("GET", "/replace/"+username+path+"?new_place="+new_path)
    res = conn.getresponse()
    if res.status==200:
        return (res.read())
    else:
        return ("there was a conection eror")
def get_type(path,conection):
    conection.request("GET", "/get_type/"+path)
    res = conection.getresponse()
    if res.status==200:
        return (res.read())
    else:
        return ("there was a conection eror")

def change_per(username,path,per_list,group_per_list,conn):
    conn.request("GET", "/change_per/"+username+path+"?names="+dumps(per_list,group_per_list))
    res = conn.getresponse()
    if res.status==200:
        return (res.read())
    else:
        return ("there was a conection eror")

def get_per(path,conn):
    conn.request("GET", "/get_per/"+path)
    res = conn.getresponse()
    if res.status==200 or res.read()=='the file didnt found' :
        return (loads(res.read()))
    else:
        return ("there was a conection eror")

def get_log(conn):
    conn.request("GET", "/get_log")
    res = conn.getresponse()
    if res.status==200:
        return (res.read())
    else:
        return ("there was a conection eror")
