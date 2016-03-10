# Only run with python 3 and above

# Importing necessary modules
from urllib.request import urlopen
import os, re

# Gets all books of the bible from an online source
homepage = "http://www.centralbaptistfwb.com/bible/"
source = urlopen(homepage).read().decode("utf-8")
bible_chapters = re.findall(r'<li><a href="/bible/(.*?)/">.*?</a></li>', source)

# Stores the number of chapters
book_info = {}
for book in bible_chapters:
	book_link = urlopen("%s%s" % (homepage, book)).read().decode("utf-8")
	total_chapter = re.findall(r'<li><a href="/bible/.*?">(\d+)</a></li>', book_link)[-1]

	chapter = book.replace("-", " ")
	book_info[chapter] = int(total_chapter)

# Create a folder called `text` if not already present
foldername = "text"
if not os.path.exists(foldername): os.makedirs(foldername)

# Method to get rid of unnecessary HTML entities
def replaced(text):
	TEXT = text.replace("\n", " ").replace("\t", "").replace("\r", "").replace("&nbsp;", " ").replace("\'", "'").replace("&quot;", "\"").replace("\\;", "").replace("\\'", "'").replace("&lt;", "<").replace("&gt;", ">").replace("&#8220;", "\"").replace("&#8221;", "\"").replace("\xe2\x80\x94", " -- ").replace("\\xe2\\x80\\x94", " -- ").replace("&#8217;", "'").replace("&para;", "|").replace("&uarr", "↑").replace("\xe2\x80\x98", "'").replace("\\xe2\\x80\\x98", "'").replace("\xe2\x80\x99", "'").replace("\\xe2\\x80\\x99", "'").replace("\xe2\x80\x9c", "\"").replace("\\xe2\\x80\\x9c", "\"").replace("\xe2\x80\x9c", "\"").replace("\\xe2\\x80\\x9c", "\"").replace("\xe2\x80\x9d", "\"").replace("\\xe2\\x80\\x9d", "\"").replace("\xe2\x80\x9d", "\"").replace("\\xe2\\x80\\x9d", "\"").replace("\xe2\x80\x93", "-").replace("\\xe2\\x80\\x93", "-")
	return TEXT

# method to text data into file
def write_bible_into_files(book_data):
	"""
		Takes one argument which is the book_info dictionary that contains chapter:total verse
	"""
	for book in book_data:
		chapters = book_data[book]

		# Contains subdirectories named after each books of the bible to be placed into the `text` folder
		book_subdirectory = "%s/%s" % (foldername, book)
		if not os.path.exists(book_subdirectory): os.makedirs(book_subdirectory)

		# Read each chapter from th online source
		print("\nwriting contents of %s" % (book))
		for chapter_num in range(1, chapters + 1):
			verses_link = urlopen("%s%s/%s" % (homepage,
				book.replace(" ", "-"), chapter_num)).read().decode("utf-8")

			verses_list = re.findall(r'<dt><a rel="verse" title=.*?<dd>(.*?)</dd>', replaced(verses_link))
			bible_verse_folder = "%s/%s/chapter-%s.txt" % (foldername, book, chapter_num)

			# Write the verses into the .txt document
			with open(bible_verse_folder, "w") as fobj:
				for verse_num, verses in enumerate(verses_list):
					fobj.write("%s %s:%s - %s\n\n" % (book.title(), chapter_num, verse_num + 1, verses))
			print("\t%s:%s completed" % (book, chapter_num))

# Call method to text data into file
write_bible_into_files(book_info)
print("%s books of the bible has been completely written" % len(bible_chapters))