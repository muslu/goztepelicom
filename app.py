import requests
import tornado.ioloop
import tornado.web
from bs4 import BeautifulSoup


class MainHandler(tornado.web.RequestHandler):
    def get(self):
        self.render("index.html")


class PuanDurumuHandler(tornado.web.RequestHandler):
    def get(self):
        url = "https://www.tff.org/Default.aspx?pageId=198"
        response = requests.get(url)
        response.encoding = "utf-8"  # Türkçe karakter desteği için
        soup = BeautifulSoup(response.text, "html.parser")

        # İlgili tabloyu seç
        table = soup.find("table", {"class": "alanlar2 marginB"})

        if table:
            self.write(table.prettify())  # Tabloyu HTML olarak döndür
        else:
            self.write("<p>Puan durumu tablosu bulunamadı.</p>")


def make_app():
    return tornado.web.Application(
        [
            (r"/", MainHandler),
            (r"/puan-durumu", PuanDurumuHandler),
        ],
        static_path="static",
        template_path="templates",
    )


if __name__ == "__main__":
    app = make_app()
    app.listen(8888)
    print("Server running at http://localhost:8888")
    tornado.ioloop.IOLoop.current().start()
