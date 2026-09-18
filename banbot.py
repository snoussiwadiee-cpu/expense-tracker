import menu
from db import connect
from datetime import datetime,timedelta
connection,cursor= connect()
def ban(mail):
    until=(datetime.now()+timedelta(minutes=5)).isoformat()
    cursor.execute("insert into ban_list values(?,?)",(mail,until))
    connection.commit()
def unban(mail,cin):
    if isbanned(mail)==False:
        print("u are still banned ")
        #still i am going to add remaining time to get unbvan soon
        exit()
    else :
        cursor.execute("delete from ban_list where email=?",(mail,))
        connection.commit()
        menu.manage(cin)
def isbanned(mail):
    cursor.execute("select * from ban_list where email=? and banned_until<=? ", (mail, datetime.now(),))
    table = cursor.fetchone()
    return table is not None




