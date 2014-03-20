import sys

def get_info(filename):
    fh = open(filename)
    av_link = ""
    dname = ""
    location = ""
    num_posts = ""
    next_span_user = False
    next_img_av = False
    next_dd_posts = False
    for l in fh:
	if l.find("<dl class=\"left-box\">") > 0:
	    next_img_av = True
	if l.find("<img src=") > 0 and next_img_av == True:
	    av_link = "<" + l.strip().lstrip("<dt>").rstrip("</dt>").strip() + ">"
	    next_img_av = False
	if l.find("<dt>Username:</dt>") > 0:
	    next_span_user = True
	if l.find("span") > 0 and next_span_user == True:
	    dname =  l.strip()
	    next_span_user = False
	    next_img_av = False
	if l.find("<dt>Location:</dt>") > 0:
	    start = l.find("<dd>")
	    stop = l.find("</dd>")
	    location = l[start+4:stop]
	if l.find("<dt>Total posts:</dt>") > 0:
	    next_dd_posts = True
	if l.find("<dd>") > 0 and next_dd_posts == True:
	    num_posts = l.split("|")[0].strip().lstrip("<dd>").strip()
	    next_dd_posts = False	

    return {"av_link":av_link, "dname":dname, "location":location, "num_posts":num_posts}

if __name__=='__main__':
    get_info(sys.argv[1])
