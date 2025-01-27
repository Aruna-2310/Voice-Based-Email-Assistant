from django.shortcuts import render, redirect
from . import forms
from .models import Details
from .models import Compose
import imaplib,email
from gtts import gTTS
import os
from .models import Mail
from playsound import playsound
from django.http import HttpResponse
import speech_recognition as sr
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
from django.http import JsonResponse
import re
import imaplib
import email
# login
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login as auth_login




file = "good"
i=0
passwrd = ""
addr = ""
item =""
subject = ""
body = ""
s = smtplib.SMTP('smtp.gmail.com', 587)
#email_username = 'satyamtiwari4430@digipodium.com'
#email_password = 'projectforblind'
email_username = 'group91235@gmail.com'
email_password = 'rfqrbippjcypxzrg'

s.starttls()
s.login(email_username, email_password)
attachment_dir = 'C:/Users/HP/Desktop/voice_based_email/mysite/homepage/attachments'

def texttospeech(text, filename):
    filename = f'{filename}.mp3'
    flag = True
    while flag:
        try:
            tts = gTTS(text=text, lang='en', slow=False)
            tts.save(filename)
            flag = False
        except Exception as e:
            print('Trying again', e)
            os.remove(filename)
    if os.path.exists(filename):
        playsound(filename)
        os.remove(filename)
    else:
        print("The file does not exist")
    return

def speechtotext(duration):
    global i, addr, passwrd
    r = sr.Recognizer()
    with sr.Microphone() as source:
        r.adjust_for_ambient_noise(source, duration=1)
        #r.adjust_for_ambient_noise(source, duration=0.2)
        playsound('speak.mp3')
        #audio = r.listen(source, phrase_time_limit=duration)
        audio = r.listen(source, timeout=4)
        #audio = r.listen(source)
    try:
        response = r.recognize_google(audio,language="en-US")
        print("Res is ",response)
    except:
        
        response = 'N'
        print("Res is1 ",response)
    return response

def convert_special_char(text):
    temp=text
    special_chars = ['attherate','dot','underscore','dollar','hash','star','plus','minus','space','dash']
    for character in special_chars:
        while(True):
            pos=temp.find(character)
            if pos == -1:
                break
            else :
                if character == 'attherate':
                    temp=temp.replace('attherate','@')
                elif character == 'dot':
                    temp=temp.replace('dot','.')
                elif character == 'underscore':
                    temp=temp.replace('underscore','_')
                elif character == 'dollar':
                    temp=temp.replace('dollar','$')
                elif character == 'hash':
                    temp=temp.replace('hash','#')
                elif character == 'star':
                    temp=temp.replace('star','*')
                elif character == 'plus':
                    temp=temp.replace('plus','+')
                elif character == 'minus':
                    temp=temp.replace('minus','-')
                elif character == 'space':
                    temp = temp.replace('space', '')
                elif character == 'dash':
                    temp=temp.replace('dash','-')
                elif character==' ':
                    temp=temp.replace(' ','')
    return temp


def login_view(request):
    #if request.user.is_authenticated:
    #    return redirect('homepage:options')
    global i, addr, passwrd 
    print(i, addr, passwrd)
    if request.method == 'POST':
        text1 = "Welcome to our Voice Based Email. Login with your email account in order to continue. "
        texttospeech(text1, f'{file}{i}')
        i += 1
        
        flag = True
        while (flag):
            texttospeech("Enter your Email", f'{file}{i}')
            i += 1
            addr = speechtotext(10)
            #addr='group91235@gmail.com'
            if addr=='group 91235@gmail.com':
                addr='group91235@gmail.com'
            if addr != 'N':
                texttospeech("You meant " + addr + " say Continue to confirm or repeat to enter again", f'{file}{i}')
                i += 1
                say = speechtotext(3)
                #say='yes'
                print("Say is  ",say)
                #if say == 'yes' or say == 'Yes':
                say=say.lower()
                if say == 'continue':
                    flag = False
            else:
                texttospeech("could not understand what you meant:", f'{file}{i}')
                i +=1
        addr = addr.strip()
        addr = addr.replace(' ', '')
        addr = addr.lower()
        addr = convert_special_char(addr)
        print(addr)
        request.email = addr

        flag = True
        while (flag):
            texttospeech("Enter your password", f'{file}{i}')
            i +=1
            passwrd = speechtotext(10)
            
            if addr != 'N':
                texttospeech("You meant " + passwrd + " say continue to confirm or repeat to enter again", f'{file}{i}')
                i +=1
                say = speechtotext(3)
                #say='yes'
                say=say.lower()
                if say == 'continue':
                    flag = False
            else:
                texttospeech("could not understand what you meant:", f'{file}{i}')
                i +=1
        passwrd = passwrd.strip()
        passwrd = passwrd.replace(' ', '')
        passwrd = passwrd.lower()
        passwrd = convert_special_char(passwrd)
        print(passwrd)
        try:
            #user = User.objects.get(email=addr)
            #if user.check_password(passwrd):
            #    login(request, user)
            #if request.user.is_authenticated:
            print("Email ",addr)
            print("Password ",passwrd)
            if addr=='group91235@gmail.com' and passwrd=='12345':
                texttospeech("Congratulations. You have logged in successfully. You will now be redirected to the menu page.", f'{file}{i}')
                i +=1
                #return render(request,'homepage/options.html')
                return JsonResponse({'result' : 'success'})
            else:
                texttospeech("Invalid Login Details. Please try again.", f'{file}{i}')
                i +=1
                #return render(request,'homepage/login.html')
                return JsonResponse({'result': 'failure'})
        except:
            #texttospeech("exception"):
            #texttospeech("Invalid Login Details. Please try again.", f'{file}{i}')
            #i +=1
            #return JsonResponse({'result': 'failure'})
            texttospeech("Congratulations. You have logged in successfully. You will now be redirected to the menu page.", f'{file}{i}')
            i +=1
                #return render(request,'homepage/options.html')
            return JsonResponse({'result' : 'success'})
    
    detail  = Details()
    detail.email = addr
    detail.password = passwrd
    return render(request, 'homepage/login.html', {'detail' : detail}) 
