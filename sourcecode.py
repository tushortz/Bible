# Importing necessary modules
from urllib.request import urlopen
import os, re

# Declaring necessary variables
homepage = "http://www.centralbaptistfwb.com/bible/"
page_content = str(urlopen(homepage).read())
bookdict = {}

# Extracting data online to be stored in `result`
result = re.findall(r'<li><a href="/bible/[\'"]?([^\'" >]+)/">', page_content)

# Function to create and write bible verses into file
def writepack(link, maindir):
	each_link = homepage + link
	page_content = str(urlopen(each_link).read())

	chapters = re.findall(r'">[\'"]?([^\'" >]+)</a></li>', page_content)
	chapters.remove("Bible")
	
	for chapter_no in chapters:
		filename = "Chapter " + chapter_no + ".txt"
		chp_link = "%s/%s/" % (each_link, chapter_no)
		chp_content = str(urlopen(chp_link).read())

		# print(chp_content)
		chp_res =  re.findall(r'<dd>[\w\s&#,\:\?\.\;\[\]\(\)\-\_\'\"\!]+', chp_content)

		filepath = os.path.join(maindir, filename)

		verse = 0
		with open(filepath, "w") as chp:
			for x in chp_res:
				x = x.replace("<dd>", "").replace("&#39;", "'")

				verse += 1
				chp.write("\n%s %s:%s --> %s \n" % (maindir, chapter_no, verse, x))
			print(maindir + " " + str(filename) + " created")
		
for x in result:
	y = x.title()
	y = y.replace("-", " ")
	bookdict[x] = y

	if not os.path.exists(y): os.makedirs(y)
	writepack(x, y)
