"""Build the DCC website. Use --production for the public, indexable release."""
from pathlib import Path
from html import escape
import json
from hashlib import sha256
import argparse

parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument('--production', action='store_true')
args = parser.parse_args()

ROOT = Path(__file__).resolve().parent
OUT = ROOT
EMAIL = 'wakeforestdcc@gmail.com'
INSTAGRAM = 'https://www.instagram.com/wfudcc/'
LIBRARY = 'https://drive.google.com/drive/folders/1q9VJMApmxaVNnsFuPd0IaL99cgaR_UpA?usp=drive_link'
JOIN = 'https://mail.google.com/mail/?view=cm&fs=1&to=wakeforestdcc@gmail.com&su=Joining%20the%20Deacon%20Consulting%20Club'
ARROW = '<span aria-hidden="true">↗</span>'
NAV = [('work', 'Our work'), ('analysts', 'Analyst Program'), ('club', 'The club'), ('people', 'Our people'), ('resources', 'Resources')]

def link(href, label, cls='text-link', external=False):
    ext = ' target="_blank" rel="noopener noreferrer"' if external else ''
    return f'<a class="{cls}" href="{escape(href, quote=True)}"{ext}>{label} {ARROW}</a>'

def photo(src, alt, caption='', cls='', eager=False):
    dims = {'campus.jpg': (1536,624), 'club-meeting.webp': (2200,1650), 'club-discussion.webp': (1600,1200), 'farrell-interior.webp': (2000,796), 'farrell-exterior.webp': (1500,500), 'hearn-autumn.webp': (1400,933)}
    w,h = dims[src]
    loading = 'fetchpriority="high"' if eager else 'loading="lazy"'
    return f'<figure class="photo {cls}"><img src="assets/{src}" alt="{escape(alt, quote=True)}" width="{w}" height="{h}" {loading}>{f"<figcaption>{caption}</figcaption>" if caption else ""}</figure>'


def campus_photo(src, alt, caption, source, cls='', eager=False):
    credit=f'<span class="photo-credit"><a href="{source}" target="_blank" rel="noopener noreferrer">Wake Forest University ↗</a></span>'
    return photo(src, alt, f'{caption} {credit}', f'campus-photo {cls}', eager)


def intro(label, title, desc, extra=''):
    return f'<section class="page-intro wrap"><p class="eyebrow">{label}</p><div class="intro-grid"><h1>{title}</h1><div class="intro-copy"><p>{desc}</p>{extra}</div></div></section>'

def close(title='Get involved with DCC.', desc='Explore consulting with fellow Deacs, or bring a new perspective to the club.', first=None, second=None):
    first = first or ('club.html#join', 'Join the club')
    second = second or ('partner.html', 'Partner with DCC')
    return f'<section class="closing"><div class="wrap closing-grid"><div><p class="eyebrow">Deacon Consulting Club</p><h2>{title}</h2><p>{desc}</p></div><div class="closing-actions">{link(*first, cls="button light")}{link(*second, cls="text-link")}</div></div></section>'

