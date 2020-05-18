import requests

class Car:
    mileage = None
    price = None
    year = None
    title = None

    def __init__(self, mileage, price, year, title):
        self.mileage = mileage
        self.price = price
        self.year = year
        self.title = title
    
    def summary(self):
        print(mileage + "\t" + price + "\t" + year + "\t" + title)


def getPageContents(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/46.0.2490.80 Safari/537.36',
        'Content-Type': 'text/html',
    }
    response = requests.get(url, headers=headers)
    return(response.text)


def processingPage(html):
    nextMileage = False
    nextTitle = False
    mileage = []
    price = []
    year = []
    title = []

    for line in html.splitlines():
        if nextMileage:
            nextMileage = False
            mileage.append(line.split(" ")[-2].replace(",", ""))
        if nextTitle:
            nextTitle = False
            title.append(line.strip(" "))
            year.append(line.strip(" ")[:4])
        if line.find("<div class=\"kms\">") > 0:
            nextMileage = True
        if line.find("<span itemprop=\"itemOffered\">") > 0 or line.find("<span class=\"result-title\">") > 0:
            nextTitle = True
        if line.find("<span class=\"price-amount\">") > 0:
            price.append(line.strip(" ")[28: -7])
    
    return mileage, price, year, title


def listsToObjects(mileage, price, year, title):
    cars = []
    for i in range (0, len(mileage)):
        cars.append(Car(mileage[i], price[i], year[i], title[i]))
    return cars


# ------------------- MAIN METHOD -------------------
url = "https://www.autotrader.ca/cars/bmw/3%20series/on/burlington/?rcp=15&rcs=0&srt=4&prx=100&prv=Ontario&loc=l7l3x5&hprc=True&wcp=True&sts=New-Used&inMarket=basicSearch"

#url = input("Input filtered URL: ")

# Getting initial rcs value
rcs = int(url[url.find("rcp="):][4:url[url.find("rcp="):].find("&")])
url = url.replace(url[url.find("rcs="):][:url[url.find("rcs="):].find("&") + 1], "") + "&rcs=" + str(rcs)
multiplier = 0
total = []

for i in range (1, 50):
    # Loop through all pages
    url = url[:url.find("&rcs")] + "&rcs=" + str(rcs * i)
    html = getPageContents(url)
    mileage, price, year, title = processingPage(html)
    cars = listsToObjects(mileage, price, year, title)
    total.extend(cars)

for model in total:
    print(model[0].mileage, model[0].price, model[0].year, model[0].title)