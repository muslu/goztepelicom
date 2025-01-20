import json
from datetime import datetime, timedelta

import redis
import requests
import tornado.ioloop
import tornado.web

# Redis Bağlantısı
redis_client = redis.StrictRedis(host='goztepeli.com', port=6379, password='dD5Yz6xE5m', decode_responses=True)

# API Bilgileri
API_URL = "https://api.collectapi.com/sport/league?data.league=super-lig"
HEADERS = {
    'content-type': "application/json",
    'authorization': "apikey 1G5HqgQXJ4W3saJspMJTVT:7cuUTEsc6OyE55ewv64Umj"
}


# Göztepe'yi Kalın Yapacak HTML
def highlight_goztepe(teams_json):
    html = "<table border='1' style='width:100%; text-align:left;'>"
    html += "<tr><th>Sıra</th><th>Takım</th><th>Puan</th><th>Oynanan Maç</th></tr>"
    for team in teams_json:
        # Eksik anahtarlar için varsayılan değerler ekleyin
        rank = team.get("rank", "Bilinmiyor")
        team_name = team.get("team", "Bilinmiyor")
        points = team.get("points", "0")  # Varsayılan puan 0
        played = team.get("played", "0")  # Varsayılan oynanan maç 0

        # Göztepe'yi kalın yaz
        if "Göztepe" in team_name:
            team_name = f"<b>{team_name}</b>"

        html += f"<tr><td>{rank}</td><td>{team_name}</td><td>{points}</td><td>{played}</td></tr>"
    html += "</table>"
    return html


# Puan Durumu Güncelleme
def update_puan_durumu():
    response = requests.get(API_URL, headers=HEADERS)
    if response.status_code == 200:
        data = response.json()
        print(data["result"])  # JSON yapısını görmek için

        redis_client.set("puan_durumu", json.dumps(data["result"]))
        redis_client.set("last_update", str(datetime.now()))
    else:
        print(f"API Hatası: {response.status_code}")


# Tornado Handler
class MainHandler(tornado.web.RequestHandler):
    def get(self):
        # Redis'ten Puan Durumu Verilerini Al
        puan_durumu = redis_client.get("puan_durumu")
        last_update = redis_client.get("last_update")

        if not puan_durumu:
            self.write("<p>Puan durumu verisi bulunamadı. Lütfen daha sonra tekrar deneyin.</p>")
            return

        teams = json.loads(puan_durumu)
        html = highlight_goztepe(teams)

        self.write(f"<h1>Trendyol Süper Lig 2024-2025 Puan Durumu</h1>")
        self.write(f"<p>Son Güncelleme: {last_update}</p>")
        self.write(html)


# Tornado Uygulaması
def make_app():
    return tornado.web.Application([(r"/puan-durumu", MainHandler), ])


if __name__ == "__main__":
    # İlk Veri Güncellemesi
    if not redis_client.get("puan_durumu"):
        update_puan_durumu()


    # Günlük Veri Güncelleyici
    def daily_update():
        print("Puan durumu verisi güncelleniyor...")
        update_puan_durumu()


    # Günlük Güncelleme Planlama
    ioloop = tornado.ioloop.IOLoop.current()
    now = datetime.now()
    next_update = datetime.combine(now + timedelta(days=1), datetime.min.time())
    delay = (next_update - now).total_seconds()
    tornado.ioloop.PeriodicCallback(daily_update, delay * 1000).start()

    # Tornado Uygulamasını Başlat
    app = make_app()
    app.listen(8888)
    print("Server is running at http://localhost:8888")
    ioloop.start()
