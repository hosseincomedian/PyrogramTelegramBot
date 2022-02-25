from pyrogram import Client ,filters 
from pyrogram.handlers import MessageHandler,CallbackQueryHandler
import psycopg2
from psycopg2 import Error
from pyrogram.raw.functions.messages import DeleteMessages
from pyrogram.types import InlineKeyboardButton,InlineKeyboardMarkup,MessageEntity

# manage db
try:
    # Connect to an existing database
    connection = psycopg2.connect(host="", 
                                        port = 00, 
                                        database="", 
                                        user="",
                                        password="")
    # Create a cursor to perform database operations
    cursor = connection.cursor()
    # Print PostgreSQL details

except (Exception, Error) as error:
    print ('error')




api_id = 'your_api_id'
api_hash = 'your_api_hash'
token = 'bot_token'

app = Client("bot",api_id= api_id,api_hash= api_hash , bot_token=token) 

me  = [] #list_of_bot_manager

# manage messages
def dump(client, message):

        if message.chat.type == 'private':
            sender = message.from_user.id
            text = message.text
            chat_id = message.chat.id
            message_id = message.message_id
            if sender in me:
                if text == 'تبچی ها':
                    cursor.execute('select admin_id,person_id,gp_id from gp_tabchi;')
                    data = cursor.fetchall()
                    if len(data) == 0:
                        return
                    for i in data:
                        list_tab = ''
                        list_tab += "ادمین:[admin](tg://user?id={}).\n".format(i[0])
                        list_tab += "تبچی شده:[tabchi khorde](tg://user?id={}).\n".format(i[1])
                        client.send_message(chat_id=chat_id,
                                                    text=list_tab,
                                                    reply_to_message_id=message_id)
                
                elif text == 'گروه ها':
                    cursor.execute('select owner_id,gp_id from gp;')
                    data = cursor.fetchall()
                    if len(data) == 0:
                        client.send_message(chat_id=chat_id,
                                            text="گروهی وجود ندارد !!!!",
                                            reply_to_message_id=message_id)
                        return
                    
                    for i in data:
                        list_tab = ''
                        link =''
                        try:
                            link = client.get_chat(i[1]).invite_link
                        except:
                            pass
                        list_tab += "مدیر:\n[owner](tg://user?id={}).  : {}\n".format(i[0],i[0])
                        list_tab += "گروه:\n{}.\n".format(link)
                        list_tab += "ایدی گروه:\n{}.".format(i[1])
                        client.send_message(chat_id=chat_id,
                                                    text=list_tab,
                                                    reply_to_message_id=message_id)
                
                elif text[:8] == 'حذف گروه':
                    gp_id = text[9:]
                    cursor.execute('delete from gp where gp_id = {};'.format(str(gp_id)))
                    connection.commit()
                    client.send_message(chat_id=chat_id,
                                        text="گروه و همه ی اطلاعات حذف شد.",
                                        reply_to_message_id=message_id)
                
                elif text == 'کینگ ها':
                    
                    cursor.execute('select admin_id from kings;')
                    data = cursor.fetchall()
                    if len(data) == 0:
                        client.send_message(chat_id=chat_id,
                                            text="کینگی وجود ندارد !!!!",
                                            reply_to_message_id=message_id)
                        return
                    for i in data:
                        list_tab = "[king](tg://user?id={})\n".format(i[0])
                        client.send_message(chat_id=chat_id,
                                                    text=list_tab,
                                                    reply_to_message_id=message_id)
                
                elif text[:7] == 'اددکینگ':
                    data = (text.split(' '))[1]
                    cursor.execute('select admin_id from kings where admin_id = {};'.format(data))
                    data = cursor.fetchall()
                    if len(data) != 0:
                        client.send_message(chat_id=chat_id,
                                            text="کاربر کینگ است !!!!",
                                            reply_to_message_id=message_id)
                        return
                    cursor.execute('INSERT INTO kings('+
                                    'admin_id)'+
                                    'VALUES ({});'.format(str(data)))
                    connection.commit()
                
                elif text[:7] == 'حذفکینگ':
                    data = (text.split(' '))[1]
                    cursor.execute('DELETE FROM kings WHERE admin_id ={};'.format(str(data)))
                    connection.commit()
                    client.send_message(chat_id=chat_id,
                                            text=" کینگ حذف شد!!!!",
                                            reply_to_message_id=message_id)

                elif text[:8] == 'حذف تبچی' or text[:10] == 'del tabchi':
                    if text[:8] == 'حذف تبچی':
                        try:
                            person_id = int(text[9:])
                        except:
                            person_id = text[9:]
                    if text[:10] == 'del tabchi':
                        try:
                            person_id = int(text[11:])
                        except:
                            person_id = text[11:]
                    try :
                        person = client.get_chat_member(
                                    chat_id=chat_id,
                                    user_id=person_id)
                    except:
                        return
                    person_id = person.user.id
                    try:
                        cursor.execute('delete from gp_tabchi where '+    
                                        'person_id = {})'.format(person.user.id))
                        connection.commit()

                    except:
                        return
                    client.send_message(chat_id=chat_id,
                                            text="کاربر\n[{}](tg://user?id={})\nاز لیست تبچی خارج شد."
                                                    .format(person.user.first_name,person.user.id),
                                            reply_to_message_id=message_id)

                else:
                    pass

            else:
                client.send_message(chat_id=chat_id,
                                        text="کاربر\n[hossein](tg://user?id=623934098)\nادمین ربات است.",)

        if message.chat.type == 'public':
            bot_id = 1664865972
            chat_id = message.chat.id
            message_id = message.message_id
            sender = message.from_user.id 
            text = message.text
            cursor.execute('select owner_id,check_text,check_all,check_link,check_id,check_hashtag'+
                            ' from gp where gp_id = {};'.format(str(chat_id)))
            data = cursor.fetchall()

            #configBot
            if len(data) == 0:
                if sender in me:
                    if text[:9] == 'configbot':
                        admin = text[10:] 
                        try :
                            try :
                                admin_id = int(admin)
                            except:
                                admin_id = admin
                            try:
                                admin = client.get_chat_member(
                                            chat_id= chat_id,
                                            user_id= admin_id
                                        )
                                admin_id = admin.user.id
                            except:
                                return
                            cursor.execute('select gp_id from gp where gp_id ={};'
                                .format(chat_id)
                                )
                            data = cursor.fetchall()
                            if len(data) != 0:
                                client.send_message(chat_id=chat_id,
                                            text="گروه کانفیگ شده !!!!",
                                            reply_to_message_id=message_id)
                                return
                            cursor.execute('INSERT INTO gp('+
                                            'owner_id, gp_id)'+
                                                'VALUES ({},{}); '.format(admin_id, chat_id))
                            connection.commit()
                            client.send_message(chat_id=chat_id,
                                                text="گروه کانفیگ شد",
                                                reply_to_message_id=message_id)
                            return
                        except:
                            return
                return

            owner = data[0][0]
            silent_mode = data[0][1] or data[0][2]
            check_link  = data[0][3]
            check_id    = data[0][4]
            check_hashtag= data[0][5]
            admins = []
            vizirs = []
            
            #lists
            if True:
                #vip list
                cursor.execute('select owner_id from vips where gp_id ={} ;'
                                .format(chat_id)
                            )
                data = cursor.fetchall()
                vips = []
                for i in data :
                    vips.append(i[0])
                    
                #silent list
                cursor.execute('select person_id from gp_lock_user where gp_id = {};'.format(chat_id))
                data = cursor.fetchall()
                silent_list = []
                for i in data :
                    silent_list.append(i[0])
                if sender in silent_list: #silent
                    message.delete()   
                    return
                
                #vazir list
                vizirs.append(owner)
                cursor.execute('select admin_id from vizir where gp_id = {};'.format(chat_id))
                data = cursor.fetchall()
                for i in data:
                    vizirs.append(i[0])
                
                #admin list
                cursor.execute('select admin_id from gp_ad where gp_id = {};'.format(chat_id))
                data = cursor.fetchall()
                for i in data:
                    admins.append(i[0])
                cursor.execute('select admin_id from kings;')
                data = cursor.fetchall()
                kings = []
                for i in data:
                    kings.append(i[0])
                admins = admins  + vizirs           

            if sender in me:
                #king
                if text == 'کینگ' or text == 'King' or text == 'king':  ####s
                        if message.reply_to_message != None:
                                member = message.reply_to_message.from_user                            
                                if member.id in kings:
                                    client.send_message(chat_id=chat_id,
                                                        text="کاربر محترم \n[{}](tg://user?id={})\n کینگ است!!!"
                                                            .format(member.first_name,member.id),
                                                    reply_to_message_id=message_id)
                                    return
                                
                                cursor.execute('INSERT INTO kings('+
                                                    'admin_id)'+
                                                    'VALUES ({}); '.format(member.id))
                                connection.commit()
                                client.send_message(chat_id=chat_id,
                                                        text="کاربر محترم \n[{}](tg://user?id={})\n کینگ شد."
                                                            .format(member.first_name,member.id),
                                                    reply_to_message_id=message_id)
                        return

            if sender in kings or sender in me:
                #tabchi
                if True:
                    if text == 'تبچی' or text == 'tabchi':
                        if message.reply_to_message != None:
                            member = message.reply_to_message.from_user
                            if member.id in admins :
                                client.send_message(chat_id=chat_id,
                                                        text="کاربر\n[{}](tg://user?id={})\nادمین است!!!"
                                                            .format(member.first_name,member.id),
                                                    reply_to_message_id=message_id)
                                return       
                            try:
                                cursor.execute('select person_id from gp_tabchi where person_id={};'.format(member.id))
                                data = cursor.fetchall()
                                if data != 0:
                                    client.kick_chat_member(chat_id,member.id)
                                    return
                                client.kick_chat_member(chat_id,member.id)
                                cursor.execute('INSERT INTO gp_tabchi('+    
                                                'person_id, gp_id, admin_id)'+
                                                'VALUES ({},{},{}); '.format(member.id,chat_id,sender))
                                connection.commit() 

                            except:
                                return

                            client.send_message(chat_id=chat_id,
                                                    text="کاربر\n[{}](tg://user?id={})\n بن شد."
                                                    .format(member.first_name,member.id),
                                                    reply_to_message_id=message_id)
                            return
                        return
                    
                    elif text[:5] == 'تبچی ' or text[:7] == 'tabchi ':
                        if text[:5] == 'تبچی ':
                            try:
                                person_id = int(text[5:])
                            except:
                                person_id = text[5:]
                        if text[:7] == 'tabchi ':
                            try:
                                person_id = int(text[7:])
                            except:
                                person_id = text[7:]
                        try :
                            person = client.get_chat_member(
                                        chat_id=chat_id,
                                        user_id=person_id
                                    )
                        except: 
                            return
                        person_id = person.user.id
                        if person_id in admins:
                            client.send_message(chat_id=chat_id,
                                                text="کاربر\n[{}](tg://user?id={})\nکاربر ادمین است شما چنین دسترسی ای ندارید."
                                                        .format(person.user.first_name,person.user.id),
                                                reply_to_message_id=message_id)
                            return
                        try:
                            client.kick_chat_member(chat_id,person_id)
                            cursor.execute('select person_id from gp_tabchi where person_id = {};'.format(person_id))
                            data = cursor.fetchall()
                            if len(data) != 0:
                                return
                            cursor.execute('INSERT INTO gp_tabchi('+    
                                            'person_id, gp_id, admin_id)'+
                                            'VALUES ({},{},{}); '.format(person.user.id,chat_id,sender))
                            connection.commit()

                        except:
                            return
                        client.send_message(chat_id=chat_id,
                                                text="کاربر\n[{}](tg://user?id={})\nاز گروه اخراج شد."
                                                        .format(person.user.first_name,person.user.id),
                                                reply_to_message_id=message_id)
                        return

                    elif text == 'حذف تبچی' or text == 'del tabchi':
                        if message.reply_to_message != None:
                            member = message.reply_to_message.from_user
                            try:
                                cursor.execute('delete from gp_tabchi '+    
                                                'where person_id = {};'.format(member.id))
                                connection.commit() 
                            
                            except:
                                return

                            client.send_message(chat_id=chat_id,
                                            text="کاربر\n[{}](tg://user?id={})\n از لیست تبچی خارج شد."
                                                    .format(member.first_name,member.id),
                                            reply_to_message_id=message_id)
                            return
                        return

                    elif text[:8] == 'حذف تبچی' or text[:10] == 'del tabchi':
                        if text[:8] == 'حذف تبچی':
                            try:
                                person_id = int(text[9:])
                            except:
                                person_id = text[9:]
                        if text[:10] == 'del tabchi':
                            try:
                                person_id = int(text[11:])
                            except:
                                person_id = text[11:]
                        try :
                            person = client.get_chat_member(
                                        chat_id=chat_id,
                                        user_id=person_id)
                        except:
                            return
                        person_id = person.user.id
                        try:
                            cursor.execute('delete from gp_tabchi where '+    
                                            'person_id = {})'.format(person.user.id))
                            connection.commit()

                        except:
                            return
                        client.send_message(chat_id=chat_id,
                                                text="کاربر\n[{}](tg://user?id={})\nاز لیست تبچی خارج شد."
                                                        .format(person.user.first_name,person.user.id),
                                                reply_to_message_id=message_id)
                        return

            if sender in vizirs or sender in me:
                #config vazir admin        
                if sender == owner or sender in me:
                    if text == 'پیکربندی' or text == 'config' or text == 'Config':
                        admins_list='لیست ادمین ها \n '
                        for i in app.get_chat_members(chat_id, filter="administrators"):
                            if i.user.id == bot_id :
                                continue
                            else:
                                admin = client.get_chat_member(
                                                chat_id= chat_id,
                                                user_id= i.user.id
                                            )
                                admins_list +="[{}](tg://user?id={})\n".format(admin.user.first_name,admin.user.id)
                                if i.user.id in admins:
                                        continue
                                cursor.execute('INSERT INTO gp_ad('+
                                                        'admin_id, gp_id)'+
                                                        'VALUES ({},{}); '.format(i.user.id,chat_id))
                                connection.commit()
                        client.send_message(chat_id=chat_id,
                                                    text=admins_list,
                                                    reply_to_message_id=message_id)
                        return            

                    elif text == 'وزیر' or text == 'vazir' or text == 'Vazir':  ####s
                            if message.reply_to_message != None:
                                    member = message.reply_to_message.from_user                            
                                    if member.id in vizirs:
                                        client.send_message(chat_id=chat_id,
                                                            text="کاربر محترم \n[{}](tg://user?id={})\n وزیر است!!!"
                                                                .format(member.first_name,member.id),
                                                        reply_to_message_id=message_id)
                                        return

                                    cursor.execute('INSERT INTO vizir('+
                                                        'admin_id, gp_id)'+
                                                        'VALUES ({},{}); '.format(member.id,chat_id))
                                    connection.commit()
                                    client.send_message(chat_id=chat_id,
                                                            text="کاربر محترم \n[{}](tg://user?id={})\n وزیر شد."
                                                                .format(member.first_name,member.id),
                                                        reply_to_message_id=message_id)
                                    return
                            return

                    elif text[:5] == 'وزیر ' or text[:6] == 'vazir ' or text[:6] == 'Vazir ':
                        if text[:5] == 'وزیر ':
                            admin = text[5:]
                        elif text[:6] == 'vazir ' or text[:6] == 'Vazir ':
                            admin = text[6:]
                        try :
                            try:
                                admin_id = int(admin)
                            except:
                                admin_id = admin
                            try:
                                admin = client.get_chat_member(
                                            chat_id= chat_id,
                                            user_id= admin_id
                                        )
                                admin_id = admin.user.id
                            except:
                                return
                            if admin_id in vizirs:
                                client.send_message(chat_id=chat_id,
                                                    text="کاربر محترم \n[{}](tg://user?id={})\n وزیر است!!!"
                                                                .format(admin.user.first_name,admin.user.id),
                                                    reply_to_message_id=message_id)
                                return

                            cursor.execute('INSERT INTO vizir('+
                                                'admin_id, gp_id)'+
                                                'VALUES ({},{}); '.format(admin_id,chat_id))
                            connection.commit()
                            client.send_message(chat_id=chat_id,
                                                    text="کاربر محترم \n[{}](tg://user?id={})\n وزیر شد."
                                                                .format(admin.user.first_name,admin.user.id),
                                                reply_to_message_id=message_id)
                            return
                        except:
                            return

                    elif text == 'حذف وزیر' or text == 'del vazir' or text == 'Del vazir':                       
                        if message.reply_to_message != None:
                            member = message.reply_to_message.from_user
                            if member.id not in vizirs:
                                client.send_message(chat_id=chat_id,
                                                text="کاربر محترم \n[{}](tg://user?id={})\n وزیر نیست!!!"
                                                                .format(member.first_name,member.id),
                                                reply_to_message_id=message_id)
                                return
                            cursor.execute('DELETE FROM vizir'+
                                                ' WHERE admin_id = '
                                                +str(member.id)+
                                                ' AND gp_id = '
                                                +str(chat_id))
                            connection.commit()
                            client.send_message(chat_id=chat_id,
                                                    text="کاربر محترم \n[{}](tg://user?id={})\n از لیست وزیر ها حذف شد."
                                                                .format(member.first_name,member.id),
                                                reply_to_message_id=message_id)
                        return           

                    elif text[:8] == 'حذف وزیر' or text[:9] == 'del vazir' or text[:9] == 'Del vazir':    
                        if text[:8] == 'حذف وزیر':
                            admin = text[9:]
                        elif text[:9] == 'del vazir' or text[:9] == 'Del vazir':
                            admin = text[10:]
                        try :
                            admin_id = int(admin)
                        except:
                            admin_id = admin
                        try:
                            admin = client.get_chat_member(
                                        chat_id=chat_id,
                                        user_id=admin_id
                                    )
                        except:
                            return
                        admin_id = admin.user.id
                        if admin_id not in admins:
                            client.send_message(chat_id=chat_id,
                                                        text="کاربر محترم \n[{}](tg://user?id={})\n ادمین نیست!!!"
                                                            .format(admin.user.first_name,admin.user.id),
                                                            reply_to_message_id=message_id)
                            return
                        cursor.execute('DELETE FROM gp_ad'+
                                                    ' WHERE admin_id = {} AND gp_id = {}'.format(
                                                        str(admin_id),str(chat_id)))
                        connection.commit()
                        client.send_message(chat_id=chat_id,
                                                text="کاربر\n[{}](tg://user?id={})\nاز لیست ادمین ها حذف شد."
                                                            .format(admin.user.first_name,admin.user.id),
                                            reply_to_message_id=message_id)
                        return
                        
                    elif text == 'ادمین' or text == 'admin' or text == 'Admin':  ####s
                            if message.reply_to_message != None:
                                    member = message.reply_to_message.from_user                            
                                    if member.id in admins:
                                        client.send_message(chat_id=chat_id,
                                                            text="کاربر محترم \n[{}](tg://user?id={})\n ادمین است!!!"
                                                                .format(member.first_name,member.id),
                                                        reply_to_message_id=message_id)
                                        return

                                    cursor.execute('INSERT INTO gp_ad('+
                                                        'admin_id, gp_id)'+
                                                        'VALUES ({},{}); '.format(member.id,chat_id))
                                    connection.commit()
                                    client.send_message(chat_id=chat_id,
                                                            text="کاربر محترم \n[{}](tg://user?id={})\n ادمین شد."
                                                                .format(member.first_name,member.id),
                                                        reply_to_message_id=message_id)
                                    return
                            return
                            
                    elif text[:6] == 'ادمین ' or text[:6] == 'admin ' or text[:6] == 'Admin ':
                            admin = text[6:] 
                            try :
                                try:
                                    admin_id = int(admin)
                                except:
                                    admin_id = admin
                                try:
                                    admin = client.get_chat_member(
                                                chat_id= chat_id,
                                                user_id= admin_id
                                            )
                                    admin_id = admin.user.id
                                except:
                                    return
                                if admin_id in admins:
                                    client.send_message(chat_id=chat_id,
                                                        text="کاربر محترم \n[{}](tg://user?id={})\n ادمین است!!!"
                                                                    .format(admin.user.first_name,admin.user.id),
                                                        reply_to_message_id=message_id)
                                    return

                                cursor.execute('INSERT INTO gp_ad('+
                                                    'admin_id, gp_id)'+
                                                    'VALUES ({},{}); '.format(admin_id,chat_id))
                                connection.commit()
                                client.send_message(chat_id=chat_id,
                                                        text="کاربر محترم \n[{}](tg://user?id={})\n ادمین شد."
                                                                    .format(admin.user.first_name,admin.user.id),
                                                    reply_to_message_id=message_id)
                                return
                            except:
                                return
                        
                    elif text == 'حذف ادمین' or text == 'del admin' or text == 'Del admin':           
                        if message.reply_to_message != None:
                            member = message.reply_to_message.from_user
                            if member.id not in admins:
                                client.send_message(chat_id=chat_id,
                                                text="کاربر محترم \n[{}](tg://user?id={})\n ادمین نیست!!!"
                                                                .format(member.first_name,member.id),
                                                reply_to_message_id=message_id)
                                return
                            cursor.execute('DELETE FROM gp_ad'+
                                                ' WHERE admin_id = '
                                                +str(member.id)+
                                                ' AND gp_id = '
                                                +str(chat_id))
                            connection.commit()
                            client.send_message(chat_id=chat_id,
                                                    text="کاربر محترم \n[{}](tg://user?id={})\n از لیست ادمین ها حذف شد."
                                                                .format(member.first_name,member.id),
                                                reply_to_message_id=message_id)
                        return            

                    elif text[:9] == 'حذف ادمین' or text[:9] == 'del admin' or text[:9] == 'Del admin':
                        admin = text[10:]
                        try :
                            admin_id = int(admin)
                        except:
                            admin_id = admin
                        try:
                            admin = client.get_chat_member(
                                        chat_id=chat_id,
                                        user_id=admin_id
                                    )
                        except:
                            return
                        admin_id = admin.user.id
                        if admin_id not in admins:
                            client.send_message(chat_id=chat_id,
                                                        text="کاربر محترم \n[{}](tg://user?id={})\n ادمین نیست!!!"
                                                            .format(admin.user.first_name,admin.user.id),
                                                            reply_to_message_id=message_id)
                            return
                        cursor.execute('DELETE FROM gp_ad'+
                                                    ' WHERE admin_id = {} AND gp_id = {}'.format(
                                                        str(admin_id),str(chat_id)))
                        connection.commit()
                        client.send_message(chat_id=chat_id,
                                                text="کاربر\n[{}](tg://user?id={})\nاز لیست ادمین ها حذف شد."
                                                            .format(admin.user.first_name,admin.user.id),
                                            reply_to_message_id=message_id)
                        return

            if sender in admins or sender in me:  

                if text == 'پین' or text == 'pin' or text == 'Pin':
                    if message.reply_to_message != None:
                        pin_message = message.reply_to_message.message_id
                        client.pin_chat_message(
                                    chat_id=chat_id,
                                    message_id=pin_message
                                )    
                    return                            

                elif text == 'حذف پین' or text == 'unpin' or text == 'Unpin':
                    if message.reply_to_message != None:
                        pin_message = message.reply_to_message.message_id
                        client.unpin_chat_message(
                                    chat_id=chat_id,
                                    message_id=pin_message
                                )  
                    return                              

                elif text == 'لیست ادمین' or text=='admin list' or text=='Admin list':
                    admins_list = 'لیست ادمین ها:\n'
                    if len(admins) == 0:
                        client.send_message(chat_id=chat_id,
                                                text='لیست ادمین ها خالی است.',
                                                reply_to_message_id=message_id)
                        return
                    for i in admins:
                        try:
                            admin = client.get_chat_member(
                                                chat_id= chat_id,
                                                user_id= i
                                            )
                        except:
                            continue
                        admins_list +="[{}](tg://user?id={})\n".format(admin.user.first_name,admin.user.id)
                    client.send_message(chat_id=chat_id,
                                                text=admins_list,
                                                reply_to_message_id=message_id)
                    return

                elif text == 'لیست سکوت' or text=='silent list' or text=='Silent list':
                    admins_list = 'لیست سکوت :\n'
                    if len(silent_list) == 0:
                        client.send_message(chat_id=chat_id,
                                                text='لیست سکوت خالی است.',
                                                reply_to_message_id=message_id)
                        return
                    for i in silent_list:
                        try:
                            admin = client.get_chat_member(
                                                chat_id= chat_id,
                                                user_id= i
                                            )
                        except:
                            continue
                        admins_list +="[{}](tg://user?id={})\n".format(admin.user.first_name,admin.user.id)
                    client.send_message(chat_id=chat_id,
                                                text=admins_list,
                                                reply_to_message_id=message_id)
                    return

                elif text == 'لیست ویژه' or text=='vip list' or text=='Vip list':
                    admins_list = 'لیست ویژه :\n' 
                    if len(vips) == 0:
                        client.send_message(chat_id=chat_id,
                                                text='لیست ویژه خالی است.',
                                                reply_to_message_id=message_id)
                        return
                    for i in vips:
                        try:
                            admin = client.get_chat_member(
                                                chat_id= chat_id,
                                                user_id= i
                                            )
                        except:
                            continue
                        admins_list +="[{}](tg://user?id={})\n".format(admin.user.first_name,admin.user.id)
                    client.send_message(chat_id=chat_id,
                                                text=admins_list,
                                                reply_to_message_id=message_id)
                    return

                elif text == 'لیست وزیران' or text=='vazir list' or text=='Vazir list':
                        vizirs_list = 'لیست وزرا:\n'
                        if len(vizirs) == 0:
                            client.send_message(chat_id=chat_id,
                                                    text='لیست وزرا خالی است.',
                                                    reply_to_message_id=message_id)
                        for i in vizirs:
                            try:
                                admin = client.get_chat_member(
                                                    chat_id= chat_id,
                                                    user_id= i
                                                )
                            except:
                                continue
                            vizirs_list +="[{}](tg://user?id={})\n".format(admin.user.first_name,admin.user.id)
                        client.send_message(chat_id=chat_id,
                                                    text=vizirs_list,
                                                    reply_to_message_id=message_id)
                        return

                elif text == 'رباط' or text == 'bot' or text == 'Bot':
                    client.send_message(chat_id=chat_id,
                                                    text="در خدمتم...",
                                                reply_to_message_id=message_id)
                    
                elif text == 'قفل متن' or text == 'loc text' or text == 'Loc text':
                    cursor.execute('UPDATE gp '+
                                                ' SET check_text=%s '+
                                                ' WHERE gp_id = %s; ',('t',chat_id))
                    connection.commit()
                    client.send_message(chat_id=chat_id,
                                                    text="قفل متن گروه فعال شد.",
                                                reply_to_message_id=message_id)
                    return                            

                elif text == 'حذف قفل متن' or text == 'unloc text' or text == 'Unloc text':
                    cursor.execute('UPDATE gp '+
                                                ' SET check_text=%s '+
                                                ' WHERE gp_id = %s; ',('f',chat_id))
                    connection.commit()
                    client.send_message(chat_id=chat_id,
                                                    text="قفل متن گروه غیر فعال شد.",
                                                reply_to_message_id=message_id)
                    return

                elif text == 'قفل ویس' or text == 'loc voice' or text == 'Loc voice':
                    cursor.execute('UPDATE gp '+
                                                ' SET check_voice=%s '+
                                                ' WHERE gp_id = %s; ',('t',chat_id))
                    connection.commit()
                    client.send_message(chat_id=chat_id,
                                                    text="قفل ویس گروه فعال شد.",
                                                reply_to_message_id=message_id)
                    return                            
                
                elif text == 'حذف قفل ویس' or text == 'unloc voice' or text == 'Unloc voice':
                    cursor.execute('UPDATE gp '+
                                                ' SET check_voice=%s '+
                                                ' WHERE gp_id = %s; ',('f',chat_id))
                    connection.commit()
                    client.send_message(chat_id=chat_id,
                                                    text="قفل ویس گروه غیر فعال شد.",
                                                reply_to_message_id=message_id)
                    return

                elif text == 'قفل گیف' or text == 'loc gif' or text == 'Loc gif':
                    cursor.execute('UPDATE gp '+
                                                ' SET check_gif=%s '+
                                                ' WHERE gp_id = %s; ',('t',chat_id))
                    connection.commit()
                    client.send_message(chat_id=chat_id,
                                                    text="قفل گیف گروه فعال شد.",
                                                reply_to_message_id=message_id)
                    return                            

                elif text == 'حذف قفل گیف' or text == 'unloc gif' or text == 'Unloc gif':
                    cursor.execute('UPDATE gp '+
                                                ' SET check_gif=%s '+
                                                ' WHERE gp_id = %s; ',('f',chat_id))
                    connection.commit()
                    client.send_message(chat_id=chat_id,
                                                text="قفل گیف گروه غیر فعال شد.",
                                                reply_to_message_id=message_id)
                    return

                elif text == 'قفل گروه' or text == 'loc gp' or text == 'Loc gp':
                    cursor.execute('UPDATE gp '+
                                                ' SET check_all=%s '+
                                                ' WHERE gp_id = %s; ',('t',chat_id))
                    connection.commit()
                    client.send_message(chat_id=chat_id,
                                                    text="قفل گروه فعال شد.",
                                                reply_to_message_id=message_id)
                    return                            

                elif text == 'حذف قفل گروه' or text == 'unloc gp' or text == 'Unloc gp': 
                    cursor.execute('UPDATE gp '+
                                                ' SET check_all=%s '+
                                                ' WHERE gp_id = %s; ',('t',chat_id))
                    connection.commit()
                    client.send_message(chat_id=chat_id,
                                                    text="قفل ویدئو گروه فعال شد.",
                                                reply_to_message_id=message_id)
                    return 

                elif text == 'قفل فیلم' or text == 'loc video' or text == 'Loc video':
                    cursor.execute('UPDATE gp '+
                                                ' SET check_video=%s '+
                                                ' WHERE gp_id = %s; ',('t',chat_id))
                    connection.commit()
                    client.send_message(chat_id=chat_id,
                                                    text="قفل ویدئو گروه فعال شد.",
                                                reply_to_message_id=message_id)
                    return                            

                elif text == 'حذف قفل فیلم' or text == 'unloc video' or text == 'Unloc video':
                    cursor.execute('UPDATE gp '+
                                                ' SET check_video=%s '+
                                                ' WHERE gp_id = %s; ',('f',chat_id))
                    connection.commit()
                    client.send_message(chat_id=chat_id,
                                                    text="قفل ویدئو گروه غیر فعال شد.",
                                                reply_to_message_id=message_id)
                    return

                elif text == 'قفل استیکر' or text == 'loc sticker' or text == 'Loc sticker':
                    cursor.execute('UPDATE gp '+
                                                ' SET check_stick=%s '+
                                                ' WHERE gp_id = %s; ',('t',chat_id))
                    connection.commit()
                    client.send_message(chat_id=chat_id,
                                                    text="قفل استیگر گروه فعال شد.",
                                                reply_to_message_id=message_id)
                    return                            

                elif text == 'حذف قفل استیکر' or text == 'unloc sticker' or text == 'Unloc sticker':
                    cursor.execute('UPDATE gp '+
                                                ' SET check_stick=%s '+
                                                ' WHERE gp_id = %s; ',('f',chat_id))
                    connection.commit()
                    client.send_message(chat_id=chat_id,
                                                    text="قفل استیکر گروه غیر فعال شد.",
                                                reply_to_message_id=message_id)
                    return

                elif text == 'قفل لینک' or text == 'loc link' or text == 'Loc link':
                    cursor.execute('UPDATE gp '+
                                                ' SET check_link=%s '+
                                                ' WHERE gp_id = %s; ',('t',chat_id))
                    connection.commit()
                    client.send_message(chat_id=chat_id,
                                                    text="قفل لینک گروه فعال شد.",
                                                reply_to_message_id=message_id)
                    return                            

                elif text == 'حذف قفل لینک' or text == 'unloc link' or text == 'Unloc link':
                    cursor.execute('UPDATE gp '+
                                                ' SET check_link=%s '+
                                                ' WHERE gp_id = %s; ',('f',chat_id))
                    connection.commit()
                    client.send_message(chat_id=chat_id,
                                                    text="قفل لینک گروه غیر فعال شد.",
                                                reply_to_message_id=message_id)
                    return

                elif text == 'قفل ایدی' or text == 'loc id' or text == 'Loc id':
                    cursor.execute('UPDATE gp '+
                                                ' SET check_id=%s '+
                                                ' WHERE gp_id = %s; ',('t',chat_id))
                    connection.commit()
                    client.send_message(chat_id=chat_id,
                                                    text="قفل ایدی گروه فعال شد.",
                                                reply_to_message_id=message_id)
                    return                            

                elif text == 'حذف قفل ایدی' or text == 'unloc id' or text == 'Unloc id':
                    cursor.execute('UPDATE gp '+
                                                ' SET check_id=%s '+
                                                ' WHERE gp_id = %s; ',('f',chat_id))
                    connection.commit()
                    client.send_message(chat_id=chat_id,
                                                    text="قفل ایدی گروه غیر فعال شد.",
                                                reply_to_message_id=message_id)
                    return

                elif text == 'قفل عکس' or text == 'loc photo' or text == 'Loc photo':
                    cursor.execute('UPDATE gp '+
                                                ' SET check_photo=%s '+
                                                ' WHERE gp_id = %s; ',('t',chat_id))
                    connection.commit()
                    client.send_message(chat_id=chat_id,
                                                    text="قفل عکس گروه فعال شد.",
                                                reply_to_message_id=message_id)
                    return                            

                elif text == 'حذف قفل عکس' or text == 'unloc photo' or text == 'Unloc photo':
                    cursor.execute('UPDATE gp '+
                                                ' SET check_photo=%s '+
                                                ' WHERE gp_id = %s; ',('f',chat_id))
                    connection.commit()
                    client.send_message(chat_id=chat_id,
                                                    text="قفل عکس گروه غیر فعال شد.",
                                                reply_to_message_id=message_id)
                    return

                elif text == 'قفل هشتگ' or text == 'loc hashtag' or text == 'Loc hashtag':
                    cursor.execute('UPDATE gp '+
                                                ' SET check_hashtag=%s '+
                                                ' WHERE gp_id = %s; ',('t',chat_id))
                    connection.commit()
                    client.send_message(chat_id=chat_id,
                                                    text="قفل هشتگ گروه فعال شد.",
                                                reply_to_message_id=message_id)
                    return                            

                elif text == 'حذف قفل هشتگ' or text == 'unloc hashtag' or text == 'Unloc hashtag':
                    cursor.execute('UPDATE gp '+
                                                ' SET check_hashtag=%s '+
                                                ' WHERE gp_id = %s; ',('f',chat_id))
                    connection.commit()
                    client.send_message(chat_id=chat_id,
                                                    text="قفل هشتگ گروه غیر فعال شد.",
                                                reply_to_message_id=message_id)
                    return

                elif text == 'پاکسازی تبچی' or text == 'del tabchi' or text == 'Del tabchi':
                    try:
                        cursor.execute('select person_id from gp_tabchi')
                        data = cursor.fetchall()
                        tabchi = []
                        for i in data:
                            tabchi.append(i[0])
                        for i in tabchi:
                            try:
                                client.kick_chat_member(chat_id,i)
                            except:
                                pass
                        client.send_message(chat_id=chat_id,
                                        text="پاکسازی انجام شد.",
                                            reply_to_message_id=message_id)
                        return
                    except:
                        return

                elif text[:9] == 'قفل کلمه ' or text[:9] == 'loc word ' or text[:9] == 'Loc word ':
                    word = text[9:]
                    if len(word)>=15:
                        return
                    cursor.execute('select gp_id,word from gp_lock_word where gp_id = %s AND word = %s'
                                                                    ,(chat_id, word))
                    data = cursor.fetchall()
                    if len(data) != 0:
                        client.send_message(chat_id=chat_id,
                                            text="کلمه فیلتر است!!!!",
                                                reply_to_message_id=message_id)
                        return
                    cursor.execute(' INSERT INTO gp_lock_word('+
                                    'word, gp_id)'+
                                    'VALUES (%s,%s)',(str(word), str(chat_id)))
                    connection.commit()
                    client.send_message(chat_id=chat_id,
                                            text=".کلمه فیلتر شد",
                                                reply_to_message_id=message_id)          
                    return

                elif text[:12] == 'بازکردن کلمه' or  text[:10] == 'unloc word' or  text[:10] == 'Unloc word':  
                    if text[0:12] == 'بازکردن کلمه':
                        word = text[13:]
                    else:
                        word = text[11:]
                    cursor.execute('select gp_id,word from gp_lock_word where gp_id = %s'+
                                                ' AND word = %s',(str(chat_id), str(word)))
                    data = cursor.fetchall()
                    if len(data) == 0:
                        client.send_message(chat_id=chat_id,
                                            text="کلمه فیلتر نیست!!!!",
                                                reply_to_message_id=message_id)
                        return
                        

                    cursor.execute(' DELETE FROM public.gp_lock_word'+
                                    ' WHERE gp_id = %s AND word = %s ',(str(chat_id), str(word)))
                    connection.commit()
                    client.send_message(chat_id=chat_id,
                                            text=".فیلتر کلمه آزاد شد",
                                                reply_to_message_id=message_id)          
                    return

                elif text == 'حذف سکوت' or text == 'unmute' or text == 'Unmute':
                    if message.reply_to_message != None:
                            member = message.reply_to_message.from_user
                            cursor.execute('select person_id from gp_lock_user where gp_id = {} AND person_id = {}'
                                                        .format(str(chat_id), 
                                                        str(member.id)))
                            data = cursor.fetchall()
                            if len(data) == 0:
                                client.send_message(chat_id=chat_id,
                                                    text="کاربر  \n[{}](tg://user?id={})\n در لیست سکوت نیست!!!"
                                                                .format(member.first_name,member.id),
                                                reply_to_message_id=message_id)
                                return
                            cursor.execute('DELETE FROM gp_lock_user'+
                                                ' WHERE person_id = {} AND gp_id = {}'
                                                .format(member.id,chat_id))
                            connection.commit()
                            client.send_message(chat_id=chat_id,
                                                text="کاربر  \n[{}](tg://user?id={})\n از لیست سکوت حذف و آزاد شد."
                                                                .format(member.first_name,member.id),
                                                reply_to_message_id=message_id)
                            return
                    return      

                elif text[:8] == 'حذف سکوت' or text[:5] == 'umute' or text[:5] == 'Umute':
                    if text[:8] == 'حذف سکوت':
                        member = text[9:]
                    elif text[:5] == 'umute' or text[:5] == 'Umute':
                        member = text[6:]
                    try:
                        person_id = int(member)
                    except:
                        person_id = member
                    try:
                        member = client.get_chat_member(
                                    chat_id=chat_id,
                                    user_id=person_id
                                )
                        person_id = member.user.id
                    except:
                        return
                    cursor.execute('select * FROM gp_lock_user'+
                                                ' WHERE person_id = {} AND gp_id = {}'.format(
                                                    str(member.user.id),str(chat_id)))

                    data = cursor.fetchall()
                    if(len(data) == 0):
                        client.send_message(chat_id=chat_id,
                                            text="کاربر\n[{}](tg://user?id={})\nدر لیست سکوت نیست!!!"
                                                        .format(member.user.first_name,member.user.id),
                                        reply_to_message_id=message_id)
                        return
                    cursor.execute('DELETE FROM gp_lock_user'+
                                    ' WHERE person_id = {} AND gp_id = {}'.format(
                                        str(person_id),str(chat_id)))
                    connection.commit()
                    client.send_message(chat_id=chat_id,
                                        text="کاربر\n[{}](tg://user?id={})\از لیست سکوت حذف شد."
                                                        .format(member.user.first_name,member.user.id),
                                        reply_to_message_id=message_id)
                    return

                elif text == 'سکوت' or text == 'mute' or text == 'Mute':
                    if message.reply_to_message != None:
                            member = message.reply_to_message.from_user
                            if member.id in admins :
                                client.send_message(chat_id=chat_id,
                                                    text="کاربر\n[{}](tg://user?id={})\nادمین است."
                                                        .format(member.first_name,member.id),
                                                reply_to_message_id=message_id)
                                return

                            cursor.execute('select person_id from gp_lock_user where gp_id = {} AND person_id = {}'
                                                            .format(str(chat_id), 
                                                            str(member.id)))
                            data = cursor.fetchall()              
                            if len(data) != 0:
                                client.send_message(chat_id=chat_id,
                                                text="کاربر\n[{}](tg://user?id={})\nدر لیست سکوت قرار دارد!!!"
                                                        .format(member.first_name,member.id),
                                                reply_to_message_id=message_id)
                                return
                            cursor.execute('INSERT INTO gp_lock_user('+
                                                'person_id, gp_id)'+
                                                'VALUES ({},{}); '.format(member.id,chat_id))
                            connection.commit()
                            client.send_message(chat_id=chat_id,
                                                    text="کاربر\n[{}](tg://user?id={})\nدر لیست سکوت قرار گرفت."
                                                        .format(member.first_name,member.id),
                                                reply_to_message_id=message_id)
                            return
                    return

                elif text[:4] == 'سکوت' or text[:4] == 'mute' or text[:4] == 'Mute':
                    admin = text[5:]
                    if len (admin) == 0:
                        return
                    try :
                        person_id = int(admin)
                    except:
                        person_id = admin
                    try:    
                        person = client.get_chat_member(
                                    chat_id=chat_id,
                                    user_id=person_id
                                )
                        person_id = person.user.id
                    except:
                        return
                    if person_id in admins:
                        client.send_message(chat_id=chat_id,
                                            text="کاربر\n[{}](tg://user?id={})\nادمین است!!!"
                                                    .format(person.user.first_name,person.user.id),
                                            reply_to_message_id=message_id)
                        return
                    cursor.execute('select person_id from gp_lock_user where gp_id = {} AND person_id = {}'
                                                            .format(str(chat_id), 
                                                            str(person_id)))
                    data = cursor.fetchall()              
                    if len(data) != 0:
                        client.send_message(chat_id=chat_id,
                                        text="کاربر\n[{}](tg://user?id={})\nدر لیست سکوت قرار دارد!!!"
                                                .format(person.user.first_name,person_id),
                                        reply_to_message_id=message_id)
                        return
                    cursor.execute('INSERT INTO gp_lock_user('+
                                            'person_id, gp_id)'+
                                            'VALUES ({},{}); '.format(person.user.id,chat_id))
                    connection.commit()
                    client.send_message(chat_id=chat_id,
                                        text="کاربر {} در لیست سکوت قرار گرفت."
                                                .format(person.user.first_name),
                                        reply_to_message_id=message_id)
                    return

                elif text == 'بن' or text == 'ban' or text == 'Ban':
                    if message.reply_to_message != None:
                        member = message.reply_to_message.from_user
                        if member.id in admins :
                            client.send_message(chat_id=chat_id,
                                                    text="کاربر\n[{}](tg://user?id={})\nادمین است!!!"
                                                        .format(member.first_name,member.id),
                                                reply_to_message_id=message_id)
                            return
                        try:
                            client.kick_chat_member(chat_id,member.id)
                        except:
                            return

                        client.send_message(chat_id=chat_id,
                                        text="کاربر\n[{}](tg://user?id={})\n بن شد."
                                                .format(member.first_name,member.id),
                                        reply_to_message_id=message_id)
                        return

                elif text[:3] == 'بن ' or text[:4] == 'ban ' or text[:4] == 'Ban ':
                    if text[0:3] == 'بن ':
                        try:
                            person_id = int(text[3:])
                        except:
                            person_id = text[3:]
                    if text[0:4] == 'ban ' or text[:4] == 'Ban ':
                        try:
                            person_id = int(text[4:])
                        except:
                            person_id = text[4:]
                    try :
                        person = client.get_chat_member(
                                    chat_id=chat_id,
                                    user_id=person_id
                                )
                    except:
                        return
                    person_id = person.user.id
                    if person_id in admins:
                        client.send_message(chat_id=chat_id,
                                            text="کاربر\n[{}](tg://user?id={})\nکاربر ادمین است شما چنین دسترسی ای ندارید."
                                                    .format(person.user.first_name,person.user.id),
                                            reply_to_message_id=message_id)
                        return
                    try:
                        client.kick_chat_member(chat_id,person_id)
                    except:
                        return
                    client.send_message(chat_id=chat_id,
                                            text="کاربر\n[{}](tg://user?id={})\nاز گروه اخراج شد."
                                                    .format(person.user.first_name,person.user.id),
                                            reply_to_message_id=message_id)

                elif text == 'اخطار' or text == 'warn' or text == 'Warn':
                    if message.reply_to_message != None:
                        member = message.reply_to_message.from_user
                        if member.id in admins :
                            client.send_message(chat_id=chat_id,
                                                text="کاربر\n[{}](tg://user?id={})\nکاربر ادمین است شما چنین دسترسی ای ندارید."
                                                    .format(member.first_name,member.id),
                                                reply_to_message_id=message_id)
                            return
                        cursor.execute('select count from warning_member where gp_id = {} AND person_id = {}'
                                                        .format(str(chat_id), 
                                                        str(member.id)))
                        data = (cursor.fetchall())
                        if len (data) == 0:
                            cursor.execute('INSERT INTO warning_member('+
                                            'person_id, gp_id, count)'+
                                            'VALUES ({},{},{}); '.format(member.id,chat_id,1))
                            connection.commit()
                            client.send_message(chat_id=chat_id,
                                                text="تعداد 1|3 اخطار برای کاربر: \n[{}](tg://user?id={})\n ثبت شد."
                                                    .format(member.first_name,member.id),
                                                reply_to_message_id=message_id)
                            return
                                                
                        count = int(data[0][0])
                        if count == 2:
                            cursor.execute(' delete from'+
                                            ' warning_member'+
                                            ' WHERE person_id = %s and gp_id = %s; ',
                                            (member.id,chat_id))
                            connection.commit()
                            try:
                                client.kick_chat_member(chat_id,member.id)
                            except:
                                return
                            client.send_message(chat_id,'تعداد اخطار 3|3 \n کاربر {} از گروه حذف شد.'.format(
                                                                    member.first_name))
                            return
                                                            
                        if count < 2:
                            cursor.execute(' UPDATE warning_member'+
                                            ' SET count = %s'+
                                            ' WHERE person_id = %s and gp_id = %s; ',
                                            (count+1,member.id,chat_id))
                            connection.commit()
                            client.send_message(chat_id,'تعداد  {}|3 اخطار برای کاربر :\n [{}](tg://user?id={}) \n ثبت شد.'
                                                                .format(count+1,member.first_name,member.id),
                                                                reply_to_message_id=message_id)
                        return

                elif text[:6] == 'اخطار ' or text[:5] == 'warn ' or text[:5] == 'Warn ': 
                    if text[:5] == 'اخطار':
                        try:
                            person_id = int(text[6:])
                        except:
                            person_id = text[6:]
                    if text[:5] == 'warn ' or text[:5] == 'Warn ':
                        try:
                            person_id = int(text[5:])
                        except:
                            person_id = text[5:]
                    try:
                        person = client.get_chat_member(
                                chat_id=chat_id,
                                user_id=person_id
                            )
                    except:
                        return
                    person_id = person.user.id
                    if person_id in admins :
                        client.send_message(chat_id=chat_id,
                                            text="کاربر\n[{}](tg://user?id={})\nکاربر ادمین است شما چنین دسترسی ای ندارید."
                                                    .format(person.user.first_name,person.user.id),
                                            reply_to_message_id=message_id)
                        return
                    cursor.execute('select count from warning_member where gp_id = {} AND person_id = {}'
                                                    .format(str(chat_id), 
                                                    str(person.user.id)))
                    data = (cursor.fetchall())
                    if len (data) == 0:
                        cursor.execute('INSERT INTO warning_member('+
                                        'person_id, gp_id, count)'+
                                        'VALUES ({},{},{}); '.format(person.user.id,chat_id,1))
                        connection.commit()
                        client.send_message(chat_id=chat_id,
                                            text="تعداد 1|3 اخطار برای کاربر: \n[{}](tg://user?id={})\n ثبت شد."
                                                .format(person.user.first_name,person.user.id),
                                            reply_to_message_id=message_id)
                        client.send_message(chat_id=chat_id,
                                            text="کاربر\n[{}](tg://user?id={})\ ادمین است شما چنین دسترسی ای ندارید."
                                                    .format(person.user.first_name,person.user.id),
                                            reply_to_message_id=message_id)
                        return
                                            
                    count = int(data[0][0])
                    if count == 2:
                        try:
                            cursor.execute(' delete from'+
                                            ' warning_member'+
                                            ' WHERE person_id = %s and gp_id = %s; ',
                                            (person.user.id,chat_id))
                            connection.commit()
                            client.kick_chat_member(chat_id,person.user.id)
                        except:
                            return
                        client.send_message(chat_id,'تعداد اخطار 3|3  کاربر \n[{}](tg://user?id={})\n از گروه حذف شد.'
                                                        .format(person.user.first_name,person.user.id),)
                        return
                                                                                                    
                    if count < 2:
                        cursor.execute(' UPDATE warning_member'+
                                            ' SET count = %s'+
                                            ' WHERE person_id = %s and gp_id = %s; ',
                                            (count+1,person.user.id,chat_id))
                        connection.commit()
                        client.send_message(chat_id,'کاربر \n[{}](tg://user?id={})\n {}|3 اخطار دریافت کرده.'.format(
                                                                person.user.first_name,person.user.id, count+1))                            
                    return

                elif text == 'حذف اخطار' or text == 'del warn' or text == 'Del warn':
                    if message.reply_to_message != None:
                        member = message.reply_to_message.from_user                                               
                        cursor.execute(' delete from'+
                                        ' warning_member'+
                                        ' WHERE person_id = %s and gp_id = %s; ',
                                        (member.id,chat_id))
                        connection.commit()
                        client.send_message(chat_id=chat_id,
                                            text="اخطار های کاربر\n[{}](tg://user?id={})\n حذف شد."
                                                    .format(member.first_name,member.id),
                                            reply_to_message_id=message_id)
                        return        

                elif text[:9] == 'حذف اخطار' or text[:8] == 'del warn' or text[:8] == 'Del warn':
                    if text[0:9] == 'حذف اخطار':
                        try:
                            person_id = int(text[10:])
                        except:
                            person_id = text[10:]
                    if text[0:8] == 'del warn' or text[:8] == 'Del warn':
                        try:
                            person_id = int(text[9:])
                        except:
                            person_id = text[9:]
                    try:
                        person = client.get_chat_member(
                                chat_id=chat_id,
                                user_id=person_id
                            )
                    except:

                        return
                    cursor.execute(' delete from'+
                                            ' warning_member'+
                                            ' WHERE person_id = %s and gp_id = %s; ',
                                            (person.user.id,chat_id))
                    client.send_message(chat_id,'اخطار های کاربر \n[{}](tg://user?id={})\n  حذف شد.'.format(
                                                                person.user.first_name,person.user.id))                            
                
                    connection.commit()

                elif text == 'ویژه' or text == 'vip' or text == 'Vip':
                    if message.reply_to_message != None:
                            member = message.reply_to_message.from_user
                            if member.id in admins :
                                client.send_message(chat_id=chat_id,
                                                    text="کاربر\n[{}](tg://user?id={})\nادمین است."
                                                        .format(member.first_name,member.id),
                                                reply_to_message_id=message_id)
                                return
                            cursor.execute('select person_id from gp_vip where gp_id = {} AND person_id = {}'
                                                            .format(str(chat_id), 
                                                            str(member.id)))
                            data = cursor.fetchall()              
                            if len(data) != 0:
                                client.send_message(chat_id=chat_id,
                                                text="کاربر\n[{}](tg://user?id={})\nدر لیست ویژه قرار دارد!!!"
                                                        .format(member.first_name,member.id),
                                                reply_to_message_id=message_id)
                                return
                            cursor.execute('INSERT INTO gp_vip('+
                                                'person_id, gp_id)'+
                                                'VALUES ({},{}); '.format(member.id,chat_id))
                            connection.commit()
                            client.send_message(chat_id=chat_id,
                                                    text="کاربر\n[{}](tg://user?id={})\nدر لیست ویژه قرار گرفت."
                                                        .format(member.first_name,member.id),
                                                reply_to_message_id=message_id)
                            return
                    return

                elif text[:5] == 'ویژه ' or text[:4] == 'vip ' or text[:4] == 'Vip ':
                    if text[:4] == 'ویژه':   
                        admin = text[5:]
                    if text[:3] == 'vip' or text[:4] == 'Vip ':
                        admin = text[4:]
                    try :
                        person_id = int(admin)
                    except:
                        person_id = admin
                    try:
                        person = client.get_chat_member(
                                    chat_id=chat_id,
                                    user_id=person_id
                                )
                        member = person.user
                    except:
                        return
                    if person_id in admins:
                        client.send_message(chat_id=chat_id,
                                            text="کاربر\n[{}](tg://user?id={})\nادمین است!!!"
                                                    .format(person.user.first_name,person.user.id),
                                            reply_to_message_id=message_id)
                        return
                    cursor.execute('select person_id from gp_vip where gp_id = {} AND person_id = {}'
                                                            .format(str(chat_id), 
                                                            str(person.user.id)))
                    data = cursor.fetchall()              
                    if len(data) != 0:
                        client.send_message(chat_id=chat_id,
                                        text="کاربر\n[{}](tg://user?id={})\nدر لیست ویژه قرار دارد!!!"
                                                .format(member.first_name,member.id),
                                        reply_to_message_id=message_id)
                        return
                    cursor.execute('INSERT INTO gp_vip('+
                                            'person_id, gp_id)'+
                                            'VALUES ({},{}); '.format(person.user.id,chat_id))
                    connection.commit()
                    client.send_message(chat_id=chat_id,
                                                    text="کاربر\n[{}](tg://user?id={})\nدر لیست ویژه قرار گرفت."
                                                        .format(member.first_name,member.id),
                                                reply_to_message_id=message_id)
                    return            

                elif text == 'حذف ویژه' or text == 'del vip' or text == 'Del vip':
                    if message.reply_to_message != None:
                            member = message.reply_to_message.from_user
                            cursor.execute('select person_id from gp_vip where gp_id = {} AND person_id = {}'
                                                            .format(str(chat_id), 
                                                            str(member.id)))
                            data = cursor.fetchall()              
                            if len(data) == 0:
                                client.send_message(chat_id=chat_id,
                                                text="کاربر\n[{}](tg://user?id={})\nدر لیست ویژه قرار ندارد!!!"
                                                        .format(member.first_name,member.id),
                                                reply_to_message_id=message_id)
                                return
                            cursor.execute('delete from gp_vip where gp_id = {} AND person_id = {}'
                                                            .format(str(chat_id), 
                                                            str(member.id)))
                            connection.commit()
                            client.send_message(chat_id=chat_id,
                                                    text="کاربر\n[{}](tg://user?id={})\nاز لیست ویژه حذف شد."
                                                        .format(member.first_name,member.id),
                                                reply_to_message_id=message_id)
                            return
                    return

                elif text[:9] == 'حذف ویژه ' or text[:8] == 'del vip ' or text[:8] == 'Del vip ':
                    if text[:9] == 'حذف ویژه ':   
                        admin = text[9:]
                    if text[:8] == 'delvip ' or text[:8] == 'Del vip ':
                        admin = text[8:]
                    try :
                        person_id = int(admin)
                    except:
                        person_id = admin
                    try:
                        person = client.get_chat_member(
                                    chat_id=chat_id,
                                    user_id=person_id
                                )
                        member = person.user
                    except:
                        return

                    cursor.execute('select person_id from gp_vip where gp_id = {} AND person_id = {}'
                                                            .format(str(chat_id), 
                                                            str(person.user.id)))
                    data = cursor.fetchall()              
                    if len(data) == 0:
                        client.send_message(chat_id=chat_id,
                                        text="کاربر\n[{}](tg://user?id={})\nدر لیست ویژه قرار ندارد!!!"
                                                .format(member.first_name,member.id),
                                        reply_to_message_id=message_id)
                        return
                    cursor.execute('delete from gp_vip where gp_id = {} AND person_id = {}'
                                                            .format(str(chat_id), 
                                                            str(person.user.id)))
                    connection.commit()
                    client.send_message(chat_id=chat_id,
                                                    text="کاربر\n[{}](tg://user?id={})\nاز لیست ویژه حذف شد."
                                                        .format(member.first_name,member.id),
                                                reply_to_message_id=message_id)
                    return            

                elif text[:4] == 'del ' or text[:4] == 'حذف ' or text[:4] == 'Del ' :
                    try:
                        count = int(message.text[4:])
                    except:
                        return
                    a=[]
                    if (count > 1000):
                        client.send_message(chat_id=chat_id,
                                                    text="حداکثر تعداد 1000 پیام",
                                                reply_to_message_id=message_id)
                        return
                    message_id2 = message_id - 2
                    j = int(count / 100)
                    if j != 0:
                        if count % 100 != 0:
                            j+=1
                    counter = j+20
                    
                    a.append(message_id)
                    a.append(message_id-1)
                    a.append(message_id-2)
                    client.delete_messages(chat_id=chat_id, message_ids=a)
                    if j == 0:
                        while True:
                            counter-=1
                            a.clear()
                            for i in range(message_id2-count,message_id2+1):
                                a.append(i)
                            if(client.delete_messages(chat_id=chat_id, message_ids=a) or counter == 0):
                                break
                            message_id2 = message_id2-count
                    else:
                        while True:
                            counter-=1
                            a.clear()
                            for i in range(message_id2-100,message_id2+1):
                                if(i<1):
                                  j = 0 
                                  continue 
                                a.append(i)

                            try:
                              if(client.delete_messages(chat_id=chat_id, message_ids=a)):
                                  j-=1
                            except:
                              j = 0
                              lenn = len(a)
                              c = int(lenn / 10)
                              for i in range(0,c):
                                try:
                                  client.delete_messages(chat_id=chat_id, message_ids=a[lenn-(i+1)*10:lenn-(i)*10 ])
                                except:
                                  break
                            if(j==0 or counter == 0):
                                break
                            message_id2 = message_id2-100
                    client.send_message(chat_id=chat_id,
                                                text="پاکسازی انجام شد:)",
                                            reply_to_message_id=message_id)                        
                         
                elif text == 'بازکردن بن' or text == 'unban' or text == 'Unban':
                    if message.reply_to_message != None:
                        member = message.reply_to_message.from_user
                        client.unban_chat_member(
                            chat_id=chat_id,
                            user_id=member.id
                        )    
                        client.send_message(chat_id=chat_id,
                                                text="کاربر\n[{}](tg://user?id={})\n از لیست بن شده ها حذف شد."
                                                        .format(member.first_name,member.id),
                                                reply_to_message_id=message_id)
                        return

                elif text[:10] == 'بازکردن بن' or text[:5] == 'unban' or text[:5] == 'Unban':
                    if text[:10] == 'بازکردن بن':
                        try:
                            person_id = int(text[11:])
                        except:
                            person_id = text[11:]
                    if text[0:5] == 'unban' or text[:5] == 'Unban':
                        try:
                            person_id = int(text[6:])
                        except:
                            person_id = text[6:]
                    try :
                        person = client.get_chat_member(
                                    chat_id=chat_id,
                                    user_id=person_id
                                )
                    except:
                        return
                    client.unban_chat_member(
                            chat_id=chat_id,
                            user_id=person.user.id
                        )    
                    client.send_message(chat_id=chat_id,
                                            text="کاربر\n[{}](tg://user?id={})\n از لیست بن شده ها حذف شد."
                                                    .format(person.user.first_name,person.user.id),
                                            reply_to_message_id=message_id)
                    return

                elif text == 'پنل' or text == 'pannel' or text == 'Pannel':
                    keyboard = [
                        [
                            InlineKeyboardButton('راهنمایی دستورات','guidance'),
                            InlineKeyboardButton('تنظیمات اصلی','option')
                        ],
                        [
                            InlineKeyboardButton('گزارشات','records'),
                            InlineKeyboardButton('پشتیبانی','Support')
                        ],
                        [
                            InlineKeyboardButton('لینک گروه','link')
                        ],
                        [
                            InlineKeyboardButton('بستن راهنما','close')
                        ]
                    ]
                    client.send_message(chat_id=chat_id,
                                                            text="گزینه ی مورد نظر را انتخاب کنید",          
                                                        reply_to_message_id=message_id,
                                                        reply_markup = InlineKeyboardMarkup(keyboard))

            elif sender not in vips :
                cursor.execute('select word from gp_lock_word where gp_id = '+str(chat_id))
                data = cursor.fetchall()
                lock_words = []
                for i in data:
                    lock_words.append(i[0])  
                new_text = text.split(' ')
                for i in lock_words:
                    if i in new_text:
                        message.delete()
                        return

                if(silent_mode):
                    message.delete()
                    return
                if message.entities != None:
                    if(check_link):
                        for i in message.entities:
                            if i['type'] == 'url':
                                message.delete()

                    if(check_id):
                        for i in message.entities:
                            if i['type'] == 'mention':
                                message.delete()
                    
                    if(check_hashtag):
                        for i in message.entities:
                            if i['type'] == 'url':
                                message.delete()

