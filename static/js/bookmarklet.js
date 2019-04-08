(function () {
    let siteUrl = 'http://127.0.0.1:8000'
    let staticUrl = `${siteUrl}/static`
    let r = Math.floor(Math.random() * 99999999999999999999)

    let css = document.createElement('link')
    css.rel = 'stylesheet'
    css.type = 'text/css'
    css.href = `${staticUrl}/css/bookmarklet.css?r=${r}`
    document.head.appendChild(css)

    let html = '<div id="bookmarklet"><a href="#" id="close">&times;</a><h1>Select an image to bookmark:</h1><div class="images"></div></div>'
    document.body.insertAdjacentHTML('beforeend', html)

    let bookmarklet = document.getElementById('bookmarklet')
    document.querySelector('#bookmarklet #close').addEventListener('click', () => {
        bookmarklet.parentNode.removeChild(bookmarklet)
    })

    Array.from(document.getElementsByTagName('img')).forEach((value, index) => {
        let imageUrl = value.src
        let imageTitle = value.title
        let imageHTML = `<a href="#"><img src=${imageUrl} title="${imageTitle}"></a>`
        document.querySelector('#bookmarklet .images').insertAdjacentHTML('beforeend', imageHTML)
    })

    document.querySelectorAll('#bookmarklet .images a').forEach(a => {
        a.addEventListener('click', e => {
            let selectedImage = e.target.src
            bookmarklet.parentNode.removeChild(bookmarklet)
            window.open(`${siteUrl}/images/create/?url=${selectedImage}&title=${e.target.title||document.title}`, '_blank')
        })
    })
})()