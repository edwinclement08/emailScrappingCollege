import re
from pprint import pprint
import requests
from bs4 import BeautifulSoup
import urlparse
import base64

emailValidationRegEx = re.compile(r"""[a-z0-9!#$%&'*+/=?^_`{|}~-]+(?:\.[a-z0-9!#$%&'*+/=?^_`{|}~-]+)*@(?:[a-z0-9](?:[a-z0-9-]*[a-z0-9])?\.)+(?:[A-Z]{2}|com|org|net|gov|mil|biz|info|mobi|name|aero|edu|jobs|museum)""")




image_list = "tif tiff gif jpeg jpg jif jfif jp2 jpx j2k j2c fpx pcd png pdf".split()

class Crawler:
    donePages = []
    toDoPages = []

    def __init__(self, root):
        self.root = root[0]
        self.file = open(base64.urlsafe_b64encode(self.root), 'w')
        rootDomain = [urlparse.urljoin(self.root, '/').strip()]

        self.output = open("emails-" + "".join(x for x in rootDomain[0] if x.isalnum()) + ".txt", 'w')
        self.file.write(self.root + '\n')

        self.emails = set()


        self.toDoPages.append(self.root)
        self.crawler(10000)

    def crawler(self,  maxPages):
        page = 1
        while len(self.toDoPages) > 0 and page < maxPages:
            url = self.toDoPages.pop()
            if not url in self.donePages:
                self.donePages.append(url)


                j = url.split('.')[-1]
                if j.lower() not in ['pdf', 'bmp',  'jpeg'] + image_list:
                    # print "Running Crawler on :", url
                    source = requests.get(url).text
                    soup = BeautifulSoup(source, "html.parser")

                    l = soup.text.encode('ascii','ignore')
                    # self.file.write(l)



                    self.getAllLinks(soup)

                    # the actual searching of emails
                    gg = l
                    op = emailValidationRegEx.findall(l)
                    # print op
                    for i in op:
                        if i not in self.emails:
                            self.emails.add(i)
                            self.output.write(i)
                            self.output.write('\n')
                            print i
                            self.output.flush()



                    page += 1

    def getAllLinks(self, pageSoup):
        links = [g['href'] for g in pageSoup.findAll("a", {'href': True})]
        links = [ k for k in links if (k[0] in ['/', 'h'] and len(k) > 1)]

        # absoluteLinks = [urlparse.urljoin(self.root, path) if path[0] == '/' else path for path in links]
        absoluteLinks = []
        for path in links:
            if path[0] == '/':
                absoluteLinks.append(urlparse.urljoin(self.root, path))
            else:
                absoluteLinks.append(path)

        absoluteLinksFiltered = []
        # rootDomain = '{uri.netloc}'.format(uri=urlparse.urlparse(self.root))
        # for m in absoluteLinks:
        #     domain = '{uri.netloc}'.format(uri=urlparse.urlparse(m))
        #
        #     print domain == rootDomain
        #     if domain == rootDomain:
        #         absoluteLinksFiltered.append(m)
        #     else:
        #         print m + " not of this domain"
        rootDomain = [urlparse.urljoin(self.root, '/').strip()]
        if(rootDomain[0] == 'http://www.vit.edu.in/'):
            rootDomain.append('http://vit.edu.in/')
        for m in absoluteLinks:
            domain = urlparse.urljoin(m, '/')
            if domain in rootDomain:
                absoluteLinksFiltered.append(m)
            else:

                k = m.split("//")
                if k > 1: # there is scheme
                    p = '//'.join([k[0], k[1].split('/')[0]]).strip(' /') + '/'
                else:
                    p = k[1].split('/')[0]

                # print p, rootDomain, p in rootDomain
                if (p in rootDomain):
                    absoluteLinksFiltered.append(m)
                else:
                    # print m + " not of this domain"
                    pass
        [self.file.write(i + '\n') for i in absoluteLinksFiltered]
        self.toDoPages += absoluteLinksFiltered





listOfSites = [k.strip() for k in """http://www.vit.edu.in/faculty/rajashree-soman
http://www.vit.edu.in
http://www.acpce.org
http://www.pvppcoe.ac.in 
http://www.shahandanchor.com
https://www.tcetmumbai.in
http://www.atharvacoe.ac.in
http://www.spce.ac.in
http://www.spit.ac.in
http://www.bvcoenm.org.in
http://www.dmce.edu
http://www.dbit.in
http://www.umit.ac.in
http://www.acpce.org 
http://www.somaiya.edu/kjsieit
http://ltce.ltjss.net
 http://www.mgmmumbai.ac.in/mgmcet/index.html
 http://www.pvppcoe.ac.in
 http://www.rait.ac.in
http://www.saraswatiengg.org
http://www.terna.org/2
 http://www.tsec.edu
 http://www.vit.edu.in
 https://ves.ac.in/vesit
""".split('\n') if k][:2]

responseArray = []
retryArray = []

pprint(listOfSites)

for site in listOfSites:
    try:
        r = requests.get(site, timeout=5)
    except Exception as e:
        print e
        retryArray.append((site, e))
    print site, r
    responseArray.append((site, r))

print "NUMBER OF SITES LEFT?? " + str(len(listOfSites) - (len(responseArray) + len(retryArray)))
print "WHAT SITES ARE LEFT"
pprint(retryArray)

for site in responseArray[:1]:
    Crawler(site)

