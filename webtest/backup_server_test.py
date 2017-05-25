import tornado
import tornado.ioloop
import tornado.web

import os
import sys
import requests
from PIL import Image

sys.path.append('..')
import cls_web_test

#import random
#import string


__UPLOADS__ = './uploads/'
#RAN_LETTERS_DIGITS = string.ascii_letters + string.digits
#rld = ''.join(random.sample(RAN_LETTERS_DIGITS, 6))
#f_name = 'your_image_' + rld


class MainHandler(tornado.web.RequestHandler):
    def get(self):
        self.render("main_page.html")


class FileHandler(tornado.web.RequestHandler):
    def post(self):
        if self.get_arguments('urlarg'):
            u_name = self.get_arguments('urlarg')[0]
            print 'url :', u_name
            f_name = os.path.basename(u_name)
            f_name = f_name.split('?')[0]
            print 'file_name :', f_name
            response = requests.get(u_name)
            if response.status_code == 200:
                f = open(__UPLOADS__ + f_name, 'wb')
                f.write(response.content)
                f.close()
            t5res = cls.get_info(__UPLOADS__ + f_name)
        else:
            f_info = self.request.files['filearg'][0]
            f_name = f_info['filename']
            print 'file_name :', f_name
            f = open(__UPLOADS__ + f_name, 'wb')
            f.write(f_info['body'])
            f.close()
            t5res = cls.get_info(__UPLOADS__ + f_name)

        self.render('result_page.html', file_name=__UPLOADS__ + f_name,
                    cls_results='Top5 Classification Results',
                    items=t5res)




application = tornado.web.Application([
            (r"/", MainHandler),
            (r'/result', FileHandler),
            (r"/uploads/(.*)", tornado.web.StaticFileHandler, {'path': __UPLOADS__})
            ], debug=True)


if __name__ == "__main__":
    cls = cls_test.CLS()
    application.listen(8888)
    tornado.ioloop.IOLoop.instance().start()
