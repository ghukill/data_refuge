import os
from bs4 import BeautifulSoup
import re


class Tree(object):

	def __init__(self, filename):

		print "instantiating %s" % filename
		self.soup = BeautifulSoup(open('data/trees/%s' % filename))


class Publication(object):

	def __init__(self, bs4_pub):

		print "instantiating publication chunk %s" % bs4_pub
		self.pub = bs4_pub
		self.a = self.pub.find('a')

		# debug
		print self.a



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

		# get table with links
		table = tree.soup.findAll("table", { "class" : "data_new" })

		# pop first
		table.pop(0)

		for pub in table:

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