def logout(request):
    print("Logout 1")
    return render(request, 'homepage/login.html') 
def options_view(request):
    global i, addr, passwrd
    if request.method == 'POST':
        flag = True
        texttospeech("You are logged into your account. What would you like to do ?", f'{file}{i}')
        i +=1
        while(flag):
            texttospeech("To compose an email say compose. To open Inbox folder say Inbox. To open drive folder say drive. To open Trash folder say Trash. To Logout say Logout. say continue to continue the process and repeat to repeat again?", f'{file}{i}')
            i +=1
            #playsound('speak.mp3')
            say = speechtotext(3)
            say=say.lower()
            if say == 'continue':
                flag = False
            #if say == 'No' or say == 'no':
            #    flag = False
        texttospeech("Enter your desired action", f'{file}{i}')
        i +=1
        act = speechtotext(5)
        act = act.lower()
        #act='sent'
        print('action is ', act)
        if act == 'compose':
            return JsonResponse({'result' : 'compose'})
        elif act == 'inbox':
            return JsonResponse({'result' : 'inbox'})
        elif act == 'drive':
            return JsonResponse({'result' : 'sent'})
        elif act == 'trash':
            return JsonResponse({'result' : 'trash'})
        elif act == 'log out' or act =='logout':
            addr = ""
            passwrd = ""
            texttospeech("You have been logged out of your account and now will be redirected back to the login page.",f'{file}{i}')
            i +=1
            return JsonResponse({'result': 'logout'})
        else:
            texttospeech("Invalid action. Please try again.", f'{file}{i}')
            i +=1
            return JsonResponse({'result': 'failure'})
    elif request.method == 'GET':
        return render(request, 'homepage/options.html')

def compose_view(request):
    global i, addr, passwrd, s, item, subject, body
    if request.method == 'POST':
        text1 = "You have reached the page where you can compose and send an email. "
        texttospeech(text1, f'{file}{i}')
        i +=1
        flag = True
        flag1 = True
        #fromaddr = "satyamtiwari.345@yahoo.com"
        fromaddr=email_username
        toaddr = list()
        while flag1:
            while flag:
                texttospeech("enter receiver's email address:", f'{file}{i}')
                i +=1
                to = ""
                to = speechtotext(15)
                if to != 'N':
                    
                    texttospeech("You meant " + to + " say continue to confirm or repeat to enter again", f'{file}{i}')
                    i +=1
                    say = speechtotext(5)
                    say=say.lower()
                    if say == 'continue':
                        toaddr.append(to)
                        flag = False
                else:
                    texttospeech("could not understand what you meant", f'{file}{i}')
                    i +=1
            texttospeech("Do you want to enter more recipients ?  Say continue or reject.", f'{file}{i}')
            i +=1
            say1 = speechtotext(3)
            if say1 == 'reject':
                flag1 = False
            flag = True
        newtoaddr = list()
        for item in toaddr:
        #toaddr[0]="group91235@gmail.com"    
            item = toaddr[0]
            item = item.strip()
            item = item.replace(' ', '')
            item = item.lower()
            item = convert_special_char(item)
        
        msg = MIMEMultipart()
        
        msg['From'] = fromaddr
        msg['To'] = item
        
        flag = True
        while (flag):
            texttospeech("enter subject", f'{file}{i}')
            i +=1
            subject = speechtotext(10)
            if subject == 'N':
                texttospeech("could not understand what you meant", f'{file}{i}')
                i +=1
            else:
                flag = False
        msg['Subject'] = subject
        flag = True
        while flag:
            texttospeech("enter body of the mail", f'{file}{i}')
            i +=1
            body = speechtotext(20)
            if body == 'N':
                texttospeech("could not understand what you meant", f'{file}{i}')
                i +=1
            else:
                flag = False
       
        msg.attach(MIMEText(body, 'plain'))
        texttospeech("any attachment? say continue or reject", f'{file}{i}')
        i +=1
        x = speechtotext(3)
        x = x.lower()
        if x == 'continue':
            texttospeech("Do you want to record an audio and send as an attachment? Say continue. Or else say next to send a file attachment.", f'{file}{i}')
            i +=1
            say = speechtotext(2)
            say = say.lower()
            if say == 'continue':
                texttospeech("Enter filename.", f'{file}{i}')
                i +=1
                filename = speechtotext(5)
                filename = filename.lower()
                filename = filename + '.mp3'
                filename = filename.replace(' ', '')
                print(filename)
                texttospeech("Enter your audio message.", f'{file}{i}')
                i +=1
                audio_msg = speechtotext(10)
                flagconf = True
                while flagconf:
                    try:
                        tts = gTTS(text=audio_msg, lang='en', slow=False)
                        tts.save(filename)
                        flagconf = False
                    except:
                        print('Trying again')
                attachment = open(filename, "rb")
                p = MIMEBase('application', 'octet-stream')
                p.set_payload((attachment).read())
                encoders.encode_base64(p)
                p.add_header('Content-Disposition', "attachment; filename= %s" % filename)
                msg.attach(p)
            elif say == 'next':
                texttospeech("Enter filename with extension", f'{file}{i}')
                i +=1
                filename = speechtotext(5)
                filename = filename.strip()
                filename = filename.replace(' ', '')
                filename = filename.lower()
                filename = convert_special_char(filename)
                
                attachment = open(filename, "rb")
                p = MIMEBase('application', 'octet-stream')
                p.set_payload((attachment).read())
                encoders.encode_base64(p)
                p.add_header('Content-Disposition', "attachment; filename= %s" % filename)
                msg.attach(p)
        try:
            msg.attach(MIMEText(body, 'plain'))
            
            s.sendmail(fromaddr, item, msg.as_string())

            #s.sendmail(fromaddr, newtoaddr, msg.as_string())
            texttospeech("Your email has been sent successfully. You will now be redirected to the menu page.", f'{file}{i}')
            i +=1
        except Exception as e:
            texttospeech("Sorry, your email failed to send. please try again. You will now be redirected to the the compose page again.", f'{file}{i}')
            i +=1
            print(e)
            return JsonResponse({'result': 'failure'})
        s.quit()
        return JsonResponse({'result' : 'success'})
    
    compose  = Compose()
    compose.recipient = item
    compose.subject = subject
    compose.body = body


    return render(request, 'homepage/compose.html', {'compose' : compose})
    
    
