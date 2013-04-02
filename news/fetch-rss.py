## Read the RSS feed specified at sys.argv[1]. Output important metadata
## in a list in corpora/news.index and the value of the url in the <link> 
## field to corpora/news/. 
import urllib2, sys, hashlib
import xml.etree.ElementTree as etree

if len(sys.argv) > 2:
  print 'Please provide a URL.'
  sys.exit(1)

feed_url = sys.argv[1]
print 'Reading feed from ', feed_url

try:
  handle = urllib2.urlopen(feed_url)
except urllib2.URLError as e:
  print 'Error: ' + e

rss = handle.read()

feed_out = open('corpora/news.index', 'a+')

# Read rss
root = etree.fromstring(rss)
for chan in root.findall('channel'):
  num_articles = len(chan.findall('item'))
  current_article = 1
  for item in chan.findall('item'):
    title = item.find('title').text.strip().encode('utf-8')
    link = item.find('link').text.strip().encode('utf-8')
    desc = item.find('description').text.strip().encode('utf-8')
    pubdate = item.find('pubDate').text.strip().encode('utf-8')
    
    digest = hashlib.sha224(title + pubdate).hexdigest()

    feed_out.write(title + '\n')
    feed_out.write(pubdate + '\n')
    feed_out.write(feed_url + '\n')
    feed_out.write(link + '\n')
    feed_out.write(digest + '\n')
    feed_out.write(desc + '\n\n')
    
    print '  [%d / %d] Reading: %s' % (current_article, num_articles, link)
    try:
      article = urllib2.urlopen(link)
    except urllib2.URLError as e:
      print 'Error loading article: ' + e
      
    html = article.read()
    
    with open('corpora/news/%s' % digest, 'wb') as article_out:
      article_out.write(html)
   
    current_article += 1
    
feed_out.close()
handle.close()
