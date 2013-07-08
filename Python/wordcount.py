def get_word_counts(url):
    d = feedparser.parse(url)
    wc = {}
    if d.entries is None:
        return None, 0
    for e in d.entries:
        if "summary" in e:
            summary = e.summary
        elif "description" in e:
            summary = e.description
        else: 
            summary = ''
        try: 
            etitle = e.title
        except AttributeError:
            etitle = ""

        words = getwords(etitle + ' ' + summary)
        for word in words:
            wc.setdefault(word, 0)
            wc[word] += 1
    
    title = url
    try: 
        title = d.feed.title
    except AttributeError:
        pass 
    return title, wc

def getwords(html):

    # Get rid of special HTML characters
    txt = re.compile(r'<[^>]+>').sub('', html)
    words = re.compile(r'[^A-Z^a-z]+').split(txt)

    # Return a list of lower-cased words, not counting the empty string
    return [word.lower() for word in words if word != '']

if __name__ == "__main__":
    from collections import defaultdict
    with open("marketing_blogs.txt","r") as blog_list:
        apcount = defaultdict(int)
        wordcounts = {}
        blog_set = set([blog for blog in blog_list])
        print len(blog_set), "blogs to scrape!"
        files_processed = 0
        for blog in blog_set:
            title, wc = get_word_counts(blog)
            print "Processing:", title
            wordcounts[title] = wc
            for word, count in wc.items():
                if count > 1:
                    apcount[word] += 1
            files_processed += 1
            if files_processed % 10 == 0:
                print "%d of %d FILES PROCESSED!!!!" % (files_processed, len(blog_set))
        wordlist = []

        for w, bc in apcount.items():
            frac = float(bc)/len(blog_set)
            if 0.1 < frac < 0.5:
                wordlist.append(w)
        with open("marketing_blogdata.txt","w") as outfile:
            outfile.write('Blog')
            for word in wordlist:
                outfile.write("\t%s" % word)
            outfile.write("\n")
            for blog, wc in wordcounts.items():
                blog = blog.encode('ascii', 'ignore')
                outfile.write(blog)
                for word in wordlist:
                    if word in wc:
                        outfile.write("\t%d" % wc[word])
                    else:
                        outfile.write("\t0")
                outfile.write("\n")