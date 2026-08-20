/* ============================================================================
   쉴드광택 통합 측정 스크립트  (GA4 + 네이버 애널리틱스 + 전환 이벤트)
   ----------------------------------------------------------------------------
   이 파일 하나만 각 페이지 <head> 에 넣으면 측정이 끝납니다.
       <script src="/assets/js/analytics.js" defer></script>

   ★ 처음 한 번만 할 일 ★
   아래 CONFIG 의 GA4_ID / NAVER_ID 두 줄에 발급받은 번호를 넣으세요.
   (발급 방법은 D:\shiled-line\측정_설치가이드.md 참고)
   비어 있으면 아무것도 실행되지 않으므로, 넣기 전까지는 사이트에 영향이 없습니다.

   무엇이 자동으로 잡히나:
     · 모든 페이지 조회 (해시 라우팅 #/price 같은 화면 이동 포함)
     · 전화번호 클릭      → generate_lead (method: tel)     ← 전환
     · 카카오톡 클릭      → generate_lead (method: kakao)   ← 전환
     · 네이버 플레이스 클릭 → outbound_click
     · 가격 계산기 사용    → price_calculate
     · 시공증명서 조회     → cert_lookup
   ========================================================================== */
(function () {
  'use strict';

  /* ==== CONFIG ============================================================ */
  var CONFIG = {
    GA4_ID:   'G-CQY0GHZH3G',   // 구글 애널리틱스 측정 ID (2026-08-20 등록)
    NAVER_ID: '1bd0c6016501f40',   // 네이버 애널리틱스 발급ID (사이트 '쉴드광택')
    DEBUG:    false // true 로 두면 콘솔에 잡히는 이벤트가 찍힘 (설치 확인용)
  };
  /* ======================================================================= */

  var hasGA = /^G-[A-Z0-9]+$/i.test(CONFIG.GA4_ID);
  // 네이버 발급ID는 's_xxxx' 형태도 있고 '1bd0c6016501f40' 같은 16진 문자열도 있다.
  // 형식을 좁게 잡으면 멀쩡한 키를 거부하므로 영숫자/언더바 8자 이상만 확인한다.
  var hasNA = /^[A-Za-z0-9_]{8,}$/.test(CONFIG.NAVER_ID);

  function log() {
    if (CONFIG.DEBUG && window.console) {
      console.log.apply(console, ['[측정]'].concat([].slice.call(arguments)));
    }
  }

  if (!hasGA && !hasNA) {
    log('GA4_ID / NAVER_ID 가 아직 비어 있어 측정을 실행하지 않습니다.');
    return;
  }

  /* ---------- 1. GA4 ------------------------------------------------------ */
  window.dataLayer = window.dataLayer || [];
  function gtag() { window.dataLayer.push(arguments); }
  window.gtag = window.gtag || gtag;

  if (hasGA) {
    var g = document.createElement('script');
    g.async = true;
    g.src = 'https://www.googletagmanager.com/gtag/js?id=' + encodeURIComponent(CONFIG.GA4_ID);
    document.head.appendChild(g);

    gtag('js', new Date());
    // 해시 라우팅 사이트라 자동 page_view 를 끄고 직접 쏜다 (중복 방지)
    gtag('config', CONFIG.GA4_ID, { send_page_view: false });
    sendPageView();
  }

  function sendPageView() {
    if (!hasGA) return;
    gtag('event', 'page_view', {
      page_location: location.href,
      page_title: document.title,
      page_path: location.pathname + location.hash
    });
    log('page_view', location.pathname + location.hash);
  }

  // 해시 라우팅(#/price, #/products …) 화면 이동도 한 페이지로 집계
  window.addEventListener('hashchange', sendPageView);

  /* ---------- 2. 네이버 애널리틱스 ---------------------------------------- */
  if (hasNA) {
    var n = document.createElement('script');
    n.async = true;
    n.src = 'https://wcs.pstatic.net/wcslog.js';
    n.onload = function () {
      try {
        if (!window.wcs_add) window.wcs_add = {};
        window.wcs_add.wa = CONFIG.NAVER_ID;
        if (!window._nasa) window._nasa = {};
        if (window.wcs) {
          // 네이버가 발급한 공식 스니펫과 동일한 호출 (페이지뷰 수집)
          window.wcs_do();
          log('네이버 애널리틱스 로드 완료');
        }
      } catch (e) { log('네이버 애널리틱스 오류', e); }
    };
    document.head.appendChild(n);
  }

  // 네이버 전환(신청/예약) 보고 — 전화·카톡 클릭 시 호출
  function naverConversion() {
    if (!hasNA || !window.wcs || !window.wcs_do) return;
    try {
      if (!window._nasa) window._nasa = {};
      // "2" = 신청/예약 유형, "1" = 건수
      window._nasa.cnv = window.wcs.cnv('2', '1');
      window.wcs_do(window._nasa);
      log('네이버 전환 보고');
    } catch (e) { log('네이버 전환 오류', e); }
  }

  /* ---------- 3. 전환 이벤트 ---------------------------------------------- */

  // 이 페이지가 어떤 종류인지 (블로그 글 / 가격 / FAQ / 홈)
  function pageType() {
    var p = location.pathname;
    if (/^\/blog\/index\.html?$|^\/blog\/?$/.test(p)) return 'blog_list';
    if (p.indexOf('/blog/') === 0) return 'blog_post';
    if (p.indexOf('price') > -1) return 'price';
    if (p.indexOf('faq') > -1) return 'faq';
    if (p.indexOf('coating-layers') > -1) return 'coating';
    return 'home';
  }

  function track(name, params) {
    params = params || {};
    params.page_type = pageType();
    if (hasGA) gtag('event', name, params);
    log(name, params);
  }

  // 전화·카톡·플레이스 클릭을 문서 전체에서 한 번에 감시 (버튼이 나중에 생겨도 잡힘)
  document.addEventListener('click', function (ev) {
    var a = ev.target && ev.target.closest ? ev.target.closest('a') : null;
    if (!a) return;
    var href = (a.getAttribute('href') || '').toLowerCase();
    if (!href) return;

    if (href.indexOf('tel:') === 0) {
      track('generate_lead', { method: 'tel', link_text: (a.textContent || '').trim().slice(0, 60) });
      naverConversion();

    } else if (href.indexOf('pf.kakao.com') > -1 || href.indexOf('open.kakao.com') > -1) {
      track('generate_lead', { method: 'kakao', link_text: (a.textContent || '').trim().slice(0, 60) });
      naverConversion();

    } else if (href.indexOf('map.naver.com') > -1 || href.indexOf('place.naver.com') > -1) {
      track('outbound_click', { destination: 'naver_place' });

    } else if (href.indexOf('blog.naver.com') > -1) {
      track('outbound_click', { destination: 'naver_blog' });

    } else if (href.indexOf('youtube.com') > -1 || href.indexOf('instagram.com') > -1) {
      track('outbound_click', { destination: href.indexOf('youtube') > -1 ? 'youtube' : 'instagram' });
    }
  }, true);

  /* ---------- 4. 다른 스크립트에서 부를 수 있는 창구 ------------------------ */
  // 가격 계산기 / 증명서 조회에서 window.shiledTrack(...) 으로 호출
  window.shiledTrack = function (name, params) {
    track(name, params || {});
    if (name === 'generate_lead') naverConversion();
  };

  log('측정 스크립트 준비 완료 · GA4:' + (hasGA ? 'ON' : 'OFF') + ' · 네이버:' + (hasNA ? 'ON' : 'OFF'));
})();