def shell(key, title, description, body):
    canonical = 'https://wfudcc.org/' + ('' if key == 'index' else key + '.html')
    indexing = ('<meta name="robots" content="index,follow"><link rel="canonical" href="' + canonical + '">') if args.production else '<meta name="robots" content="noindex,nofollow">'
    css_version=sha256((OUT/'site.css').read_bytes()).hexdigest()[:10]
    campus_version=sha256((OUT/'campus.css').read_bytes()).hexdigest()[:10]
    js_version=sha256((OUT/'site.js').read_bytes()).hexdigest()[:10]
    events_version=sha256((OUT/'events.js').read_bytes()).hexdigest()[:10]
    nav=''.join(f'<a href="{slug}.html"{chr(32)+"aria-current=\"page\"" if slug==key else ""}>{name}</a>' for slug,name in NAV)
    footer_nav=''.join(f'<a href="{slug}.html">{name}</a>' for slug,name in NAV)
    return f'''<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta name="color-scheme" content="light">{indexing}<title>{title} | Deacon Consulting Club</title><meta name="description" content="{escape(description,quote=True)}"><meta name="theme-color" content="#20211e"><link rel="icon" href="assets/dcc-monogram.png"><link rel="preload" href="assets/open-sans-regular.ttf" as="font" type="font/ttf" crossorigin><link rel="stylesheet" href="site.css?v={css_version}"><link rel="stylesheet" href="campus.css?v={campus_version}"><script src="events.js?v={events_version}" defer></script><script src="site.js?v={js_version}" defer></script></head>
<body data-page="{key}"><a class="skip-link" href="#main">Skip to content</a>
<header class="site-header"><div class="header-inner wrap"><a class="brand" href="index.html" aria-label="Deacon Consulting Club home"><img src="assets/dcc-monogram.png" alt="" width="76" height="35"><span>Deacon Consulting Club<small>Wake Forest University</small></span></a><button class="menu-toggle" aria-expanded="false" aria-controls="main-nav">Menu <span class="menu-icon" aria-hidden="true"></span></button><nav id="main-nav" aria-label="Main navigation">{nav}<a class="nav-partner" href="partner.html"{' aria-current="page"' if key=='partner' else ''}>Partner with us {ARROW}</a></nav></div></header>
<main id="main">{body}</main>
<footer class="site-footer"><div class="wrap footer-grid"><div class="footer-about"><a class="footer-name" href="index.html">Deacon<br>Consulting Club<span class="gold-dot">.</span></a><p>A student-led consulting organization<br>at Wake Forest University.<br>Winston-Salem, North Carolina.</p></div><div class="footer-links"><p class="eyebrow">Explore</p>{footer_nav}<a href="partner.html">Partner with us</a></div><div class="footer-contact"><p class="eyebrow">Stay connected</p><a href="mailto:{EMAIL}">{EMAIL}</a><a href="{INSTAGRAM}" target="_blank" rel="noopener noreferrer">Instagram ↗</a><a href="{LIBRARY}" target="_blank" rel="noopener noreferrer">DCC case library ↗</a></div></div><div class="wrap footer-bottom"><span>© <span data-year>2026</span> Deacon Consulting Club</span><span>Pro Humanitate</span></div></footer></body></html>'''

pages = {}

pages['index'] = ('Student consulting at Wake Forest', 'Deacon Consulting Club brings Wake Forest students together for case preparation, alumni connections, and pro bono consulting.', f'''
<section class="home-intro wrap"><p class="eyebrow">Wake Forest University <span class="label-divider"></span> Winston-Salem, NC</p><div class="home-intro-grid"><h1>Student consulting.<br>Rooted at Wake Forest.</h1><div class="hero-copy"><p>We bring Wake Forest students together for case preparation, alumni connections, and pro bono work in our community.</p>{link('club.html','Get to know DCC')}</div></div></section>
<div class="wrap hero-photo">{photo('campus.jpg','Wait Chapel overlooking the green lawn at Wake Forest University','Our campus. Our starting point. <span>Wait Chapel · Wake Forest University</span>',eager=True)}</div>
<div class="wrap program-note"><span class="eyebrow">The Analyst Program</span><p>14 students. Hands-on client work. A semester of learning.</p>{link('analysts.html','Explore the program')}</div>
<section class="section wrap campus-learning" id="wake-campus"><div><p class="eyebrow">What brings us together</p><h2>How we learn<br>consulting.</h2><div class="learning-rows"><a href="resources.html"><div><span class="small-label">Learn</span><h3>Practice with other Deacs.</h3><p>Work through cases, prepare for interviews, and learn to explain your thinking.</p></div>{ARROW}</a><a href="work.html"><div><span class="small-label">Apply</span><h3>Take on a real question.</h3><p>Bring research and analysis to pro bono projects for local organizations.</p></div>{ARROW}</a><a href="club.html"><div><span class="small-label">Connect</span><h3>Get to know the community.</h3><p>Find your peers, learn from Wake alumni, and hear from practicing consultants.</p></div>{ARROW}</a></div></div>{campus_photo('hearn-autumn.webp','Autumn leaves frame students walking across Hearn Plaza at Wake Forest','Fall on Hearn Plaza.','https://admissions.wfu.edu/visit/tour/','autumn-portrait')}</section>
<section class="warm-section"><div class="wrap section split-feature">{photo('club-meeting.webp','DCC members taking part in a classroom session, with a speaker at the front','A gathering of DCC members at Wake Forest.','meeting-photo')}<div class="feature-copy"><p class="eyebrow">Inside the club</p><h2>Start with<br>a conversation.</h2><p>You don’t need a business major or a polished case framework to walk into a DCC meeting. General membership is open to every Wake Forest major and class year.</p><p>Come with a question. Find a practice partner. Get to know the people behind the work.</p>{link('club.html#join','Join the club','button')}</div></div></section>
<section class="section wrap work-feature"><div><p class="eyebrow">Our work</p><h2>Pro Humanitate,<br>put into practice.</h2></div><div><p class="large-copy">Student teams working on questions that matter to local organizations.</p><p>Our pro bono work connects the consulting skills we practice with the needs of nonprofits and small businesses in Winston-Salem. Projects bring together research, analysis, and a final presentation to the client.</p>{link('work.html','How we work')}</div></section>
<section class="wrap campus-event" id="farrell">{campus_photo('farrell-interior.webp','The open atrium and study spaces of the Founders Living Room in Farrell Hall','Founders Living Room · Farrell Hall','https://parents.wfu.edu/2017/02/panoramic-view-of-farrell-hall-living-room/','farrell-event')}<div class="campus-event-copy"><p class="eyebrow">On the calendar</p><h2>Meet us<br>at Farrell.</h2><div data-next-event><h3>Fall 2026 at DCC</h3><p>Case practice, alumni conversations, and project presentations.</p></div>{link('club.html#calendar','See the calendar')}</div></section>
{close()}
''')

