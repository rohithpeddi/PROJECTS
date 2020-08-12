import email
import glob
import os
import time
 
from email.parser import Parser
 
def parse_rfc2047_charset(encoded):
    "Process an encoded header. Multiple encodings may exist in the same header. Returns an unicode string or '-' on error"
    output  = ""
 
    try:
        parts = email.header.decode_header(encoded)
        for text, charset in parts:
            if (isinstance(text, bytes)):
                #text = text.decode(charset or 'ascii', 'ignore')
                text = text.decode('ascii', 'ignore')
            output += text
    except Exception:
        output = "-"
 
    return output
 
path   = "/src/emails_backup/"
ext    = ".eml";
files  = glob.glob(path + "**/*" + ext)
index  = 0
parser = Parser()
 
for file_path in files:

    index += 1
    percent_done = "{:0>7.2%}".format(index/len(files))

 
    # open the file for reading
    try:
        fp = open(file_path)
    except IOError:
        print("{} Error opening {}: {}".format(percent_done, file_path, e.reason))
        continue
    except FileNotFoundError:
        print("{} File {} no longer exists".format(percent_done, file_path))
        continue
 
    # parse the file as email
    try:
        msg = parser.parse(fp, True)
        fp.close()
    except UnicodeDecodeError as e:
        print("{} Error parsing {}: {}".format(percent_done, file_path, e.reason))
        continue
 
    #convert the email date from 'Thu, 14 Jan 2010 13:10:46 +0530' to '20100114 131046'
    try:
        timestamp = email.utils.mktime_tz(email.utils.parsedate_tz(msg['Date']))
        mail_date = time.strftime("%Y-%m-%d", time.gmtime(timestamp))
    except TypeError as e:
        mail_date = "00000000"
 
    # get and process encoded From, To and Subject headers
    mail_from = email.utils.parseaddr(msg['From'])[1]
    mail_to = email.utils.parseaddr(msg['To'])[1]
    mail_subj = msg['Subject']
 
    # format the new name
    base_name = "{} [{} -- {}] {}".format(mail_date, mail_from, mail_to, mail_subj)
 
    # strip illegal characters
    for char in '<>:"/\\|?*\n':
        base_name = base_name.replace(char, '')
 
    # truncate name if needed
    base_name = base_name[:240]    
 
    #don't rename if already in the desired format
    name = os.path.basename(file_path)
    if (name == base_name + ext):
        print("{} File {} already ok".format(percent_done, file_path))
        continue
 
    # check if new file name already exists, if so append a number
    i = 1
    new_name = base_name + ext
    while(os.path.isfile(path + new_name)):
        new_name = base_name + " (" + str(i) + ")" + ext
        i = i+1

    abs_path = os.path.dirname(file_path)
 
    #compose the full path
    new_file_path = abs_path +"/"+ new_name
 
    # rename the file
    try:
        os.utime(file_path, (timestamp, timestamp))
        os.rename(file_path, new_file_path)
        print("{} {} -> {}".format(percent_done, name, new_name))
    except OSError as e:
        print("{} Error renaming {} to {}: {}".format(percent_done, file_path, new_file_path, e.strerror))