# manage CallbackQueryHandler
def helper(client,call_back):
    admin = call_back.message.reply_to_message.from_user.id
    changer = call_back.from_user.id
    if admin != changer:
        return
    message_id = call_back.message.message_id
    chat_id = call_back.message.chat.id

    if call_back.data == 'pannel': 
        keyboard = [
                    [
                        InlineKeyboardButton('راهنمایی دستورات','guidance'),
                        InlineKeyboardButton('تنظیمات اصلی','option')
                    ],
                    [
                        InlineKeyboardButton('گزارشات','records'),
                        InlineKeyboardButton('پشتیبانی','Support')
                    ],
                    [
                        InlineKeyboardButton('لینک گروه','link')
                    ],
                    [
                        InlineKeyboardButton('بستن راهنما','close')
                    ]
                ]
        client.edit_message_text(chat_id=chat_id,
                                text="گزینه ی مورد نظر را انتخاب کنید",    
                                    message_id=message_id,      
                            reply_markup = InlineKeyboardMarkup(keyboard))

    elif call_back.data == 'link': 
        keyboard = [
                    
                    [
                        InlineKeyboardButton('بازگشت','pannel'),
                        InlineKeyboardButton('بستن راهنما','close')
                    ]
                ]
        client.edit_message_text(chat_id=chat_id,
                            message_id=message_id,
                            text="لینک گروه: \n{}".format(client.get_chat(chat_id).invite_link),          
                            reply_markup = InlineKeyboardMarkup(keyboard))

    elif call_back.data == 'Support':
        keyboard = [
                        [
                            InlineKeyboardButton('بازگشت','pannel'), #
                        ],
                        [
                            InlineKeyboardButton('بستن راهنما','close'), #
                        ]
        ]
        client.edit_message_text(
            reply_markup = InlineKeyboardMarkup(keyboard),
            chat_id=chat_id,
            message_id=message_id,
            text = 'برای ارتباط با پشتیبانی :\n @Amierrrrrrrrrr'
                       )

    elif call_back.data == 'guidance': 
        keyboard = [
                    [
                        InlineKeyboardButton('تغییر مقام ها و اعضا','change members'),
                        
                    ],
                    [
                        InlineKeyboardButton('تنظیمات قفل ها','change gp')
                    ],
                    [
                        InlineKeyboardButton('پیام ها','pms')
                    ],
                    [
                        InlineKeyboardButton('لیست ها','lists')
                    ],
                    [
                        InlineKeyboardButton('بازگشت','pannel'),
                        InlineKeyboardButton('بستن راهنما','close')
                    ]
                ]
        client.edit_message_text(chat_id=chat_id,
                            message_id=message_id,
                                text="گزینه ی مورد نظر را انتخاب کنید",          
                            reply_markup = InlineKeyboardMarkup(keyboard))

    elif call_back.data == 'change members': #
        keyboard = [
                        [
                            InlineKeyboardButton('بن کردن','ban'), #
                            InlineKeyboardButton('سکوت','silent'),#
                        ],
                        [
                            InlineKeyboardButton('اخطار','ekhtar'),#
                            InlineKeyboardButton('تبچی','tabchi'),#
                        ],
                        [
                            InlineKeyboardButton('ویژه','vip'), #
                        ],
                        [
                            InlineKeyboardButton('دستوران مخصوص مدیر و ویزران','owner_vizir'), #
                        ],
                        [
                            InlineKeyboardButton('بازگشت','guidance'), #
                        ],
                        [
                            InlineKeyboardButton('بستن راهنما','close'), #
                        ]
        ]
        client.edit_message_text(
            chat_id=chat_id,
            message_id=message_id,
            text = 'خب کدومش؟',
            reply_markup = InlineKeyboardMarkup(keyboard)
            )

    elif call_back.data == 'lists': #
        keyboard = [
                        [
                            InlineKeyboardButton('لیست سکوت','silent_list'), #
                            InlineKeyboardButton('لیست وزرا','vazir_list'),#
                        ],
                        [
                            InlineKeyboardButton('لیست ادمین ها','admin_list'),#
                            InlineKeyboardButton('لیست ویژه','vip_list'),#
                        ],
                        [
                            InlineKeyboardButton('بازگشت','guidance'), #
                        ],
                        [
                            InlineKeyboardButton('بستن راهنما','close'), #
                        ]
        ]
        client.edit_message_text(
            chat_id=chat_id,
            message_id=message_id,
            text = 'خب کدومش؟',
            reply_markup = InlineKeyboardMarkup(keyboard)
            )

    elif call_back.data == 'silent_list':
        keyboard = [
                        [
                            InlineKeyboardButton('بازگشت','lists'), #
                        ],
                        [
                            InlineKeyboardButton('بستن راهنما','close'), #
                        ]
        ]
        client.edit_message_text(
            chat_id=chat_id,
            message_id=message_id,
            reply_markup = InlineKeyboardMarkup(keyboard),
            text = 'لیست سکوت\n'+
                   ':::::::::::::::::::::::::::::::::::::::::::\n'+ 
                   'دستورات فارسی برای این منظور:\n'+
                   'ᴥ لیست سکوت \n\n'+
                   'دستورات انگلیسی برای این منظور:\n'+
                   'ᴥ silent list\n'
                       )

    elif call_back.data == 'vazir_list':
        keyboard = [
                        [
                            InlineKeyboardButton('بازگشت','lists'), #
                        ],
                        [
                            InlineKeyboardButton('بستن راهنما','close'), #
                        ]
        ]
        client.edit_message_text(
            chat_id=chat_id,
            message_id=message_id,
            reply_markup = InlineKeyboardMarkup(keyboard),
            text = 'لیست سکوت\n'+
                   ':::::::::::::::::::::::::::::::::::::::::::\n'+ 
                   'دستورات فارسی برای این منظور:\n'+
                   'ᴥ لیست وزیران \n\n'+
                   'دستورات انگلیسی برای این منظور:\n'+
                   'ᴥ vazir list\n'
                       )

    elif call_back.data == 'admin_list':
        keyboard = [
                        [
                            InlineKeyboardButton('بازگشت','lists'), #
                        ],
                        [
                            InlineKeyboardButton('بستن راهنما','close'), #
                        ]
        ]
        client.edit_message_text(
            chat_id=chat_id,
            message_id=message_id,
            reply_markup = InlineKeyboardMarkup(keyboard),
            text = 'لیست سکوت\n'+
                   ':::::::::::::::::::::::::::::::::::::::::::\n'+ 
                   'دستورات فارسی برای این منظور:\n'+
                   'ᴥ لیست ادمین  \n\n'+
                   'دستورات انگلیسی برای این منظور:\n'+
                   'ᴥ admin list\n'
                       )

    elif call_back.data == 'vip_list':
        keyboard = [
                        [
                            InlineKeyboardButton('بازگشت','lists'), #
                        ],
                        [
                            InlineKeyboardButton('بستن راهنما','close'), #
                        ]
        ]
        client.edit_message_text(
            chat_id=chat_id,
            message_id=message_id,
            reply_markup = InlineKeyboardMarkup(keyboard),
            text = 'لیست سکوت\n'+
                   ':::::::::::::::::::::::::::::::::::::::::::\n'+ 
                   'دستورات فارسی برای این منظور:\n'+
                   'ᴥ لیست ویژه  \n\n'+
                   'دستورات انگلیسی برای این منظور:\n'+
                   'ᴥ vip list\n'
                       )

    elif call_back.data == 'owner_vizir':
        keyboard = [
                        [
                            InlineKeyboardButton('ادمین','admin'), #
                            InlineKeyboardButton('دستورات مدیر','owner'),#
                        ],
                        [
                            InlineKeyboardButton('بازگشت','change members'), #
                        ],
                        [
                            InlineKeyboardButton('بستن راهنما','close'), #
                        ]
                
        ]
        client.edit_message_text(
            chat_id=chat_id,
            message_id=message_id,
            text = 'خب کدومش؟',
            reply_markup = InlineKeyboardMarkup(keyboard)
            )

    elif call_back.data == 'owner':
        keyboard = [
                        [
                            InlineKeyboardButton('وزیر','vazir'), #
                            InlineKeyboardButton('پیکربندی','config'),#
                        ],
                        [
                            InlineKeyboardButton('بازگشت','owner_vizir'), #
                        ],
                        [
                            InlineKeyboardButton('بستن راهنما','close'), #
                        ]
                
        ]
        client.edit_message_text(
            chat_id=chat_id,
            message_id=message_id,
            text = 'خب کدومش؟',
            reply_markup = InlineKeyboardMarkup(keyboard)
            )

    elif call_back.data == 'vazir':
        keyboard = [
                        [
                            InlineKeyboardButton('بازگشت','owner'), #
                        ],
                        [
                            InlineKeyboardButton('بستن راهنما','close'), #
                        ]
        ]
        client.edit_message_text(
            reply_markup = InlineKeyboardMarkup(keyboard),
            chat_id=chat_id,
            message_id=message_id,
            text = 'تایین کاربر بعنوان وزیر\n وزیر علاوه بر اختیارات ادمین قابلیت ادمین گذاری و خلع ادمین را دارد'+
                   ':::::::::::::::::::::::::::::::::::::::::::\n'+ 
                   'دستورات فارسی برای این منظور:\n'+
                   'ᴥ وزیر\n'+
                   'ᴥ  __id__ وزیر\n'+
                   'ᴥ __username__ وزیر \n'+
                   'ᴥ حذف وزیر\n'+
                   'ᴥ __id__ حذف وزیر \n'+
                   'ᴥ __username__ حذف وزیر \n\n'+
                   'دستورات انگلیسی برای این منظور:\n'+
                   'ᴥ vazir\n'+
                   'ᴥ vazir __id__\n'+
                   'ᴥ vazir __username__\n'+
                   'ᴥ del vazir\n'+
                   'ᴥ del vazir __id__\n'+
                   'ᴥ del vazir __username__\n'
                       )

    elif call_back.data == 'admin':
        keyboard = [
                        [
                            InlineKeyboardButton('بازگشت','owner_vizir'), #
                        ],
                        [
                            InlineKeyboardButton('بستن راهنما','close'), #
                        ]
        ]
        client.edit_message_text(
            reply_markup = InlineKeyboardMarkup(keyboard),
            chat_id=chat_id,
            message_id=message_id,
            text = 'تایین کاربر بعنوان ادمین رباط (فقط به دست مدیر گپ)\n'+
                   ':::::::::::::::::::::::::::::::::::::::::::\n'+ 
                   'دستورات فارسی برای این منظور:\n'+
                   'ᴥ ادمین\n'+
                   'ᴥ  __id__ ادمین\n'+
                   'ᴥ __username__ ادمین \n'+
                   'ᴥ حذف ادمین\n'+
                   'ᴥ __id__ حذف ادمین \n'+
                   'ᴥ __username__ حذف ادمین \n\n'+
                   'دستورات انگلیسی برای این منظور:\n'+
                   'ᴥ admin\n'+
                   'ᴥ admin __id__\n'+
                   'ᴥ admin __username__\n'+
                   'ᴥ del admin\n'+
                   'ᴥ del admin __id__\n'+
                   'ᴥ del admin __username__\n'
                       )

    elif call_back.data == 'change gp':       
        keyboard = [
                        [
                            InlineKeyboardButton('قفل هشتگ','lock hashtag'), #
                            InlineKeyboardButton('قفل ایدی','lock id'), #
                        ],
                        [
                            InlineKeyboardButton('قفل گپ','lock'), #
                            InlineKeyboardButton('قفل لینک','lock link'), #
                        ],
                        [
                            InlineKeyboardButton('قفل ویس','lock voice'), #
                            InlineKeyboardButton('قفل متن','lock text'), #
                        ],
                        [
                            InlineKeyboardButton('قفل عکس','lock photo'),
                            InlineKeyboardButton('قفل فیلم','lock film'),
                        ],
                        [
                            InlineKeyboardButton('قفل گیف','lock gif'),
                            InlineKeyboardButton('قفل ایدی','lock id'),
                        ],
                        [
                            InlineKeyboardButton('قفل کلمه','lock word'), #
                        ],
                        [
                            InlineKeyboardButton('بازگشت','guidance'), #
                        ],
                        [
                            InlineKeyboardButton('بستن راهنما','close'), #
                        ]
        ]
        client.edit_message_text(
            chat_id=chat_id,
            message_id=message_id,
            text = 'خب کدومش؟',
            reply_markup = InlineKeyboardMarkup(keyboard)
            )

    elif call_back.data == 'ban':
        keyboard = [
                        [
                            InlineKeyboardButton('بازگشت','change members'), #
                        ],
                        [
                            InlineKeyboardButton('بستن راهنما','close'), #
                        ]
        ]
        client.edit_message_text(
            chat_id=chat_id,
            message_id=message_id,
            reply_markup = InlineKeyboardMarkup(keyboard),
            text = 'حذف عضو از گروه\n'+
                   ':::::::::::::::::::::::::::::::::::::::::::\n'+ 
                   'دستورات فارسی برای این منظور:\n'+
                   'ᴥ بن\n'+
                   'ᴥ  __id__ بن\n'+
                   'ᴥ __username__ بن \n'+
                   'ᴥ بازکردن بن\n'+
                   'ᴥ __id__ بازکردن بن \n'+
                   'ᴥ __username__ بازکردن بن \n\n'+
                   'دستورات انگلیسی برای این منظور:\n'+
                   'ᴥ ban\n'+
                   'ᴥ ban __id__\n'+
                   'ᴥ ban __username__\n'+
                   'ᴥ unban\n'+
                   'ᴥ unban __id__\n'+
                   'ᴥ unban __username__\n'
            
                       )

    elif call_back.data == 'silent':
        keyboard = [
                        [
                            InlineKeyboardButton('بازگشت','change members'), #
                        ],
                        [
                            InlineKeyboardButton('بستن راهنما','close'), #
                        ]
        ]
        client.edit_message_text(
            reply_markup = InlineKeyboardMarkup(keyboard),
            chat_id=chat_id,
            message_id=message_id,
            text = 'این دستور به منظور حذف هر گونه پیام ارسالی از ممبر است\n'+
                   ':::::::::::::::::::::::::::::::::::::::::::\n'+ 
                   'دستورات فارسی برای این منظور:\n'+
                   'ᴥ سکوت\n'+
                   'ᴥ  __id__ سکوت\n'+
                   'ᴥ __username__ سکوت \n'+
                   'ᴥ حذف سکوت\n'+
                   'ᴥ __id__ حذف سکوت \n'+
                   'ᴥ __username__ حذف سکوت \n\n'+
                   'دستورات انگلیسی برای این منظور:\n'+
                   'ᴥ mute\n'+
                   'ᴥ mute __id__\n'+
                   'ᴥ mute __username__\n'+
                   'ᴥ unmute\n'+
                   'ᴥ unmute __id__\n'+
                   'ᴥ unmute __username__\n'
                       )

    elif call_back.data == 'ekhtar':
        keyboard = [
                        [
                            InlineKeyboardButton('بازگشت','change members'), #
                        ],
                        [
                            InlineKeyboardButton('بستن راهنما','close'), #
                        ]
        ]
        client.edit_message_text(
            reply_markup = InlineKeyboardMarkup(keyboard),
            chat_id=chat_id,
            message_id=message_id,
            text = 'این دستور به منظور اخظار برای ممبر است.\n'+
                   ':::::::::::::::::::::::::::::::::::::::::::\n'+ 
                   'دستورات فارسی برای این منظور:\n'+
                   'ᴥ اخطار\n'+
                   'ᴥ  __id__ اخطار\n'+
                   'ᴥ __username__ اخطار \n'+
                   'ᴥ حذف اخطار\n'+
                   'ᴥ __id__ حذف اخطار \n'+
                   'ᴥ __username__ حذف اخطار \n\n'+
                   'دستورات انگلیسی برای این منظور:\n'+
                   'ᴥ warn\n'+
                   'ᴥ warn __id__\n'+
                   'ᴥ warn __username__\n'+
                   'ᴥ del warn\n'+
                   'ᴥ del warn __id__\n'+
                   'ᴥ del warn __username__\n'
                       )

    elif call_back.data == 'tabchi':
        keyboard = [
                        [
                            InlineKeyboardButton('بازگشت','change members'), #
                        ],
                        [
                            InlineKeyboardButton('بستن راهنما','close'), #
                        ]
        ]
        client.edit_message_text(
            reply_markup = InlineKeyboardMarkup(keyboard),
            chat_id=chat_id,
            message_id=message_id,
            text = 'این دستور به منظور گزارش تبچی برای کاربر است که فقط مدیران اصلی\n   یعنی ادمین های ربات قادر به انجام آن هستند\n'+
                   ':::::::::::::::::::::::::::::::::::::::::::\n'+ 
                   'دستورات فارسی برای این منظور:\n'+
                   'ᴥ تبچی\n'+
                   'ᴥ  __id__ تبچی\n'+
                   'ᴥ __username__ تبچی \n'+
                   'ᴥ حذف تبچی\n'+
                   'ᴥ __id__ حذف تبچی \n'+
                   'ᴥ __username__ حذف تبچی \n\n'+
                   'دستورات انگلیسی برای این منظور:\n'+
                   'ᴥ tabchi\n'+
                   'ᴥ tabchi __id__\n'+
                   'ᴥ tabchi __username__\n'+
                   'ᴥ del tabchi\n'+
                   'ᴥ del tabchi __id__\n'+
                   'ᴥ del tabchi __username__\n'
                       )

    elif call_back.data == 'vip':
        keyboard = [
                        [
                            InlineKeyboardButton('بازگشت','change members'), #
                        ],
                        [
                            InlineKeyboardButton('بستن راهنما','close'), #
                        ]
            ]
        client.edit_message_text(
            reply_markup = InlineKeyboardMarkup(keyboard),
            chat_id=chat_id,
            message_id=message_id,
            text = 'عضو ویژه در برابر قفل ها و فیلتر های گپ استثنا است \n'+
                   ':::::::::::::::::::::::::::::::::::::::::::\n'+ 
                   'دستورات فارسی برای این منظور:\n'+
                   'ᴥ ویژه\n'+
                   'ᴥ  __id__ ویژه\n'+
                   'ᴥ __username__ ویژه \n'+
                   'ᴥ حذف ویژه\n'+
                   'ᴥ __id__ حذف ویژه \n'+
                   'ᴥ __username__ حذف ویژه \n\n'+
                   'دستورات انگلیسی برای این منظور:\n'+
                   'ᴥ vip\n'+
                   'ᴥ vip __id__\n'+
                   'ᴥ vip __username__\n'+
                   'ᴥ del vip\n'+
                   'ᴥ del vip __id__\n'+
                   'ᴥ del vip __username__\n'
                       )

    elif call_back.data == 'config':
        keyboard = [
                        [
                            InlineKeyboardButton('بازگشت','owner'), #
                        ],
                        [
                            InlineKeyboardButton('بستن راهنما','close'), #
                        ]
        ]
        client.edit_message_text(
            reply_markup = InlineKeyboardMarkup(keyboard),
            chat_id=chat_id,
            message_id=message_id,
            text = 'حتما در ابتدا از پیکربندی استفاده کنید.\n'+
                   ':::::::::::::::::::::::::::::::::::::::::::\n'+ 
                   'دستورات فارسی برای این منظور:\n'+
                   'ᴥ  پیکربندی\n'+
                   'دستورات انگلیسی برای این منظور:\n'+
                   'ᴥ config\n'
                       )

    elif call_back.data == 'lock voice':
        keyboard = [
                        [
                            InlineKeyboardButton('بازگشت','change gp'), #
                        ],
                        [
                            InlineKeyboardButton('بستن راهنما','close'), #
                        ]
        ]
        client.edit_message_text(
            reply_markup = InlineKeyboardMarkup(keyboard),
            chat_id=chat_id,
            message_id=message_id,
            text = 'قفل ویس گپ' +
                   '\n:::::::::::::::::::::::::::::::::::::::::::\n'+ 
                   'دستورات فارسی برای این منظور:\n'+
                   'ᴥ قفل ویس\n'+
                   'ᴥ حذف قفل ویس\n'+
                   'دستورات انگلیسی برای این منظور:\n'+
                   'ᴥ loc voice\n'+
                   'ᴥ unloc voice\n'
                       )

    elif call_back.data == 'lock text':
        keyboard = [
                        [
                            InlineKeyboardButton('بازگشت','change gp'), #
                        ],
                        [
                            InlineKeyboardButton('بستن راهنما','close'), #
                        ]
        ]
        client.edit_message_text(
            reply_markup = InlineKeyboardMarkup(keyboard),
            chat_id=chat_id,
            message_id=message_id,
            text = 'قفل متن گپ' +
                   ':::::::::::::::::::::::::::::::::::::::::::\n'+ 
                   'دستورات فارسی برای این منظور:\n'+
                   'ᴥ قفل متن\n'+
                   'ᴥ حذف قفل متن\n'+
                   'دستورات انگلیسی برای این منظور:\n'+
                   'ᴥ loc text\n'+
                   'ᴥ unloc text\n'
                       )

    elif call_back.data == 'lock photo':
        keyboard = [
                        [
                            InlineKeyboardButton('بازگشت','change gp'), #
                        ],
                        [
                            InlineKeyboardButton('بستن راهنما','close'), #
                        ]
        ]
        client.edit_message_text(
            reply_markup = InlineKeyboardMarkup(keyboard),
            chat_id=chat_id,
            message_id=message_id,
            text = 'قفل عکس گپ' +
                   '\n:::::::::::::::::::::::::::::::::::::::::::\n'+ 
                   'دستورات فارسی برای این منظور:\n'+
                   'ᴥ قفل عکس\n'+
                   'ᴥ حذف قفل عکس\n'+
                   'دستورات انگلیسی برای این منظور:\n'+
                   'ᴥ loc photo\n'+
                   'ᴥ unloc photo\n'
                       )

    elif call_back.data == 'lock film':
        keyboard = [
                        [
                            InlineKeyboardButton('بازگشت','change gp'), #
                        ],
                        [
                            InlineKeyboardButton('بستن راهنما','close'), #
                        ]
        ]
        client.edit_message_text(
            reply_markup = InlineKeyboardMarkup(keyboard),
            chat_id=chat_id,
            message_id=message_id,
            text = 'قفل فیلم گپ' +
                   '\n:::::::::::::::::::::::::::::::::::::::::::\n'+ 
                   'دستورات فارسی برای این منظور:\n'+
                   'ᴥ قفل فیلم\n'+
                   'ᴥ حذف قفل فیلم\n'+
                   'دستورات انگلیسی برای این منظور:\n'+
                   'ᴥ loc video\n'+
                   'ᴥ unloc video\n'
                       )

    elif call_back.data == 'lock gif':
        keyboard = [
                        [
                            InlineKeyboardButton('بازگشت','change gp'), #
                        ],
                        [
                            InlineKeyboardButton('بستن راهنما','close'), #
                        ]
        ]
        client.edit_message_text(
            reply_markup = InlineKeyboardMarkup(keyboard),
            chat_id=chat_id,
            message_id=message_id,
            text = 'قفل گیف گپ' +
                   '\n:::::::::::::::::::::::::::::::::::::::::::\n'+ 
                   'دستورات فارسی برای این منظور:\n'+
                   'ᴥ قفل گیف\n'+
                   'ᴥ حذف قفل گیف\n'+
                   'دستورات انگلیسی برای این منظور:\n'+
                   'ᴥ loc gif\n'+
                   'ᴥ unloc gif\n'
                       )

    elif call_back.data == 'lock hashtag':
        keyboard = [
                        [
                            InlineKeyboardButton('بازگشت','change gp'), #
                        ],
                        [
                            InlineKeyboardButton('بستن راهنما','close'), #
                        ]
        ]
        client.edit_message_text(
            reply_markup = InlineKeyboardMarkup(keyboard),
            chat_id=chat_id,
            message_id=message_id,
            text = 'قفل هشتگ گپ' +
                   '\n:::::::::::::::::::::::::::::::::::::::::::\n'+ 
                   'دستورات فارسی برای این منظور:\n'+
                   'ᴥ قفل هشتگ\n'+
                   'ᴥ حذف قفل هشتگ\n'+
                   'دستورات انگلیسی برای این منظور:\n'+
                   'ᴥ loc hashtag\n'+
                   'ᴥ unloc hashtag\n'
                       )

    elif call_back.data == 'lock id':
        keyboard = [
                        [
                            InlineKeyboardButton('بازگشت','change gp'), #
                        ],
                        [
                            InlineKeyboardButton('بستن راهنما','close'), #
                        ]
        ]
        client.edit_message_text(
            reply_markup = InlineKeyboardMarkup(keyboard),
            chat_id=chat_id,
            message_id=message_id,
            text = 'قفل ایدی گپ' +
                   '\n:::::::::::::::::::::::::::::::::::::::::::\n'+ 
                   'دستورات فارسی برای این منظور:\n'+
                   'ᴥ قفل ایدی\n'+
                   'ᴥ حذف قفل ایدی\n'+
                   'دستورات انگلیسی برای این منظور:\n'+
                   'ᴥ loc id\n'+
                   'ᴥ unloc id\n'
                       )

    elif call_back.data == 'lock':
        keyboard = [
                        [
                            InlineKeyboardButton('بازگشت','change gp'), #
                        ],
                        [
                            InlineKeyboardButton('بستن راهنما','close'), #
                        ]
        ]
        client.edit_message_text(
            reply_markup = InlineKeyboardMarkup(keyboard),
            chat_id=chat_id,
            message_id=message_id,
            text = 'قفل کلی گپ' +
                   '\n:::::::::::::::::::::::::::::::::::::::::::\n'+ 
                   'دستورات فارسی برای این منظور:\n'+
                   'ᴥ قفل گروه\n'+
                   'ᴥ حذف قفل گروه\n'+
                   'دستورات انگلیسی برای این منظور:\n'+
                   'ᴥ loc gp\n'+
                   'ᴥ unloc gp\n'
                       )

    elif call_back.data == 'lock link':
        keyboard = [
                        [
                            InlineKeyboardButton('بازگشت','change gp'), #
                        ],
                        [
                            InlineKeyboardButton('بستن راهنما','close'), #
                        ]
        ]
        client.edit_message_text(
            reply_markup = InlineKeyboardMarkup(keyboard),
            chat_id=chat_id,
            message_id=message_id,
            text = 'قفل لینک گپ' +
                   '\n:::::::::::::::::::::::::::::::::::::::::::\n'+ 
                   'دستورات فارسی برای این منظور:\n'+
                   'ᴥ قفل لینک\n'+
                   'ᴥ حذف قفل لینک\n'+
                   'دستورات انگلیسی برای این منظور:\n'+
                   'ᴥ loc link\n'+
                   'ᴥ unloc link\n'
                       )

    elif call_back.data == 'lock word':
        keyboard = [
                        [
                            InlineKeyboardButton('بازگشت','change gp'), #
                        ],
                        [
                            InlineKeyboardButton('بستن راهنما','close'), #
                        ]
        ]
        client.edit_message_text(
            reply_markup = InlineKeyboardMarkup(keyboard),
            chat_id=chat_id,
            message_id=message_id,
            text = 'قفل کلمات گپ' +
                   '\n:::::::::::::::::::::::::::::::::::::::::::\n'+ 
                   'دستورات فارسی برای این منظور:\n'+
                   'ᴥ قفل کلمه\n'+
                   'ᴥ حذف قفل کلمه\n'+
                   'دستورات انگلیسی برای این منظور:\n'+
                   'ᴥ loc word\n'+
                   'ᴥ unloc word\n'
                       )

    elif call_back.data == 'lock link':
        keyboard = [
                        [
                            InlineKeyboardButton('بازگشت','change gp'), #
                        ],
                        [
                            InlineKeyboardButton('بستن راهنما','close'), #
                        ]
        ]
        client.edit_message_text(
            reply_markup = InlineKeyboardMarkup(keyboard),
            chat_id=chat_id,
            message_id=message_id,
            text = 'قفل ایدی گپ' +
                '\n:::::::::::::::::::::::::::::::::::::::::::\n'+ 
                'دستورات فارسی برای این منظور:\n'+
                'ᴥ قفل ایدی\n'+
                'ᴥ حذف قفل ایدی\n'+
                'دستورات انگلیسی برای این منظور:\n'+
                'ᴥ loc id\n'+
                'ᴥ unloc id\n'
                    )

    elif call_back.data == 'pin':
        keyboard = [
                        [
                            InlineKeyboardButton('بازگشت','pms'), #
                        ],
                        [
                            InlineKeyboardButton('بستن راهنما','close'), #
                        ]
        ]
        client.edit_message_text(
            reply_markup = InlineKeyboardMarkup(keyboard),
            chat_id=chat_id,
            message_id=message_id,
            text = 'پین پیام گپ' +
                '\n:::::::::::::::::::::::::::::::::::::::::::\n'+ 
                'دستورات فارسی برای این منظور:\n'+
                'ᴥ پین\n'+
                'ᴥ حذف پین\n'+
                'دستورات انگلیسی برای این منظور:\n'+
                'ᴥ pin \n'+
                'ᴥ unpin \n'
                    )

    elif call_back.data == 'pms':       
        keyboard = [
                        [
                            InlineKeyboardButton('پین پیام','pin'), #
                            InlineKeyboardButton('پاکسازی','delete messages'), #
                        ],
                        [
                            InlineKeyboardButton('بازگشت','guidance'), #
                        ],
                        [
                            InlineKeyboardButton('بستن راهنما','close'), #
                        ]
        ]
        client.edit_message_text(
            chat_id=chat_id,
            message_id=message_id,
            text = 'خب کدومش؟',
            reply_markup = InlineKeyboardMarkup(keyboard)
            )

    elif call_back.data == 'delete messages':       
        keyboard = [
                        [
                            InlineKeyboardButton('بازگشت','pms'), #
                        ],
                        [
                            InlineKeyboardButton('بستن راهنما','close'), #
                        ]
        ]
        client.edit_message_text(
            chat_id=chat_id,
            message_id=message_id,
            text = 'پاکسازی گپ\n'+
            '\n:::::::::::::::::::::::::::::::::::::::::::\n'+ 
                'دستورات فارسی برای این منظور:\n'+
                'ᴥ جذف تعداد\n'+
                'دستورات انگلیسی برای این منظور:\n'+
                'ᴥ del تعداد\n'+
                'تعداد حداکثر 1000 پیام',
            reply_markup = InlineKeyboardMarkup(keyboard)
            )

    elif call_back.data == 'close':
            client.delete_messages(
                chat_id=chat_id,
                message_ids=message_id,
                        )
    
    elif call_back.data == 'option': 
        keyboard=locks(chat_id) 
        client.edit_message_text(
            chat_id=chat_id,
            message_id=message_id,
            text = 'خب کدومش؟',
            reply_markup = InlineKeyboardMarkup(keyboard)
            )

    elif call_back.data == 'do lock hashtag':
        cursor.execute('select check_hashtag'+
                        ' from gp where gp_id = {};'.format(str(chat_id))) 
        data = cursor.fetchall()
        myupdate = 't'
        if data[0][0] :
            myupdate = 'f'
        cursor.execute('UPDATE gp '+
                        ' SET check_hashtag=%s '+
                        ' WHERE gp_id = %s; ',(myupdate,chat_id))
        connection.commit()
         
        keyboard=locks(chat_id)

        client.edit_message_text(
            chat_id=chat_id,
            message_id=message_id,
            text = 'خب کدومش؟',
            reply_markup = InlineKeyboardMarkup(keyboard)
            )

    elif call_back.data == 'do lock stick':
        cursor.execute('select check_stick'+
                        ' from gp where gp_id = {};'.format(str(chat_id))) 
        data = cursor.fetchall()
        myupdate = 't'
        if data[0][0] :
            myupdate = 'f'
        cursor.execute('UPDATE gp '+
                        ' SET check_stick=%s '+
                        ' WHERE gp_id = %s; ',(myupdate,chat_id))
        connection.commit()
         
        keyboard=locks(chat_id)
        
        client.edit_message_text(
            chat_id=chat_id,
            message_id=message_id,
            text = 'خب کدومش؟',
            reply_markup = InlineKeyboardMarkup(keyboard)
            )

    elif call_back.data == 'do lock id':
        cursor.execute('select check_id'+
                        ' from gp where gp_id = {};'.format(str(chat_id))) 
        data = cursor.fetchall()
        myupdate = 't'
        if data[0][0] :
            myupdate = 'f'
        cursor.execute('UPDATE gp '+
                        ' SET check_id=%s '+
                        ' WHERE gp_id = %s; ',(myupdate,chat_id))
        connection.commit()
         
        keyboard=locks(chat_id)

        client.edit_message_text(
            chat_id=chat_id,
            message_id=message_id,
            text = 'خب کدومش؟',
            reply_markup = InlineKeyboardMarkup(keyboard)
            )

    elif call_back.data == 'do lock':
        cursor.execute('select check_all'+
                        ' from gp where gp_id = {};'.format(str(chat_id))) 
        data = cursor.fetchall()
        myupdate = 't'
        if data[0][0] :
            myupdate = 'f'
        cursor.execute('UPDATE gp '+
                        ' SET check_all=%s '+
                        ' WHERE gp_id = %s; ',(myupdate,chat_id))
        connection.commit()
         
        keyboard=locks(chat_id)

        client.edit_message_text(
            chat_id=chat_id,
            message_id=message_id,
            text = 'خب کدومش؟',
            reply_markup = InlineKeyboardMarkup(keyboard)
            )

    elif call_back.data == 'do lock link':
        cursor.execute('select check_link'+
                        ' from gp where gp_id = {};'.format(str(chat_id))) 
        data = cursor.fetchall()
        myupdate = 't'
        if data[0][0] :
            myupdate = 'f'
        cursor.execute('UPDATE gp '+
                        ' SET check_link=%s '+
                        ' WHERE gp_id = %s; ',(myupdate,chat_id))
        connection.commit()
         
        keyboard=locks(chat_id)

        client.edit_message_text(
            chat_id=chat_id,
            message_id=message_id,
            text = 'خب کدومش؟',
            reply_markup = InlineKeyboardMarkup(keyboard)
            )

    elif call_back.data == 'do lock voice':
        cursor.execute('select check_voice'+
                        ' from gp where gp_id = {};'.format(str(chat_id))) 
        data = cursor.fetchall()
        myupdate = 't'
        if data[0][0] :
            myupdate = 'f'
        cursor.execute('UPDATE gp '+
                        ' SET check_voice=%s '+
                        ' WHERE gp_id = %s; ',(myupdate,chat_id))
        connection.commit()

        keyboard=locks(chat_id) 
        
        client.edit_message_text(
            chat_id=chat_id,
            message_id=message_id,
            text = 'خب کدومش؟',
            reply_markup = InlineKeyboardMarkup(keyboard)
            )

    elif call_back.data == 'do lock text':
        cursor.execute('select check_text'+
                        ' from gp where gp_id = {};'.format(str(chat_id))) 
        data = cursor.fetchall()
        myupdate = 't'
        if data[0][0] :
            myupdate = 'f'
        cursor.execute('UPDATE gp '+
                        ' SET check_text=%s '+
                        ' WHERE gp_id = %s; ',(myupdate,chat_id))
        connection.commit()
         
        cursor.execute('select check_gif,check_stick,'+
                        'check_text,check_video,check_voice,'+
                        'check_photo,check_id,check_link,check_all,check_hashtag'+
                        ' from gp where gp_id = {};'.format(str(chat_id))) 
        data = cursor.fetchall()
        gif = 'غیر فعال'
        stick = 'غیر فعال'
        text = 'غیر فعال'
        video = 'غیر فعال'
        voice = 'غیر فعال'
        photo = 'غیر فعال'
        id_ = 'غیر فعال'
        link ='غیر فعال'
        all_ = 'غیر فعال'
        hashtag ='غیر فعال'
        if data[0][0]:
            gif = 'فعال'
        if data[0][1]:
            stick = 'فعال'
        if data[0][2]:
            text = 'فعال'
        if data[0][3]:
            video = 'فعال'
        if data[0][4]:
            voice = 'فعال'
        if data[0][5]:
            photo = 'فعال'
        if data[0][6]:
            id_ = 'فعال'
        if data[0][7]:
            link = 'فعال'
        if data[0][8]:
            all_ = 'فعال'
        if data[0][9]:
            hashtag = 'فعال' 
        keyboard = [
                        [
                            InlineKeyboardButton('قفل هشتگ :{}'.format(hashtag),'do lock hashtag'), #
                        ],
                        [
                            InlineKeyboardButton('قفل استیکر :{}'.format(stick),'do lock stick'), #
                        ],
                        [
                            InlineKeyboardButton('قفل ایدی :{}'.format(id_),'do lock id'), #
                        ],
                        [
                            InlineKeyboardButton('قفل گپ :{}'.format(all_),'do lock'), #
                        ],
                        [
                            InlineKeyboardButton('قفل لینک :{}'.format(link),'do lock link'), #
                        ],
                        [
                            InlineKeyboardButton('قفل ویس :{}'.format(voice),'do lock voice'), #
                        ],
                        [
                            InlineKeyboardButton('قفل متن :{}'.format(text),'do lock text'), #
                        ],
                        [
                            InlineKeyboardButton('قفل عکس :{}'.format(photo),'do lock photo'),
                        ],
                        [
                            InlineKeyboardButton('قفل فیلم :{}'.format(video),'do lock film'),
                        ],
                        [
                            InlineKeyboardButton('قفل گیف :{}'.format(gif),'do lock gif'),
                        ],
                        [
                            InlineKeyboardButton('بازگشت','pannel'), #
                        ],
                        [
                            InlineKeyboardButton('بستن راهنما','close'), #
                        ]
        ]
        client.edit_message_text(
            chat_id=chat_id,
            message_id=message_id,
            text = 'خب کدومش؟',
            reply_markup = InlineKeyboardMarkup(keyboard)
            )

    elif call_back.data == 'do lock photo':
        cursor.execute('select check_photo'+
                        ' from gp where gp_id = {};'.format(str(chat_id))) 
        data = cursor.fetchall()
        myupdate = 't'
        if data[0][0] :
            myupdate = 'f'
        cursor.execute('UPDATE gp '+
                        ' SET check_photo=%s '+
                        ' WHERE gp_id = %s; ',(myupdate,chat_id))
        connection.commit()
         
        cursor.execute('select check_gif,check_stick,'+
                        'check_text,check_video,check_voice,'+
                        'check_photo,check_id,check_link,check_all,check_hashtag'+
                        ' from gp where gp_id = {};'.format(str(chat_id))) 
        data = cursor.fetchall()
        gif = 'غیر فعال'
        stick = 'غیر فعال'
        text = 'غیر فعال'
        video = 'غیر فعال'
        voice = 'غیر فعال'
        photo = 'غیر فعال'
        id_ = 'غیر فعال'
        link ='غیر فعال'
        all_ = 'غیر فعال'
        hashtag ='غیر فعال'
        if data[0][0]:
            gif = 'فعال'
        if data[0][1]:
            stick = 'فعال'
        if data[0][2]:
            text = 'فعال'
        if data[0][3]:
            video = 'فعال'
        if data[0][4]:
            voice = 'فعال'
        if data[0][5]:
            photo = 'فعال'
        if data[0][6]:
            id_ = 'فعال'
        if data[0][7]:
            link = 'فعال'
        if data[0][8]:
            all_ = 'فعال'
        if data[0][9]:
            hashtag = 'فعال' 
        keyboard = [
                        [
                            InlineKeyboardButton('قفل هشتگ :{}'.format(hashtag),'do lock hashtag'), #
                        ],
                        [
                            InlineKeyboardButton('قفل استیکر :{}'.format(stick),'do lock stick'), #
                        ],
                        [
                            InlineKeyboardButton('قفل ایدی :{}'.format(id_),'do lock id'), #
                        ],
                        [
                            InlineKeyboardButton('قفل گپ :{}'.format(all_),'do lock'), #
                        ],
                        [
                            InlineKeyboardButton('قفل لینک :{}'.format(link),'do lock link'), #
                        ],
                        [
                            InlineKeyboardButton('قفل ویس :{}'.format(voice),'do lock voice'), #
                        ],
                        [
                            InlineKeyboardButton('قفل متن :{}'.format(text),'do lock text'), #
                        ],
                        [
                            InlineKeyboardButton('قفل عکس :{}'.format(photo),'do lock photo'),
                        ],
                        [
                            InlineKeyboardButton('قفل فیلم :{}'.format(video),'do lock film'),
                        ],
                        [
                            InlineKeyboardButton('قفل گیف :{}'.format(gif),'do lock gif'),
                        ],
                        [
                            InlineKeyboardButton('بازگشت','pannel'), #
                        ],
                        [
                            InlineKeyboardButton('بستن راهنما','close'), #
                        ]
        ]
        client.edit_message_text(
            chat_id=chat_id,
            message_id=message_id,
            text = 'خب کدومش؟',
            reply_markup = InlineKeyboardMarkup(keyboard)
            )

    elif call_back.data == 'do lock film':
        cursor.execute('select check_video'+
                        ' from gp where gp_id = {};'.format(str(chat_id))) 
        data = cursor.fetchall()
        myupdate = 't'
        if data[0][0] :
            myupdate = 'f'
        cursor.execute('UPDATE gp '+
                        ' SET check_video=%s '+
                        ' WHERE gp_id = %s; ',(myupdate,chat_id))
        connection.commit()
         
        cursor.execute('select check_gif,check_stick,'+
                        'check_text,check_video,check_voice,'+
                        'check_photo,check_id,check_link,check_all,check_hashtag'+
                        ' from gp where gp_id = {};'.format(str(chat_id))) 
        data = cursor.fetchall()
        gif = 'غیر فعال'
        stick = 'غیر فعال'
        text = 'غیر فعال'
        video = 'غیر فعال'
        voice = 'غیر فعال'
        photo = 'غیر فعال'
        id_ = 'غیر فعال'
        link ='غیر فعال'
        all_ = 'غیر فعال'
        hashtag ='غیر فعال'
        if data[0][0]:
            gif = 'فعال'
        if data[0][1]:
            stick = 'فعال'
        if data[0][2]:
            text = 'فعال'
        if data[0][3]:
            video = 'فعال'
        if data[0][4]:
            voice = 'فعال'
        if data[0][5]:
            photo = 'فعال'
        if data[0][6]:
            id_ = 'فعال'
        if data[0][7]:
            link = 'فعال'
        if data[0][8]:
            all_ = 'فعال'
        if data[0][9]:
            hashtag = 'فعال' 
        keyboard = [
                        [
                            InlineKeyboardButton('قفل هشتگ :{}'.format(hashtag),'do lock hashtag'), #
                        ],
                        [
                            InlineKeyboardButton('قفل استیکر :{}'.format(stick),'do lock stick'), #
                        ],
                        [
                            InlineKeyboardButton('قفل ایدی :{}'.format(id_),'do lock id'), #
                        ],
                        [
                            InlineKeyboardButton('قفل گپ :{}'.format(all_),'do lock'), #
                        ],
                        [
                            InlineKeyboardButton('قفل لینک :{}'.format(link),'do lock link'), #
                        ],
                        [
                            InlineKeyboardButton('قفل ویس :{}'.format(voice),'do lock voice'), #
                        ],
                        [
                            InlineKeyboardButton('قفل متن :{}'.format(text),'do lock text'), #
                        ],
                        [
                            InlineKeyboardButton('قفل عکس :{}'.format(photo),'do lock photo'),
                        ],
                        [
                            InlineKeyboardButton('قفل فیلم :{}'.format(video),'do lock film'),
                        ],
                        [
                            InlineKeyboardButton('قفل گیف :{}'.format(gif),'do lock gif'),
                        ],
                        [
                            InlineKeyboardButton('بازگشت','pannel'), #
                        ],
                        [
                            InlineKeyboardButton('بستن راهنما','close'), #
                        ]
        ]
        client.edit_message_text(
            chat_id=chat_id,
            message_id=message_id,
            text = 'خب کدومش؟',
            reply_markup = InlineKeyboardMarkup(keyboard)
            )

    elif call_back.data == 'do lock gif':
        cursor.execute('select check_gif'+
                        ' from gp where gp_id = {};'.format(str(chat_id))) 
        data = cursor.fetchall()
        myupdate = 't'
        if data[0][0] :
            myupdate = 'f'
        cursor.execute('UPDATE gp '+
                        ' SET check_gif=%s '+
                        ' WHERE gp_id = %s; ',(myupdate,chat_id))
        connection.commit()
         
        keyboard=locks(chat_id)
        
        client.edit_message_text(
            chat_id=chat_id,
            message_id=message_id,
            text = 'خب کدومش؟',
            reply_markup = InlineKeyboardMarkup(keyboard)
            )

    elif call_back.data == 'records': #
        keyboard = [
                        [
                            InlineKeyboardButton('لیست سکوت','silent list'), #
                            InlineKeyboardButton('لیست وزرا','vazir list'),#
                        ],
                        [
                            InlineKeyboardButton('لیست ادمین ها','admin list'),#
                            InlineKeyboardButton('لیست ویژه','vip list'),#
                        ],
                        [
                            InlineKeyboardButton('بازگشت','pannel'), #
                        ],
                        [
                            InlineKeyboardButton('بستن راهنما','close'), #
                        ]
        ]
        client.edit_message_text(
            chat_id=chat_id,
            message_id=message_id,
            text = 'خب کدومش؟',
            reply_markup = InlineKeyboardMarkup(keyboard)
            )

    elif call_back.data == 'silent list': #
        keyboard = [
                        [
                            InlineKeyboardButton('خالی کردن لیست سکوت','empty silent list'), #
                        ],
                        [
                            InlineKeyboardButton('بازگشت','records'), #
                        ],
                        [
                            InlineKeyboardButton('بستن راهنما','close'), #
                        ]
        ]
        admins_list = 'لیست سکوت :\n'   
        cursor.execute('select person_id from gp_lock_user where gp_id = '+str(chat_id))
        data = cursor.fetchall()
        silent_list = []
        for i in data :
            silent_list.append(i[0])         
        for i in silent_list:
            try:
                admin = client.get_chat_member(
                                    chat_id= chat_id,
                                    user_id= i
                                )
            except:
                continue
            admins_list +="[{}](tg://user?id={})\n".format(admin.user.first_name,admin.user.id)

        client.edit_message_text(
            chat_id=chat_id,
            message_id=message_id,
            text = admins_list,
            reply_markup = InlineKeyboardMarkup(keyboard)
            )

    elif call_back.data == 'empty silent list': #
        cursor.execute('delete  from gp_lock_user where gp_id = '+str(chat_id))
        connection.commit()
        keyboard = [
                        [
                            InlineKeyboardButton('بازگشت','records'), #
                        ],
                        [
                            InlineKeyboardButton('بستن راهنما','close'), #
                        ]
        ]
        admins_list = 'لیست سکوت :\n'   
        client.edit_message_text(
            chat_id=chat_id,
            message_id=message_id,
            text = admins_list,
            reply_markup = InlineKeyboardMarkup(keyboard)
            )

    elif call_back.data == 'vip list': #
        keyboard = [
                        [
                            InlineKeyboardButton('خالی کردن لیست ویژه','empty vip list'), #
                        ],
                        [
                            InlineKeyboardButton('بازگشت','records'), #
                        ],
                        [
                            InlineKeyboardButton('بستن راهنما','close'), #
                        ]
        ]
        admins_list = 'لیست ویژه :\n'   
        cursor.execute('select person_id from gp_vip where gp_id = '+str(chat_id))
        data = cursor.fetchall()
        silent_list = []
        for i in data :
            silent_list.append(i[0])         
        for i in silent_list:
            try:
                admin = client.get_chat_member(
                                    chat_id= chat_id,
                                    user_id= i
                                )
            except:
                continue
            admins_list +="[{}](tg://user?id={})\n".format(admin.user.first_name,admin.user.id)

        client.edit_message_text(
            chat_id=chat_id,
            message_id=message_id,
            text = admins_list,
            reply_markup = InlineKeyboardMarkup(keyboard)
            )

    elif call_back.data == 'empty silent list': #
        cursor.execute('delete  from gp_vip where gp_id = '+str(chat_id))
        connection.commit()
        keyboard = [
                        [
                            InlineKeyboardButton('بازگشت','records'), #
                        ],
                        [
                            InlineKeyboardButton('بستن راهنما','close'), #
                        ]
        ]
        admins_list = 'لیست ویژه :\n'   
        client.edit_message_text(
            chat_id=chat_id,
            message_id=message_id,
            text = admins_list,
            reply_markup = InlineKeyboardMarkup(keyboard)
            )

    elif call_back.data == 'admin list': #
        keyboard = [
                        [
                            InlineKeyboardButton('بازگشت','records'), #
                        ],
                        [
                            InlineKeyboardButton('بستن راهنما','close'), #
                        ]
        ]
        admins_list = 'لیست ادمین ها :\n'   
        cursor.execute('select admin_id from gp_ad where gp_id = '+str(chat_id))
        data = cursor.fetchall()
        silent_list = []
        for i in data :
            silent_list.append(i[0])         
        for i in silent_list:
            try:
                admin = client.get_chat_member(
                                    chat_id= chat_id,
                                    user_id= i
                                )
            except:
                continue
            admins_list +="[{}](tg://user?id={})\n".format(admin.user.first_name,admin.user.id)

        client.edit_message_text(
            chat_id=chat_id,
            message_id=message_id,
            text = admins_list,
            reply_markup = InlineKeyboardMarkup(keyboard)
            )

    elif call_back.data == 'vazir list': #
        keyboard = [
                        [
                            InlineKeyboardButton('بازگشت','records'), #
                        ],
                        [
                            InlineKeyboardButton('بستن راهنما','close'), #
                        ]
        ]
        admins_list = 'لیست وزیران :\n'   
        cursor.execute('select admin_id from vizir where gp_id = '+str(chat_id))
        data = cursor.fetchall()
        silent_list = []
        for i in data :
            silent_list.append(i[0])         
        for i in silent_list:
            try:
                admin = client.get_chat_member(
                                    chat_id= chat_id,
                                    user_id= i
                                )
            except:
                continue
            admins_list +="[{}](tg://user?id={})\n".format(admin.user.first_name,admin.user.id)

        client.edit_message_text(
            chat_id=chat_id,
            message_id=message_id,
            text = admins_list,
            reply_markup = InlineKeyboardMarkup(keyboard)
            )

