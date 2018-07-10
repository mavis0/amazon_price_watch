#coding=utf8
from bs4 import BeautifulSoup
from urllib import request
import smtplib, logging, time
from email.header import Header
from email.mime.text import MIMEText
logging.basicConfig(filename='amazon_logger.log', level=logging.INFO)

class email():
    def __init__(self, mail_host, mail_user, mail_pass, sender, receiver, title):
        self.mail_host = mail_host
        self.mail_user = mail_user
        self.mail_pass = mail_pass
        self.sender = sender
        self.receiver = receiver
        self.title = title

    def sendEmail(self, content):
        message = MIMEText(content, 'plain', 'utf-8')  # 内容, 格式, 编码
        message['From'] = "{}".format(self.sender)
        message['To'] = ",".join(self.receivers)
        message['Subject'] = self.title

        try:
            smtpObj = smtplib.SMTP_SSL(self.mail_host, 465)  # 启用SSL发信, 端口一般是465
            smtpObj.login(self.mail_user, self.mail_pass)  # 登录验证
            smtpObj.sendmail(self.sender, self.receivers, message.as_string())  # 发送
            print("mail has been send successfully.")
        except smtplib.SMTPException as e:
            print(e)

def getItem(url):
    req = request.Request(url)
    req.add_header('User-Agent', 'Mozilla/6.0 (iPhone; CPU iPhone OS 8_0 like Mac OS X) AppleWebKit/536.26 (KHTML, like Gecko) Version/8.0 Mobile/10A5376e Safari/8536.25')
    text = request.urlopen(req).read()
    soup = BeautifulSoup(text, 'html.parser')
    try:
        price = soup.find("span",{"id":"newBuyBoxPrice"}).get_text()[1:]
    except Exception as e:
        logging.info('get price error', e)
        return 0.0
    return float(price)

if __name__ == '__main__':

    # 第三方 SMTP 服务
    mail_host = "smtp.163.com"  # SMTP服务器
    mail_user = ""  # 用户名
    mail_pass = ""  # 授权密码，非登录密码

    sender = ''  # 发件人邮箱(最好写全, 不然会失败)
    receiver = ['']  # 接收邮件，可设置为你的QQ邮箱或者其他邮箱
    title = ''  # 邮件主题,比如降价信息什么的

    url = "https://www.amazon.com/gp/product/B0716S22WB"#这个是你要监控的商品的链接
    price = getItem(url)
    #记录价格变化
    logging.info(time.strftime('%Y-%m-%d %X', time.localtime()) + str(':') + str(price))
    #低于多少时价格发送邮件提醒
    e = email(mail_host, mail_user, mail_pass, sender, receiver, title)
    if price <= 100:
        e.sendEmail(price)