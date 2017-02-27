import os
from bs4 import BeautifulSoup
import re
import urllib2
import json


class Manifest(object):

	def __init__(self):
		self.publications = []

	def to_json(self):
		print "writing manifest as json"
		with open('data/manifest.json','w') as f:
			f.write(json.dumps(self.publications))


class Tree(object):

	def __init__(self, filename):

		print "instantiating %s" % filename
		self.soup = BeautifulSoup(open('trees/%s' % filename))
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

	def __init__(self, filename):
		self.filename = filename
		self.soup = BeautifulSoup(open('data/details_html/%s' % self.filename))
		self.meta_table = self.soup.findAll('table')
		self.metadata = {
			'Title':None,
			'details_html_relative_path':'data/details_html/%s' % self.filename,
			'binary':{
				'relative_file_path':None,
				'downloaded':None
			}
		}


	def parse_metadata_from_table(self):

		# parse title
		self.metadata['Title'] = self.meta_table[0].text.strip()

		# extract details and append to dictionary
		rows = self.meta_table[1].findAll('tr')
		for row in rows:
			cols = row.find_all('td')			
			self.metadata[cols[0].text.strip()] = cols[1].text.strip()


	def check_if_downloaded(self):
		filename = self.metadata['URL'].split("/")[-1]
		filename_path = 'data/pdfs/%s' % filename
		print filename

		if os.path.exists(filename_path):
			print "file exists, skipping download"
			self.metadata['binary']['relative_file_path'] = filename_path
			self.metadata['binary']['downloaded'] = True

		else:
			print "downloading %s" % self.metadata['URL']
			try:
				response = urllib2.urlopen(self.metadata['URL'])
				with open(filename_path,'w') as f:
					f.write(response.read())
				self.metadata['binary']['relative_file_path'] = filename_path
				self.metadata['binary']['downloaded'] = True
			except:
				self.metadata['binary']['relative_file_path'] = False
				self.metadata['binary']['downloaded'] = False



# iterate through html pages, extract publication details
def get_all_publication_details():
	
	trees = [ f for f in os.listdir('trees') if f.endswith('.html') ]
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
				tree.details_write_fail.append(pub.id)



def download_and_parse(m):
	files = os.listdir('data/details_html')
	for details_html in files:
		print details_html
		dpub = DetailsPublication(details_html)

		# generate metadata
		dpub.parse_metadata_from_table()

		# check download
		dpub.check_if_downloaded()

		# append to manifest
		m.publications.append(dpub.metadata)



# as script
if __name__ == '__main__':

	# final run to assemble
	m = Manifest()

	# download all pdfs and parse
	download_and_parse(m)

	# write to file
	m.to_json()












