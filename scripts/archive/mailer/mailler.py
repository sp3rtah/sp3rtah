import smtplib,os
from email.message import EmailMessage
from getpass import getpass
from dotenv import load_dotenv


print('[Leave empty to use environment variables]')
mail_addr = str(input('Enter mail address: '))
mail_pwd = getpass('Password: ')

## read from config file if not entered manually
if not mail_pwd.strip().strip('\n') or not mail_addr.strip().strip('\n'):
   if not os.path.exists('.env'):
      raise RuntimeError('No addr or password specified!')
   ## read auth data from .env
   load_dotenv()
   mail_addr = os.getenv('MAIL_ADDR','')
   mail_pwd = os.getenv('MAIL_PWD','')

   if not mail_addr or not mail_pwd:
      print(f'addr: <{len(mail_addr)} ,pwd: <{len(mail_pwd)}>')
      raise RuntimeError('No addr or password specified!')

# spawn local test server -> python -m DebuggingServer -c localhost:<port>

msg = EmailMessage()
msg['From'] = mail_addr
msg['To'] = mail_addr
msg['Subject'] = 'First message'
msg.set_content('This is my first live message!')


# with smtplib.SMTP('localhost',1025) as mailman:     ## for testing with local server, no mailman.login(<>)

port = 587
ssl_port = 465

with smtplib.SMTP_SSL('smtp.gmail.com',ssl_port) as mailman:
   mailman.login(mail_addr,mail_pwd)

   attachments_count = 0
   # to send an image
   import imghdr
   img_path = 'image.png'
   ## check if image presend in curr directory
   if os.path.exists(img_path):
      with open(img_path,'rb') as img:
         file_data = img.read()
         file_name = img.name
         file_type = imghdr.what(file_name)

      msg.add_attachment(file_data,maintype='image',subtype=file_type,filename=file_name)
      print('Attached image...')
      attachments_count += 1

   ## send pdf if exists
   pdf_path = 'file.pdf'

   if os.path.exists(pdf_path):
      with open(pdf_path,'rb') as pdf:
         file_data = pdf.read()
         file_name = pdf.name

      msg.add_attachment(file_data,maintype='application',subtype='octet-stream',filename=file_name)
      print('Attached pdf...')
      attachments_count += 1

   ## to display as html, (with if enabled by receiver)
   if not attachments_count:
      text = '<h1>This an alternative html message</h1>'
      msg.add_alternative(text,subtype='html')

   ## send message
   print('Sending imail...')
   mailman.send_message(msg)
   print('Email sent!')