def get_body(msg):
    if msg.is_multipart():
        return get_body(msg.get_payload(0))
    else:
        return msg.get_payload(None, True)

def get_attachment(msg):
    global i
    for part in msg.walk():
        if part.get_content_maintype() == 'multipart':
            continue
        if part.get('Content-Disposition') is None:
            continue
        filename = part.get_filename()
        if bool(filename):
            filepath = os.path.join(attachment_dir, filename)
            with open(filepath, "wb") as f:
                f.write(part.get_payload(decode=True))
                texttospeech("Attachment has been downloaded", f'{file}{i}')
                i +=1
                path = 'C:/Users/MATCHA ARUNA/OneDrive/'
                files = os.listdir(path)
                paths = [os.path.join(path, basename) for basename in files]
                file_name = max(paths, key=os.path.getctime)
            with open(file_name, "rb") as f:
                if file_name.find('.jpg') != -1:
                    texttospeech("attachment is an image", f'{file}{i}')
                    i +=1
                if file_name.find('.png') != -1:
                    texttospeech("attachment is an image", f'{file}{i}')
                    i +=1
                if file_name.find('.mp3') != -1:
                    texttospeech("Playing the downloaded audio file.", f'{file}{i}')
                    i +=1
                    playsound(file_name)

def reply_mail(msg_id, message):
    global i,s
    TO_ADDRESS = message['From']
    FROM_ADDRESS = addr
    msg = email.mime.multipart.MIMEMultipart()
    msg['to'] = TO_ADDRESS
    msg['from'] = FROM_ADDRESS
    msg['subject'] = message['Subject']
    msg.add_header('In-Reply-To', msg_id)
    flag = True
    while(flag):
        texttospeech("Enter body.", f'{file}{i}')
        i +=1
        body = speechtotext(20)
        print(body)
        try:
            msg.attach(MIMEText(body, 'plain'))
            s.sendmail(msg['from'], msg['to'], msg.as_string())
            texttospeech("Your reply has been sent successfully.", f'{file}{i}')
            i +=1
            flag = False
        except:
            texttospeech("Your reply could not be sent. Do you want to try again? Say yes or no.", f'{file}{i}')
            i +=1
            act = speechtotext(3)
            act = act.lower()
            if act != 'yes':
                flag = False

def frwd_mail(item, message):
    global i,s
    flag1 = True
    flag = True
    global i
    newtoaddr = list()
    while flag:
        while flag1:
            while True:
                texttospeech("Enter receiver's email address", f'{file}{i}')
                i +=1
                to = speechtotext(15)
                texttospeech("You meant " + to + " say continue to confirm or repeat to enter again", f'{file}{i}')
                i +=1
                yn = speechtotext(3)
                yn = yn.lower()
                if yn == 'continue':
                    to = to.strip()
                    to = to.replace(' ', '')
                    to = to.lower()
                    to = convert_special_char(to)
                    print(to)
                    newtoaddr.append(to)
                    break
            texttospeech("Do you want to add more recepients?", f'{file}{i}')
            i +=1
            ans1 = speechtotext(3)
            ans1 = ans1.lower()
            print(ans1)
            if ans1 == "no" :
                flag1 = False
        message['From'] = addr
        message['To'] = ",".join(newtoaddr)
        try:
            s.sendmail(addr, newtoaddr, message.as_string())
            texttospeech("Your mail has been forwarded successfully.", f'{file}{i}')
            i +=1
            flag = False
        except:
            texttospeech("Your mail could not be forwarded. Do you want to try again? Say continue or repeat.", f'{file}{i}')
            i +=1
            act = speechtotext(3)
            act = act.lower()
            if act != 'yes':
                flag = False

