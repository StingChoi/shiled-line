/* ============================================================================
   Before / After 비교 슬라이더
   ----------------------------------------------------------------------------
   왜 슬라이더인가
     좌우로 나란히 붙여두면 보는 사람이 두 사진을 눈으로 왕복하며 비교해야 한다.
     같은 자리에 겹쳐놓고 경계를 직접 끌게 하면, 손가락 하나로 차이가 드러난다.
     '내가 움직여서 확인했다'는 경험이 사진 두 장보다 훨씬 강하게 남는다.

   구현 메모
     · 위치 조절은 <input type="range"> 가 맡는다.
       직접 만들면 터치·키보드·접근성을 전부 다시 짜야 하는데, range 는 공짜로 준다.
     · 실제 가림은 CSS clip-path 로 한다. 리페인트가 없어 끌 때 매끄럽다.
   ========================================================================== */
(function () {
  'use strict';

  function bind(fig) {
    var range = fig.querySelector('.ba-range');
    var view = fig.querySelector('.ba-view');
    if (!range || !view) return;

    function apply() {
      view.style.setProperty('--p', range.value + '%');
      range.setAttribute('aria-valuetext', '시공 전 ' + range.value + '% 표시');
    }
    range.addEventListener('input', apply);
    apply();

    // 끌 수 있다는 걸 모르고 지나치는 경우가 많아, 처음 보일 때 한 번만 살짝 움직인다.
    if (window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches) return;
    if (!('IntersectionObserver' in window)) return;

    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (e) {
        if (!e.isIntersecting) return;
        io.disconnect();
        var from = 50, to = 68, t0 = null, dur = 900;
        function step(ts) {
          if (t0 === null) t0 = ts;
          var p = Math.min((ts - t0) / dur, 1);
          var eased = p < .5 ? 2 * p * p : 1 - Math.pow(-2 * p + 2, 2) / 2;   // easeInOutQuad
          // 갔다가 돌아온다 — 움직인다는 것만 알리고 원위치로
          var v = p < .5 ? from + (to - from) * (eased * 2)
                         : to + (from - to) * ((eased - .5) * 2);
          range.value = Math.round(v);
          view.style.setProperty('--p', range.value + '%');
          if (p < 1) requestAnimationFrame(step);
          else { range.value = 50; view.style.setProperty('--p', '50%'); }
        }
        requestAnimationFrame(step);
      });
    }, { threshold: 0.5 });
    io.observe(fig);
  }

  function boot() {
    Array.prototype.forEach.call(document.querySelectorAll('.ba'), bind);
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', boot);
  } else {
    boot();
  }
})();
