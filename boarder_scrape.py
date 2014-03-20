import sqlite3
import mechanize
import re
import os
import time

def find_next_boarder(found_boarders, br):
	for link in br.links():
		if str(link).find("viewprofile") > 0:
			text_open = str(link).find("text='") + 6
			text_close = str(link).find("'", text_open)
			boarder_name = str(link)[text_open:text_close].replace("/", "_")
			if boarder_name not in found_boarders:
				found_boarders.append(boarder_name)
				print boarder_name
				resp = br.follow_link(link)
				outfh = open("boarder_files/" + boarder_name, 'w')
				outfh.write(resp.read())
				outfh.close()
				br.back()
				return boarder_name
	return -1

def scan_page(found_boarders, br):
	found_boarder = ""
	while found_boarder <> -1:
		found_boarder = find_next_boarder(found_boarders, br)
		found_boarders.append(found_boarder)
		time.sleep(3)


conn = sqlite3.connect("boarders.sqlite")
curs = conn.cursor()

login_url = "http://forums.hipinion.com/ucp.php"
username = "mouse pad"
password = "hunter2"

found_boarders = os.listdir('boarder_files')
found_boarder = ""

br = mechanize.Browser()
resp = br.open(login_url)
flist = br.forms()
for f in flist:
	if str(f).find("login") > 0:
		print "Found form"
		br.form = f
br['username'] = username
br['password'] = password
resp = br.submit()
resp = br.follow_link(text_regex=r"Members")
resp = br.follow_link(text_regex=r"Posts")
resp = br.follow_link(text_regex=r"Posts")
print br.title()
print br.geturl()
page_no = 0
while 1:
	page_no += 1
	scan_page(found_boarders, br)
	looking_for = "start=" + str(page_no*50)
	for link in br.links():
		if str(link).find(looking_for) > 0:
			br.follow_link(link)



