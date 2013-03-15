from pybtex.database import Entry, Person
from pybtex.style import FormattedBibliography
from pybtex.plugin import find_plugin
import io


authors = [Person('Daniel A. Lazewatsky'), Person('William D. Smart')]
# fields={u'doi': u'10.1109/ROMAN.2012.6343878', u'title': u'Context-sensitive in-the-world interfaces for mobile manipulation robots', u'booktitle': u'RO-MAN, 2012 IEEE', u'issn': u'1944-9445', u'number': u'', u'abstract': u"We present an interface that allows users to direct a mobile manipulation robot in tabletop pick-and-place tasks using only their head motions and a single button. The system uses an estimate of the user's head pose and a 3d world model maintained by the robot to determine where the user is pointing their head. We give the results of some preliminary evaluations of our system, which suggest that it is both intuitive and effective. We also describe an example trash-sorting application where the user directs a PR2 robot sort objects in to #x201C;trash #x201D; and #x201C;recycle #x201D; piles.", u'month': u'sept.', u'volume': u'', u'year': u'2012', u'keywords': u'', u'pages': u'989 -994'}
fields = {u'abstract': u"We present an interface that allows users to direct a mobile manipulation robot in tabletop pick-and-place tasks using only their head motions and a single button. The system uses an estimate of the user's head pose and a 3d world model maintained by the robot to determine where the user is pointing their head. We give the results of some preliminary evaluations of our system, which suggest that it is both intuitive and effective. We also describe an example trash-sorting application where the user directs a PR2 robot sort objects in to #x201C;trash #x201D; and #x201C;recycle #x201D; piles.",
 u'booktitle': u'RO-MAN, 2012 IEEE',
 u'doi': u'10.1109/ROMAN.2012.6343878',
 u'issn': u'1944-9445',
 u'keywords': u'',
 u'month': u'sept.',
 u'number': u'',
 u'pages': u'989 -994',
 u'title': u'Context-sensitive in-the-world interfaces for mobile manipulation robots',
 u'volume': u'',
 u'year': u'2012'}

fields = {
 u'booktitle': u'RO-MAN',
 # 'conference': u'RO-MAN',
 # 'dblp_id': 1423712,
 u'doi': u'http://dx.doi.org/10.1109/ROMAN.2012.6343878',
 # 'id': 5,
 # u'key': u'LazewatskyS12',
 u'pages': u'989-994',
 u'title': u'Context-sensitive in-the-world interfaces for mobile manipulation robots. ',
 # 'type': u'inproceedings',
 # 'venue': u'RO-MAN 2012:989-994',
 # 'venue_url': u'db/conf/ro-man/ro-man2012.html#LazewatskyS12',
 u'year': '2012'}


entry = Entry('inproceedings', persons=dict(author=authors), fields=fields)
entry.key = 'asdf'
output_backend = find_plugin('pybtex.backends', 'html')
style_cls = find_plugin('pybtex.style.formatting', 'plain')
style = style_cls()

entries = [entry]
formatted_entries = style.format_entries(entries)
formatted_bibliography = FormattedBibliography(formatted_entries, style)
stream = io.StringIO()
ob = output_backend(None)
for entry in formatted_bibliography:
    print u'<dt>%s</dt>\n' % entry.label
    print u'<dd>%s</dd>\n' % entry.text.render(ob)

    # entry.key, entry.label, entry.text.render(ob))

# ob.write_to_stream(formatted_bibliography, stream)
# stream.seek(0)
print stream.read()

# from citation_manager import models; models.Publication.objects.filter(type="inproceedings")[0].html()