import re
import sys
import bs4
import requests
from collections import defaultdict
from xml.etree import ElementTree
from xml.etree.ElementTree import *
from xml.dom import minidom



class Crawler():
	#or search based on category "Chef & Categories.... Magazines"
	DEFAULT_PAGE = "http://www.gourmet.com/search/query?query="
	DOMAIN_PAGE = "http://www.gourmet.com"

	def __init__(self):
		pass


           #this part is so crappy...
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
			
			article['date'] = res.find("div", {"class" : re.compile("date")}).getText()
			article['category'] = res.find("h5", {"class" : True}).getText().encode('utf-8')
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
		url = Crawler.DOMAIN_PAGE + url
		#print url
		try:
			response = requests.get(url)
			soup = bs4.BeautifulSoup(response.content)
			paragraphs = soup.find("div", {"class" : "text"}).find_all("p")
		except:
			print 'Enable open webpage or find contents'
			return ' '

		try:
			sentences = []
			for p in paragraphs:
				contents = p.contents
				sentence = [' '.join(part.string.split(' ')).encode('utf-8') if part.string else '' for part in contents]
				sentences.append(sentence)
			sentences = str([' '.join(sentence) for sentence in sentences])
			#TODO: implement a filtering for the decode, unicode staff
			#But now at least it can be written to the xml....
			return sentences
			f.close()
		except IOError: 
			"Exception"
			return ' '

	@staticmethod
	def prettify(elem):
		rough_string = tostring(elem, 'utf-8', method='xml')
		reparsed = minidom.parseString(rough_string)
		return reparsed.toprettyxml(indent="   ")

	

	#TODO: also change this part
	def write_xml(self, articles, filename):
		f = open(filename, 'w')
		if not articles:
			print 'No staff to write to file'
			sys.exit(1)
		xml = Element('Gourmet')
		doc_attributes_list = articles[0].keys()
		for article in articles:
			doc = SubElement(xml, 'doc')
			for attribute in doc_attributes_list:
				node = SubElement(doc, attribute)
				if attribute == 'url':
					node.text = self.extract_content(article[attribute])
				else:
					node.text = article[attribute].decode('utf-8') if article[attribute] else ' '
				print 
		f.write(Crawler.prettify(xml).encode('utf-8'))
		f.close()

	

def main():
	crawler = Crawler()
	articles = crawler.search("Italy")
	crawler.write_xml(articles, 'test.xml')
	#crawler.extract_content('http://www.gourmet.com/restaurants/2007/01/epi_colmans_italy')
	#'http://www.gourmet.com/food/gourmetlive/2012/103112/welcome-italian-2012')


	



if __name__ == '__main__':
    sys.exit(main())	