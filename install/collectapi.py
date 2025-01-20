import http.client

conn = http.client.HTTPSConnection("api.collectapi.com")

headers = {
    'content-type': "application/json",
    'authorization': "apikey 1G5HqgQXJ4W3saJspMJTVT:"
    }

conn.request("GET", "/sport/league?data.league=super-lig", headers=headers)

res = conn.getresponse()
data = res.read()

print(data.decode("utf-8"))