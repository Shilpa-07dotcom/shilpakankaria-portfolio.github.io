/* ============================================================
   Shilpa — "Maison" interactions
   ============================================================ */
(function () {
  'use strict';
  const reduce = window.matchMedia('(prefers-reduced-motion: reduce)').matches;

  /* Masthead entrance */
  requestAnimationFrame(() => {
    document.getElementById('display')?.classList.add('in');
  });

  /* Top bar: condense on scroll + progress */
  const topbar = document.getElementById('topbar');
  const progress = document.getElementById('progress');
  const onScroll = () => {
    topbar.classList.toggle('scrolled', window.scrollY > 40);
    const h = document.documentElement.scrollHeight - window.innerHeight;
    if (progress) progress.style.width = (window.scrollY / h) * 100 + '%';
  };
  window.addEventListener('scroll', onScroll, { passive: true });
  onScroll();

  /* Mobile nav */
  const burger = document.getElementById('burger');
  const topnav = document.getElementById('topnav');
  burger?.addEventListener('click', () => {
    burger.classList.toggle('open');
    topnav.classList.toggle('open');
  });
  topnav?.querySelectorAll('a').forEach(a =>
    a.addEventListener('click', () => {
      burger.classList.remove('open');
      topnav.classList.remove('open');
    })
  );

  /* Reveal on scroll */
  const io = new IntersectionObserver((entries) => {
    entries.forEach(e => {
      if (e.isIntersecting) { e.target.classList.add('in'); io.unobserve(e.target); }
    });
  }, { threshold: 0.12, rootMargin: '0px 0px -8% 0px' });
  document.querySelectorAll('.reveal').forEach(el => io.observe(el));

  /* Active nav link by section */
  const sections = [...document.querySelectorAll('section[id]')];
  const linkFor = id => document.querySelector(`.topnav a[href="#${id}"]`);
  const spy = new IntersectionObserver((entries) => {
    entries.forEach(e => {
      const l = linkFor(e.target.id);
      if (l && e.isIntersecting) {
        document.querySelectorAll('.topnav a').forEach(a => a.classList.remove('active'));
        l.classList.add('active');
      }
    });
  }, { rootMargin: '-48% 0px -50% 0px' });
  sections.forEach(s => spy.observe(s));
})();
