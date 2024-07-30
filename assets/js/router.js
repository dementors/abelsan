window.onload = function(){
    console.log('DOM loaded');
    var history = '';

    var routes = {
        '':           'assets/docs/home.html',     
        '/':          'assets/docs/home.html',
        '#/home':     'assets/docs/home.html',        
        '#/bio':      'assets/docs/bio.html',
        '#/research': 'assets/docs/research.html',
        '#/teaching': 'assets/docs/teaching.html',
        '#/speaking': 'assets/docs/speaking.html',
        '#/podcast':  'assets/docs/podcast.html',
        '#/blog':     'assets/docs/blog.html',
        '#/books':    'assets/docs/books.html'
    };

    function router(){
        console.log('document.referrer: ' + document.referrer);
        var link         = window.location.hash;
        var innerElement = '';

        // ----------------------------------------
        // If more than one parameter in the link, 
        // I am targeting an element in the page, 
        // an anchor. First load page, the scroll
        // the element into view.
        // ----------------------------------------

        var count = (link.split("/").length - 1);        
        if (count > 1) {
            // anchor element 
            innerElement = link.split("/")[2];            

            // page to load
            link = '#/' + link.split("/")[1];
        }

        // ----------------------------------------
        // Remember loaded page - used to avoid
        // page reload on internal linking
        // ----------------------------------------        
        if (history === link && innerElement){
            scrollIntoView(innerElement);
            history = link;
            return;            
        }
        history = link;  


        // get path (route) for page
        console.log('link: ' + link);
        var route = routes[link];

        // if route exists, load page
        console.log('route:' + route);
        if (route) loadPage(route, innerElement);
    }
    router();

    // listen hash path changes
    window.addEventListener('hashchange', router);


    async function loadPage(url, innerElement){
        // load page
        const res     = await fetch(url);
        const content = await res.text();
        const element = document.getElementById('content');
        element.innerHTML = content;

        // ------------------------------------------
        // Scroll to top -- need to avoid navigation 
        // drift on page. Else the scroll state 
        // carries over on to next page
        // ------------------------------------------
        window.scrollTo(0, 0);

        // element scroll into view
        if (innerElement) {            
            scrollIntoView(innerElement);
        }
    };            

    function scrollIntoView(id){
        document.getElementById(id).scrollIntoView();
    }    
};
