import re
import urllib

pdflink = re.compile(r'href="(.*\.pdf)"')

with open('index.html','r') as f:
	for line in f:
		matches = re.findall(pdflink,line)
		if len(matches) > 0:
			pdf_url = matches[0]
			filename = pdf_url.split("/")[-1]
			urllib.urlretrieve(pdf_url,'../data/%s' % filename)

