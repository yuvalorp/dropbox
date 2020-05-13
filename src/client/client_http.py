from json import  loads
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