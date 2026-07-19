// Mobile nav toggle
(function () {
  var toggle = document.querySelector('.nav-toggle');
  var nav = document.querySelector('.site-nav');
  if (!toggle || !nav) return;

  toggle.addEventListener('click', function () {
    var open = nav.classList.toggle('open');
    toggle.setAttribute('aria-expanded', open);
  });
})();

// Countdown timer
(function () {
  var el = document.getElementById('countdown');
  if (!el) return;

  var target = new Date(el.dataset.target).getTime();

  function update() {
    var now = Date.now();
    var diff = target - now;
    if (diff <= 0) { el.innerHTML = '<p>C\'est parti !</p>'; return; }

    var days  = Math.floor(diff / 86400000);
    var hours = Math.floor((diff % 86400000) / 3600000);
    var mins  = Math.floor((diff % 3600000)  / 60000);
    var secs  = Math.floor((diff % 60000)    / 1000);

    el.innerHTML =
      unit(days,  'jours') +
      unit(hours, 'heures') +
      unit(mins,  'minutes') +
      unit(secs,  'secondes');
  }

  function unit(v, label) {
    return '<div class="countdown-unit">' +
      '<span class="countdown-value">' + String(v).padStart(2, '0') + '</span>' +
      '<span class="countdown-label">' + label + '</span>' +
      '</div>';
  }

  update();
  setInterval(update, 1000);
})();

// Slideshows
(function () {
  document.querySelectorAll('[data-slideshow]').forEach(function (el) {
    var track   = el.querySelector('.slideshow-track');
    var imgs    = track ? Array.from(track.querySelectorAll('img')) : [];
    var dotsEl  = el.querySelector('.slide-dots');
    var prevBtn = el.querySelector('.slide-prev');
    var nextBtn = el.querySelector('.slide-next');
    var counter = el.querySelector('.slide-counter');
    var placeholder = el.querySelector('.gallery-placeholder');
    var current = 0;

    if (imgs.length === 0) {
      if (prevBtn) prevBtn.hidden = true;
      if (nextBtn) nextBtn.hidden = true;
      if (dotsEl)  dotsEl.hidden  = true;
      if (counter) counter.hidden = true;
      return;
    }

    if (placeholder) placeholder.hidden = true;
    if (counter) counter.querySelector('.slide-total').textContent = imgs.length;

    // Activate first slide
    imgs[0].classList.add('slide-active');

    // Build dots
    imgs.forEach(function (_, i) {
      var dot = document.createElement('button');
      dot.className = 'slide-dot' + (i === 0 ? ' active' : '');
      dot.setAttribute('aria-label', 'Photo ' + (i + 1));
      dot.addEventListener('click', function () { goTo(i); });
      dotsEl.appendChild(dot);
    });

    if (imgs.length === 1) {
      if (prevBtn) prevBtn.hidden = true;
      if (nextBtn) nextBtn.hidden = true;
      if (dotsEl)  dotsEl.hidden  = true;
      if (counter) counter.hidden = true;
    }

    function goTo(index) {
      imgs[current].classList.remove('slide-active');
      current = (index + imgs.length) % imgs.length;
      imgs[current].classList.add('slide-active');
      el.querySelectorAll('.slide-dot').forEach(function (d, i) {
        d.classList.toggle('active', i === current);
      });
      if (counter) counter.querySelector('.slide-current').textContent = current + 1;
    }

    if (prevBtn) prevBtn.addEventListener('click', function () { goTo(current - 1); });
    if (nextBtn) nextBtn.addEventListener('click', function () { goTo(current + 1); });

    el.setAttribute('tabindex', '0');
    el.addEventListener('keydown', function (e) {
      if (e.key === 'ArrowLeft')  { goTo(current - 1); e.preventDefault(); }
      if (e.key === 'ArrowRight') { goTo(current + 1); e.preventDefault(); }
    });

    var touchX = 0;
    el.addEventListener('touchstart', function (e) { touchX = e.touches[0].clientX; }, { passive: true });
    el.addEventListener('touchend', function (e) {
      var diff = touchX - e.changedTouches[0].clientX;
      if (Math.abs(diff) > 40) goTo(diff > 0 ? current + 1 : current - 1);
    }, { passive: true });
  });
})();