# manage gif
def gif_manage(client, message):
    sender = message.from_user.id 
    chat_id = message.chat.id
    cursor.execute('select owner_id,check_text,check_all,check_link,check_id,check_hashtag'+
                        ' from gp where gp_id = {};'.format(str(chat_id)))
    data = cursor.fetchall()

    if len(data) == 0:
        return
    cursor.execute('select owner_id from vips where gp_id is null or gp_id ={} '
                            .format(chat_id)
                            )
    data = cursor.fetchall()
    vips = []
    for i in data :
        vips.append(i[0])
    if sender in vips:
        return
    cursor.execute('select check_gif,check_all from gp where gp_id = '+str(chat_id))
    data = cursor.fetchall()
    silent_mode = data[0][0] or data[0][1]
    if(silent_mode):
        message.delete()
        return

    cursor.execute('select person_id from gp_lock_user where gp_id = '+str(chat_id))
    data = cursor.fetchall()
    silent_list = []
    for i in data :
        silent_list.append(i[0])
    if sender in silent_list: #silent
        message.delete()
        return

# manage video
def video_manage(client, message):
    sender = message.from_user.id 
    chat_id = message.chat.id
    cursor.execute('select owner_id,check_text,check_all,check_link,check_id,check_hashtag'+
                        ' from gp where gp_id = {};'.format(str(chat_id)))
    data = cursor.fetchall()

    if len(data) == 0:
        return
    cursor.execute('select owner_id from vips where gp_id is null or gp_id ={} '
                            .format(chat_id)
                            )
    data = cursor.fetchall()
    vips = []
    for i in data :
        vips.append(i[0])
    if sender in vips:
        return
    cursor.execute('select check_video,check_all from gp where gp_id = '+str(chat_id))
    data = cursor.fetchall()
    silent_mode = data[0][0] or data[0][1]
    if(silent_mode):
        message.delete()
        return

    cursor.execute('select person_id from gp_lock_user where gp_id = '+str(chat_id))
    data = cursor.fetchall()
    silent_list = []
    for i in data :
        silent_list.append(i[0])
    if sender in silent_list: #silent
        message.delete()
        return