def read_mails(mail_list,folder):
    global s, i
    mail_list.reverse()
    mail_count = 0
    to_read_list = list()
    for item in mail_list:
        To = item.sender.username
        From = item.recipient.username
        Subject = item.subject
        texttospeech("Email number " + str(mail_count + 1) + "    .The mail is from " + From + " to " + To + "  . The subject of the mail is " + Subject, f'{file}{i}')
        i +=1
        print('message id= ', item.id)
        print('From :', From)
        print('To :', To)
        print('Subject :', Subject)
        print("\n")
        to_read_list.append(item.id)
        mail_count = mail_count + 1

    flag = True
    while flag :
        n = 0
        flag1 = True
        while flag1:
            texttospeech("Enter the email number of mail you want to read.",f'{file}{i}')
            i +=1
            n = speechtotext(2)
            print(n)
            texttospeech("You meant " + str(n) + ". Say continue or Repeat .", f'{file}{i}')
            i +=1
            say = speechtotext(2)
            say = say.lower()
            if say == 'continue':
                flag1 = False
        n = int(n)
        msgid = to_read_list[n - 1]
        print("message id is =", msgid)
        message = Mail.objects.get(id=msgid)
        To = message.sender.username
        From = message.recipient.username
        Subject = message.subject
        Msg_id = message.id
        print('From :', From)
        print('To :', To)
        print('Subject :', Subject)
        texttospeech("The mail is from " + From + " to " + To + "  . The subject of the mail is " + Subject, f'{file}{i}')
        i +=1
        Body = message.body()
        Body = re.sub('<.*?>', '', Body)
        Body = os.linesep.join([s for s in Body.splitlines() if s])
        if Body != '':
            texttospeech(Body, f'{file}{i}')
            i +=1
        else:
            texttospeech("Body is empty.", f'{file}{i}')
            i +=1
        get_attachment(message)

        if folder == 'inbox':
            texttospeech("Do you want to reply to this mail? Say continue or reject ", f'{file}{i}')
            i +=1
            ans = speechtotext(3)
            ans = ans.lower()
            print(ans)
            if ans == "continue":
                reply_mail(Msg_id, message)

        if folder == 'inbox' or folder == 'sent':
            texttospeech("Do you want to forward this mail to anyone? Say continue or rejects. ", f'{file}{i}')
            i +=1
            ans = speechtotext(3)
            ans = ans.lower()
            print(ans)
            if ans == "continue":
                frwd_mail(Msg_id, message)


        if folder == 'inbox' or folder == 'sent':
            texttospeech("Do you want to delete this mail? Say continue or rejects. ", f'{file}{i}')
            i +=1
            ans = speechtotext(3)
            ans = ans.lower()
            print(ans)
            if ans == "contine":
                try:
                    message.delete()
                    texttospeech("The mail has been deleted successfully.", f'{file}{i}')
                    i +=1
                    print("mail deleted")
                except:
                    texttospeech("Sorry, could not delete this mail. Please try again later.", f'{file}{i}')
                    i +=1

        if folder == 'trash':
            texttospeech("Do you want to delete this mail? Say contine or reject. ", f'{file}{i}')
            i +=1
            ans = speechtotext(3)
            ans = ans.lower()
            print(ans)
            if ans == "continue":
                try:
                    message.delete()
                    texttospeech("The mail has been deleted permanently.", f'{file}{i}')
                    i +=1
                    print("mail deleted")
                except:
                    texttospeech("Sorry, could not delete this mail. Please try again later.", f'{file}{i}')
                    i +=1

        texttospeech("Email ends here.", f'{file}{i}')
        i +=1
        texttospeech("Do you want to read more mails? say continue for yes ,rejects for no", f'{file}{i}')
        i +=1
        ans = speechtotext(2)
        ans = ans.lower()
        if ans == "reject":
            flag = False

def search_specific_mail(folder,key,value,foldername):
    # global i, conn
    # mails = Mail.objects.filter(recipient=, status=folder)
  
    # mail_list=data[0].split()
    # if len(mail_list) != 0:
    #     texttospeech("There are " + str(len(mail_list)) + " emails with this email ID.", f'{file}{i}')
    #     i +=1
    # if len(mail_list) == 0:
    #     texttospeech("There are no emails with this email ID.", f'{file}{i}')
    #     i +=1
    # else:
    #     read_mails(mail_list,foldername)
    pass

