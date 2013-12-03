const path = require('path')
const http = require('http')
const nunjucks = require('nunjucks')
const ecstatic = require('ecstatic')
const pages = require('./page-data')
const url = require('url')

const mimeHtml = 'text/html; charset=utf8'
const staticHandler = ecstatic({
  root: path.join(__dirname, 'static'),
  handleError: false
})

// tell nunjucks where to find the templates
nunjucks.configure(path.join(__dirname, 'templates'))

http.createServer(function (req, res) {
  return staticHandler(req, res, function otherwise() {
    const pathname = url.parse(req.url).pathname

    if (pathname == '/') {
      res.writeHead(200, {'content-type': mimeHtml })
      return res.end(nunjucks.render('index.html', {
        page: "home",
        pages: pages
      }))
    }

    const fixedPath = pathname.slice(1).replace(/\/$/, '')

    if (fixedPath == '/contact') {
      res.writeHead(200, {'content-type': mimeHtml })
      return res.end(nunjucks.render('contact.html', {
        page: 'contact',
      }))
    }

    if (fixedPath == '/resume') {
      res.writeHead(200, {'content-type': mimeHtml })
      return res.end(nunjucks.render('resume.html', {
        page: 'resume',
      }))
    }

    const page = findPage(fixedPath, pages)

    if (!page) {
      res.writeHead(404, {'content-type': mimeHtml })
      res.write(nunjucks.render('404.html'))
      return res.end()
    }

    res.writeHead(200, {'content-type': mimeHtml })
    res.write(nunjucks.render('page.html', page))
    return res.end()
  }
)
}).listen(9000, function () {
  console.log('listening on %j', this.address())
})



function findPage(title, pages) {
  for (var idx = 0, len = pages.length; idx < len; idx++) {
    if (pages[idx].page == title) {
      return {
        previous: pages[idx - 1],
        current: pages[idx],
        next: pages[idx + 1]
      }
    }
  }
  return false
}
