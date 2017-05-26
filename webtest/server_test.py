import tornado
import tornado.ioloop
import tornado.web

import sys
import requests
import base64

from StringIO import StringIO
from io import BytesIO
from PIL import Image

sys.path.append('..')
import cls_web_test


class MainHandler(tornado.web.RequestHandler):
    def get(self):
        self.render("main_page.html")


class FileHandler(tornado.web.RequestHandler):
    def post(self):
        if self.get_arguments('urlarg'):
            u_name = self.get_arguments('urlarg')[0]
            response = requests.get(u_name)
            if response.status_code == 200:
                img = Image.open(StringIO(response.content))
            top5_res = cls.get_info(img)
        else:
            f_info = self.request.files['filearg'][0]
            u_name = "data:image/jpg;base64," + base64.b64encode(BytesIO(f_info['body']).getvalue())
            img = Image.open(StringIO(f_info['body']))
            top5_res = cls.get_info(img)

        self.render('result_page.html', file_name=u_name,
                    cls_results='Top5 Classification Results',
                    items=top5_res)


application = tornado.web.Application([
            (r"/", MainHandler),
            (r'/result', FileHandler),
            ], debug=True)


if __name__ == "__main__":
    cls = cls_web_test.CLS()
    application.listen(8888)
    tornado.ioloop.IOLoop.instance().start()
