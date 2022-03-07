#!/usr/bin/env python
# -*- coding: utf-8 -*-
import smtplib
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
from email.header import Header
import jj
import os

class Mail(object):
    def __init__(self, host, nickname, username, password, postfix):
        self.host = host
        self.nickname = nickname
        self.username = username
        self.password = password
        self.postfix = postfix

    def send_mail(self, to_list, subject, content, cc_list=[], encode='gbk', is_html=True, images=[]):
        me = str(Header(self.nickname, encode)) + "<" + self.username + "@" + self.postfix + ">"
        msg = MIMEMultipart()
        msg['Subject'] = Header(subject, encode)
        msg['From'] = me
        msg['To'] = ','.join(to_list)
        msg['Cc'] = ','.join(cc_list)
        if is_html:
            mail_msg = ''
            for i in range(len(images)):
                mail_msg += '<p><img src="cid:image%d" height="240" width="320"></p>' % (i+1)
            msg.attach(MIMEText(content + mail_msg, 'html', 'utf-8'))

            for i, img_name in enumerate(images):
                with open(img_name, 'rb') as fp:
                    img_data = fp.read()
                msg_image = MIMEImage(img_data)
                msg_image.add_header('Content-ID', '<image%d>' % (i+1))
                msg.attach(msg_image)
                # 将图片作为附件
                # image = MIMEImage(img_data, _subtype='octet-stream')
                # image.add_header('Content-Disposition', 'attachment', filename=images[i])
                # msg.attach(image)
        else:
            msg_content = MIMEText(content, 'plain', encode)
            msg.attach(msg_content)

        try:
            s = smtplib.SMTP()
            # s.set_debuglevel(1)
            s.connect(self.host)
            s.login(self.username, self.password)
            s.sendmail(me, to_list + cc_list, msg.as_string())
            s.quit()
            s.close()
            return True
        except Exception as e:
            print(e)
            return False

def send_mail(to_list, title, content, cc_list=[], encode='utf-8', is_html=True, images=[]):
    SCKEY = os.environ["SCKEY"]
    content = '<pre>%s</pre>' % content
    nickname = '温度机器人'
    email = '1449621606'
    password = SCKEY
    m = Mail('smtp.qq.com', nickname, email, password, 'qq.com')
    m.send_mail(to_list, title, content, cc_list, encode, is_html, images)


if __name__ == '__main__':
    images = [
        './近期天气情况.png',
        './天气双重柱状图.png',
        './天气散点图.png',
        './天气堆叠图.png',
        './天气横向柱状图.png',
        './绘制普通图像.png',
        './双折线图.png',

    ]
    import time
    title = '近2周天气趋势图 %s' % time.strftime('%H:%M:%S')
    content = '近2周天气趋势图。发送时间： %s' % time.strftime('%H:%M:%S')+'<br/>'+jj.main('shanghai')
    send_mail(['1449621606@qq.com'], title, content, ['1181259728@qq.com'],  'utf-8', True, images)
