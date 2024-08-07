import requests
from bs4 import BeautifulSoup

# RSS feed URLs
feeds = {
    'Substack': 'https://abelsan.substack.com/feed',
    'YouTube': 'https://www.youtube.com/feeds/videos.xml?channel_id=UCqiQs3iTyDbIy3HvtslAoWQ',
    'Spotify Podcast': 'https://anchor.fm/s/f8df75fc/podcast/rss'
}

# Function to fetch and parse the RSS feed
def fetch_feed(url):
    response = requests.get(url)
    response.raise_for_status()
    return BeautifulSoup(response.content, 'xml')

# Function to extract feed items
def get_all_posts(soup, source):
    items = soup.find_all(['item', 'entry'])  # all items
    posts = []
    for item in items:
        title = item.find('title').text.strip()
        description = item.find('description').text.strip()
        id_tag = item.find(['guid', 'id'])
        if id_tag:
            id = id_tag.text.strip()
        else:
            id = ''
        if source == 'YouTube':
            link = item.find('link', {'rel': 'alternate'})['href']
        else:
            link = item.find('link').text.strip() if item.find('link') else item.find('link')['href']
        if source == 'Substack':
            enclosure = item.find('enclosure')
            image_url = enclosure['url'] if enclosure else ''
        else:
            image_url = ''
        posts.append({'title': title, 'link': link, 'description': description, 'id': id, 'image_url': image_url})
    return posts

# Fetch and parse all feeds
substack_posts = fetch_feed(feeds['Substack'])
substack_posts = get_all_posts(substack_posts, 'Substack')

youtube_posts = fetch_feed(feeds['YouTube'])
youtube_posts = get_all_posts(youtube_posts, 'YouTube')

spotify_posts = fetch_feed(feeds['Spotify Podcast'])
spotify_posts = get_all_posts(spotify_posts, 'Spotify Podcast')

# Create a list of items from the Substack feed
substack_items = [{'title': post['title'], 'link': post['link'], 'description': post['description'], 'image_url': post['image_url']} for post in substack_posts]

# Helper function to find matching post link by title
def find_matching_post(posts, title):
    for post in posts:
        if post['title'] == title:
            return post['link']
    return None

# Loop through the Substack titles and look for corresponding titles in Spotify and YouTube
for item in substack_items:
    item['spotify_link'] = find_matching_post(spotify_posts, item['title'])
    item['youtube_link'] = find_matching_post(youtube_posts, item['title'])

# Inspect grouped posts
print('Grouped Posts:')
for post in substack_items:
    print(f"Title: {post['title']}")
    print(f"Substack Link: {post['link']}")
    print(f"Substack Description: {post['description']}")
    print(f"Substack Image URL: {post['image_url']}")
    if post['spotify_link']:
        print(f"Spotify Podcast Link: {post['spotify_link']}")
    if post['youtube_link']:
        print(f"YouTube Link: {post['youtube_link']}")
    print('---')

# ----------------
#     content
# ----------------

# html payload
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

'''

html_min = '''
    <!-- -------------------- -->
    <!--     Page content     -->
    <!-- -------------------- -->

    <main class="container">
      <div class="bg-body-secondary p-5 rounded">
        <h1 class="display-3">Welcome to Abelsan</h1>
        <p class="lead">
          Welcome to Daily Intelligence. We explore AI technology, data, and
          strategy, focusing on how AI and generative AI are transforming modern
          organizations. 
        </p>
            <a href="https://professional.mit.edu/programs/faculty-profiles/abel-sanchez" title="Courses"><i class="bi bi-mortarboard-fill fs-6"></i> Courses</a> |
            <a href="https://abelsan.substack.com/"><i class="bi bi-substack fs-6"></i> Blog</a> |             
            <a href="http://www.linkedin.com/in/abelsanc" title="LinkedIn"><i class="bi bi-linkedin"></i> LinkedIn</a> |    
            <a href="https://www.youtube.com/@abelsanx" title="YouTube"><i class="bi bi-youtube"></i> YouTube</a> | 
            <a href="https://podcasters.spotify.com/pod/show/abelsan"><i class="bi bi-mic-fill"></i> Podcast</a> |
            <a href="https://abelsan.com/" title="Daily Intelligence"><i class="bi bi-cpu-fill"></i> Daily</a>          

      </div>

      <h1 class="display-6 p-2">Content</h1>
''' 

def shorten(s, max_length=30):
    return s[:max_length]

# populate page with feed data
for post in substack_items:
    # post links
    substack_link = ''
    spotify_link = ''
    youtube_link = ''

    # post links
    substack_link = f'''newsletter="{post['link']}"'''
    if post['spotify_link']:
        spotify_link = f'''podcast="{post['spotify_link']}"'''
    if post['youtube_link']:
        youtube_link = f'''video="{post['youtube_link']}"'''

    html_min += f'''
        <abel-card
            title="{post['title']}"
            description="{post['description']}"
            img="{post['image_url']}"
            {substack_link}
            {spotify_link}
            {youtube_link}
        ></abel-card>

    '''

html_min += '''
    </main>
'''

# Write html_min to abel.mit.edu
mit_site = '../abelsan.github.io/assets/docs/podcast.html'
with open(mit_site, 'w', encoding='utf-8') as file:
    file.write(html_min)

# append html_min to html_full
html_full += html_min

# finish local page
html_full += '''
    <script
      src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/js/bootstrap.bundle.min.js"
      integrity="sha384-YvpcrYf0tY3lHB60NNkmXc5s9fDVZLESaAA55NDzOxhy9GkcIdslK1eN7N6jIeHz"
      crossorigin="anonymous"
    ></script>

    <!-- Local JS files -->
    <script src="assets/js/components.js"></script>
  </body>
</html>      
'''    

# Write HTML to abelsan locally
with open('index.html', 'w', encoding='utf-8') as file:
    file.write(html_full)

print('HTML file created successfully.')