# manage voice
def voice_manage(client, message):
    sender = message.from_user.id 
    chat_id = message.chat.id
    cursor.execute('select owner_id,check_text,check_all,check_link,check_id,check_hashtag'+
                        ' from gp where gp_id = {};'.format(str(chat_id)))
    data = cursor.fetchall()

    if len(data) == 0:
        return
    cursor.execute('select owner_id from vips where gp_id is null or gp_id ={} '
                            .format(chat_id)
                            )
    data = cursor.fetchall()
    vips = []
    for i in data :
        vips.append(i[0])
    if sender in vips:
        return
    cursor.execute('select check_voice,check_all from gp where gp_id = '+str(chat_id))
    data = cursor.fetchall()
    silent_mode = data[0][0] or data[0][1]
    if(silent_mode):
        message.delete()
        return

    cursor.execute('select person_id from gp_lock_user where gp_id = '+str(chat_id))
    data = cursor.fetchall()
    silent_list = []
    for i in data :
        silent_list.append(i[0])
    if sender in silent_list: #silent
        message.delete()
        return

# manage photo
def photo_manage(client, message):
    
    sender = message.from_user.id 
    chat_id = message.chat.id
    cursor.execute('select owner_id,check_text,check_all,check_link,check_id,check_hashtag'+
                        ' from gp where gp_id = {};'.format(str(chat_id)))
    data = cursor.fetchall()

    if len(data) == 0:
        return
    cursor.execute('select owner_id from vips where gp_id is null or gp_id ={} '
                            .format(chat_id)
                            )
    data = cursor.fetchall()
    vips = []
    for i in data :
        vips.append(i[0])
    if sender in vips:
        return
    cursor.execute('select check_photo,check_all from gp where gp_id = '+str(chat_id))
    data = cursor.fetchall()
    silent_mode = data[0][0] or data[0][1]
    if(silent_mode):
        message.delete()
        return
    cursor.execute('select person_id from gp_lock_user where gp_id = '+str(chat_id))
    data = cursor.fetchall()
    silent_list = []
    for i in data :
        silent_list.append(i[0])
    if sender in silent_list: #silent
        message.delete()
        return

