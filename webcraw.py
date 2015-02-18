import re
import sys
import bs4
import requests
from collections import defaultdict
from xml.etree.ElementTree import *


class Crawler():
	DEFAULT_PAGE = "http://www.gourmet.com/search/query?query="
	DOMAIN_PAGE = "http://www.gourmet.com"

	def __init__(self):
		pass

	@staticmethod
	def gourmet():
		concentrate_tag_list = ['results', 'result']
		class_compile = "info"
		doc_tags = ['title', 'contributor' ,'category', 'date', 'keywords']
		return concentrate_tag_list



	STYLES = {"Gourmet" : gourmet.__func__()}

	def search(self, search, article_list = []): 
		base_url = Crawler.DOMAIN_PAGE if article_list else Crawler.DEFAULT_PAGE

		search_url = base_url + search
		response = requests.get(search_url)
		soup = bs4.BeautifulSoup(response.content)

		body = soup.find("div", {"class" : "results"}).find_all("div", {"class" : "result"})
		result_list = [res.find("div", {"class" : re.compile("info")}) for res in body]
		count = 0
		for res in result_list:
			article = defaultdict(str)
			try:
				title_info = res.find("h3", {"class" : True}).find("a")
				article['title'] = title_info.getText().encode('utf-8')
				article['url'] = title_info['href']
			except KeyError:
				print ("Article without url and title is not valid {url} in result list {line}: ").format(url=search_url, line=count)
				count += 1
				continue
			
			article['date'] = res.find("div", {"class" : re.compile("date")})
			article['category'] = res.find("h5", {"class" : True})
			article['contributor'] = res.find("div", {"class" : "contributor"})
			try:
				keywords = res.find("div", {"class" : "keywords"}).find_all("dd")
				keywords = [keyword.contents[0].string for keyword in keywords]
				keywords = ';'.join(keywords)
				article['keywords'] = keywords

			except:
				article['keywords'] = None
			count += 1
			article_list.append(article)
		nextpage = soup.find("span", {"class" : re.compile("paginationNext")})
		try:
			if "off" in nextpage['class'][0]:
				return article_list
			else:
				search = nextpage.contents[0]['href']
				self.search(search, article_list)

		except KeyError, TypeError:
			return article_list
		return article_list
		


	def extract_content(self, url):
		f = open('test.txt', 'w')
		response = requests.get(url)
		soup = bs4.BeautifulSoup(response.content)
		paragraphs = soup.find("div", {"class" : "text"}).find_all("p")
		articles = ''
		for p in paragraphs:
			parts = p.contents
			#sentences = [part.string for part in parts]
			sentences = [' '.join(part.string.split(' ')) for part in parts]
			for s in sentences:
				f.write(str(s.encode('utf-8')))
			#print sentences
		f.close()

	def write_xml(self, articles, filename):
		#for article in articles:

		#print articles[0].keys()
		#article is a wrapped 'object' which includes the article's attributes and url
		#for article in articles:
		article = articles[0]

			

	

def main():
	crawler = Crawler()
	articles = crawler.search("Italy")
	crawler.write_xml(articles, 'test.xml')
	#crawler.extract_content('http://www.gourmet.com/food/gourmetlive/2012/103112/welcome-italian-2012')
	



if __name__ == '__main__':
    sys.exit(main())	