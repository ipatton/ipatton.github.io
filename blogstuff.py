def count_words(url):

    import bs4
    import feedparser

    feed = feedparser.parse(url)
    title = feed.feed.title

    print "Processing", title

    total_words = 0
    wordcomment_list = []
    for entry in feed.entries:
        print "---------> ", entry.title
        text = bs4.BeautifulSoup(entry.content[0].value)
        word_count = len(text.get_text().split())
        comment_count = int(entry.slash_comments)
        poop_list.append((word_count, comment_count))
    print "\n"

    return title, wordcomment_list



def get_rss_links(url):

    """
    Given the URL for a webpage known to have links 
    to RSS feeds, a call to this function returns
    a set of those links (hopefully), which we will
    then be able to use to scrape content
    """

    import re
    import requests 

    # Use the requests module to get page source
    page_source = requests.get(url)

    # Find all of the RSS links according to some pattern.
    # The pattern that is searched for can be changed, and will probably
    # be site specific.  You may also want to look for multiple patterns.
    # We use set() here to eliminate duplicate links. 

    return set(re.findall(r'http.*\.xml', page_source.text))

def get_links_from_unbounce(html):
    """
    This function was implemented specifically to scrape links
    to RSS feeds from two separate unbounce.com posts about the top
    75 marketing blogs. Since we couldn't access these pages using
    the requests module, I copied and pasted the html text into a file.
    The plain html text for the page should be passed as an argument. 
    The code takes advantage of the fact that every blog listed had
    a link to its RSS feed, titled "RSS". A set of all such links is 
    returned. 
    """

    import bs4

    soup = bs4.BeautifulSoup(html)

    return set([link.get('href') for link in soup.find_all("a") if link.string == "RSS"])


def compile_blog_data(link_set):

    import numpy as np
    blog_dict = {}

    for link in link_set:

        try:
            title, counts = count_words(link)
        except AttributeError:
            print "**** Error Processing %s****\n" % link
            continue

        # Calculate averages across posts
        avg_words = np.mean([x[0] for x in counts])
        avg_comments = np.mean([x[1] for x in counts])
        blog_dict[title] = (avg_words, avg_comments)

    return blog_dict


def plot_blog_data(blog_dict):

    import matplotlib.pyplot as plt 

    plt.scatter([x[0] for x in blog_dict.values()], [x[1] for x in blog_dict.values()])
    plt.xlabel("Average Number of Words Per Post")
    plt.ylabel("Number of Comments Per Post")
    plt.title("Blog Data")
    plt.show()


if __name__ == "__main__":
    links = set()
    for in_file in ["unbounce_source.txt", "unbounce_source2.txt"]:
        with open(in_file) as f:
            links.update(get_links_from_unbounce(f.read()))

    blog_dict = compile_blog_data(links)
    plot_blog_data(blog_dict)














