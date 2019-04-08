(function () {
    let r = Math.floor(Math.random() * 99999999999999999999); // prevent browser cache
    if (window.myBookmarklet) {
        myBookmarklet();
    } else {
        document.body.appendChild(document.createElement('script')).src ='http://127.0.0.1:8000/static/js/bookmarklet.js?r='+r
    }
})();