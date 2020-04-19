# -*- coding: utf-8 -*-
import sqlite3 as lite
from time import time,localtime
import sqlite3 as lite
import sys
from os import remove

#cur.execute("select * from people where name_last=:who and age=:age", {"who": who, "age": age})
class Server:
    def __init__(self, db_file, data_dir):
        self.db_file=db_file
        self.data_dir=data_dir
        self.conn = None
        self.permission_eror="the user isn't have permishion to do it"
        file_name=db_file
        #'C:\\Users\\yuval\\projects\\drop_box\\clients_files.db'
        try:
            self.conn = lite.connect(file_name)
        except lite.Error, e:
            print "Error %s:" % file_name
            sys.exit(1)
        finally:
            if self.conn:
                print "Opened database successfully";
                #self.cur = self.conn.cursor()
                self.conn.execute('''CREATE TABLE IF NOT EXISTS users (
                user_name TEXT unique, user_password TEXT, grouppp TEXT)''')
                self.conn.execute('''CREATE TABLE IF NOT EXISTS file_table (_id INTEGER PRIMARY KEY,name TEXT,
                creator TEXT,location_id INTEGER,type TEXT,size INTEGER,last_update INTEGER )''')
                self.conn.execute('''CREATE TABLE IF NOT EXISTS permission_table (user TEXT,
                file_id INTEGER,type INTEGER )''')#type 0 can see,1 can edit
                self.conn.commit()

    def get_file_list(self,user,dir_id):
        """
        get_file_list returns a list of files in a specific directory
        argoments:
        - user - the name of the user
        - dir - the db id of the directory for which the file list is requested
        returns:
        list of file object or dir object
        """
        #cur = self.conn.cursor()
        creator=self.conn.execute('''SELECT _id ,creator  from file_table WHERE _id=?''', (dir_id,))[0][1]
        if_user_can_see =self.conn.execute('''SELECT user_id,file_id,type from permission_table
        WHERE user_id=? and file_id =? and type=? ''', (user,dir_id,0))
        if user==creator or len(if_user_can_see)!=0:
            file_list=self.conn.execute('''SELECT name ,creator ,location_id,file_table.type,permission_table.type
             ,size ,last_update from dir_table WHERE location_id=? inner join permission_table WHERE user=? file_table._id=permission_table.file_id''', (dir_id,user))
            '''file_L=[]
            for fille in file_list:
                if user in fille[2] or fille[1]==user:
                    file_L.append(fille)'''
            return file_list
        else:
            return self.permission_eror
    def get_file(self,user,dir_id):
        """
        get_file returns the content of a specific file
        argoments:
        - user - an object of type User
        - file_id - the db id of the file
        returns:
        the content in a string
        """
        can_see=self.conn.execute('''SELECT file_id,user,from file_table WHERE file_id=? and user=? ''', (dir_id,user))
        if len(can_see)!=0:
            try:
                content_file=file(self.data_dir+str(dir_id)+'.txt','r')
            except:
                return "the server coudnt open the file"
            content=content_file.read()
            return (content)
        else:
            return self.permission_eror
    def fake_uploud(self,user,name,dir_id,read_permission):
        x=self.conn.execute("INSERT INTO file_table (name ,creator ,location_id ,type ,size ,last_update) VALUES (?,?, ?, ?, ?,?)",(name,user,dir_id,'str',0,int(time())))
        self.conn.commit()
        #print(x.lastrowid)
        #can_see=self.conn.execute('''SELECT file_id,user,from file_table WHERE file_id=? and user=? ''', (dir_id,user))
        #y=self.conn.execute('''SELECT _id,creator,last_update from file_table WHERE _id=? ''', (3,))
        #print(y)
        self.conn.execute("INSERT INTO  permission_table (user,file_id ,type ) VALUES (?,?, ?)",(user,x.lastrowid,1))
        for man in read_permission: self.conn.execute("INSERT INTO  permission_table (user,file_id ,type ) VALUES (?,?, ?)",(man,x.lastrowid,0))


    def put_file(self,user,name,dir_id,read_permission):
        """
        put_file save a file in the server
        argoments:
        - user - an object of type User, the creator of the file
        - dir - the name of the directory to place the file in
        - read_permission - list of the users that can read the file, list of type User
        returns:
        nothing
        """

        pass
    def create_dir(self,user,dir,read_permission):
        """
        create new directory in the server
        argoments:
        - user - an object of type User, the creator of the dir
        - dir - the name of the directory to place the directory in
        - read_permission - list of the users that can read the dir, list of type User
        returns:
        nothing
        """

        pass
    def del_file(self,user,dir_id):
        """
        delete file
        argoments:
        - user - an object of type User
        - dir_id - the db id of the file
        returns:
        messege "deleted" or "the user isn't have permission to do it"
        """

        location=self.cur.execute('''SELECT _id ,creator  from file_table WHERE _id=?''', (dir_id,))
        if location[0][1]==user:
            remove(self.data_dir+str(dir_id)+'.txt')
            self.con.execute("DELETE from file_table WHERE _id=?", (dir_id,))
            return "deleted"
        else:
            return self.permission_eror

    def rename_file(self,user,file_id,new_name):
        """
        rename the file
        argoments:
        - user - an object of type User
        - file_id - the db id of the file
        - new_name - the new name of the file
        returns:
        messege "ok" or "the user isn't have permission to do it"
        """
        location=self.cur.execute('''SELECT _id ,creator  from file_table WHERE _id=?''', (file_id,))
        if location[0][1]==user:
            self.cur.execute("DELETE from file_table WHERE _id=?", (file_id,))
            self.conn
            return "ok"
        else:
            return self.permission_eror

    def replace_dir(self,user,dir_id,new_name):
        """
        replace the dir
        argoments:
        - user - an object of type User
        - dir_id - the db id of the dir
        - new_name - the new name of the dir
        returns:
        nothing
        """
        pass
    def replace_file(self,user,file_id,new_name):
        """
        replace the dir
        argoments:
        - user - an object of type User
        - file_id - the db id of the file
        - new_name - the new name of the dir
        returns:
        nothing
        """
        pass
'''
class file:
    def __init__(self):pass
    pass
class User:
    def __init__(self,pasward,name,group=""):
        self.pasward=pasward
        self.name= name
        self.group = group
    def change_pasward(self,pasward,new_pasward):
        if self.pasward == pasward:
            self.pasward=new_pasward
            return "ok"
        else:
            return "incorect pasward"


'''



def main():
    """
    Add Documentation here
    """





if __name__ == '__main__':
    main()