pages['work'] = ('Our work', 'Pro bono student consulting for nonprofits and small businesses in Winston-Salem.', f'''
{intro('Our work','Pro bono consulting<br>in Winston-Salem.','DCC connects Wake Forest students with nonprofits and small businesses through pro bono consulting. Our teams turn a business question into research, analysis, and recommendations.',link('partner.html#clients','Discuss a project'))}
<section class="warm-section"><div class="wrap section work-overview"><div><p class="eyebrow">Pro bono consulting</p><h2>Research, analysis,<br>and a recommendation.</h2><p>Semester-long projects give students the opportunity to work through a real challenge with a client. The work concludes with a presentation of findings and recommendations.</p><p>We’re a student-led club. Project conversations help us understand where our teams’ skills and a local organization’s needs fit together.</p></div><div class="service-list"><article><span class="small-label">Strategy & research</span><h3>Understand the challenge.</h3><p>Research the organization’s context, examine the problem, and explore possible approaches.</p></article><article><span class="small-label">Data & analysis</span><h3>Make sense of the evidence.</h3><p>Organize information, analyze data, and connect findings to the question at hand.</p></article><article><span class="small-label">Recommendations</span><h3>Communicate a clear next step.</h3><p>Bring the work together in a client presentation, with findings and practical recommendations.</p></article></div></div></section>
<section class="section wrap"><div class="section-heading"><p class="eyebrow">From the classroom to the community</p><h2>The people doing the work.</h2></div><div class="work-people"><div>{photo('club-discussion.webp','A DCC member explaining a point during a small-group discussion','Discussion and practice are part of life at DCC.','discussion-photo')}</div><div class="feature-copy"><p class="large-copy">The Analyst Program connects preparation with experience.</p><p>The 14-person program combines client projects with case and fit interview practice, feedback, and conversations with practicing consultants.</p><p>Analysts remain part of the wider DCC community, learning and practicing alongside fellow members.</p>{link('analysts.html','Meet the Analyst Program')}</div></div></section>
<section class="wrap section ruled-section"><div class="work-feature"><div><p class="eyebrow">For prospective clients</p><h2>Tell us what<br>you’re working on.</h2></div><div><p class="large-copy">A useful first conversation starts with the question you want to answer.</p><p>Introduce your organization, the challenge you’re exploring, and your preferred timing. We’ll discuss whether there’s a fit for a student project.</p>{link('mailto:'+EMAIL+'?subject=DCC%20project%20inquiry','Email us about a project','button')}</div></div></section>
{close('Learning through real work.','Explore the program behind our student consulting teams.',('analysts.html','The Analyst Program'),('people.html','Our people'))}
''')