def inbox_view(request):
    global i, addr, passwrd, conn
    if request.method == 'POST':
        print(email_username)
    
        texttospeech("You have reached your inbox. To read unread emails say unread. To search a specific email say search. To go back to the menu page say return. To logout say logout.", f'{file}{i}')
        i +=1
        flag = True
        while(flag):
            act = speechtotext(5)
            act = act.lower()
            print(act)
            if act == 'unread' or act=='android' or act=='hundred':
                import imaplib
                import email
                from email.header import decode_header

                # Replace 'your_email@gmail.com' and 'your_password' with your Gmail credentials
                email_address = 'group91235@gmail.com'
                password = 'rfqrbippjcypxzrg'
                # Connect to Gmail server
                mail = imaplib.IMAP4_SSL("imap.gmail.com")

                # Login to your account
                mail.login(email_address, password)

                # Select the mailbox you want to access (e.g., 'inbox')
                mail.select("inbox")

                # Search for unread emails in the selected mailbox
                status, messages = mail.search(None, "UNSEEN")
                messages_ids = messages[0].split()
                no=len(messages_ids)
                flag = False
                if no!=0:
                    for mail_id in messages_ids:
                        status, msg_data = mail.fetch(mail_id, "(RFC822)")
                        raw_email = msg_data[0][1]
                        
                        # Parse the raw email using the email library
                        msg = email.message_from_bytes(raw_email)
                        
                        # Get email subject and sender
                        subject, encoding = decode_header(msg["Subject"])[0]
                        sender, encoding = decode_header(msg.get("From"))[0]
                        
                        # If the sender is bytes, decode it to string
                        if isinstance(sender, bytes):
                            sender = sender.decode(encoding or "utf-8")

                        print(f"Subject: {subject}\nFrom: {sender}")
                        
                        # Accessing email body
                        body = ""
                        for part in msg.walk():
                            if part.get_content_type() == "text/plain":
                                body = part.get_payload(decode=True).decode('utf-8')
                                break

                        print("Email Body:\n", body)
                        texttospeech(body, f'{file}{i}')                

                else:
                    texttospeech("You have no unread emails.", f'{file}{i}')
                    i +=1
            elif act == 'search':
                flag = False
                emailid = ""
                sub=''
                while True:
                    #texttospeech("Enter email ID of the person who's email you want to search.", f'{file}{i}')
                    texttospeech("Enter subject of the  email you want to search.", f'{file}{i}')
                    i +=1
                    sub = speechtotext(15)
                    sub=convert_special_char(sub)
                    texttospeech("You meant " + sub + " say continue to confirm or repeat to enter again", f'{file}{i}')
                    i +=1
                    yn = speechtotext(5)
                    yn = yn.lower()
                    if yn == 'continue':
                        break

                import imaplib
                import email
                from email.header import decode_header

                # Replace 'your_email@gmail.com' and 'your_password' with your Gmail credentials
                email_address = 'group91235@gmail.com'
                password = 'rfqrbippjcypxzrg'

                # Connect to Gmail server
                mail = imaplib.IMAP4_SSL("imap.gmail.com")

                # Login to your account
                mail.login(email_address, password)

                # Select the mailbox you want to access (e.g., 'inbox')
                mail.select("inbox")

                # Search for all emails in the selected mailbox
                status, messages = mail.search(None, "ALL")
                messages_ids = messages[0].split()
                #sub="datapro"
                # Loop through the email IDs and fetch the email data
                print("subject is ",sub)
                for mail_id in messages_ids:
                    status, msg_data = mail.fetch(mail_id, "(RFC822)")
                    raw_email = msg_data[0][1]
                    
                    # Parse the raw email using the email library
                    msg = email.message_from_bytes(raw_email)
                    
                    # Get email subject and sender
                    subject, encoding = decode_header(msg["Subject"])[0]
                    sender, encoding = decode_header(msg.get("From"))[0]
                    
                    # If the sender is bytes, decode it to string
                    if isinstance(sender, bytes):
                        sender = sender.decode(encoding or "utf-8")

                    #print(f"Subject: {subject}\nFrom: {sender}\n")
                    if subject==sub:
                      body = ""
                      for part in msg.walk():
                          if part.get_content_type() == "text/plain":
                              body = part.get_payload(decode=True).decode('utf-8')
                              break
                      print(body)
                      i=i+1
                      texttospeech(body, f'{file}{i}')

            elif act == 'return':
                texttospeech("You will now be redirected to the menu page.", f'{file}{i}')
                i +=1
                logout(request)
                return JsonResponse({'result': 'success'})

            elif act == 'log out' or act == 'logout':
                addr = ""
                passwrd = ""
                texttospeech("You have been logged out of your account and now will be redirected back to the login page.", f'{file}{i}')
                i +=1
                return JsonResponse({'result': 'logout'})

            else:
                texttospeech("Invalid action. Please try again.", f'{file}{i}')
                i +=1

            texttospeech("If you wish to do anything else in the inbox or logout of your mail say continue or else say reject.", f'{file}{i}')
            i +=1
            ans = speechtotext(3)
            ans = ans.lower()
            if ans == 'continue':
                flag = True
                texttospeech("Enter your desired action. Say unread, search, return or logout. ", f'{file}{i}')
                i +=1
            elif ans == 'reject':
                texttospeech("You will now be redirected to the menu page.", f'{file}{i}')
                i +=1
                logout(request)
                return JsonResponse({'result': 'success'})

    elif request.method == 'GET':
        return render(request, 'homepage/inbox.html')

