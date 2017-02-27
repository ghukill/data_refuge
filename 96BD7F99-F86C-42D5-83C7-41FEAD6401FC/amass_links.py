import os
from bs4 import BeautifulSoup
import re
import urllib2


class Tree(object):

	def __init__(self, filename):

		print "instantiating %s" % filename
		self.soup = BeautifulSoup(open('data/trees/%s' % filename))
		self.details_write_fail = []

	def get_pubs(self):
		table = self.soup.findAll("table", { "class" : "data_new" })
		table.pop(0)
		return table


class TopicPublication(object):

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
		print "wrote %s to disk." % self.id
		return True

class DetailsPublication(object):

	def __init__(self, pub_details_filename):
		self.filename = pub_details_filename
		self.soup = BeautifulSoup(open('data/pub_details/%s' % self.filename))
		self.meta_table = self.soup.findAll('table')
		self.metadata = {
			'Title':None
		}


	def parse_metadata_from_table(self):

		# parse title
		self.metadata['Title'] = self.meta_table[0].text.strip()

		# extract details and append to dictionary
		rows = self.meta_table[1].findAll('tr')
		for row in rows:
			cols = row.find_all('td')			
			self.metadata[cols[0].text.strip()] = cols[1].text.strip()




# iterate through html pages, extract publication details
def get_all_publication_details():
	
	trees = [ f for f in os.listdir('data/trees') if f.endswith('.html') ]
	print trees
	for tree in trees:

		print "working on %s" % tree

		# instantiate Tree
		tree = Tree(tree)

		# iterate through pubs on page
		for pub in tree.get_pubs():

			publication = TopicPublication(pub)

			# write pub details to disk
			try:
				publication.write_details_to_disk()
			except:
				print "########### ERROR ############"
				tree.details_write_fail.append(pub.id)





# as script
# if __name__ == '__main__':



