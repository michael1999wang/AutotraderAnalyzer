import requests
import matplotlib.pyplot as plt

class Car:
    mileage = None
    price = None
    year = None
    title = None

    def __init__(self, mileage, price, year, title):
        self.mileage = int(mileage)
        self.price = int(price)
        self.year = int(year)
        self.title = title
    
    def summary(self):
        print(str(self.mileage) + "\t" + str(self.price) + "\t" + str(self.year) + "\t" + self.title)


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
            price.append(line.strip(" ")[28: -7].replace(",", ""))
    
    return mileage, price, year, title


def listsToObjects(mileage, price, year, title):
    cars = []
    for i in range (0, len(mileage)):
        cars.append(Car(mileage[i], price[i], year[i], title[i]))
    return cars


def visualize(cars):
    fig = plt.figure(figsize=(20,10))
    ax = fig.add_subplot(111, projection='3d')

    for car in cars:
        ax.scatter(car.year, car.mileage, car.price, color="r")

    ax.set_xlabel('Year')
    ax.set_ylabel('Mileage')
    ax.set_zlabel('Price')

    plt.show()


# ------------------- MAIN METHOD -------------------

# User input of URL (or constant url for 3-series to test)
url = "https://www.autotrader.ca/cars/bmw/3%20series/on/burlington/?rcp=15&rcs=0&srt=4&prx=100&prv=Ontario&loc=l7l3x5&hprc=True&wcp=True&sts=New-Used&inMarket=basicSearch"
# url = input("Input filtered URL: ")

# Getting initial rcs value
rcs = int(url[url.find("rcp="):][4:url[url.find("rcp="):].find("&")])
url = url.replace(url[url.find("rcs="):][:url[url.find("rcs="):].find("&") + 1], "") + "&rcs=" + str(rcs)
rcs = 15
total = []

# Optional user pages
pages = 50
# pages = int(input("Number of pages:")) - 1

# Looping through x top pages
for i in range (0, pages):
    # Loop through all pages
    url = url[:url.find("&rcs")] + "&rcs=" + str(rcs * i)
    print(url)
    html = getPageContents(url)
    total.extend(listsToObjects(processingPage(html)[0], processingPage(html)[1], processingPage(html)[2], processingPage(html)[3]))

# Debugging line
# for i in range(0, 100):
#     total[i].summary()

# MACHINE LEARNING
visualize(total)