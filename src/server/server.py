# -*- coding: utf-8 -*-

import sqlite3 as lite
import sys


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
                user_name TEXT unique, user_password TEXT)''')

                self.conn.execute('''CREATE TABLE IF NOT EXISTS file_table (_id INTEGER PRIMARY KEY,name TEXT,
                creator TEXT,location_id INTEGER,type TEXT)''')

                self.conn.execute('''CREATE TABLE IF NOT EXISTS groups (user TEXT,groupp TEXT)''')

                self.conn.execute('''CREATE TABLE IF NOT EXISTS permission_table (user TEXT,file_id INTEGER)''')

                self.conn.execute('''CREATE TABLE IF NOT EXISTS group_permission_table (groupp TEXT,
                file_id INTEGER)''')
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

        if user=='admin':
            return (True)#admin have a permition to do evrithing

        creator=self.conn.execute('''SELECT _id ,creator  from file_table WHERE _id=?''', (dir_id,)).fetchone()[1]
        if type==0:
            if_user_can_see =self.conn.execute('''SELECT user,file_id from permission_table
            WHERE user=? and file_id =?  ''', (user,dir_id))
            if_user_can_see=if_user_can_see.fetchall()
            if_group_can_see=self.conn.execute('''select groupp from groups WHERE user=? INTERSECT
             select groupp from group_permission_table WHERE file_id=? ''',(user,dir_id)).fetchall()
            return (user==creator or len(if_user_can_see)!=0 or len(if_group_can_see)!=0)

        elif type==1:
            return user==creator

    def check_type(self,id):
        x=self.conn.execute('''SELECT _id ,type  from file_table WHERE _id=?''',(id,)).fetchone()[1]
        return(x )

    def get_id(self,path):
        path=path.split('/')
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

            file_list=self.conn.execute('''SELECT name ,creator ,location_id,type
            ,size ,last_update FROM file_table  INNER JOIN permission_table  on
            file_table._id=permission_table.file_id WHERE location_id=? and user=?''', (dir_id,user)).fetchall()
            #return file_list
            file_list2=[]
            for fille in file_list:
                file_list2.append({'name':fille[0],'creator':fille[1],'type':fille[2]})
            return file_list2
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
        - user - an object of type string, the creator of the file
        - dir - the name of the directory to place the file in
        returns:
        file id
        """
        if self.exists(dir_id):
            if name!=user:


                q=self.conn.execute('''SELECT _id ,name,location_id  from file_table WHERE location_id=? and name =?''',(dir_id,name)).fetchall()
                if len(q)==0:

                    x=self.conn.execute("INSERT INTO file_table (name ,creator ,location_id ,type) VALUES (?,?, ?, ?)",(name,user,dir_id,Type))

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
                self.conn.execute("DELETE from  permission_table WHERE file_id=?", (dir_id,))
                self.conn.execute("DELETE from  group_permission_table WHERE file_id=?", (dir_id,))
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

    def who_can_see(self,file_id):
        """
        return all of the users in the input group
        """
        users=self.conn.execute('''SELECT (user_name,file_id) from permission_table WHERE file_id=?''',(file_id)).fetchall()
        users_list=[]
        for user in users:
            users_list.append(user[0])
        return(users_list)

    #====================================================user functions

    def check_pasward(self,name,pasward):
        try:
            return(self.conn.execute('''SELECT user_name,user_password  from users WHERE user_name=?''',(name,)).fetchone()[1]==pasward)
        except:return (False)

    def create_user(self,name,pasward,group=''):
        q=self.conn.execute('''SELECT user_name  from users WHERE user_name =?''',(name,)).fetchall()
        if len(q)==0 :
            if name!="admin" and name!="ADMIN":
                self.conn.execute("INSERT INTO  users (user_name, user_password ) VALUES (?,?, ?)",(name,pasward))
                self.conn.commit()
                x=self.conn.execute("INSERT INTO file_table (name ,creator ,location_id ,type) VALUES (?,?, ?, ?)",(name,name,1,'file'))
                return 'ok'
            else:
                return("the username cant be 'admin'")
        else:
            return 'there is a user in this name'
    def files_can_see(self,user):
        """
        return all of the file that the user can see and they arent his files
        """
        files=self.conn.execute('''SELECT user_name,file_id from permission_table WHERE user_name=?''',(user)).fetchall()
        file_list=[]
        for filee in files:
            file_list.append(filee[1])
        return(file_list)
    #====================================================groups functions
    def who_in_group(self,group_name):
        """
        return all of the users in the input group
        """
        users=self.conn.execute('''SELECT user_name,groupp from groups WHERE groupp=?''',(group_name)).fetchall()
        users_list=[]
        for user in users:
            users_list.append(user[0])
        return(users_list)
    def groups_user_in(self,user):
        """
        return all of the groups that the user is in them
        """
        groups=self.conn.execute('''SELECT user_name,groupp from groups WHERE user_name=?''',(user)).fetchall()
        group_list=[]
        for groupp in groups:
            group_list.append(groupp[1])
        return(group_list)


def main():pass
if __name__ == '__main__': main()