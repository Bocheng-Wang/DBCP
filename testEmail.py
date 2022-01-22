import os
from django.core.mail import send_mail

from DBCP import settings as S
#
# os.environ['DJANGO_SETTINGS_MODULE'] = 'DBCP.settings'
#
# if __name__ == '__main__':
#     send_mail(
#         '主题',
#         '内容',
#         'wangboc@cuz.edu.cn',
#         ['447537045@qq.com'],
#     )

# # HTML格式邮件
import os
from django.core.mail import EmailMultiAlternatives

os.environ['DJANGO_SETTINGS_MODULE'] = 'DBCP.settings'

if __name__ == '__main__':
    subject, from_email, to = '主题测试', 'wangboc@cuz.edu.cn', '447537045@qq.com'
    text_content = '欢迎访问www.xxxxx.com，这里是xx站点，专注于xx技术的分享！'
    html_content = '<p>欢迎访问<a href="http://www.baidu.com" target=blank>www.xxx.com</a>，这里是xx的站点，专注于xx技术的分享！</p>'
    code='s'
    html_content = '<p>欢迎注册<a href="http://{}/confirm/?code={}" target=blank>www.xxx.com</a>，这里是xx的站点，专注于xx技术的分享！</p>'.format(
        '127.0.0.1', code, 7)
    msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
    msg.attach_alternative(html_content, "text/html")
    msg.send()
