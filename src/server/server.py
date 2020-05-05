# -*- coding: utf-8 -*-

from time import time,localtime
import sqlite3 as lite
import sys

#cur.execute("select * from people where name_last=:who and age=:age", {"who": who, "age": age})
class Server:
    def __init__(self, db_file, data_dir):
        self.db_file=db_file
        self.data_dir=data_dir
        self.conn = None
        self.permission_eror="the user isn't have permishion to do it"
        self.exists_eror="the file doesnt exists"
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
                user_name TEXT unique, user_password TEXT, groupp TEXT)''')
                self.conn.execute('''CREATE TABLE IF NOT EXISTS file_table (_id INTEGER PRIMARY KEY,name TEXT,
                creator TEXT,location_id INTEGER,type TEXT,size INTEGER,last_update INTEGER )''')
                self.conn.execute('''CREATE TABLE IF NOT EXISTS permission_table (user TEXT,
                file_id INTEGER,type INTEGER )''')#type 0 can see,1 can edit
                self.conn.commit()

    def exists(self,id):
        '''
        return if exists
        '''
        return len(self.conn.execute('''SELECT _id  from file_table WHERE _id=?''', (id,)).fetchall())==1

    def check_permission(self,user,dir_id,type=0):
        '''
        check if user have permition to a file
        '''
        creator=self.conn.execute('''SELECT _id ,creator  from file_table WHERE _id=?''', (dir_id,)).fetchone()[1]
        if type==0:
            if_user_can_see =self.conn.execute('''SELECT user,file_id,type from permission_table
            WHERE user=? and file_id =?  ''', (user,dir_id))
            if_user_can_see=if_user_can_see.fetchall()
            return (user==creator or len(if_user_can_see)!=0)
        elif type==1:
            return user==creator

    def check_type(self,id):
        x=self.conn.execute('''SELECT _id ,type  from file_table WHERE _id=?''',(id,)).fetchone()[1]
        return(x )

    def get_id(self,user,path):
        path=[user]+path.split('/')
        location_id=-1

        for dir in path:
            x=self.conn.execute('''SELECT _id ,name,location_id,type  from file_table WHERE location_id=? and name =?''',(location_id,dir)).fetchall()
            #print((location_id,dir,x))
            if len(x)!=1:
                return "the file didnt found"
            else:
                location_id=x[0][0]
        return location_id

    def print_db(self,id,space=0):
        if self.exists(id):

            this=self.conn.execute('''SELECT _id ,name,type  from file_table WHERE _id=?''',(id,))
            this=this.fetchone()
            #print(this)
            print('  '*space+str(this[0])+' '+this[1]+'   type='+str(this[2]))
            file_list=self.conn.execute('''SELECT _id ,location_id  from file_table WHERE location_id=?''',(id,)).fetchall()
            for filee in file_list:
                self.print_db(filee[0],space+1)

    def get_file_list(self,user,dir_id):
        """
        get_file_list returns a list of files in a specific directory
        argoments:
        - user - the name of the user
        - dir - the db id of the directory for which the file list is requested
        returns:
        list of file object or dir object
        """
        if self.exists(dir_id):
            permiton=self.check_permission(user,dir_id)
            if permiton:
                file_list=self.conn.execute('''SELECT name ,creator ,location_id,file_table.type,
                permission_table.type,size ,last_update FROM file_table  INNER JOIN permission_table  on
                file_table._id=permission_table.file_id WHERE location_id=? and user=?''', (dir_id,user)).fetchall()
                file_str=''
                for f in file_list:
                    file_str+=f[0]+','+f[1]+','+f[2]+','+f[4]+','+f[5]+'!'
                return file_str
            else:
                return self.permission_eror
        else :
            return self.exists_eror

    def get_file(self,user,dir_id):
        """
        get_file returns the content of a specific file
        argoments:
        - user - an object of type User
        - file_id - the db id of the file
        returns:
        ok, eror string
        """
        if self.exists(dir_id):
            can_see=self.check_permission(user,dir_id)

            if can_see:
                file_type=self.conn.execute('''SELECT _id ,type  from file_table WHERE _id=?''',(dir_id,)).fetchone()[1]
                if file_type!='file':
                    return ('ok')
                else:
                    return('eror- the file is directory ')
            else:
                return self.permission_eror
        else:
            return self.exists_eror

    def put_file(self,user,name,dir_id,Type='file'):
        """
        put_file save a file in the server
        argoments:
        - user - an object of type User, the creator of the file
        - dir - the name of the directory to place the file in
        returns:
        file id
        """
        if self.exists(dir_id):
            q=self.conn.execute('''SELECT _id ,name,location_id,type  from file_table WHERE location_id=? and name =?''',(dir_id,dir)).fetchall()
            if len(q)==0:

                x=self.conn.execute("INSERT INTO file_table (name ,creator ,location_id ,type ,size ,last_update) VALUES (?,?, ?, ?, ?,?)",(name,user,dir_id,Type,0,int(time())))

                self.conn.execute("INSERT INTO  permission_table (user,file_id ,type ) VALUES (?,?, ?)",(user,x.lastrowid,1))
                self.conn.commit()
                return x.lastrowid
            else:
                return 'there is a file in this name'
        else:
            return self.exists_eror

    def add_permition(self,user,id,read_permission):
        if self.check_permission(user,id,1):
            for man in read_permission:
                if not self.check_permission(man,id,0):
                    self.conn.execute("INSERT INTO  permission_table (user,file_id ,type ) VALUES (?,?, ?)",(man,id,0))
            self.conn.commit()
        else:return self.permission_eror
    def remove_permition(self,user,id,read_permission):
        if self.check_permission(user,id,1):
            for man in read_permission:
                self.conn.execute("DELETE from permission_table WHERE file_id=? and user=? and type=?", (id,man,0))
            self.conn.commit()
        else:return self.permission_eror
    def del_file(self,user,dir_id):
        """
        delete file
        argoments:
        - user - an object of type User
        - dir_id - the db id of the file
        returns:
        messege list of files in the deleted file  or eror string
        """

        if self.exists(dir_id):
            file_type=self.conn.execute('''SELECT _id ,type  from file_table WHERE _id=?''', (dir_id,))
            file_type=file_type.fetchone()[1]
            if self.check_permission(user,dir_id,type=1):
                #remove(self.data_dir+str(dir_id)+'.'+file_type)

                self.conn.execute("DELETE from file_table WHERE _id=?", (dir_id,))
                self.conn.commit()
                files_to_delete=[]
                if file_type=='file':
                    files_in_dir=self.conn.execute('''SELECT _id ,location_id  from file_table WHERE location_id=?''', (dir_id,)).fetchall()
                    for filee in files_in_dir:
                        files_to_delete+=self.del_file(user,filee[1])
                    return filee
                return [dir_id]
            else:
                return self.permission_eror
        else:
            return self.exists_eror

    def rename_file(self,user,dir_id,new_name):
        """
        rename the file
        argoments:
        - user - an object of type User
        - file_id - the db id of the file
        - new_name - the new name of the file
        returns:
        messege "ok" or "the user isn't have permission to do it"
        """
        if self.exists(dir_id):
            if self.check_permission(user,dir_id,type=1):

                self.conn.execute('''UPDATE file_table SET name = ? WHERE _id = ? ''',(new_name,dir_id))
                self.conn.commit()
                return 'ok'
            else:
                return self.permission_eror
        else:
            return self.exists_eror

    def replace_file(self,user,file_id,new_place):
        """
        replace the dir
        argoments:
        - user - an object of type User
        - file_id - the db id of the file
        - new_place - the new name of the dir
        returns:
        ok,eror string
        """
        if self.exists(file_id) and self.exists(new_place):
            if self.check_permission(user,file_id,type=1):
                if new_place!=file_id:
                    self.conn.execute('''UPDATE file_table SET location_id = ? WHERE _id = ? ''',(new_place,file_id))
                    self.conn.commit()
                    return 'ok'
                else:
                    return 'you cant put file in imself'
            else:
                return self.permission_eror
        else:
            return self.exists_eror
def main():
    pass

if __name__ == '__main__': main()