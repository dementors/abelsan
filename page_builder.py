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


# Create HTML content
html = '''
  <!-- PLACEHOLDER -->
'''

html = '''

    <!-- -------------------------------- -->      
    <!--           STYLES START           -->
    <!-- -------------------------------- -->      

    <style>
      .bd-placeholder-img {
        font-size: 1.125rem;
        text-anchor: middle;
        -webkit-user-select: none;
        -moz-user-select: none;
        -ms-user-select: none;
        user-select: none;
      }

      @media (min-width: 768px) {
        .bd-placeholder-img-lg {
          font-size: 3.5rem;
        }
      }
      .container {
          max-width: 700px;
      }

      .pricing-header {
        max-width: 700px;
      }
      .card-img{
        filter: brightness(65%);
      }
      .card-img-overlay:hover{
        background-color: rgba(0, 0, 0, 0.65);;
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

    <!-- ------------------------------ -->      
    <!--           STYLES END           -->
    <!-- ------------------------------ -->      


    <!-- ------------------------------------------------- -->      
    <!--           START COLOR SWITCHING + ICONS           -->
    <!-- ------------------------------------------------- -->      

    <svg xmlns="http://www.w3.org/2000/svg" class="d-none">
      <symbol id="check2" viewBox="0 0 16 16">
        <path d="M13.854 3.646a.5.5 0 0 1 0 .708l-7 7a.5.5 0 0 1-.708 0l-3.5-3.5a.5.5 0 1 1 .708-.708L6.5 10.293l6.646-6.647a.5.5 0 0 1 .708 0z"/>
      </symbol>
      <symbol id="circle-half" viewBox="0 0 16 16">
        <path d="M8 15A7 7 0 1 0 8 1v14zm0 1A8 8 0 1 1 8 0a8 8 0 0 1 0 16z"/>
      </symbol>
      <symbol id="moon-stars-fill" viewBox="0 0 16 16">
        <path d="M6 .278a.768.768 0 0 1 .08.858 7.208 7.208 0 0 0-.878 3.46c0 4.021 3.278 7.277 7.318 7.277.527 0 1.04-.055 1.533-.16a.787.787 0 0 1 .81.316.733.733 0 0 1-.031.893A8.349 8.349 0 0 1 8.344 16C3.734 16 0 12.286 0 7.71 0 4.266 2.114 1.312 5.124.06A.752.752 0 0 1 6 .278z"/>
        <path d="M10.794 3.148a.217.217 0 0 1 .412 0l.387 1.162c.173.518.579.924 1.097 1.097l1.162.387a.217.217 0 0 1 0 .412l-1.162.387a1.734 1.734 0 0 0-1.097 1.097l-.387 1.162a.217.217 0 0 1-.412 0l-.387-1.162A1.734 1.734 0 0 0 9.31 6.593l-1.162-.387a.217.217 0 0 1 0-.412l1.162-.387a1.734 1.734 0 0 0 1.097-1.097l.387-1.162zM13.863.099a.145.145 0 0 1 .274 0l.258.774c.115.346.386.617.732.732l.774.258a.145.145 0 0 1 0 .274l-.774.258a1.156 1.156 0 0 0-.732.732l-.258.774a.145.145 0 0 1-.274 0l-.258-.774a1.156 1.156 0 0 0-.732-.732l-.774-.258a.145.145 0 0 1 0-.274l.774-.258c.346-.115.617-.386.732-.732L13.863.1z"/>
      </symbol>
      <symbol id="sun-fill" viewBox="0 0 16 16">
        <path d="M8 12a4 4 0 1 0 0-8 4 4 0 0 0 0 8zM8 0a.5.5 0 0 1 .5.5v2a.5.5 0 0 1-1 0v-2A.5.5 0 0 1 8 0zm0 13a.5.5 0 0 1 .5.5v2a.5.5 0 0 1-1 0v-2A.5.5 0 0 1 8 13zm8-5a.5.5 0 0 1-.5.5h-2a.5.5 0 0 1 0-1h2a.5.5 0 0 1 .5.5zM3 8a.5.5 0 0 1-.5.5h-2a.5.5 0 0 1 0-1h2A.5.5 0 0 1 3 8zm10.657-5.657a.5.5 0 0 1 0 .707l-1.414 1.415a.5.5 0 1 1-.707-.708l1.414-1.414a.5.5 0 0 1 .707 0zm-9.193 9.193a.5.5 0 0 1 0 .707L3.05 13.657a.5.5 0 0 1-.707-.707l1.414-1.414a.5.5 0 0 1 .707 0zm9.193 2.121a.5.5 0 0 1-.707 0l-1.414-1.414a.5.5 0 0 1 .707-.707l1.414 1.414a.5.5 0 0 1 0 .707zM4.464 4.465a.5.5 0 0 1-.707 0L2.343 3.05a.5.5 0 1 1 .707-.707l1.414 1.414a.5.5 0 0 1 0 .708z"/>
      </symbol>
    </svg>

    <div class="dropdown position-fixed bottom-0 end-0 mb-3 me-3 bd-mode-toggle">
      <button class="btn btn-bd-primary py-2 dropdown-toggle d-flex align-items-center"
              id="bd-theme"
              type="button"
              aria-expanded="false"
              data-bs-toggle="dropdown"
              aria-label="Toggle theme (auto)">
        <svg class="bi my-1 theme-icon-active" width="1em" height="1em"><use href="#circle-half"></use></svg>
        <span class="visually-hidden" id="bd-theme-text">Toggle theme</span>
      </button>
      <ul class="dropdown-menu dropdown-menu-end shadow" aria-labelledby="bd-theme-text">
        <li>
          <button type="button" class="dropdown-item d-flex align-items-center" data-bs-theme-value="light" aria-pressed="false">
            <svg class="bi me-2 opacity-50" width="1em" height="1em"><use href="#sun-fill"></use></svg>
            Light
            <svg class="bi ms-auto d-none" width="1em" height="1em"><use href="#check2"></use></svg>
          </button>
        </li>
        <li>
          <button type="button" class="dropdown-item d-flex align-items-center" data-bs-theme-value="dark" aria-pressed="false">
            <svg class="bi me-2 opacity-50" width="1em" height="1em"><use href="#moon-stars-fill"></use></svg>
            Dark
            <svg class="bi ms-auto d-none" width="1em" height="1em"><use href="#check2"></use></svg>
          </button>
        </li>
        <li>
          <button type="button" class="dropdown-item d-flex align-items-center active" data-bs-theme-value="auto" aria-pressed="true">
            <svg class="bi me-2 opacity-50" width="1em" height="1em"><use href="#circle-half"></use></svg>
            Auto
            <svg class="bi ms-auto d-none" width="1em" height="1em"><use href="#check2"></use></svg>
          </button>
        </li>
      </ul>
    </div>

    
    <svg xmlns="http://www.w3.org/2000/svg" class="d-none">
      <symbol id="arrow-right-circle" viewBox="0 0 16 16">
        <path d="M8 0a8 8 0 1 1 0 16A8 8 0 0 1 8 0zM4.5 7.5a.5.5 0 0 0 0 1h5.793l-2.147 2.146a.5.5 0 0 0 .708.708l3-3a.5.5 0 0 0 0-.708l-3-3a.5.5 0 1 0-.708.708L10.293 7.5H4.5z"/>
      </symbol>
      <symbol id="bootstrap" viewBox="0 0 118 94">
        <title>Bootstrap</title>
        <path fill-rule="evenodd" clip-rule="evenodd" d="M24.509 0c-6.733 0-11.715 5.893-11.492 12.284.214 6.14-.064 14.092-2.066 20.577C8.943 39.365 5.547 43.485 0 44.014v5.972c5.547.529 8.943 4.649 10.951 11.153 2.002 6.485 2.28 14.437 2.066 20.577C12.794 88.106 17.776 94 24.51 94H93.5c6.733 0 11.714-5.893 11.491-12.284-.214-6.14.064-14.092 2.066-20.577 2.009-6.504 5.396-10.624 10.943-11.153v-5.972c-5.547-.529-8.934-4.649-10.943-11.153-2.002-6.484-2.28-14.437-2.066-20.577C105.214 5.894 100.233 0 93.5 0H24.508zM80 57.863C80 66.663 73.436 72 62.543 72H44a2 2 0 01-2-2V24a2 2 0 012-2h18.437c9.083 0 15.044 4.92 15.044 12.474 0 5.302-4.01 10.049-9.119 10.88v.277C75.317 46.394 80 51.21 80 57.863zM60.521 28.34H49.948v14.934h8.905c6.884 0 10.68-2.772 10.68-7.727 0-4.643-3.264-7.207-9.012-7.207zM49.948 49.2v16.458H60.91c7.167 0 10.964-2.876 10.964-8.281 0-5.406-3.903-8.178-11.425-8.178H49.948z"></path>
      </symbol>
    </svg>

    <!-- ------------------------------------------------- -->      
    <!--            END COLOR SWITCHING + ICONS            -->
    <!-- ------------------------------------------------- -->      

<div class="col-lg-8 mx-auto p-4 py-md-5">

  <main>

   <!-- ---------- -->      
   <!--   header   -->
   <!-- ---------- -->      

    <div class="pricing-header px-3 py-3 pt-md-3 pb-md-1 mx-auto">
      <h1 class="display-4">Dr. Abel Sanchez</h1>
          <a href="https://abel.mit.edu/" title="MIT site"><img src="assets/img/logo_gray.svg" height="15"> </a> |    
          <a href="https://professional.mit.edu/programs/faculty-profiles/abel-sanchez" title="Courses"><i class="bi bi-mortarboard-fill"></i> Courses</a> |
          <a href="https://abelsan.substack.com/"><i class="bi bi-substack"></i> Blog</a> |             
          <a href="http://www.linkedin.com/in/abelsanc" title="LinkedIn"><i class="bi bi-linkedin"></i> LinkedIn</a> |    
          <a href="https://www.youtube.com/@abelsanx" title="YouTube"><i class="bi bi-youtube"></i> YouTube</a> | 
          <a href="https://podcasters.spotify.com/pod/show/abelsan"><i class="bi bi-mic-fill"></i> Podcast</a> | 
          <a href="https://professional.mit.edu/course-catalog/applied-generative-ai-digital-transformation"><i class="bi bi-cpu-fill"></i> New: Gen-AI course</a> 
    </div>

    <!-- --------------------------------- -->      
    <!--   ONLINE DAILY AI CONTENT START   -->
    <!-- --------------------------------- -->      

    <div class="col-lg-8 mx-auto p-3">


      <main>

        <!-- ------------ -->      
        <!--   overview   -->
        <!-- ------------ -->      
        <hr class="w-100 mb-3">    
        <h1 class="display-6">Generative AI - Daily Intelligence</h1>
        <p>Welcome to Daily Intelligence. We explore AI strategy and data insights, focusing on how AI and generative AI transform organizations. Find valuable insights to navigate the evolving tech landscape.</p>
        <hr class="w-100 mb-3">

        <!-- ----------------- -->      
        <!--   START CONTENT   -->
        <!-- ----------------- -->      
        <div class="row g-5">

'''

# populate page with feed data
for title, posts in feed_data.items():

    html += f'''
        <div class="col-md-6">
            <h2 class="text-body-emphasis">{title}</h2>
            <!-- <p>Description.</p> -->
            <ul class="list-unstyled ps-0">
        '''


    for post_title, post_link in posts:
        html += f'''
                <li>
                    <a class="icon-link mb-1" href="{post_link}" rel="noopener" target="_blank">
                    <svg class="bi" width="16" height="16"><use xlink:href="#arrow-right-circle"/></svg>
                    {post_title}
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
