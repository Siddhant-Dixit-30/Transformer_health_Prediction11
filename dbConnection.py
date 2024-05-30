import mysql.connector as con
import mysql

db = con.connect(
        host="localhost",
        user="root",
        password="123456",
        database="db_projectml"
)

def getUserID(user,db=db):
        cur = db.cursor()
        query="SELECT usr_id FROM tbl_users where usr_email='"+user+"'"
        cur.execute(query)
        UserID=cur.fetchall()
        UserID= [i[0] for i in UserID]
        return int(UserID[0])
    
def db_login( email, password, db=db):
        cur = db.cursor()
        query="SELECT *  FROM tbl_users where usr_email='"+email+"' and usr_pass='"+password+"'"
        cur.execute(query)
        names=cur.fetchall()
        if(int(len(names))>0):
            return "yes"
        else:
             return "no"
    
def db_register(name, email, password, mobile, db=db):
        cur = db.cursor()
        query="SELECT *  FROM tbl_users where usr_email='"+email+"'"
        cur.execute(query)
        names=cur.fetchall()
        counter = 1 
        if(int(len(names))>0):
            print("User already exist..")
        else:
            query="insert into tbl_users(usr_name, usr_email, usr_mobile, usr_pass, usr_counter) values(%s,%s,%s,%s,%s)"
            value=[name, email, mobile, password, counter]
            cur.execute(query,value)
            db.commit()
            print('Inserted')
        
def block(user,db=db):
        cur = db.cursor()
        query="SELECT usr_counter FROM tbl_users where usr_email="+"'"+user+"'"
        cur.execute(query)
        names=cur.fetchall()
        names= [i[0] for i in names]
        if(int(names[0])>=3):
            return 1
        else:
             return 0

def alter_counter(user,db=db):
        cur = db.cursor()
        query="SELECT usr_counter FROM tbl_users where usr_email="+"'"+user+"'"
        cur.execute(query)
        counter=cur.fetchall()
        counter= [i[0] for i in counter]
        i = int(counter[0])
        print(i)
        i +=1
        query = "UPDATE tbl_users SET usr_counter = "+" '"+str(i)+"' "+" WHERE usr_email ="+"'"+user+"'"
        cur.execute(query)
        db.commit()        


def WritePredictedData(id,InputData,aa,religious, abusive, comparative,db=db):
        cur = db.cursor() 
        query="insert into tbl_records(userid, text, label, religious, abusive, comparative) values(%s,%s,%s,%s,%s,%s)"
        value=[id,InputData,aa,religious, abusive, comparative]
        cur.execute(query,value)
        db.commit()  


def ReadUsers(db=db):
        cur = db.cursor()
        cur.execute("SELECT * FROM tbl_users")
        data = cur.fetchall()
        db.commit()  
        return data

def ReadTweets(db=db):
        cur = db.cursor()
        cur.execute("SELECT * FROM tbl_records")
        data = cur.fetchall()
        db.commit()  
        return data



def ReadUsersTweets(username,db=db):
        cur = db.cursor()
        cur.execute("SELECT * FROM tbl_records where userid='"+username+"'")
        data = cur.fetchall()
        db.commit()  
        return data

def Activation(user,db=db):
        cur = db.cursor()
        print("1 Check")
        print(user)
        cur.execute("UPDATE tbl_users SET usr_counter = 1 WHERE usr_email ="+"'"+user+"'")
        print("2 Check")
        db.commit()  
        return "yes"
