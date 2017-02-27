import os
from bs4 import BeautifulSoup
import re
import urllib2


class Tree(object):

	def __init__(self, filename):

		print "instantiating %s" % filename
		self.soup = BeautifulSoup(open('data/trees/%s' % filename))

	def get_pubs(self):
		table = self.soup.findAll("table", { "class" : "data_new" })
		table.pop(0)
		return table


class Publication(object):

	def __init__(self, bs4_pub):

		print "instantiating publication chunk %s" % bs4_pub
		self.pub = bs4_pub
		
		# get main a tag
		self.a = self.pub.find('a')

		# get id
		self.id = re.findall(r'&id=([\d]+)', self.a.attrs['href'])[0]
		print self.id

		# derive details page
		self.details_url = 'https://www1.eere.energy.gov/library/viewdetails.aspx?productid=%s&Page=2' % (self.id)

	def write_details_to_disk(self):

		page_html = urllib2.urlopen(self.details_url).read()
		with open('data/pub_details/%s.html' % self.id, 'w') as f:
			f.write(page_html)





# as script
if __name__ == '__main__':

	# iterate through html pages
	trees = [ f for f in os.listdir('data/trees') if f.endswith('.html') ]
	print trees
	for tree in trees:

		print "working on %s" % tree

		# open as BeautifulSoup
		# soup = BeautifulSoup(open('trees/%s' % tree))
		tree = Tree(tree)

		# # get table with links
		# table = tree.soup.findAll("table", { "class" : "data_new" })

		# # pop first
		# table.pop(0)

		for pub in tree.get_pubs():

			publication = Publication(pub)

			# pub_dict = {}
			
			# get details link
			# a = pub.find('a')
			# URL = a.attrs['href'].replace("http://www1.eere.energy.gov/library/asset_handler.aspx?src=","")
			# URL = re.sub(r'&id=.*$','',URL)
			# print URL
			# pub_dict['URL'] = URL

			# # get id
			# a = pub.find('a')

			# # get title
			# pub_dict['title'] = a.text

			# get description

