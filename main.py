import csv
import smtplib
import time
from email.mime.text import MIMEText
from email.header import Header

""" 密码到期提醒时间 """
expiry = 5                                  # 单位：天


""" csv文件 """
csv_file = "./test.csv"                   # 表单格式：name,date,email


""" 第三方 SMTP 服务 """
mail_host = "smtp.qq.com"                 # 邮件服务器地址
mail_port = 25                              # 邮件服务器端口
mail_user = "xxxxxxxxx@qq.com"           # 用户名
mail_pass = "xxxxxxxxxxxxxxxx"           # 口令


""" 邮件信息配置 """
email_to = "receiver"                      # 接受者
email_from = "sender"                      # 发送者
email_title = "EmailSubject"              # 邮件主题
email_content = "EmailContent"            # 邮件内容


def main():

    sender = mail_user                      # 发送者
    receivers = []                          # 接收邮件列表
    header = []                             # 表头

    csv_reader = csv.reader(open(csv_file))
    line_nu = 0  # 计数器
    for row in csv_reader:
        if line_nu == 0:
            header = row
        if line_nu != 0:
            print("ID:" + row[0])
            print("\t" + header[0] + ": " + row[0])
            print("\t" + header[1] + ": " + row[1])
            print("\t" + header[2] + ": " + row[2])

            user_expiry = time.mktime(time.strptime(row[1], "%Y/%m/%d %H:%M"))

            if time.time() + expiry * 24 * 60 * 60 >= user_expiry:
                print("\t" + "[密码到期：是]\t需要发送邮件通知\t[添加到收件人列表]")
                receivers.append(row[2])
            else:
                print("\t" + "[密码到期：否]")

        line_nu += 1

    print("收件人列表：")
    print(receivers)

    message = MIMEText(email_content, 'plain', 'utf-8')
    message['Subject'] = Header(email_title, 'utf-8')

    message['From'] = Header(email_from, 'utf-8')
    message['To'] = Header(email_to, 'utf-8')

    try:
        smtpObj = smtplib.SMTP()
        smtpObj.connect(mail_host, mail_port)
        smtpObj.ehlo()
        smtpObj.starttls()
        smtpObj.ehlo()
        smtpObj.login(mail_user,mail_pass)
        smtpObj.sendmail(sender, receivers, message.as_string())
        smtpObj.quit()
        print("邮件发送成功")
    except smtplib.SMTPException as e:
        print("Error: 无法发送邮件：" , end="")
        print(e)


if __name__ == '__main__':
    main()