faqs = [
 ('How is the Analyst Program different from general membership?', 'General membership is open to all Wake Forest students. The Analyst Program is a selective opportunity within the club, with client-team responsibilities and additional preparation, events, and consultant connections. Analysts remain full members of DCC.'),
 ('Who can apply?', 'The program is open to Wake Forest undergraduates across majors and class years. No prior consulting experience is required.'),
 ('How does selection work?', 'The current process includes a short application and video response, followed by a conversation with members of the executive board. Selected analysts join a pro bono client team.'),
 ('When is the next application cycle?', 'Applications for the fall 2026 cohort are closed. The next cycle will be announced at general meetings and on the DCC Instagram account.'),
 ('Can I participate while applications are closed?', 'Yes. Come to general meetings, attend club workshops, and use the case-prep resources. General club participation is separate from selection into the Analyst Program.')
]
faq_html=''.join(f'<details><summary>{q}<span aria-hidden="true">+</span></summary><div class="details-body"><p>{a}</p></div></details>' for q,a in faqs)
pages['analysts'] = ('Analyst Program', 'A 14-person program combining pro bono client work, interview preparation, and consultant connections.', f'''
{intro('The Analyst Program','The DCC<br>Analyst Program.','A selective program for Wake Forest students ready to take on client projects and deepen their consulting preparation. Fourteen analysts, learning through experience.')}
<div class="wrap program-campus">{campus_photo('farrell-interior.webp','Students studying in the Founders Living Room at Farrell Hall','Founders Living Room · Farrell Hall','https://parents.wfu.edu/2017/02/panoramic-view-of-farrell-hall-living-room/','',True)}</div>
<section class="analyst-banner"><div class="wrap analyst-banner-inner"><div><span class="cohort-number">14</span><span class="cohort-label">Analysts in the<br>fall 2026 cohort</span></div><div class="cohort-message"><p class="eyebrow">Current cohort</p><h2>Applications are closed.</h2><p>The next cycle will be announced at general meetings and on Instagram.</p>{link(INSTAGRAM,'Follow @wfudcc','text-link',True)}</div></div></section>
<section class="section wrap"><div class="section-heading"><p class="eyebrow">The experience</p><h2>What analysts do.</h2></div><div class="program-grid"><article><h3>Client work</h3><p>Join a pro bono engagement team, work through a client challenge, and present the team’s recommendations.</p></article><article><h3>Interview preparation</h3><p>Practice case and fit interviews through workshops, mock interviews, and personalized feedback.</p></article><article><h3>Professional connections</h3><p>Learn from practicing consultants and Wake alumni through networking events and introductions.</p></article><article><h3>Office visits</h3><p>Explore the work and culture of consulting firms through in-person office treks.</p></article></div></section>
<section class="warm-section"><div class="wrap section application-layout"><div><p class="eyebrow">Joining the program</p><h2>The application<br>process.</h2><p>Open to undergraduates across Wake Forest. Prior consulting experience is not required.</p>{link('club.html','Get involved with DCC')}</div><ol class="application-steps"><li><h3>Apply</h3><p>Complete a short application and video response when the next cycle opens.</p></li><li><h3>Interview</h3><p>Have a conversation with members of the executive board.</p></li><li><h3>Join a team</h3><p>Take on a pro bono project and participate in the analyst calendar of preparation and events.</p></li></ol></div></section>
<section class="section wrap faq-layout"><div><p class="eyebrow">A few useful details</p><h2>Before you apply.</h2><p>For questions about the program,<br>{link('mailto:'+EMAIL+'?subject=DCC%20Analyst%20Program','contact the board')}.</p></div><div class="accordions">{faq_html}</div></section>
{close('Keep learning with DCC.','General meetings and club resources are open while Analyst Program applications are closed.',('club.html#join','Join the club'),('resources.html','Explore resources'))}
''')

