#General URL scraper class using BeautifulSoup
#create an instance along with url base and scrape several items from one base page (soup item)
#items from pages are scraped via scrapeSubItem and scrapeSubItems methods
from urllib.request import Request, urlopen
from bs4 import BeautifulSoup

class Scraper:
    def __init__(self, base_url):
        if base_url:
            print("Initializing Scraper")
            self.urlbase = base_url
            self.header = {'User-Agent':'Mozilla/6.0'}
        else:
            print(str(base_url) + " is not a valid base URL for scraping.")
            self.urlbase = "http://"
            self.header = {'User-Agent':'Mozilla/6.0'}

    #Set base url
    def setBaseUrl(self, base_url):
        if base_url:
            self.urlbase = base_url
        else:
            print(str(base_url) + " is not a valid base URL for scraping.")
            self.urlbase = "http://"

    #Set base header for url request (needed for most webpages to not reject request)
    def setHeader(self, header):
        self.header = header

    #Initializes scraping of webpage and storing to basesoup
    def scrapeBase(self):
        self.basereq = Request(self.urlbase,headers = self.header)
        self.basepage = urlopen(self.basereq)
        self.basesoup = BeautifulSoup(self.basepage,"html.parser")

    #Scrape one item using soup.find()
    def scrapeSubItem(self, component, attributes, returntype = "soup", retattr = "href", soup = None):
        if soup is None:
            soup = self.basesoup
        item = soup.find(component, attrs=attributes)
        if returntype == "text":
            return item.text
        if returntype == "attribute":
            return item.attrs[retattr]
        return item

    #Scrape several soup items using find()
    def scrapeSubItems(self, component, attributes, returntype = "soup", soup = None):
        if soup is None:
            soup = self.basesoup
        items = soup.find_all(component, attrs=attributes)
        if returntype == "text":
            return [i.text for i in items]
        return items

    #Get specific information from a set of soup items, returns a dict on same form as the input
    def scrapeInfo(self, soup_items, information_dict):
        returnDict = {k:"" for k in information_dict}
        for i in soup_items:
            tstring = i.text
            print(tstring)
            for k in information_dict:
                ival = information_dict[k]
                if ival in tstring:
                    returnDict[k] = tstring.replace(ival,"").replace("\xa0","").strip()
        return returnDict

    #Run scraping and print
    def scrapeAndPrint(self, component, attributes, returntype, information_dict):
        soup_items = self.scrapeSubItems(component,attributes,returntype,soup=subitem)
        retval = self.scrapeInfo(soup_items,information_dict)
        print(retval)
