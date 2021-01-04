#! /usr/bin/env python
#! -*-coding:utf-8-*-

import sys
import os
import argparse
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.header import Header
from email.utils import formataddr


def AttachObj(file_path):
    attach = None
    with open(file_path, 'rb') as file_handle:
        attach = MIMEText(file_handle.read(), 'base64', 'utf-8')
        attach["Content-Type"] = 'application/octet-stream'
        base_name = os.path.basename(file_path)
        attach["Content-Disposition"] = "attachment; filename=%s" % (base_name)
    return attach


# stmp_address:     邮件服务器地址
# stmp_port:        邮件服务器端口
# sender_username:  发件人帐户名称
# sender_password:  发件人帐户密码
# receivers_lists:  收件人列表
# mail_context:     邮件正文
# attach:           附件
def mail(stmp_address,
         stmp_port,
         sender_username,
         sender_password,
         receivers_lists,
         mail_context,
         attach_file=None):

    msg = None
    if attach_file is None:
        msg = MIMEText(mail_context, 'plain', 'utf-8')
    else:
        msg = MIMEMultipart()
        msg.attach(MIMEText(mail_context, 'plain', 'utf-8'))
        if type(attach_file) is str:
            msg.attach(AttachObj(attach_file))
        elif type(attach_file) is list:
            for ele in attach_file:
                msg.attach(AttachObj(ele))
        else:
            print("Attach None")

    msg['Subject'] = "TKDL SDK"
    msg['From'] = formataddr(["TKDL Runner", sender_username])
    msg['To'] = formataddr(["TKDL Developer", receivers_lists])

    try:
        server = smtplib.SMTP_SSL(stmp_address, stmp_port)
        server.login(sender_username, sender_password)
        server.sendmail(sender_username, receivers_lists, msg.as_string())
        server.quit()
        return True
    except Exception:
        return False


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--stmp_address",
                        type=str,
                        default="smtp.exmail.qq.com",
                        required=False,
                        help="邮件服务器地址 smtp.hostname.com")
    parser.add_argument("--stmp_port",
                        type=int,
                        default=465,
                        required=False,
                        help="邮件服务器端口 465")
    parser.add_argument("--sender_username",
                        type=str,
                        default="jenkins@trunk.tech",
                        required=False,
                        help="发送者邮箱账号 jenkins@trunk.tech")
    parser.add_argument("--sender_password",
                        type=str,
                        required=True,
                        help="发送者邮箱密码")
    parser.add_argument("--mail_context",
                        type=str,
                        required=False,
                        help="邮箱正文")
    parser.add_argument("--receivers",
                        nargs='+',
                        required=True,
                        help="收件人邮箱列表")
    parser.add_argument("--attachment",
                        nargs='+',
                        required=False,
                        help="附件簇列表")
    parser.usage = "python ./mail.py  --sender_password ***** --receivers juhaoming@trunk.tech jenkins@trunk.ch"
    args = parser.parse_args()

    stmp_address = args.stmp_address
    stmp_port = args.stmp_port
    sender_username = args.sender_username
    sender_password = args.sender_password
    receivers = args.receivers
    mail_context = args.mail_context
    attach_file = args.attachment

    print "stmp_address:\t\t%s" % (stmp_address)
    print "stmp_port:\t\t%s" % (stmp_port)
    print "sender_username:\t%s" % (sender_username)
    print "receivers\t\t%s" % (receivers)
    print "mail_context:\t\t%s" % (mail_context)
    print "attach_file:\t\t%s" % (attach_file)

    ret = mail(stmp_address, stmp_port, sender_username, sender_password,
               receivers, mail_context, attach_file)

    if ret:
        print("邮件发送成功")
        sys.exit(0)
    else:
        print("邮件发送失败")
        sys.exit(-1)