events = [
 {'date':'2026-09-08','title':'DCC intro meeting','description':'Meet the board and hear the plan for the year.'},
 {'date':'2026-09-15','title':'Networking 101','description':'Coffee chats and networking, with a Wake alum consulting at Accenture.'},
 {'date':'2026-09-29','title':'Behavioral interview prep','description':'Strategic storytelling with the Office of Leadership.'},
 {'date':'2026-10-06','title':'Case interview walkthrough','description':'From the case prompt to a final recommendation.'},
 {'date':'2026-10-20','title':'Structures & frameworks','description':'Case workshop: build a framework around the problem.'},
 {'date':'2026-11-03','title':'Math & exhibits','description':'Case workshop: practice calculations and interpret charts.'},
 {'date':'2026-11-17','title':'Alumni panel','description':'Wake alumni discuss recruiting, firm culture, and their experience.'},
 {'date':'2026-12-01','title':'Pro bono final presentations','description':'Our teams present their recommendations to close the semester.'}
]
from datetime import date
event_rows = ''.join(f'''<article class="event-row" data-event-date="{e['date']}"><time datetime="{e['date']}"><span>{date.fromisoformat(e['date']).strftime('%b')}</span><strong>{date.fromisoformat(e['date']).day:02d}</strong></time><div><h3>{escape(e['title'])}</h3><p>{escape(e['description'])}</p></div><span class="event-time">5:00 PM <span>Farrell Hall A27</span></span></article>''' for e in events)
pages['club'] = ('The club', 'An open community for Wake Forest students exploring consulting. Meetings, case workshops, and alumni connections.', f'''
{intro('The club','A community for<br>curious Deacs.','Every major. Every class year. DCC brings students together to explore consulting, practice with peers, and learn from the Wake Forest community.',link('#join','Come to a meeting','button'))}
<div class="wrap club-panorama">{photo('club-meeting.webp','Wake Forest students participating in a Deacon Consulting Club meeting','Inside a DCC meeting at Wake Forest.','meeting-photo',True)}</div>
<section class="section wrap work-feature"><div><p class="eyebrow">What to expect</p><h2>Learning with<br>other students.</h2></div><div><p class="large-copy">Start wherever you are.</p><p>General meetings build from networking and behavioral preparation to live case practice. Along the way, you’ll meet other students exploring the same questions and hear from people working in the industry.</p><p>Our activities include case workshops, resume preparation, information sessions, panels, and case competition teams.</p>{link('analysts.html','Looking for client experience? Explore the Analyst Program')}</div></section>
<section class="warm-section" id="calendar"><div class="wrap section calendar-layout"><div class="calendar-intro">{campus_photo('farrell-exterior.webp','Farrell Hall in warm evening light with Wait Chapel visible beyond the trees','Farrell Hall, Wake Forest University.','https://business.wfu.edu/campus-winston-salem/farrell-hall/','calendar-campus')}<p class="eyebrow">Fall 2026</p><h2>The semester<br>at a glance.</h2><p>General meetings<br><strong>Tuesdays · 5:00 PM</strong><br>Farrell Hall A27</p><p class="muted">Follow DCC for meeting updates.</p>{link(INSTAGRAM,'Instagram','text-link',True)}<button class="text-link calendar-download" type="button">Add remaining events to calendar {ARROW}</button></div><div class="event-list">{event_rows}</div></div></section>
<section class="section wrap join-layout" id="join"><div><p class="eyebrow">Join the club</p><h2>We’ll see you<br>at the next meeting.</h2></div><div><p class="large-copy">You can join DCC without applying to the Analyst Program.</p><p>Drop in to a general meeting, or email the board to introduce yourself and get connected to the club’s GroupMe. There’s no prior consulting experience required.</p><div class="button-row">{link(JOIN,'Email us to join','button',True)}{link('resources.html','Start with the resources')}</div><p class="contact-note">{EMAIL}</p></div></section>
{close('A Wake connection that continues.','Alumni help members see what a consulting career can look like. Share your experience through a conversation, case session, or panel.',('partner.html#alumni','Get involved as an alum'),('people.html','Meet the board'))}
''')

board=[('Addison Spell','President','https://www.linkedin.com/in/addison-spell/'),('James Kaye','Vice President',''),('Alex Helmrich','Treasurer',''),('Alex Mata','VP of Engagement',''),('Olivia Anglin','VP of Education',''),('Charlie Wolff','Pro Bono Chair','https://www.linkedin.com/in/charles-wolf-89b150222/'),('Ryan Hall','VP of Marketing',''),('Sarah Burke','Secretary','')]
board_html=''.join(f'<article class="person"><p class="small-label">{role}</p><h3>{name}</h3>{link(url,"LinkedIn","person-link",True) if url else ""}</article>' for name,role,url in board)
pages['people'] = ('Our people', 'Meet the student executive board of Deacon Consulting Club at Wake Forest University.', f'''
{intro('Our people','The people<br>behind DCC.','DCC is led by Wake Forest students who organize our programs, connect with the community, and help members find their footing in consulting.')}
<section class="wrap board-section"><div class="board-heading"><h2>Executive board</h2><p class="eyebrow">2026–2027</p></div><div class="board-grid">{board_html}</div></section>
<section class="warm-section"><div class="wrap section split-feature">{photo('club-discussion.webp','DCC members in a small-group conversation','Learning together at DCC.','discussion-photo')}<div class="feature-copy"><p class="eyebrow">Beyond the board</p><h2>A club built<br>through participation.</h2><p>Practice partners, project teammates, workshop participants, and alumni all contribute to the DCC experience.</p><p>Whether you’re exploring consulting for the first time or preparing for an interview, the club is a place to learn alongside other Deacs.</p>{link('club.html','Get to know the club')}</div></div></section>
{close('Let’s get acquainted.','Have a question about membership, the Analyst Program, or working with DCC? Get in touch with the board.',('mailto:'+EMAIL,'Contact the board'),('partner.html','Explore partnerships'))}
''')

