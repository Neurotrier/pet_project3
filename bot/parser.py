import aiohttp
from bs4 import BeautifulSoup

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
    "Accepted-Language": "ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7",
}


def lasting_convert(lasting):
    lst = lasting.split(" ")
    minutes = 0
    for i in lst:
        if i[-1] == "m":
            minutes += int(i[:-1])
        elif i[-1] == "h":
            minutes += int(i[:-1]) * 60
    return minutes


async def film_preview(film):
    film_name = film.find("h3", class_="ipc-title__text").text.split(" ", 1)[1].replace(":", "")
    lst = film.find("div", class_="ipc-metadata-list-summary-item__tc").find("div").find_all("div")[1].find_all("span")
    film_lasting = lasting_convert(lst[1].text)
    film_ref = film.find("a")["href"].split("?")[0]
    return {"name": film_name, "lasting": film_lasting, "ref": film_ref}


async def get_films(lasting=None):
    url = "https://m.imdb.com/chart/top/?ref_=nv_mv_250"
    async with aiohttp.ClientSession() as session:
        response = await session.get(url=url, headers=headers)
        soup = BeautifulSoup(await response.text(), "lxml")
        films_list = soup.find("div", class_="ipc-page-grid ipc-page-grid--bias-left").find("div").find("ul").find_all(
            "li")
        films = []
        for row_film in films_list:
            film = await film_preview(row_film)
            if lasting is not None:
                if film["lasting"] >= int(lasting):
                    films.append(film)
            else:
                films.append(film)
        return films


async def get_film(film):
    async with aiohttp.ClientSession() as session:
        response = await session.get(url="https://m.imdb.com" + film['ref'], headers=headers)
        soup = BeautifulSoup(await response.text(), "lxml")
        lst = soup.find_all("a", class_="ipc-link ipc-link--baseAlt ipc-link--inherit-color")
        film["year"] = lst[-2].text
        film["lasting"] = lasting_convert(soup.find_all("li", class_="ipc-inline-list__item")[6].text)
        film["name"] = soup.find("h1").find("span").text
        film["rating"] = soup.find_all("span", class_="ipc-btn__text")[8].find("span").text
        image_url = "https://m.imdb.com" + soup.find("a", class_="ipc-lockup-overlay ipc-focusable")["href"]
        async with aiohttp.ClientSession() as ses:
            resp = await ses.get(url=image_url, headers=headers)
            sp = BeautifulSoup(await resp.text(), "lxml")
            film["image"] = sp.find_all("img")[1]["src"]
    return film


async def series_preview(series):
    series_name = series.find("h3", class_="ipc-title__text").text.split(" ", 1)[1].replace(":", "")
    lst = series.find("div", class_="ipc-metadata-list-summary-item__tc").find("div").find_all("div")[1].find_all(
        "span")
    series_lasting = int(lst[1].text.split(" ")[0])
    series_ref = series.find("a")["href"].split("?")[0]
    return {"name": series_name, "lasting": series_lasting, "ref": series_ref}


async def get_series(eps=None):
    url = "https://m.imdb.com/chart/toptv/?ref_=nv_tvv_250"
    async with aiohttp.ClientSession() as session:
        response = await session.get(url=url, headers=headers)
        soup = BeautifulSoup(await response.text(), "lxml")
        series_list = soup.find("div", class_="ipc-page-grid ipc-page-grid--bias-left").find("div").find("ul").find_all(
            "li")
        series = []
        for row_series in series_list:
            serie = await series_preview(row_series)
            if eps is not None:
                if serie["lasting"] >= int(eps):
                    series.append(serie)
            else:
                series.append(serie)
        return series


async def get_serie(serie):
    async with aiohttp.ClientSession() as session:
        response = await session.get(url="https://m.imdb.com" + serie['ref'], headers=headers)
        soup = BeautifulSoup(await response.text(), "lxml")
        lst = soup.find_all("a", class_="ipc-link ipc-link--baseAlt ipc-link--inherit-color")
        serie["year"] = lst[-2].text
        serie["name"] = soup.find("h1").find("span").text
        serie["rating"] = soup.find_all("span", class_="ipc-btn__text")[8].find("span").text
        image_url = "https://m.imdb.com" + soup.find("a", class_="ipc-lockup-overlay ipc-focusable")["href"]
        async with aiohttp.ClientSession() as ses:
            resp = await ses.get(url=image_url, headers=headers)
            sp = BeautifulSoup(await resp.text(), "lxml")
            serie["image"] = sp.find_all("img")[1]["src"]
    return serie
