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
})();