def sent_view(request):
    global i, addr, passwrd, conn
    if request.method == 'POST':
        import imaplib
        import email
        from email.header import decode_header

        imap_url = 'imap.gmail.com'
        mail = imaplib.IMAP4_SSL(imap_url)
        email_address = 'group91235@gmail.com'
        password = 'rfqrbippjcypxzrg'
        # Connect to Gmail server
        #mail = imaplib.IMAP4_SSL("imap.gmail.com")

        # Login to your account
        mail.login(email_address, password)

        mail.select('"[Gmail]/Sent Mail"')
        result1, data1 = mail.search(None, "ALL")
        mail_list = data1[0].split()
        text = "You have reached your drive mails folder. You have " + str(len(mail_list)) + " mails in your drive mails folder. To search a specific email say search. To go back to the menu page say return. To logout say logout."
        texttospeech(text, f'{file}{i}')
        i +=1
        flag = True
        while (flag):
            act = speechtotext(5)
            act = act.lower()
            print(act)
            #act='search'
            if act == 'search':
                flag = False
                sub = ""
                while True:
                    texttospeech("Enter subject To Search.", f'{file}{i}')
                    i +=1
                    sub = speechtotext(15)
                    texttospeech("You meant " + sub + " say continue to confirm or repeat to enter again", f'{file}{i}')
                    i +=1
                    yn = speechtotext(5)
                    yn = yn.lower()
                    if yn == 'continue':
                        break
                    
                status, mailbox_list = mail.list()
                mail.select('"[Gmail]/Sent Mail"')
                #mail.select("Trash") 
                # Search for emails in the selected mailbox
                status, messages = mail.search(None, "ALL")
                messages_ids = messages[0].split()

                # Loop through the email IDs and fetch the email data
                for mail_id in messages_ids:
                    status, msg_data = mail.fetch(mail_id, "(RFC822)")
                    raw_email = msg_data[0][1]
                    
                    # Parse the raw email using the email library
                    msg = email.message_from_bytes(raw_email)
                    
                    # Get email subject, sender, and date
                    subject, encoding = decode_header(msg["Subject"])[0]
                    sender, encoding = decode_header(msg.get("From"))[0]
                    date = msg.get("Date")

                    # If the sender is bytes, decode it to string
                    if isinstance(sender, bytes):
                        sender = sender.decode(encoding or "utf-8")

                    # Accessing email body
                    body = ""
                    for part in msg.walk():
                        if part.get_content_type() == "text/plain":
                            body = part.get_payload(decode=True).decode('utf-8')
                            break
                    if subject==sub:
                        texttospeech(body, f'{file}{i}')
                    #print(f"Subject: {subject}\nFrom: {sender}\nDate: {date}\nBody:\n{body}\n")

            elif act == 'return':
                texttospeech("You will now be redirected to the menu page.", f'{file}{i}')
                i +=1
                logout(request)
                return JsonResponse({'result': 'success'})

            elif act == 'log out' or act == 'logout':
                addr = ""
                passwrd = ""
                texttospeech("You have been logged out of your account and now will be redirected back to the login page.", f'{file}{i}')
                i +=1
                return JsonResponse({'result': 'logout'})

            else:
                texttospeech("Invalid action. Please try again.", f'{file}{i}')
                i +=1

            texttospeech("If you wish to do anything else in the sent mails folder or logout of your mail say continue or else say reject.", f'{file}{i}')
            i +=1
            ans = speechtotext(3)
            ans = ans.lower()
            if ans == 'continue':
                flag = True
                texttospeech("Enter your desired action. Say search, return or logout. ", f'{file}{i}')
                i +=1
            elif ans == 'reject':
                texttospeech("You will now be redirected to the menu page.", f'{file}{i}')
                i +=1
        conn.logout()
        return JsonResponse({'result': 'success'})

    elif request.method == 'GET':
        return render(request, 'homepage/sent.html')

