import tornado
import tornado.ioloop
import tornado.web
import tornado.httpclient

import sys
import requests
import base64

from StringIO import StringIO
from io import BytesIO
from PIL import Image

sys.path.append('..')
import web_classification


class MainHandler(tornado.web.RequestHandler):
    def get(self):
        self.render("main_page.html")


class FileHandler(tornado.web.RequestHandler):
    @tornado.web.asynchronous
    def post(self):
        if self.get_arguments('urlarg'):
            self.u_name = self.get_arguments('urlarg')[0]
            http_client = tornado.httpclient.AsyncHTTPClient()
            http_request = tornado.httpclient.HTTPRequest(url=self.u_name, request_timeout=50.0, connect_timeout=50.0)
            http_client.fetch(http_request, self.handle_response)
            print 'url Test : fetch finish!!'
        else:
            f_info = self.request.files['filearg'][0]
            u_name = "data:image/jpg;base64," + base64.b64encode(BytesIO(f_info['body']).getvalue())
            img = Image.open(StringIO(f_info['body']))
            top5_res = cls.get_info(img)
            self.render('result_page.html', file_name=u_name,
                        cls_results='Top5 Classification Results',
                        items=top5_res)

    def handle_response(self, response):
        if response.error:
            print 'url error : %s' % response.error
        elif response.code == 200:
            img = Image.open(StringIO(response.body))
            top5_res = cls.get_info(img)
            self.render('result_page.html', file_name=self.u_name,
                        cls_results='Top5 Classification Results',
                        items=top5_res)
            print 'url Test : Render process complete!!'



application = tornado.web.Application([
            (r"/", MainHandler),
            (r'/result', FileHandler),
            ], debug=True)


if __name__ == "__main__":
    cls = web_classification.CLS()
    application.listen(8888)
    tornado.ioloop.IOLoop.instance().start()
