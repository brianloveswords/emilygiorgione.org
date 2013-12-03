require('js-yaml')
module.exports = (function (index) {
  return index.pages.map(function (page) {
    return {
      page: page,
      context: require('./gallery/' + page + '.yml')
    }
  })
}(require('./gallery')))
