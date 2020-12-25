import email
import imaplib
import time
import os
def Diff(li1, li2):
    li_dif = [i for i in li1 + li2 if i not in li1 or i not in li2]
    return li_dif

def getContent(id):
    result, data = imap.fetch(id, "(RFC822)")
    msg = email.message_from_bytes(data[0][1])
    return msg.get_payload(0).get_payload(decode=True)

def getAttachments(id):
    result, data = imap.fetch(id, "(RFC822)")
    msg = email.message_from_bytes(data[0][1])
    fileName = []
    for part in msg.walk():
        if part.get_content_maintype() == 'multipart':
            continue
        if part.get('Content-Disposition') is None:
            continue
        fName = part.get_filename()
        if fName:
            filePath = os.path.join(detach_dir, 'attachments', fName)
            print(fName)
            file = open(fName, 'wb')
            file.write(part.get_payload(decode=True))
            file.close()
            fileName.append(file)
    if bool(fileName):
        return fileName
    else:
        return None


detach_dir = '.'
if 'attachments' not in os.listdir(detach_dir):
    os.mkdir('attachments')

#credentials
username = "shethprinter@gmail.com"
password = "Sheths@69FD"

#setup connection to email
imap = imaplib.IMAP4_SSL("imap.gmail.com", 993)
imap.login(username, password)

imap.select("Inbox", readonly=True)
result, ids = imap.search(None, "ALL")
id_list = ids[0].split()
attachments = getAttachments(id_list[len(id_list) - 1])

for attachment in attachments:
    os.startfile(attachment.name, "print")



while True:
    imap.select("Inbox", readonly=True)
    result, ids2 = imap.search(None, "ALL")
    process_ids = Diff(id_list, ids2[0].split())
    for d in process_ids:
        attachments = getAttachments(d)

        for attachment in attachments:
            os.startfile(attachment, "print")

        id_list.append(d)