# manage sticker
def stick_manage(client, message):
    sender = message.from_user.id 
    chat_id = message.chat.id
    cursor.execute('select owner_id,check_text,check_all,check_link,check_id,check_hashtag'+
                        ' from gp where gp_id = {};'.format(str(chat_id)))
    data = cursor.fetchall()

    if len(data) == 0:
        return
    cursor.execute('select owner_id from vips where gp_id is null or gp_id ={} '
                            .format(chat_id))
    data = cursor.fetchall()
    vips = []
    for i in data :
        vips.append(i[0])
    if sender in vips:
        return
    cursor.execute('select check_stick,check_all from gp where gp_id = '+str(chat_id))
    data = cursor.fetchall()
    silent_mode = data[0][0] or data[0][1]
    if(silent_mode):
        message.delete()
        return
    cursor.execute('select person_id from gp_lock_user where gp_id = '+str(chat_id))
    data = cursor.fetchall()
    silent_list = []
    for i in data :
        silent_list.append(i[0])
    if sender in silent_list: #silent
        message.delete()
        return

# manage services
def incoming(client,message):
    message.delete()


def locks(chat_id):
    cursor.execute('select check_gif,check_stick,'+
                        'check_text,check_video,check_voice,'+
                        'check_photo,check_id,check_link,check_all,check_hashtag'+
                        ' from gp where gp_id = {};'.format(str(chat_id))) 
    data = cursor.fetchall()
    gif = 'غیر فعال'
    stick = 'غیر فعال'
    text = 'غیر فعال'
    video = 'غیر فعال'
    voice = 'غیر فعال'
    photo = 'غیر فعال'
    id_ = 'غیر فعال'
    link ='غیر فعال'
    all_ = 'غیر فعال'
    hashtag ='غیر فعال'
    if data[0][0]:
        gif = 'فعال'
    if data[0][1]:
        stick = 'فعال'
    if data[0][2]:
        text = 'فعال'
    if data[0][3]:
        video = 'فعال'
    if data[0][4]:
        voice = 'فعال'
    if data[0][5]:
        photo = 'فعال'
    if data[0][6]:
        id_ = 'فعال'
    if data[0][7]:
        link = 'فعال'
    if data[0][8]:
        all_ = 'فعال'
    if data[0][9]:
        hashtag = 'فعال' 
    keyboard = [
                    [
                        InlineKeyboardButton('قفل هشتگ :{}'.format(hashtag),'do lock hashtag'), #
                    ],
                    [
                        InlineKeyboardButton('قفل استیکر :{}'.format(stick),'do lock stick'), #
                    ],
                    [
                        InlineKeyboardButton('قفل ایدی :{}'.format(id_),'do lock id'), #
                    ],
                    [
                        InlineKeyboardButton('قفل گپ :{}'.format(all_),'do lock'), #
                    ],
                    [
                        InlineKeyboardButton('قفل لینک :{}'.format(link),'do lock link'), #
                    ],
                    [
                        InlineKeyboardButton('قفل ویس :{}'.format(voice),'do lock voice'), #
                    ],
                    [
                        InlineKeyboardButton('قفل متن :{}'.format(text),'do lock text'), #
                    ],
                    [
                        InlineKeyboardButton('قفل عکس :{}'.format(photo),'do lock photo'),
                    ],
                    [
                        InlineKeyboardButton('قفل فیلم :{}'.format(video),'do lock film'),
                    ],
                    [
                        InlineKeyboardButton('قفل گیف :{}'.format(gif),'do lock gif'),
                    ],
                    [
                        InlineKeyboardButton('بازگشت','pannel'), #
                    ],
                    [
                        InlineKeyboardButton('بستن راهنما','close'), #
                    ]
    ]
    return keyboard



app.add_handler(MessageHandler(dump,filters=filters.text))
app.add_handler(CallbackQueryHandler(helper))
app.add_handler(MessageHandler(gif_manage,filters=filters.animation))
app.add_handler(MessageHandler(video_manage,filters=filters.video))
app.add_handler(MessageHandler(stick_manage,filters=filters.sticker))
app.add_handler(MessageHandler(voice_manage,filters=filters.voice))
app.add_handler(MessageHandler(photo_manage,filters=filters.photo))
app.add_handler(MessageHandler(incoming,filters=filters.service))

app.run()


