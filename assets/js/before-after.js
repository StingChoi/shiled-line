/* ============================================================================
   Before / After 비교 슬라이더
   ----------------------------------------------------------------------------
   왜 슬라이더인가
     좌우로 나란히 붙여두면 보는 사람이 두 사진을 눈으로 왕복하며 비교해야 한다.
     같은 자리에 겹쳐놓고 경계를 직접 끌게 하면, 손가락 하나로 차이가 드러난다.
     '내가 움직여서 확인했다'는 경험이 사진 두 장보다 훨씬 강하게 남는다.

   구현 메모 (2026-09-03 수정)
     처음에는 <input type="range"> 에 조작을 전부 맡겼다. 데스크톱 마우스로는 잘 끌렸지만
     휴대폰에서 전혀 움직이지 않는다는 제보를 받았다. 원인은 range 위젯의 터치 동작이다.
       · iOS 사파리는 트랙을 눌러도 손잡이가 따라오지 않는다. 손잡이를 정확히 잡아야만 끌린다.
         여기서는 손잡이가 투명한 48px 라 사실상 잡을 수가 없다.
       · 안드로이드도 touch-action 이 auto 면 첫 터치를 페이지 스크롤 후보로 물고 있다가
         슬라이더까지 넘겨주지 않는 경우가 있다.
     그래서 조작은 포인터 이벤트로 직접 처리한다. 마우스·터치·펜이 같은 코드로 처리된다.

     range 를 없애지는 않았다. 키보드 화살표 조작과 스크린리더 낭독을 그대로 쓰기 위해서다.
     JS 가 붙은 뒤에만 .ba-ready 가 달리고, 그때부터 range 는 포인터를 받지 않는다
     (CSS 참조). JS 가 실패하면 .ba-ready 가 없으니 원래의 range 동작으로 되돌아간다.

     실제 가림은 CSS clip-path 로 한다. 리페인트가 없어 끌 때 매끄럽다.
   ========================================================================== */
(function () {
  'use strict';

  function bind(fig) {
    var range = fig.querySelector('.ba-range');
    var view = fig.querySelector('.ba-view');
    if (!range || !view) return;

    var touched = false;   // 손님이 한 번이라도 만졌으면 안내 애니메이션은 그만둔다

    function paint() {
      view.style.setProperty('--p', range.value + '%');
      range.setAttribute('aria-valuenow', range.value);
      range.setAttribute('aria-valuetext', '시공 전 ' + range.value + '% 표시');
    }
    function set(v) {
      v = v < 0 ? 0 : (v > 100 ? 100 : v);
      range.value = Math.round(v);
      paint();
    }

    // 키보드 화살표 · 폴백 상황
    range.addEventListener('input', function () { touched = true; paint(); });
    paint();

    // ── 포인터로 직접 끌기 ──────────────────────────────────────────────
    if (window.PointerEvent) {
      fig.classList.add('ba-ready');

      // mouse 는 누르는 순간 그 자리로 보낸다 (클릭해서 옮기는 게 당연한 동작이다).
      // touch 는 다르다. 사진이 화면을 거의 다 덮으므로, 페이지를 내리려고 사진 위에
      // 손가락을 얹는 일이 훨씬 많다. 누르자마자 값을 바꾸면 스크롤할 때마다 경계가 튄다.
      // 그래서 터치는 '가로로 움직이기 시작한 뒤에' 잡는다.
      var dragging = false, pending = false, sx = 0, sy = 0;

      function ratio(e) {
        var r = view.getBoundingClientRect();
        return (e.clientX - r.left) / r.width * 100;
      }

      view.addEventListener('pointerdown', function (e) {
        if (e.button > 0) return;               // 오른쪽·가운데 버튼은 무시
        sx = e.clientX; sy = e.clientY;

        if (e.pointerType === 'touch') {
          pending = true;                       // 아직 값은 안 건드린다
          return;                               // 캡처도 preventDefault 도 안 한다.
                                                // 세로 스크롤 판단을 브라우저에 그대로 맡기기 위해서다.
        }
        try { view.setPointerCapture(e.pointerId); } catch (err) {}
        dragging = true;
        touched = true;
        set(ratio(e));
        e.preventDefault();                     // 사진이 드래그 고스트로 딸려오는 것을 막는다
        // 이어서 화살표 키로 미세 조정할 수 있게 초점을 넘긴다.
        // 포인터로 준 초점이라 :focus-visible 은 안 걸린다 = 테두리는 안 생긴다.
        try { range.focus({ preventScroll: true }); } catch (err) {}
      });

      view.addEventListener('pointermove', function (e) {
        if (pending) {
          var dx = Math.abs(e.clientX - sx), dy = Math.abs(e.clientY - sy);
          if (dx < 6 || dx <= dy) return;       // 아직 가로인지 세로인지 모른다
          pending = false; dragging = true; touched = true;
          // 가로로 확정된 뒤에 잡는다. 손가락이 사진 밖으로 나가도 계속 따라온다.
          try { view.setPointerCapture(e.pointerId); } catch (err) {}
        }
        if (!dragging) return;
        set(ratio(e));
        e.preventDefault();
      });

      function stop(e) {
        if (!dragging && !pending) return;
        dragging = false; pending = false;
        try { view.releasePointerCapture(e.pointerId); } catch (err) {}
      }
      // pointercancel = 브라우저가 세로 스크롤로 판단해 제스처를 가져간 경우.
      // touch-action:pan-y 덕분에 세로로 쓸면 페이지가 스크롤되고, 가로로 쓸면 여기가 받는다.
      view.addEventListener('pointerup', stop);
      view.addEventListener('pointercancel', stop);
      view.addEventListener('dragstart', function (e) { e.preventDefault(); });
    }

    // ── 끌 수 있다는 신호 ────────────────────────────────────────────────
    // 모르고 지나치는 경우가 많아, 처음 화면에 들어올 때 한 번만 살짝 움직인다.
    if (window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches) return;
    if (!('IntersectionObserver' in window)) return;

    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (e) {
        if (!e.isIntersecting) return;
        io.disconnect();
        if (touched) return;
        var from = 50, to = 68, t0 = null, dur = 900;
        function step(ts) {
          if (touched) { return; }            // 도중에 손이 닿으면 손님 쪽이 우선이다
          if (t0 === null) t0 = ts;
          var p = Math.min((ts - t0) / dur, 1);
          var eased = p < .5 ? 2 * p * p : 1 - Math.pow(-2 * p + 2, 2) / 2;   // easeInOutQuad
          // 갔다가 돌아온다 — 움직인다는 것만 알리고 원위치로
          var v = p < .5 ? from + (to - from) * (eased * 2)
                         : to + (from - to) * ((eased - .5) * 2);
          set(v);
          if (p < 1) requestAnimationFrame(step);
          else set(50);
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