def trash_view(request):
    global i, addr, passwrd, conn
    if request.method == 'POST':
        import imaplib
        import email
        from email.header import decode_header

        imap_url = 'imap.gmail.com'
        conn = imaplib.IMAP4_SSL(imap_url)
        conn.login('group91235@gmail.com', 'rfqrbippjcypxzrg')
        conn.select('"[Gmail]/Trash"')
        result1, data1 = conn.search(None, "ALL")
        mail_list = data1[0].split()
        text = "You have reached your trash folder. You have " + str(len(mail_list)) + " mails in your trash folder. To read say read. To go back to the menu page say return. To logout say logout."
        texttospeech(text, f'{file}{i}')
        i +=1
        flag = True
        while (flag):
            act = speechtotext(5)
            act = act.lower()
            print(act)
            #act='view'
            if act == 'read':
                
                # Replace 'your_email@gmail.com' and 'your_password' with your Gmail credentials
                email_address = 'group91235@gmail.com'
                password = 'rfqrbippjcypxzrg'
                # Connect to Gmail server
                mail = imaplib.IMAP4_SSL("imap.gmail.com")

                # Login to your account
                mail.login(email_address, password)

                # Select the mailbox you want to access (e.g., 'sent')
                status, mailbox_list = mail.list()
                #mail.select('"[Gmail]/Sent Mail"')
                mail.select("[Gmail]/Trash") 
                # Search for emails in the selected mailbox
                status, messages = mail.search(None, "ALL")
                messages_ids = messages[0].split()

                # Loop through the email IDs and fetch the email data
                for mail_id in messages_ids:
                    status, msg_data = mail.fetch(mail_id, "(RFC822)")
                    raw_email = msg_data[0][1]
                    
                    # Parse the raw email using the email library
                    msg = email.message_from_bytes(raw_email)
                    
                    # Get email subject, sender, and date
                    subject, encoding = decode_header(msg["Subject"])[0]
                    sender, encoding = decode_header(msg.get("From"))[0]
                    date = msg.get("Date")

                    # If the sender is bytes, decode it to string
                    if isinstance(sender, bytes):
                        sender = sender.decode(encoding or "utf-8")

                    # Accessing email body
                    body = ""
                    for part in msg.walk():
                        if part.get_content_type() == "text/plain":
                            body = part.get_payload(decode=True).decode('utf-8')
                            break
                    texttospeech(body, f'{file}{i}')
                    print(f"Subject: {subject}\nFrom: {sender}\nDate: {date}\nBody:\n{body}\n")
                    #print("="*50)

                # Logout from the server
                mail.logout()


            elif act == 'return':
                texttospeech("You will now be redirected to the menu page.", f'{file}{i}')
                i +=1
                conn.logout()
                return JsonResponse({'result': 'success'})

            elif act == 'log out' or act == 'logout':
                addr = ""
                passwrd = ""
                texttospeech(
                    "You have been logged out of your account and now will be redirected back to the login page.",
                    f'{file}{i}')
                i +=1
                return JsonResponse({'result': 'logout'})

            else:
                texttospeech("Invalid action. Please try again.", f'{file}{i}')
                i +=1

            texttospeech("If you wish to do anything else in the trash folder or logout of your mail say continue or else say Reject.", f'{file}{i}')
            i +=1
            ans = speechtotext(3)
            ans = ans.lower()
            print(ans)
            if ans == 'continue':
                flag = True
                texttospeech("Enter your desired action. Say read, return or logout. ", f'{file}{i}')
                i +=1
            elif ans == 'reject':
                flag = False
            
        texttospeech("You will now be redirected to the menu page.", f'{file}{i}')
        i +=1
        conn.logout()
        return JsonResponse({'result': 'success'})
    elif request.method == 'GET':
        return render(request, 'homepage/trash.html')
    
def fetch_emails(username, password, server, mailbox='INBOX', sender=None, subject=None):
    # create an IMAP4 instance and login
    imap = imaplib.IMAP4_SSL(server)
    imap.login(username, password)

    # select a mailbox (default is INBOX)
    imap.select(mailbox)

    # search for messages that match the specified criteria
    criteria = []
    if sender:
        criteria.append('FROM "{}"'.format(sender))
    if subject:
        criteria.append('SUBJECT "{}"'.format(subject))
    search_criteria = ' '.join(criteria)
    typ, data = imap.search(None, search_criteria)

    # loop through the list of message IDs returned by the search
    messages = []
    for msg_id in data[0].split():
        # fetch the message by ID
        typ, msg_data = imap.fetch(msg_id, '(RFC822)')

        # convert the message data to an EmailMessage object
        msg = email.message_from_bytes(msg_data[0][1])

        # add the message to the list of messages
        messages.append(msg)

    # close the mailbox and logout
    imap.close()
    imap.logout()

    return messages
    
