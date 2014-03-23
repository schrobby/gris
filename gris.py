import requests
from bs4 import BeautifulSoup

BASE_URL = "https://www.google.com"
USER_AGENT = "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.11\
            (KHTML, like Gecko) Chrome/23.0.1271.97 Safari/537.11"
RES_OPTIONS = ['All sizes', 'Middle', 'Large']

def search_by_url(image_url, timeout=None):
    """ Creates a SearchResults object for the specified image URL """
    return SearchResults(image_url=image_url, timeout=timeout)

class SearchResults:
    """ Contains the search results of the GRIS query """

    def __init__(self, image_url=None, timeout=None):
        self.best_guess = None
        self.timeout = 10 if timeout is None else timeout
        self.res_urls = dict()
        for i in RES_OPTIONS:
            self.res_urls[i] = None

        if image_url:
            self.__get_results_for_image(image_url=image_url)
        else:
            raise ValueError("Invalid image URL")

    def __get_results_for_image(self, image_url=None):
        headers = {'User-Agent': USER_AGENT}
        params = {'image_url': image_url}

        r = requests.get(BASE_URL + "/searchbyimage", headers=headers, params=params, timeout=self.timeout)
        soup = BeautifulSoup(r.text)

        for link in soup.find(id="topstuff").findAll("a"):
            if link.text in RES_OPTIONS:
                self.res_urls[link.text] = link.attrs['href']
            elif link.text:
                self.best_guess = link.text

if __name__ == "__main__":
    import sys

    urls_string = ""
    results = search_by_url(sys.argv[1])

    for k, v in results.res_urls.iteritems():
        urls_string += "\t%s: %s\n" % (k, v) if v else ""
    print("Tags: %s" % results.best_guess)
    print("URLs:\n" + urls_string if urls_string else "")
