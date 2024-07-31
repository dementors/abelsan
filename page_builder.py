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


html = '''
    <!-- ------------------ -->
    <!--       Styles       -->
    <!-- ------------------ -->

    <style>
      .bd-placeholder-img {
        font-size: 1.125rem;
        text-anchor: middle;
        -webkit-user-select: none;
        -moz-user-select: none;
        user-select: none;
      }

      @media (min-width: 768px) {
        .bd-placeholder-img-lg {
          font-size: 3.5rem;
        }
      }

      .b-example-divider {
        width: 100%;
        height: 3rem;
        background-color: rgba(0, 0, 0, .1);
        border: solid rgba(0, 0, 0, .15);
        border-width: 1px 0;
        box-shadow: inset 0 .5em 1.5em rgba(0, 0, 0, .1), inset 0 .125em .5em rgba(0, 0, 0, .15);
      }

      .b-example-vr {
        flex-shrink: 0;
        width: 1.5rem;
        height: 100vh;
      }

      .bi {
        vertical-align: -.125em;
        fill: currentColor;
      }

      .nav-scroller {
        position: relative;
        z-index: 2;
        height: 2.75rem;
        overflow-y: hidden;
      }

      .nav-scroller .nav {
        display: flex;
        flex-wrap: nowrap;
        padding-bottom: 1rem;
        margin-top: -1px;
        overflow-x: auto;
        text-align: center;
        white-space: nowrap;
        -webkit-overflow-scrolling: touch;
      }

      .btn-bd-primary {
        --bd-violet-bg: #712cf9;
        --bd-violet-rgb: 112.520718, 44.062154, 249.437846;

        --bs-btn-font-weight: 600;
        --bs-btn-color: var(--bs-white);
        --bs-btn-bg: var(--bd-violet-bg);
        --bs-btn-border-color: var(--bd-violet-bg);
        --bs-btn-hover-color: var(--bs-white);
        --bs-btn-hover-bg: #6528e0;
        --bs-btn-hover-border-color: #6528e0;
        --bs-btn-focus-shadow-rgb: var(--bd-violet-rgb);
        --bs-btn-active-color: var(--bs-btn-hover-color);
        --bs-btn-active-bg: #5a23c8;
        --bs-btn-active-border-color: #5a23c8;
      }

      .bd-mode-toggle {
        z-index: 1500;
      }

      .bd-mode-toggle .dropdown-menu .active .bi {
        display: block !important;
      }
    </style>

    <!-- --------------------- -->
    <!--       SVG icons       -->
    <!-- --------------------- -->

    <svg xmlns="http://www.w3.org/2000/svg" class="d-none">
      <symbol id="arrow-right-circle" viewBox="0 0 16 16">
        <path d="M8 0a8 8 0 1 1 0 16A8 8 0 0 1 8 0zM4.5 7.5a.5.5 0 0 0 0 1h5.793l-2.147 2.146a.5.5 0 0 0 .708.708l3-3a.5.5 0 0 0 0-.708l-3-3a.5.5 0 1 0-.708.708L10.293 7.5H4.5z"/>
      </symbol>
      <symbol id="bootstrap" viewBox="0 0 118 94">
        <title>Bootstrap</title>
        <path fill-rule="evenodd" clip-rule="evenodd" d="M24.509 0c-6.733 0-11.715 5.893-11.492 12.284.214 6.14-.064 14.092-2.066 20.577C8.943 39.365 5.547 43.485 0 44.014v5.972c5.547.529 8.943 4.649 10.951 11.153 2.002 6.485 2.28 14.437 2.066 20.577C12.794 88.106 17.776 94 24.51 94H93.5c6.733 0 11.714-5.893 11.491-12.284-.214-6.14.064-14.092 2.066-20.577 2.009-6.504 5.396-10.624 10.943-11.153v-5.972c-5.547-.529-8.934-4.649-10.943-11.153-2.002-6.484-2.28-14.437-2.066-20.577C105.214 5.894 100.233 0 93.5 0H24.508zM80 57.863C80 66.663 73.436 72 62.543 72H44a2 2 0 01-2-2V24a2 2 0 012-2h18.437c9.083 0 15.044 4.92 15.044 12.474 0 5.302-4.01 10.049-9.119 10.88v.277C75.317 46.394 80 51.21 80 57.863zM60.521 28.34H49.948v14.934h8.905c6.884 0 10.68-2.772 10.68-7.727 0-4.643-3.264-7.207-9.012-7.207zM49.948 49.2v16.458H60.91c7.167 0 10.964-2.876 10.964-8.281 0-5.406-3.903-8.178-11.425-8.178H49.948z"></path>
      </symbol>
    </svg>

    <!-- --------------------------------------------- -->      
    <!--            Content and page layout            -->
    <!-- --------------------------------------------- -->      

<div class="col-lg-8 mx-auto p-4 py-md-5">


  <main>

    <!-- ------------ -->      
    <!--   overview   -->
    <!-- ------------ -->      
    <h1 class="text-body-emphasis">Overview</h1>
    <p class="fs-5 col-md-12">Welcome to Daily Intelligence. We explore AI strategy and data insights, focusing on how AI and generative AI are transforming modern organizations. Each post highlights how these technologies drive innovation, boost efficiency, and create competitive advantages. Whether you’re a business leader, tech enthusiast, or curious about AI's future, you'll find valuable insights to navigate the evolving tech landscape.</p>
    <hr class="col-3 col-md-2 mb-5">


        <!-- ----------------- -->      
        <!--   Start content   -->
        <!-- ----------------- -->      
        <div class="row g-5">

'''

def shorten(s, max_length=30):
    return s[:max_length]

# populate page with feed data
for title, posts in feed_data.items():

    html += f'''
        <div class="col-md-6">
            <h2 class="text-body-emphasis">{title}</h2>
            <!-- <p>Description.</p> -->
            <ul class="list-unstyled ps-0">
        '''


    for post_title, post_link in posts:
        short_title = shorten(post_title)
        html += f'''
                <li>
                    <a class="icon-link mb-1" href="{post_link}" rel="noopener" data-bs-toggle="tooltip" data-bs-title="{post_title}" target="_blank">
                    <svg class="bi" width="16" height="16"><use xlink:href="#arrow-right-circle"/></svg>
                    {short_title}
                    </a>
                </li>
            '''
    # close list and div
    html += '</ul></div>'

html += '''
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

# Write HTML to abelsan locally
with open('assets/docs/home.html', 'w', encoding='utf-8') as file:
    file.write(html)

# Write HTML to abel.mit.edu
mit_site = '../abelsan.github.io/assets/docs/podcast.html'
with open(mit_site, 'w', encoding='utf-8') as file:
    file.write(html)

print('HTML file created successfully.')
