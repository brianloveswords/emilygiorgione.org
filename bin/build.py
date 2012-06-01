import os
import yaml
import shutil
from jinja2 import Environment, FileSystemLoader
from utils import slugify


ROOT = os.path.dirname(os.path.abspath(__file__))
def path(*a): return os.path.join(os.getcwd(), *a)

jinja = Environment(loader=FileSystemLoader('./_layouts'))
class Gallery(object):
    directory = '_gallery'
    
    @staticmethod
    def data_from_yml(prefix):
        filename = path(Gallery.directory, '%s.yml' % prefix)
        with open(filename) as fp:
            data = yaml.load(fp)
        return data
    
    @staticmethod
    def assoc_pages(accum, name):
        data = Gallery.data_from_yml(name)
        if not data.get('slug'):
            data['slug'] = slugify(data.get('title'))
        else:
            data['slug'] = slugify(data.get('slug'))
        accum[name] = data
        return accum
    
    @property
    def index(self):
        return self._index
        
    @property
    def pages(self):
        return self._pages
    
    def __init__(self, index, layouts={'main':'main', 'item':'item'}):
        self._index = index = Gallery.data_from_yml(index)
        self._layouts = layouts
        
        # prepare the pages
        pages = index.get('pages')
        pages_with_metadata = []
        for idx in range(len(pages)):
            prevp = None
            nextp = None

            if idx > 0:
                prevp = pages[idx - 1]
            if idx < len(pages) - 1:
                nextp = pages[idx + 1]
            
            data = {'next': nextp, 'prev': prevp, 'name': pages[idx]}
            pages_with_metadata.append(data)
        
        self._pages_meta = pages_with_metadata
        self._pages = reduce(Gallery.assoc_pages, pages, {}) 
        

    def clean(self):
        shutil.rmtree('_build', True)
    
    def prepare(self):
        os.mkdir('_build')


    def render_index(self):
        items = [self._pages[page['name']] for page in self._pages_meta]
        template = jinja.get_template('main.html')
        return template.render({'items': items}).encode('utf8')

    def write_index(self):
        index_fp = open('_build/index.html', 'w+')
        index_fp.write(self.render_index())
        index_fp.close();
        
    def write_pages(self):
        template = jinja.get_template('item.html')
        for page in self._pages_meta:
            data = self._pages[page.get('name')]
            
            if page.get('next'):
                data['next'] = self._pages[page.get('next')].get('slug')
            if page.get('prev'):
                data['previous'] = self._pages[page.get('prev')].get('slug')
            
            tpl = template.render(data).encode('utf8')
            filename = '_build/%s.html' % (data.get('slug'),)
            item_fp = open(filename, 'w+')
            item_fp.write(tpl)
            item_fp.close()
    
    def copy_things(self):
        shutil.copytree('images', '_build/images')
        shutil.copytree('css', '_build/css')
        shutil.copytree('assets', '_build/assets')
        
        
def execute():
    g = Gallery('index')
    g.clean()
    g.prepare()
    g.write_index()
    g.write_pages()
    g.copy_things()

if __name__ == '__main__':
    print "building..."
    execute()
