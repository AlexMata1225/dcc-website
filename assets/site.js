(function () {
  var nav = document.querySelector('.nav');
  var toggle = document.querySelector('.nav__toggle');
  if (toggle) {
    toggle.addEventListener('click', function () {
      var open = nav.classList.toggle('is-open');
      toggle.setAttribute('aria-expanded', open ? 'true' : 'false');
    });
    nav.querySelectorAll('.nav__links a').forEach(function (link) {
      link.addEventListener('click', function () {
        nav.classList.remove('is-open');
        toggle.setAttribute('aria-expanded', 'false');
      });
    });
  }

  var reduced = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  var revealed = document.querySelectorAll('.reveal');
  if (reduced || !('IntersectionObserver' in window)) {
    revealed.forEach(function (el) { el.classList.add('is-in'); });
  } else {
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (entry) {
        if (entry.isIntersecting) {
          entry.target.classList.add('is-in');
          io.unobserve(entry.target);
        }
      });
    }, { threshold: 0.12, rootMargin: '0px 0px -40px 0px' });
    revealed.forEach(function (el) { io.observe(el); });
  }

  var year = document.getElementById('year');
  if (year) year.textContent = new Date().getFullYear();

  // Schedule: grey out past meetings and point "Next up" + the hero banner at
  // the first meeting that hasn't happened yet (a meeting stays "next" all day).
  var rows = document.querySelectorAll('.timeline__row[data-date]');
  if (rows.length) {
    var now = new Date();
    var pad = function (n) { return (n < 10 ? '0' : '') + n; };
    var today = now.getFullYear() + '-' + pad(now.getMonth() + 1) + '-' + pad(now.getDate());
    var next = null;
    rows.forEach(function (row) {
      var past = row.getAttribute('data-date') < today;
      row.classList.toggle('is-past', past);
      row.classList.remove('is-next');
      if (!past && !next) next = row;
    });

    var title = document.querySelector('[data-next-title]');
    var when = document.querySelector('[data-next-when]');
    var announce = document.querySelector('[data-next-announce]');
    if (next) {
      next.classList.add('is-next');
      var parts = next.getAttribute('data-date').split('-');
      var date = new Date(+parts[0], +parts[1] - 1, +parts[2]);
      var where = next.getAttribute('data-where') || '5:00 PM · Farrell Hall A27';
      var long = date.toLocaleDateString('en-US', { weekday: 'long', month: 'long', day: 'numeric' });
      var short = date.toLocaleDateString('en-US', { weekday: 'short', month: 'short', day: 'numeric' });
      if (title) title.textContent = next.querySelector('h3').textContent;
      if (when) when.textContent = long + ' · ' + where;
      if (announce) announce.textContent = 'Next meeting · ' + short + ' · ' + where;
    } else {
      if (title) title.textContent = 'Spring schedule coming soon';
      if (when) when.textContent = 'General meetings resume in January. Follow us on Instagram for dates.';
      if (announce) announce.textContent = 'Spring schedule coming soon';
    }
  }
})();
