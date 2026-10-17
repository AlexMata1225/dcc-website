'use strict';
// Preserve bookmarks from the previous single-page website.
if (document.body.dataset.page === 'index') {
  const legacySections = {
    '#about': 'club.html',
    '#work': 'work.html',
    '#programs': 'club.html',
    '#analysts': 'analysts.html',
    '#schedule': 'club.html#calendar',
    '#board': 'people.html',
    '#join': 'club.html#join'
  };
  const routeLegacySection = () => {
    const destination = legacySections[window.location.hash];
    if (destination) window.location.replace(destination);
  };
  routeLegacySection();
  window.addEventListener('hashchange', routeLegacySection);
}
const menuButton = document.querySelector('.menu-toggle');
const navigation = document.querySelector('#main-nav');
const closeMenu = () => {menuButton.setAttribute('aria-expanded','false'); navigation.classList.remove('is-open');};
menuButton.addEventListener('click', () => {
  const open = menuButton.getAttribute('aria-expanded') !== 'true';
  menuButton.setAttribute('aria-expanded',String(open));
  navigation.classList.toggle('is-open',open);
});
document.addEventListener('keydown', event => {
  if(event.key === 'Escape' && menuButton.getAttribute('aria-expanded') === 'true') {closeMenu();menuButton.focus();}
});
document.addEventListener('click', event => {
  if(!event.target.closest('.site-header')) closeMenu();
});
navigation.addEventListener('click', event => {if(event.target.closest('a')) closeMenu();});
window.matchMedia('(min-width:981px)').addEventListener('change', event => {if(event.matches) closeMenu();});
document.querySelectorAll('[data-year]').forEach(el => el.textContent = new Date().getFullYear());

// Classify meetings in campus time so a visitor's timezone cannot hide a future event.
const campusParts = Object.fromEntries(new Intl.DateTimeFormat('en-CA',{timeZone:'America/New_York',year:'numeric',month:'2-digit',day:'2-digit',hour:'2-digit',minute:'2-digit',hourCycle:'h23'}).formatToParts(new Date()).filter(p=>p.type!=='literal').map(p=>[p.type,p.value]));
const campusDate = `${campusParts.year}-${campusParts.month}-${campusParts.day}`;
const campusTime = `${campusParts.hour}:${campusParts.minute}`;
const remainsUpcoming = date => date > campusDate || (date === campusDate && campusTime < '17:00');
const rows = [...document.querySelectorAll('[data-event-date]')];
let nextMarked = false;
rows.forEach(row => {
  const upcoming = remainsUpcoming(row.dataset.eventDate);
  row.classList.toggle('is-past',!upcoming);
  if(upcoming && !nextMarked){row.classList.add('is-next');nextMarked=true;}
});

if(document.querySelector('[data-next-event]') || document.querySelector('.calendar-download')) {
  Promise.resolve(window.DCC_EVENTS || []).then(events => {
    const remaining = events.filter(event=>remainsUpcoming(event.date));
    const next = remaining[0];
    const box = document.querySelector('[data-next-event]');
    if(box && next){
      box.querySelector('h3').textContent=next.title;
      const dateText = new Intl.DateTimeFormat('en-US',{timeZone:'America/New_York',weekday:'long',month:'long',day:'numeric'}).format(new Date(`${next.date}T12:00:00-04:00`));
      box.querySelector('p').textContent=`${dateText} · 5:00 PM · Farrell Hall A27`;
    }else if(box){box.querySelector('h3').textContent='See what’s next at DCC';box.querySelector('p').textContent='Follow @wfudcc for the next semester’s meeting announcements.';}
    const download = document.querySelector('.calendar-download');
    if(download){
      if(!remaining.length){download.hidden=true;return;}
      download.addEventListener('click',()=>{
        const esc=s=>s.replace(/\\/g,'\\\\').replace(/\n/g,'\\n').replace(/,/g,'\\,').replace(/;/g,'\\;');
        const stamp = new Date().toISOString().replace(/[-:]/g,'').replace(/\.\d{3}/,'');
        const lines=['BEGIN:VCALENDAR','VERSION:2.0','PRODID:-//Deacon Consulting Club//Meetings//EN','CALSCALE:GREGORIAN','BEGIN:VTIMEZONE','TZID:America/New_York','BEGIN:DAYLIGHT','DTSTART:19700308T020000','RRULE:FREQ=YEARLY;BYMONTH=3;BYDAY=2SU','TZOFFSETFROM:-0500','TZOFFSETTO:-0400','TZNAME:EDT','END:DAYLIGHT','BEGIN:STANDARD','DTSTART:19701101T020000','RRULE:FREQ=YEARLY;BYMONTH=11;BYDAY=1SU','TZOFFSETFROM:-0400','TZOFFSETTO:-0500','TZNAME:EST','END:STANDARD','END:VTIMEZONE'];
        for(const e of remaining){const date=e.date.replace(/-/g,'');lines.push('BEGIN:VEVENT',`UID:dcc-${date}@wfudcc.org`,`DTSTAMP:${stamp}`,`DTSTART;TZID=America/New_York:${date}T170000`,`SUMMARY:${esc('DCC: '+e.title)}`,`DESCRIPTION:${esc(e.description+' Check @wfudcc for updates.')}`,'LOCATION:'+esc('Farrell Hall A27, Wake Forest University'),'END:VEVENT');}
        lines.push('END:VCALENDAR');
        // Fold content lines at 70 code points (all generated text is basic Latin).
        const calendar=lines.map(line=>line.match(/.{1,70}/g).join('\r\n ')).join('\r\n')+'\r\n';
        const url=URL.createObjectURL(new Blob([calendar],{type:'text/calendar;charset=utf-8'}));
        const a=document.createElement('a');a.href=url;a.download='DCC-fall-2026.ics';document.body.append(a);a.click();a.remove();setTimeout(()=>URL.revokeObjectURL(url),1000);
      });
    }
  }).catch(()=>{const download=document.querySelector('.calendar-download');if(download)download.hidden=true;});
}

const search = document.querySelector('#resource-search');
if(search){
  const resourceRows=[...document.querySelectorAll('.resource-row')];
  const filters=[...document.querySelectorAll('[data-filter]')];
  let active='All';
  const update=()=>{
    const query=search.value.trim().toLocaleLowerCase();let count=0;
    resourceRows.forEach(row=>{const visible=(active==='All'||row.dataset.category===active)&&row.textContent.toLocaleLowerCase().includes(query);row.hidden=!visible;if(visible)count++;});
    document.querySelector('#resource-count').textContent=`${count} resource${count===1?'':'s'}`;
    document.querySelector('.resource-empty').hidden=count!==0;
  };
  search.addEventListener('input',update);
  filters.forEach(button=>button.addEventListener('click',()=>{active=button.dataset.filter;filters.forEach(b=>b.setAttribute('aria-pressed',String(b===button)));update();}));
}
