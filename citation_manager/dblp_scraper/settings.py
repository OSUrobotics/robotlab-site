# Scrapy settings for dblp_scraper project
#
# For simplicity, this file contains only the most important settings by
# default. All the other settings are documented here:
#
#     http://doc.scrapy.org/topics/settings.html
#

def setup_django_env(path):
    import imp, os
    from django.core.management import setup_environ

    f, filename, desc = imp.find_module('settings', [path])
    project = imp.load_module('settings', f, filename, desc)       

    setup_environ(project)

setup_django_env('/Users/lazewatd/Dropbox/robotlab/robotlab')

BOT_NAME = 'dblp_scraper'

SPIDER_MODULES = ['dblp_scraper.spiders']
NEWSPIDER_MODULE = 'dblp_scraper.spiders'

# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'dblp_scraper (+http://www.yourdomain.com)'
