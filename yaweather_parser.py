import webbrowser
import urllib.request
import json
import time
import requests
import urllib
import urllib.parse


html_page = None
headers = {}
headers['User-1gent'] = "Mozilla/5.0 (X11; Linux i686) AppleWebKit/537.17 (KHTML, like Gecko) Chrome/24.0.1312.27 Safari/537.17"
headers["X-Yandex-API-Key"] = "94c88e57-a2df-4706-8a71-7e1ff43b692b"


Points = [ [0] * 14  for i in range(3)]
Coordinates = [0] * 3
Coordinates[0] = [55.7443330, 37.622608]
Coordinates[1] =[-33.890876, 151.207664]
Coordinates[2] = [-22.833287, -43.291860]
Coor_rect = [0] * 3
Coor_rect[0] = [37.546858,55.698148,37.546858,55.789773,37.697264,55.789773,37.697264,55.698148,37.546858,55.698148]
Coor_rect[1] = [151.203838,-33.885104,151.203838,-33.874297,151.217586,-33.874297,151.217586,-33.885104,151.203838,-33.885104]
Coor_rect[2] = [-43.307968, -22.848086,-43.307968,-22.811683,-43.276539,-22.811683,-43.276539,-22.848086,-43.307968, -22.848086]

def forecast():
    global Points
    for y in range(3):
        url = "https://api.weather.yandex.ru/v1/forecast?lat=" + str(Coordinates[y][0]) + "&lon=" + str(Coordinates[y][1]) + "&limit=7&hours=true&extra=false"
        req = urllib.request.Request(url, headers=headers)
        resp = urllib.request.urlopen(req)
        html_page = resp.read()
        html_page = html_page.decode()
        d = json.loads(html_page)
        for i in range(7, 14):
            if d['forecasts'][i - 7]['parts']['day']['prec_mm'] > 0.1:
                Points[y][i] = True
            else:
                Points[y][i] = False


def main():
    global Points
    for i in range(3):
        Points[i] = Points[i][1:] + [0]

    forecast()


    for i in range(3):
        pour_today = False
        rain_day_last = -1
        for j in range(7):
            if Points[i][j]:
                rain_day_last = j
        if rain_day_last == -1:
            pour_today = True
        elif rain_day_last == 0:
            if Points[i][8] or Points[i][9]:
                pass
            else:
                pour_today = True

        if Points[i][7]:
            pour_today = False
        Points[i][7] = Points[i][7] or pour_today
        if pour_today:
            url_map = "https://static-maps.yandex.ru/1.x/?l=map&size=500,400&pl=c:f45642FF,f:e56f60A0,w:4," + ','.join(map(str, Coor_rect[i]))
            webbrowser.open(url_map)
        else:

            url_map = "https://static-maps.yandex.ru/1.x/?l=map&size=500,400&pl=c:85c124FF,f:9fdd3bA0,w:4," + ','.join(map(str, Coor_rect[i]))
            webbrowser.open(url_map)

    time.sleep(60)
    main()

main()