pages['partner'] = ('Partner with DCC', 'Work with Deacon Consulting Club as a prospective client, consulting firm, or Wake Forest alumnus.', f'''
{intro('Partner with DCC','Work with<br>Deacon Consulting Club.','Work with our student teams, introduce members to your firm, or help a fellow Deac prepare for a career in consulting.')}
<div class="wrap partner-jumps"><a href="#clients">For organizations <span>↓</span></a><a href="#firms">For consulting firms <span>↓</span></a><a href="#alumni">For Wake alumni <span>↓</span></a></div>
<section class="wrap partner-section" id="clients"><div><p class="eyebrow">For organizations</p><h2>A project with<br>a local connection.</h2></div><div><p class="large-copy">Explore a pro bono engagement with a Wake Forest student team.</p><p>We work with nonprofits and small businesses on strategy, research, and analysis. A first conversation helps us understand the challenge and whether there’s a fit for a student project.</p><p>Tell us about your organization, the question you’re trying to answer, and your preferred timing.</p>{link('mailto:'+EMAIL+'?subject=DCC%20project%20inquiry','Start a project conversation','button')}{link('work.html','More about our work')}</div></section>
<section class="warm-section" id="firms"><div class="wrap partner-section"><div><p class="eyebrow">For consulting firms</p><h2>Meet the next<br>generation of Deacs.</h2></div><div><p class="large-copy">Give students a closer look at the work and the people behind it.</p><p>Information sessions, career panels, case workshops, and office visits help members understand consulting and prepare thoughtfully for recruiting.</p><ul class="plain-list"><li>Introduce your firm and its work.</li><li>Lead a case or interview preparation session.</li><li>Discuss an office visit or student event.</li></ul>{link('mailto:'+EMAIL+'?subject=DCC%20firm%20engagement','Connect with the club','button')}</div></div></section>
<section class="wrap partner-section" id="alumni"><div><p class="eyebrow">For Wake alumni</p><h2>Your experience.<br>A student’s next step.</h2></div><div><p class="large-copy">A conversation with someone who has been there can make a difference.</p><p>Share what you’ve learned through a panel, lead a mock case interview, or mentor a current student. We’d love to hear where your Wake experience has taken you.</p>{link('mailto:'+EMAIL+'?subject=DCC%20alumni%20involvement','Get involved as an alum','button')}</div></section>
<section class="partner-campus">{campus_photo('farrell-exterior.webp','Farrell Hall and the Wait Chapel spire in evening light','Farrell Hall · Wake Forest University','https://business.wfu.edu/campus-winston-salem/farrell-hall/')}</section>
{close('Start a conversation.','The board can help you find the right way to get involved.',('mailto:'+EMAIL,'Email DCC'),('people.html','Meet the board'))}
''')

