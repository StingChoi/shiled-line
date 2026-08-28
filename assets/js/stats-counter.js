/* ============================================================================
   홈 '누적 시공' 카운터
   ----------------------------------------------------------------------------
   왜 이렇게 만들었나

   1) certificates 컬렉션을 통째로 읽지 않는다.
      문서가 3천 개가 넘어 방문당 3천 읽기가 발생하고, 무료 한도가
      하루 15방문에 소진된다. 게다가 이 사이트가 쓰는 Firebase v8 은
      count() 집계를 지원하지 않는다.
      → 관리자 스크립트(update_stats.py)가 미리 세어 stats/summary 에
        적어두고, 여기서는 그 문서 1건만 읽는다.

   2) 값을 localStorage 에 6시간 캐시한다.
      재방문·페이지 이동 때 Firestore 를 다시 부르지 않는다. 표시도 즉시 뜬다.

   3) 어떤 이유로든 못 읽으면 HTML 에 박아둔 기본값을 그대로 둔다.
      숫자가 사라지거나 0으로 깜빡이는 일이 없어야 한다.
   ========================================================================== */
(function () {
  'use strict';

  var CACHE_KEY = 'shiled_stats_v1';
  var TTL_MS = 6 * 60 * 60 * 1000;   // 6시간

  function readCache() {
    try {
      var raw = localStorage.getItem(CACHE_KEY);
      if (!raw) return null;
      var o = JSON.parse(raw);
      if (!o || typeof o.n !== 'number' || !o.t) return null;
      if (Date.now() - o.t > TTL_MS) return null;
      return o.n;
    } catch (e) { return null; }   // 사생활 보호 모드 등에서 접근 자체가 막힐 수 있다
  }

  function writeCache(n) {
    try {
      localStorage.setItem(CACHE_KEY, JSON.stringify({ n: n, t: Date.now() }));
    } catch (e) { /* 저장 못 해도 동작에는 지장 없다 */ }
  }

  /* 숫자를 세듯 올린다. 끝값에 가까울수록 느려져 '멈추는' 느낌을 준다. */
  function countUp(el, to, ms) {
    var final = to.toLocaleString('ko-KR');

    if (window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches) {
      el.textContent = final;
      return;
    }

    var done = false;
    function settle() {                    // 어떤 경우에도 끝값으로 마무리한다
      if (done) return;
      done = true;
      el.textContent = final;
    }

    // requestAnimationFrame 은 탭이 숨겨지면 멈춘다.
    // 애니메이션 도중 다른 탭으로 갔다가 돌아오면 숫자가 중간값에서 굳을 수 있어,
    // 시간이 지나면 무조건 끝값으로 맞추는 안전장치를 둔다.
    var guard = setTimeout(settle, ms + 400);
    document.addEventListener('visibilitychange', function onHide() {
      if (document.hidden) {
        document.removeEventListener('visibilitychange', onHide);
        settle();
      }
    });

    var t0 = null;
    function step(ts) {
      if (done) return;
      if (t0 === null) t0 = ts;
      var p = Math.min((ts - t0) / ms, 1);
      var eased = 1 - Math.pow(1 - p, 3);           // easeOutCubic
      el.textContent = Math.round(to * eased).toLocaleString('ko-KR');
      if (p < 1) {
        requestAnimationFrame(step);
      } else {
        clearTimeout(guard);
        settle();
      }
    }
    requestAnimationFrame(step);
  }

  /* 화면에 들어왔을 때 한 번만 센다. 스크롤 전에 다 올라가 있으면 못 본다. */
  function whenVisible(el, fn) {
    if (!('IntersectionObserver' in window)) { fn(); return; }
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (e) {
        if (e.isIntersecting) { io.disconnect(); fn(); }
      });
    }, { threshold: 0.4 });
    io.observe(el);
  }

  function render(n) {
    var el = document.getElementById('statCertCount');
    if (!el) return;
    el.setAttribute('data-value', String(n));
    whenVisible(el, function () { countUp(el, n, 1400); });
  }

  function boot() {
    var el = document.getElementById('statCertCount');
    if (!el) return;

    // 1) 캐시가 있으면 그대로 쓴다
    var cached = readCache();
    if (cached !== null) { render(cached); return; }

    // 2) 없으면 문서 1건만 읽는다
    var fallback = parseInt(el.getAttribute('data-fallback') || '0', 10);
    if (!window.db) { render(fallback); return; }

    window.db.collection('stats').doc('summary').get()
      .then(function (doc) {
        var n = (doc.exists && doc.data() && doc.data().certCount) || 0;
        if (n > 0) { writeCache(n); render(n); }
        else { render(fallback); }
      })
      .catch(function () { render(fallback); });   // 읽기 실패해도 화면은 멀쩡해야 한다
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', boot);
  } else {
    boot();
  }
})();
