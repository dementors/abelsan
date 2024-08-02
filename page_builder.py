import requests
from bs4 import BeautifulSoup

# RSS feed URLs
# https://abelsan.substack.com/feed
# direct substact URL failed in github, 
# workaround is to use pipedream 
# feeds = {
#     'Substack': 'https://eonx51tpttmlx5j.m.pipedream.net',
#     'YouTube': 'https://www.youtube.com/feeds/videos.xml?channel_id=UCqiQs3iTyDbIy3HvtslAoWQ',
#     'Spotify Podcast': 'https://anchor.fm/s/f8df75fc/podcast/rss'
# }

# for local creation - use above for github actions
feeds = {
    'Substack': 'https://abelsan.substack.com/feed',
    'YouTube': 'https://www.youtube.com/feeds/videos.xml?channel_id=UCqiQs3iTyDbIy3HvtslAoWQ',
    'Spotify Podcast': 'https://anchor.fm/s/f8df75fc/podcast/rss'
}

# Function to fetch and parse the RSS feed
def fetch_feed(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (compatible; GitHub Actions; +https://github.com/your-repo)'
    }
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    return response.content
    # response = requests.get(url)
    # response.raise_for_status()
    # return BeautifulSoup(response.content, 'xml')

# Function to get the last 5 posts from a feed
def get_last_five_posts(feed, source):
    soup = BeautifulSoup(feed, 'xml')
    # soup = BeautifulSoup(feed, 'html.parser')  # use for github actions  
    items = soup.find_all(['item', 'entry'])[:5]
    posts = []
    for item in items:
        title = item.find('title').text
        if source == 'YouTube':
            link = item.find('link', {'rel': 'alternate'})['href']
        else:
            link = item.find('link').text if item.find('link') else item.find('link')['href']
        posts.append((title, link))
    return posts

# Fetch and parse all feeds
feed_data = {}
for title, url in feeds.items():
    feed = fetch_feed(url)
    feed_data[title] = get_last_five_posts(feed, title)

# html payloads
html_full = '''
<!DOCTYPE html>
<html lang="en" data-bs-theme="auto">
  <head>
    <script src="https://getbootstrap.com/docs/5.3/assets/js/color-modes.js"></script>

    <meta charset="utf-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1" />
    <meta name="description" content="" />
    <meta name="author" content="Abel Sanchez, John R. Williams" />
    <title>Abelsan</title>

    <link
      href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/css/bootstrap.min.css"
      rel="stylesheet"
      integrity="sha384-QWTKZyjpPEjISv5WaRU9OFeRpok6YctnYmDr5pNlyT2bRjXh0JMhjY6hW+ALEwIH"
      crossorigin="anonymous"
    />
    <link href="assets/css/styles.css" rel="stylesheet" />
  </head>

  <body>
    <!-- ---------------------------- -->
    <!--     Navbar and svg icons     -->
    <!-- ---------------------------- -->
    <abel-svgicons></abel-svgicons>
    <abel-navbar></abel-navbar>

    <!-- -------------------- -->
    <!--     Page content     -->
    <!-- -------------------- -->

    <main class="container">
'''

html_min = '''
      <div class="bg-body-secondary p-5 rounded">
        <h1 class="display-3">Welcome to Abelsan</h1>
        <p class="lead">
          Welcome to Daily Intelligence. We explore AI technology, data, and
          strategy, focusing on how AI and generative AI are transforming modern
          organizations. Posts highlight how these technologies drive
          innovation, boost efficiency, and create competitive advantages.
          Whether you’re a business leader, technologist, or curious about AI's
          future, you'll find insights to navigate the evolving tech landscape.
        </p>
      </div>

      <h1 class="display-6 p-2">Content</h1>
''' 

def shorten(s, max_length=30):
    return s[:max_length]

# populate page with feed data
for title, posts in feed_data.items():

    html_min += f'''
        <div class="col-md-6">
            <h2 class="text-body-emphasis">{title}</h2>
            <!-- <p>Description.</p> -->
            <ul class="list-unstyled ps-0">
        '''


    for post_title, post_link in posts:
        short_title = shorten(post_title)
        html_min += f'''
                <li>
                    <a class="icon-link mb-1" href="{post_link}" rel="noopener" data-bs-toggle="tooltip" data-bs-title="{post_title}" target="_blank">
                    <svg class="bi" width="16" height="16"><use xlink:href="#arrow-right-circle"/></svg>
                    {short_title}
                    </a>
                </li>
            '''
    # close list and div
    html_min += '</ul></div>'

html_min += '''
    </div>
    <!-- --------------- -->      
    <!--   END CONTENT   -->
    <!-- --------------- -->

  </main>
</div>    
<!-- ------------------------------- -->      
<!--   ONLINE DAILY AI CONTENT END   -->
<!-- ------------------------------- -->      

<hr class="w-100 mb-4">    
'''    

# append to full html
html_full += html_min

# Write HTML to abelsan locally
with open('proto.html', 'w', encoding='utf-8') as file:
    file.write(html_full)

# # Write HTML to abel.mit.edu
# mit_site = '../abelsan.github.io/assets/docs/podcast.html'
# with open(mit_site, 'w', encoding='utf-8') as file:
#     file.write(html)

print('HTML file created successfully.')