resources=[
 ('Cases','DCC case library','Case books and practice material for working through cases with a partner.',LIBRARY,'Google Drive'),
 ('Cases','CaseQuestions.com','Marc Cosentino’s course and case interview preparation materials.','https://learning.casequestions.com/offers/PHCFopVE/checkout','Learning platform'),
 ('Cases','RocketBlocks','Drills for structures, charts, and case math.','https://www.rocketblocks.me/','Learning platform'),
 ('Careers','OPCD career resources','Wake Forest career coaching, pathways, and recruiting resources.','https://opcd.wfu.edu/','Wake Forest'),
 ('Industry','Vault','Firm research, culture guides, and industry information.','https://www.vault.com/','Research'),
 ('Industry','What is consulting?','An introduction to the consulting industry.','https://www.youtube.com/watch?v=3wPeND2gvqc','Video'),
 ('Industry','Career Crush: Is consulting right for you?','Harvard Business Review’s video introduction to consulting careers.','https://youtu.be/klhPu-B3N9E','Video · HBR'),
 ('Industry','Is consulting the right career for you?','Read the Harvard Business Review Career Crush article.','https://hbr.org/2021/11/career-crush-is-consulting-the-right-career-for-you','Article · HBR'),
 ('Industry','So you want to be a consultant?','Five signs that consulting may be a fit.','https://www.forbes.com/sites/forbesagencycouncil/2018/05/21/so-you-want-to-be-a-consultant-five-signs-consulting-is-right-for-you/','Article · Forbes'),
 ('Industry','Skills for management consulting','An overview of the skills used in consulting.','https://casecoach.com/b/skills-management-consulting/','Guide · CaseCoach'),
 ('Networking','The awkward person’s guide to networking','Advice for starting professional conversations.','https://hbr.org/2021/09/the-awkward-persons-guide-to-networking','Article · HBR'),
 ('Networking','Build your network','Wake Forest’s guide to developing professional connections.','https://opcd.wfu.edu/students/build-your-network/','Guide · WFU OPCD'),
 ('Networking','Berkeley networking guide','A practical reference for reaching out and following up.','https://www.ischool.berkeley.edu/careers/guides/networking','Guide · UC Berkeley'),
 ('Cases','Practice with DCC','Meet other members and work through cases at a club workshop.','club.html#calendar','In person'),
]
resource_html=''.join(f'<a class="resource-row" data-category="{cat}" href="{escape(url,quote=True)}"{(" target=\"_blank\" rel=\"noopener noreferrer\"" if url.startswith("https") else "")}><span class="resource-category">{cat}</span><div><h3>{title}</h3><p>{desc}</p></div><span class="resource-source">{source}</span>{ARROW}</a>' for cat,title,desc,url,source in resources)
filter_html=''.join(f'<button type="button" data-filter="{cat}" aria-pressed="{"true" if cat=="All" else "false"}">{cat}</button>' for cat in ['All','Cases','Industry','Networking','Careers'])
pages['resources'] = ('Resources', 'Case books, interview preparation, industry research, and networking resources for DCC members.', f'''
{intro('Resources','The DCC<br>resource library.','The club’s collection of case-prep tools, career resources, and reading. Explore on your own, then find a partner at a DCC meeting.')}
<section class="library-feature"><div class="wrap library-feature-inner library-with-photo"><div><p class="eyebrow">The DCC case library</p><h2>Your next case<br>starts here.</h2><p>Case books and practice material in one place. Bring a case to your next practice session.</p>{link(LIBRARY,'Open the case library','button light',True)}</div>{campus_photo('farrell-interior.webp','The study and gathering spaces inside Farrell Hall','Founders Living Room · Farrell Hall','https://parents.wfu.edu/2017/02/panoramic-view-of-farrell-hall-living-room/','library-campus')}</div></section>
<section class="section wrap resources-section"><div class="resource-controls"><div><label class="eyebrow" for="resource-search">Find a resource</label><input type="search" id="resource-search" placeholder="Search cases, networking, careers…" autocomplete="off"></div><fieldset class="filters"><legend class="sr-only">Filter resources by topic</legend>{filter_html}</fieldset></div><div class="resource-meta"><p id="resource-count" aria-live="polite">{len(resources)} resources</p><p>Some resources require an account or paid access.</p></div><div class="resource-list">{resource_html}</div><p class="resource-empty" hidden>No resources match your search. Try another term or choose All.</p></section>
<section class="warm-section"><div class="wrap section work-feature"><div><p class="eyebrow">Behavioral preparation</p><h2>Make your<br>experience clear.</h2></div><div><p class="large-copy">Practice telling the story behind your resume.</p><p>Use STAR—situation, task, action, result—to structure examples of leadership, conflict, learning, and impact. Work through them with a partner and ask for feedback.</p>{link('mailto:'+EMAIL+'?subject=DCC%20interview%20practice','Ask the board about practice sessions')}</div></div></section>
{close('Practice is better with a partner.','Find fellow students preparing for consulting at a DCC meeting.',('club.html#calendar','See the calendar'),('club.html#join','Join the club'))}
''')

(OUT/'events.js').write_text('window.DCC_EVENTS = '+json.dumps(events,ensure_ascii=True)+';\n')

for key,(title,desc,body) in pages.items():
    (OUT/f'{key}.html').write_text(shell(key,title,desc,body))
(OUT/'events.json').write_text(json.dumps(events,indent=2))
print(f'Built {len(pages)} pages in {OUT}')