def fetch_email():

    import speech_recognition as sr
    import smtplib
    # import pyaudio
    # import platform
    # import sys
    from bs4 import BeautifulSoup
    import email
    import imaplib
    from gtts import gTTS
    import pyglet
    import os, time

    #pyglet.lib.load_library('avbin')
    #pyglet.have_avbin=True

    #project: :. Project: Voice based Email for blind :. 
    # Author: Sayak Naskar

    #fetch project name
    tts = gTTS(text="Project: Voice based Email for blind", lang='en')
    ttsname=("name.mp3") #Example: path -> C:\Users\sayak\Desktop> just change with your desktop directory. Don't use my directory.
    tts.save(ttsname)

    music = pyglet.media.load(ttsname, streaming = False)
    music.play()

    time.sleep(music.duration)
    os.remove(ttsname)

    #login from os
    login = os.getlogin
    print ("You are logging from : "+login())

    #choices
    print ("1. composed a mail.")
    tts = gTTS(text="option 1. composed a mail.", lang='en')
    ttsname=("hello.mp3") #Example: path -> C:\Users\sayak\Desktop> just change with your desktop directory. Don't use my directory.
    tts.save(ttsname)

    music = pyglet.media.load(ttsname, streaming = False)
    music.play()

    time.sleep(music.duration)
    os.remove(ttsname)

    print ("2. Check your inbox")
    tts = gTTS(text="option 2. Check your inbox", lang='en')
    ttsname=("second.mp3")
    tts.save(ttsname)

    music = pyglet.media.load(ttsname, streaming = False)
    music.play()

    time.sleep(music.duration)
    os.remove(ttsname)

    #this is for input choices
    tts = gTTS(text="Your choice ", lang='en')
    ttsname=("hello.mp3") #Example: path -> C:\Users\sayak\Desktop> just change with your desktop directory. Don't use my directory.
    tts.save(ttsname)

    music = pyglet.media.load(ttsname, streaming = False)
    music.play()

    time.sleep(music.duration)
    os.remove(ttsname)

    #voice recognition part
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print ("Your choice:")
        audio=r.listen(source)
        print ("ok done!!")

    try:
        text=r.recognize_google(audio)
        print ("You said : "+text)
        
    except sr.UnknownValueError:
        print("Google Speech Recognition could not understand audio.")
         
    except sr.RequestError as e:
        print("Could not request results from Google Speech Recognition service; {0}".format(e)) 

    #choices details
    if text == '1' or text == 'One' or text == 'one':
        r = sr.Recognizer() #recognize
        with sr.Microphone() as source:
            print ("Your message :")
            audio=r.listen(source)
            print ("ok done!!")
        try:
            text1=r.recognize_google(audio)
            print ("You said : "+text1)
            msg = text1
        except sr.UnknownValueError:
            print("Google Speech Recognition could not understand audio.")
        except sr.RequestError as e:
            print("Could not request results from Google Speech Recognition service; {0}".format(e))    

        mail = smtplib.SMTP('smtp.gmail.com',587)    #host and port area
        mail.ehlo()  #Hostname to send for this command defaults to the FQDN of the local host.
        mail.starttls() #security connection
        mail.login('emailID','pswrd') #login part
        mail.sendmail('emailID','victimID',msg) #send part
        print ("Congrates! Your mail has send. ")
        tts = gTTS(text="Congrates! Your mail has send. ", lang='en')
        ttsname=("send.mp3") #Example: path -> C:\Users\sayak\Desktop> just change with your desktop directory. Don't use my directory.
        tts.save(ttsname)
        music = pyglet.media.load(ttsname, streaming = False)
        music.play()
        time.sleep(music.duration)
        os.remove(ttsname)
        mail.close()   
        
    if text == '2' or text == 'tu' or text == 'two' or text == 'Tu' or text == 'to' or text == 'To' :
        mail = imaplib.IMAP4_SSL('imap.gmail.com',993) #this is host and port area.... ssl security
        unm = ('your mail or victim mail')  #username
        psw = ('pswrd')  #password
        mail.login(unm,psw)  #login
        stat, total = mail.select('Inbox')  #total number of mails in inbox
        print ("Number of mails in your inbox :"+str(total))
        tts = gTTS(text="Total mails are :"+str(total), lang='en') #voice out
        ttsname=("total.mp3") #Example: path -> C:\Users\sayak\Desktop> just change with your desktop directory. Don't use my directory.
        tts.save(ttsname)
        music = pyglet.media.load(ttsname, streaming = False)
        music.play()
        time.sleep(music.duration)
        os.remove(ttsname)
        
        #unseen mails
        unseen = mail.search(None, 'UnSeen') # unseen count
        print ("Number of UnSeen mails :"+str(unseen))
        tts = gTTS(text="Your Unseen mail :"+str(unseen), lang='en')
        ttsname=("unseen.mp3") #Example: path -> C:\Users\sayak\Desktop> just change with your desktop directory. Don't use my directory.
        tts.save(ttsname)
        music = pyglet.media.load(ttsname, streaming = False)
        music.play()
        time.sleep(music.duration)
        os.remove(ttsname)
        
        #search mails
        result, data = mail.uid('search',None, "ALL")
        inbox_item_list = data[0].split()
        new = inbox_item_list[-1]
        old = inbox_item_list[0]
        result2, email_data = mail.uid('fetch', new, '(RFC822)') #fetch
        raw_email = email_data[0][1].decode("utf-8") #decode
        email_message = email.message_from_string(raw_email)
        print ("From: "+email_message['From'])
        print ("Subject: "+str(email_message['Subject']))
        tts = gTTS(text="From: "+email_message['From']+" And Your subject: "+str(email_message['Subject']), lang='en')
        ttsname=("mail.mp3") #Example: path -> C:\Users\sayak\Desktop> just change with your desktop directory. Don't use my directory.
        tts.save(ttsname)
        music = pyglet.media.load(ttsname, streaming = False)
        music.play()
        time.sleep(music.duration)
        os.remove(ttsname)
        
        #Body part of mails
        stat, total1 = mail.select('Inbox')
        stat, data1 = mail.fetch(total1[0], "(UID BODY[TEXT])")
        msg = data1[0][1]
        soup = BeautifulSoup(msg, "html.parser")
        txt = soup.get_text()
        print ("Body :"+txt)
        tts = gTTS(text="Body: "+txt, lang='en')
        ttsname=("body.mp3") #Example: path -> C:\Users\sayak\Desktop> just change with your desktop directory. Don't use my directory.
        tts.save(ttsname)
        music = pyglet.media.load(ttsname, streaming = False)
        music.play()
        time.sleep(music.duration)
        os.remove(ttsname)
        mail.close()
        mail.logout()
