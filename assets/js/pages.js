// Partner data
const partnerData = [
    { name: "쉴드광택 본점", location: "부산 남구", link: "https://blog.naver.com/shiledgt", image: "assets/images/partner_shield_main.jpg" },
    { name: "M팩토리", location: "경남 창원시 진해구", link: "https://m.blog.naver.com/conver2", image: "assets/images/partner_mfactory.jpg" },
    { name: "본디테일링", location: "경남 창원시 진해구", link: "https://www.instagram.com/bon_detailing?igsh=b3hvcGRsaDB0eGpy", image: "assets/images/partner_bondetailing.jpg" },
    { name: "MK 디테일링", location: "전남 영암군", link: "https://www.instagram.com/mk_detailing_story?igsh=MWFtcHA4NGN6ZjdkZg==", image: "assets/images/partner_mkdetailing.jpg" },
    { name: "미라클테크", location: "인천 부평구", link: "https://blog.naver.com/miracledetail", image: "assets/images/partner_miracletech.jpg" },
    { name: "인터페이스", location: "부산 남구", link: "https://naver.me/IxKpCeXR", image: "assets/images/partner_interface.jpg" }
];

const partnersHTML = partnerData.map(p => `
    <div class="partner-card">
        <div class="partner-img" style="background-image: url('${p.image}');"></div>
        <div class="partner-info">
            <h3 class="mb-2" style="font-size: 1.4rem;">${p.name}</h3>
            <p class="text-muted mb-6" style="font-size: 1rem; flex: 1;">${p.location}</p>
            <a href="${p.link}" target="_blank" class="btn btn-outline" style="width: 100%; text-align: center; display: block; padding: 0.8rem 0;">블로그/인스타 방문하기</a>
        </div>
    </div>
`).join('');

// Page content templates
const pages = {
    home: `
        <section class="hero">
            <div class="hero-bg"></div>
            <div class="hero-content">
                <span class="hero-tagline">SHIELD 쉴드광택 · 자체 개발 유리막코팅제</span>
                <h1 class="hero-title">어떤 차를 타냐보다<br><span class="gradient-text">어떻게 타냐</span>가 중요합니다!</h1>
                <p class="hero-desc">
                    16년 경력의 코팅제 개발자가 직접 시공합니다.<br>
                    벤츠 부산 남천점 공식 상조업체 · 자체 개발 유리막코팅제 F5 · G-PRO · G-TOP
                </p>
                <div class="hero-cta">
                    <a href="#/services" class="btn btn-primary">시공 안내 보기</a>
                    <a href="tel:01033841850" class="btn btn-outline">예약 문의하기</a>
                </div>
            </div>
        </section>

        <section class="section">
            <div class="container">
                <div class="text-center mb-8">
                    <h2 class="mb-2">WHY SHIELD GLOSS</h2>
                    <p class="text-muted">왜 쉴드광택을 선택해야 할까요?</p>
                </div>
                
                <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(280px, 1fr)); gap: 2rem;">
                    <div class="glass-card text-center">
                        <div style="font-size: 2.5rem; color: var(--primary); margin-bottom: 1rem;">✨</div>
                        <h3 class="mb-4">16년 경력 시공 전문가</h3>
                        <p class="text-muted">코팅제를 직접 개발한 전문가가 시공합니다. 단순 시공업체와 차원이 다른 이해도와 노하우로 도장면의 스트레스를 최소화합니다.</p>
                    </div>
                    <div class="glass-card text-center">
                        <div style="font-size: 2.5rem; color: var(--primary); margin-bottom: 1rem;">🛡️</div>
                        <h3 class="mb-4">자체 개발 유리막코팅제</h3>
                        <p class="text-muted">수백 번의 테스트를 거쳐 직접 개발·생산한 F5 · G-PRO · G-TOP 전용 코팅제. 시중 제품이 아닌 쉴드광택만의 독자 라인업입니다.</p>
                    </div>
                    <div class="glass-card text-center">
                        <div style="font-size: 2.5rem; color: var(--primary); margin-bottom: 1rem;">⭐</div>
                        <h3 class="mb-4">벤츠 공식 상조업체</h3>
                        <p class="text-muted">메르세데스-벤츠 부산 남천점 공식 상조업체로 신차 출고 전 최고의 외장 컨디션을 책임집니다.</p>
                    </div>
                </div>
            </div>
        </section>

        <section class="section" style="padding-top: 0; border-top: 1px solid var(--border-light);">
            <div class="container">
                <div class="text-center mb-8">
                    <h2 class="mb-2">최신 작업 일지</h2>
                    <p class="text-muted">쉴드광택 네이버 블로그에서 실제 시공 사례를 확인하세요</p>
                </div>
                <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(280px, 1fr)); gap: 2rem; margin-bottom: 3rem;">
                    <a href="https://blog.naver.com/shiledgt" target="_blank" class="glass-card" style="padding:0;overflow:hidden;display:flex;flex-direction:column;text-decoration:none;">
                        <div style="height:200px;overflow:hidden;">
                            <img src="assets/images/260428 GLE350 검정 광택/작업후-01.jpg" style="width:100%;height:100%;object-fit:cover;transition:transform 0.4s;" onmouseover="this.style.transform='scale(1.05)'" onmouseout="this.style.transform='scale(1)'">
                        </div>
                        <div style="padding:1.5rem;flex:1;display:flex;flex-direction:column;">
                            <span style="color:var(--primary);font-size:0.8rem;margin-bottom:0.5rem;">벤츠 GLE · 신차코팅</span>
                            <h4 style="font-size:1rem;margin-bottom:0.75rem;line-height:1.5;flex:1;">벤츠 GLE 신차 출고 전 유리막코팅 — 도장면 상태 확인부터 마감까지</h4>
                            <span style="color:var(--text-muted);font-size:0.85rem;">블로그에서 전체 보기 →</span>
                        </div>
                    </a>
                    <a href="https://blog.naver.com/shiledgt" target="_blank" class="glass-card" style="padding:0;overflow:hidden;display:flex;flex-direction:column;text-decoration:none;">
                        <div style="height:200px;overflow:hidden;">
                            <img src="assets/images/260418 F150 페인트 날림제거/after-02.jpg" style="width:100%;height:100%;object-fit:cover;transition:transform 0.4s;" onmouseover="this.style.transform='scale(1.05)'" onmouseout="this.style.transform='scale(1)'">
                        </div>
                        <div style="padding:1.5rem;flex:1;display:flex;flex-direction:column;">
                            <span style="color:var(--primary);font-size:0.8rem;margin-bottom:0.5rem;">Ford F-150 · 광택복원</span>
                            <h4 style="font-size:1rem;margin-bottom:0.75rem;line-height:1.5;flex:1;">Ford F-150 페인트 날림 제거 후 G-PRO 유리막코팅 시공 전후 비교</h4>
                            <span style="color:var(--text-muted);font-size:0.85rem;">블로그에서 전체 보기 →</span>
                        </div>
                    </a>
                    <a href="https://blog.naver.com/shiledgt" target="_blank" class="glass-card" style="padding:0;overflow:hidden;display:flex;flex-direction:column;text-decoration:none;">
                        <div style="height:200px;overflow:hidden;">
                            <img src="assets/images/260428 GLE350 검정 광택/작업후-12.jpg" style="width:100%;height:100%;object-fit:cover;transition:transform 0.4s;" onmouseover="this.style.transform='scale(1.05)'" onmouseout="this.style.transform='scale(1)'">
                        </div>
                        <div style="padding:1.5rem;flex:1;display:flex;flex-direction:column;">
                            <span style="color:var(--primary);font-size:0.8rem;margin-bottom:0.5rem;">B필러 · 디테일링</span>
                            <h4 style="font-size:1rem;margin-bottom:0.75rem;line-height:1.5;flex:1;">B필러 오염·스크래치 완벽 제거 — 16년 노하우로 만든 도장면 광택 복원</h4>
                            <span style="color:var(--text-muted);font-size:0.85rem;">블로그에서 전체 보기 →</span>
                        </div>
                    </a>
                </div>
                <div class="text-center">
                    <a href="https://blog.naver.com/shiledgt" target="_blank" class="btn btn-outline">네이버 블로그 전체 보기 →</a>
                </div>
            </div>
        </section>
    `,
    about: `
        <div class="page-header">
            <h1 class="page-title">회사소개</h1>
            <p class="page-desc">ABOUT SHIELD GLOSS</p>
        </div>
        <section class="section" style="padding-top: 0;">
            <div class="container">
                <div class="about-grid">
                    <div>
                        <div class="about-main-img-wrapper">
                            <img src="assets/images/260428 GLE350 검정 광택/작업후-01.jpg" alt="벤츠 GLE 시공 완료" class="about-main-img">
                        </div>
                        <div class="about-thumb-grid">
                            <div class="about-thumb-item">
                                <img src="assets/images/260428 GLE350 검정 광택/작업후-04.jpg">
                            </div>
                            <div class="about-thumb-item">
                                <img src="assets/images/260428 GLE350 검정 광택/작업후-07.jpg">
                            </div>
                            <div class="about-thumb-item">
                                <img src="assets/images/260428 GLE350 검정 광택/작업후-12.jpg">
                            </div>
                            <div class="about-thumb-item">
                                <img src="assets/images/260418 F150 페인트 날림제거/after-01.jpg">
                            </div>
                            <div class="about-thumb-item">
                                <img src="assets/images/260418 F150 페인트 날림제거/after-03.jpg">
                            </div>
                            <div class="about-thumb-item">
                                <img src="assets/images/260428 GLE350 검정 광택/작업후-15.jpg">
                            </div>
                        </div>
                    </div>
                    <div>
                        <h2 class="about-section-title">최상의 퀄리티로 보답합니다.</h2>
                        <div class="about-representative">대표 최한중</div>
                        
                        <p class="about-paragraph">
                            쉴드광택을 찾아주신 고객 여러분, 진심으로 환영합니다.
                        </p>
                        <p class="about-paragraph">
                            저희 쉴드광택은 단순한 세차를 넘어 자동차의 진정한 가치를 찾아주는 디테일링 전문샵입니다.
                            16년간 수많은 차량을 시공해온 노하우를 바탕으로, 고객님의 소중한 차량에 투명하고 깊은 광택을 선사합니다.
                        </p>
                        <p class="about-paragraph" style="margin-bottom: 2rem;">
                            특히, 저희가 직접 개발·생산하는 전용 유리막코팅제(F5 · G-PRO · G-TOP)는 압도적인 퍼포먼스를 보장하며,
                            메르세데스-벤츠 부산 남천점 공식 상조업체로서 신차 출고 전 최고의 외장 컨디션을 만들어드립니다.
                        </p>
                        
                        <div class="about-info-card">
                            <h4>⭐ 공식 협력</h4>
                            <p>메르세데스-벤츠 부산 남천점 공식 상조업체</p>
                            
                            <h4>📌 오시는 길</h4>
                            <p>부산 남구 유엔로220 1F (쉴드광택)</p>
                            
                            <h4>📞 예약 및 문의</h4>
                            <p class="about-phone">010-3384-1850</p>
                        </div>
                    </div>
                </div>
            </div>
        </section>
    `,
    products: `
        <div class="page-header">
            <h1 class="page-title">제품소개</h1>
            <p class="page-desc">OUR PRODUCTS</p>
        </div>
        <section class="section" style="padding-top: 0;">
            <div class="container">
                <div class="text-center mb-8">
                    <h2 class="mb-4 gradient-text">쉴드광택 자체 개발 유리막코팅제 라인업</h2>
                    <p class="text-muted" style="max-width: 600px; margin: 0 auto;">수백 번의 테스트를 거쳐 직접 개발·생산한 쉴드광택 전용 유리막코팅제. <br>F5 · G-PRO · G-TOP 각각의 특성을 조합해 차량에 최적화된 보호막을 구현합니다.</p>
                </div>
                
                <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(280px, 1fr)); gap: 3rem; margin-top: 4rem;">
                    <!-- Product 1: F5 -->
                    <div class="partner-card" style="padding: 0; display: flex; flex-direction: column;">
                        <div class="product-img-wrapper" onclick="window.openProductGallery('assets/images/detail_F5.jpg')">
                            <img src="assets/images/bottle_f5.jpg" alt="F5 코팅제" class="product-img">
                            <div class="product-hover-overlay">
                                <button class="view-gallery-btn">🔍 시공 결과 보기</button>
                            </div>
                        </div>
                        <div style="padding: 2rem; display: flex; flex-direction: column; flex: 1;">
                            <span style="color: var(--primary); font-size: 0.9rem; font-weight: 700; letter-spacing: 2px;">COLOR ENHANCEMENT</span>
                            <h3 style="margin: 0.5rem 0 1rem; font-size: 1.5rem;">F5 유리막코팅제 <br><span style="font-size: 1.1rem; color: var(--text-muted);">(도장채도 향상)</span></h3>
                            <p class="text-muted mb-4" style="line-height: 1.6; flex: 1;">도장면 본연의 맑고 깊은 색감을 극대화하여, 차량에 투명하고 입체적인 광택을 부여하는 최고급 채도 향상 전용 코팅제입니다.</p>
                        </div>
                    </div>
                    
                    <!-- Product 2: G-Pro -->
                    <div class="partner-card" style="padding: 0; display: flex; flex-direction: column; border-color: var(--border-gold);">
                        <div class="product-img-wrapper" onclick="window.openProductGallery('assets/images/detail_GPRO.jpg')">
                            <img src="assets/images/bottle_gpro.jpg" alt="G-Pro 코팅제" class="product-img">
                            <div style="position: absolute; top: 1rem; right: 1rem; background: var(--primary); color: #000; padding: 0.2rem 0.8rem; border-radius: 20px; font-weight: bold; font-size: 0.8rem; z-index: 1;">HARDNESS</div>
                            <div class="product-hover-overlay">
                                <button class="view-gallery-btn">🔍 시공 결과 보기</button>
                            </div>
                        </div>
                        <div style="padding: 2rem; display: flex; flex-direction: column; flex: 1;">
                            <span style="color: var(--primary); font-size: 0.9rem; font-weight: 700; letter-spacing: 2px;">HARDNESS ENHANCEMENT</span>
                            <h3 style="margin: 0.5rem 0 1rem; font-size: 1.5rem;">G-Pro 유리막코팅제 <br><span style="font-size: 1.1rem; color: var(--text-muted);">(도장경도 향상)</span></h3>
                            <p class="text-muted mb-4" style="line-height: 1.6; flex: 1;">단단한 나노 코팅막을 형성하여 일상적인 스크래치와 외부 데미지로부터 도장면을 강력하게 보호하는 하드코어 경도 향상 코팅제입니다.</p>
                        </div>
                    </div>

                    <!-- Product 3: G-Top -->
                    <div class="partner-card" style="padding: 0; display: flex; flex-direction: column;">
                        <div class="product-img-wrapper" onclick="window.openProductGallery('assets/images/detail_GTOP.jpg')">
                            <img src="assets/images/bottle_gtop.jpg" alt="G-Top 코팅제" class="product-img">
                            <div style="position: absolute; top: 1rem; right: 1rem; background: var(--primary); color: #000; padding: 0.2rem 0.8rem; border-radius: 20px; font-weight: bold; font-size: 0.8rem; z-index: 1;">WATER REPELLENT</div>
                            <div class="product-hover-overlay">
                                <button class="view-gallery-btn">🔍 시공 결과 보기</button>
                            </div>
                        </div>
                        <div style="padding: 2rem; display: flex; flex-direction: column; flex: 1;">
                            <span style="color: var(--primary); font-size: 0.9rem; font-weight: 700; letter-spacing: 2px;">HYDROPHOBIC & ANTI-FOULING</span>
                            <h3 style="margin: 0.5rem 0 1rem; font-size: 1.5rem;">G-Top 유리막코팅제 <br><span style="font-size: 1.1rem; color: var(--text-muted);">(발수력 및 방오성 향상)</span></h3>
                            <p class="text-muted mb-4" style="line-height: 1.6; flex: 1;">도장면에 나노 사이즈 유리막을 형성하여 표면을 완벽히 보호합니다. 압도적인 발수력과 뛰어난 방오성으로 오염물의 고착을 원천 차단합니다.</p>
                        </div>
                    </div>

                    <!-- Product 4: R-Alu -->
                    <div class="partner-card" style="padding: 0; display: flex; flex-direction: column;">
                        <div class="product-img-wrapper" onclick="window.openProductGallery('assets/images/molding_before.jpg', 'assets/images/molding_after.jpg')">
                            <img src="assets/images/bottle_ralu.jpg" alt="R-Alu 코팅제" class="product-img">
                            <div style="position: absolute; top: 1rem; right: 1rem; background: rgba(0,0,0,0.6); color: #fff; padding: 0.2rem 0.8rem; border-radius: 4px; font-weight: bold; font-size: 0.8rem; border: 1px solid var(--border-light); z-index: 1;">MOLDING</div>
                            <div class="product-hover-overlay">
                                <button class="view-gallery-btn">🔍 비포 / 애프터 보기</button>
                            </div>
                        </div>
                        <div style="padding: 2rem; display: flex; flex-direction: column; flex: 1;">
                            <span style="color: var(--primary); font-size: 0.9rem; font-weight: 700; letter-spacing: 2px;">ALUMINUM RESTORATION</span>
                            <h3 style="margin: 0.5rem 0 1rem; font-size: 1.5rem;">R-Alu 알루미늄 복원코팅제 <br><span style="font-size: 1.1rem; color: var(--text-muted);">(몰딩 복원 및 보호)</span></h3>
                            <p class="text-muted mb-4" style="line-height: 1.6; flex: 1;">수입차 알루미늄 도어 몰딩의 고질적인 백화현상과 부식을 완벽하게 복원하고, 산화를 원천 차단하는 특수 코팅제입니다.</p>
                        </div>
                    </div>
                </div>
            </div>
        </section>
    `,
    price: `
        <div class="page-header" style="position: relative; overflow: hidden; padding: 10rem 0 4rem;">
            <div style="position: absolute; top:0; left:0; width:100%; height:100%; background: linear-gradient(to bottom, rgba(4,5,6,0.8), rgba(4,5,6,1)), url('assets/images/20260228_121740.jpg') center/cover; z-index: -1;"></div>
            <h1 class="page-title">서비스 단가</h1>
            <p class="page-desc">PRICE LIST</p>
        </div>
        <section class="section" style="padding-top: 0; text-align: center;">
            <div class="container">
                <div class="glass-card" style="padding: 1rem; display: inline-block; max-width: 100%; background: rgba(0,0,0,0.4);">
                    <img src="assets/images/price_list.jpg" alt="SHIELD GLASS COAT 시공 단가표" style="width: 100%; max-width: 900px; height: auto; border-radius: 8px; border: 1px solid rgba(220, 165, 80, 0.4); box-shadow: 0 10px 30px rgba(0,0,0,0.5);">
                </div>
            </div>
        </section>
    `,
    services: `
        <div class="page-header" style="position: relative; overflow: hidden; padding: 10rem 0 4rem;">
            <div style="position: absolute; top:0; left:0; width:100%; height:100%; background: linear-gradient(to bottom, rgba(4,5,6,0.8), rgba(4,5,6,1)), url('assets/images/20260225_143216.jpg') center/cover; z-index: -1;"></div>
            <h1 class="page-title">서비스소개</h1>
            <p class="page-desc">PREMIUM SERVICES</p>
        </div>
        <section class="section" style="padding-top: 0;">
            <div class="container">
                <style>
                    .service-grid {
                        display: grid;
                        grid-template-columns: 1fr;
                        gap: 2rem;
                    }
                    .service-row {
                        display: grid;
                        grid-template-columns: 1fr 1fr;
                        gap: 2rem;
                        background: var(--bg-card);
                        border: 1px solid var(--border-light);
                        border-radius: 12px;
                        overflow: hidden;
                        transition: border-color var(--transition-fast);
                    }
                    .service-row:hover {
                        border-color: var(--border-gold);
                    }
                    .service-img {
                        height: 100%;
                        min-height: 380px;
                        background-size: cover;
                        background-position: center;
                    }
                    .service-info {
                        padding: 3rem;
                        display: flex;
                        flex-direction: column;
                        justify-content: center;
                    }
                    @media (max-width: 768px) {
                        .service-row {
                            grid-template-columns: 1fr;
                        }
                        .service-row:nth-child(even) .service-img {
                            order: -1;
                        }
                    }
                </style>
                
                <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(280px, 1fr)); gap: 3rem; margin-top: 2rem;">
                    <!-- Service 1 -->
                    <div class="glass-card" style="padding: 0; overflow: hidden; display: flex; flex-direction: column;">
                        <div style="height: 250px; position: relative; border-bottom: 1px solid rgba(255,255,255,0.05);">
                            <img src="assets/images/20260225_153047.jpg" alt="프리미엄 광택" style="width: 100%; height: 100%; object-fit: cover;">
                        </div>
                        <div style="padding: 2rem; display: flex; flex-direction: column; flex: 1;">
                            <span style="color: var(--primary); font-size: 0.9rem; font-weight: 700; letter-spacing: 2px;">RESTORATION</span>
                            <h3 style="margin: 0.5rem 0 1rem; font-size: 1.5rem;">프리미엄 광택 및 도장면 복원</h3>
                            <p class="text-muted mb-4" style="line-height: 1.6; flex: 1;">생활 스크래치, 스월마크, 워터스팟을 완벽하게 제거하고 도장면 본연의 맑고 깊은 광택을 끌어올립니다. (백범퍼 흠집 제거 전후 사진)</p>
                        </div>
                    </div>
                    
                    <!-- Service 2 -->
                    <div class="glass-card" style="padding: 0; overflow: hidden; display: flex; flex-direction: column;">
                        <div style="height: 250px; position: relative; border-bottom: 1px solid rgba(255,255,255,0.05);">
                            <img src="assets/images/20260228_121740.jpg" alt="하이엔드 쉴드 유리막 코팅" style="width: 100%; height: 100%; object-fit: cover;">
                            <div style="position: absolute; top: 1rem; right: 1rem; background: var(--primary); color: #000; padding: 0.2rem 0.8rem; border-radius: 20px; font-weight: bold; font-size: 0.8rem;">BEST</div>
                        </div>
                        <div style="padding: 2rem; display: flex; flex-direction: column; flex: 1;">
                            <span style="color: var(--primary); font-size: 0.9rem; font-weight: 700; letter-spacing: 2px;">PROTECTION</span>
                            <h3 style="margin: 0.5rem 0 1rem; font-size: 1.5rem;">하이엔드 쉴드 유리막 코팅</h3>
                            <p class="text-muted mb-4" style="line-height: 1.6; flex: 1;">자체 개발/생산한 최고급 세라믹 코팅제를 아낌없이 시공하여, 최상의 방오성과 슬릭감으로 차량을 보호합니다.</p>
                        </div>
                    </div>
                    
                    <!-- Service 3 -->
                    <div class="glass-card" style="padding: 0; overflow: hidden; display: flex; flex-direction: column;">
                        <div style="height: 250px; display: flex; position: relative; border-bottom: 1px solid rgba(255,255,255,0.05);">
                            <div style="flex: 1; position: relative;">
                                <img src="assets/images/service_molding_before.jpg" alt="BEFORE" style="width: 100%; height: 100%; object-fit: cover;">
                                <div style="position: absolute; top: 0.5rem; left: 0.5rem; background: rgba(0,0,0,0.6); color: #fff; padding: 0.1rem 0.6rem; border-radius: 4px; font-size: 0.75rem; font-weight: bold; letter-spacing: 1px;">BEFORE</div>
                            </div>
                            <div style="flex: 1; position: relative; border-left: 1px solid var(--primary);">
                                <img src="assets/images/service_molding_after.jpg" alt="AFTER" style="width: 100%; height: 100%; object-fit: cover;">
                                <div style="position: absolute; top: 0.5rem; right: 0.5rem; background: var(--primary); color: #000; padding: 0.1rem 0.6rem; border-radius: 4px; font-size: 0.75rem; font-weight: bold; letter-spacing: 1px;">AFTER</div>
                            </div>
                        </div>
                        <div style="padding: 2rem; display: flex; flex-direction: column; flex: 1;">
                            <span style="color: var(--primary); font-size: 0.9rem; font-weight: 700; letter-spacing: 2px;">DETAIL</span>
                            <h3 style="margin: 0.5rem 0 1rem; font-size: 1.5rem;">알루미늄 몰딩 복원 (R-Alu Coat)</h3>
                            <p class="text-muted mb-4" style="line-height: 1.6; flex: 1;">수입차 창틀 알루미늄 몰딩의 고질적인 백화현상을 깔끔하게 복원하고, 전용 코팅제로 재발을 방지합니다.</p>
                        </div>
                    </div>
                    
                    <!-- Service 4 -->
                    <div class="glass-card" style="padding: 0; overflow: hidden; display: flex; flex-direction: column;">
                        <div style="height: 250px; position: relative; border-bottom: 1px solid rgba(255,255,255,0.05);">
                            <img src="assets/images/20260305_130653.jpg?v=2" alt="유막 제거 및 초발수 코팅" style="width: 100%; height: 100%; object-fit: cover;">
                        </div>
                        <div style="padding: 2rem; display: flex; flex-direction: column; flex: 1;">
                            <span style="color: var(--primary); font-size: 0.9rem; font-weight: 700; letter-spacing: 2px;">GLASS CARE</span>
                            <h3 style="margin: 0.5rem 0 1rem; font-size: 1.5rem;">유막 제거 및 초발수 코팅</h3>
                            <p class="text-muted mb-4" style="line-height: 1.6; flex: 1;">우천 시 시야 확보를 방해하는 유막을 완벽하게 제거하고, 초발수 코팅을 통해 안전하고 쾌적한 주행 환경을 제공합니다.</p>
                        </div>
                    </div>

                    <!-- Service 5 -->
                    <div class="glass-card" style="padding: 0; overflow: hidden; display: flex; flex-direction: column;">
                        <div style="height: 250px; position: relative; border-bottom: 1px solid rgba(255,255,255,0.05);">
                            <img src="assets/images/20260306_190341.jpg" alt="프리미엄 가죽 시트 코팅" style="width: 100%; height: 100%; object-fit: cover;">
                        </div>
                        <div style="padding: 2rem; display: flex; flex-direction: column; flex: 1;">
                            <span style="color: var(--primary); font-size: 0.9rem; font-weight: 700; letter-spacing: 2px;">INTERIOR</span>
                            <h3 style="margin: 0.5rem 0 1rem; font-size: 1.5rem;">프리미엄 가죽 시트 코팅 <br><span style="font-size: 1.1rem; color: var(--text-muted);">(Seat Coating)</span></h3>
                            <p class="text-muted mb-4" style="line-height: 1.6; flex: 1;">최고급 가죽 전용 코팅제를 사용하여 이염, 스크래치, 갈라짐을 방지하고 신차 고유의 매트한 질감과 색상을 오랫동안 유지합니다.</p>
                        </div>
                    </div>

                    <!-- Service 6 -->
                    <div class="glass-card" style="padding: 0; overflow: hidden; display: flex; flex-direction: column;">
                        <div style="height: 250px; position: relative; border-bottom: 1px solid rgba(255,255,255,0.05);">
                            <img src="assets/images/service_softtop_fallback.jpg" alt="컨버터블 소프트탑 코팅" style="width: 100%; height: 100%; object-fit: cover;">
                        </div>
                        <div style="padding: 2rem; display: flex; flex-direction: column; flex: 1;">
                            <span style="color: var(--primary); font-size: 0.9rem; font-weight: 700; letter-spacing: 2px;">EXTERIOR</span>
                            <h3 style="margin: 0.5rem 0 1rem; font-size: 1.5rem;">컨버터블 소프트탑 코팅 <br><span style="font-size: 1.1rem; color: var(--text-muted);">(Soft-Top Coating)</span></h3>
                            <p class="text-muted mb-4" style="line-height: 1.6; flex: 1;">오픈카 소프트탑 전용 프리미엄 발수 코팅제로 빗물과 오염물의 스며듦을 완벽 차단하고, 자외선으로 인한 직물 변색을 예방합니다.</p>
                        </div>
                    </div>

                    <!-- Service 7 -->
                    <div class="glass-card" style="padding: 0; overflow: hidden; display: flex; flex-direction: column;">
                        <div style="height: 250px; position: relative; border-bottom: 1px solid rgba(255,255,255,0.05);">
                            <img src="assets/images/20260305_134834.jpg" alt="정밀 에바크리닝 & 냄새 제거" style="width: 100%; height: 100%; object-fit: cover;">
                        </div>
                        <div style="padding: 2rem; display: flex; flex-direction: column; flex: 1;">
                            <span style="color: var(--primary); font-size: 0.9rem; font-weight: 700; letter-spacing: 2px;">A/C CARE</span>
                            <h3 style="margin: 0.5rem 0 1rem; font-size: 1.5rem;">정밀 에바크리닝 & 냄새 제거 <br><span style="font-size: 1.1rem; color: var(--text-muted);">(A/C Odor Removal)</span></h3>
                            <p class="text-muted mb-4" style="line-height: 1.6; flex: 1;">내시경 카메라를 활용한 정밀 에바크리닝으로 에어컨 깊숙한 곳의 곰팡이와 악취 원인을 근본적으로 제거하여 쾌적한 실내를 만듭니다.</p>
                        </div>
                    </div>
                </div>
            </div>
        </section>

        <section class="section" style="padding-top: 2rem; border-top: 1px solid var(--border-light);">
            <div class="container">
                <div class="text-center mb-8">
                    <h2 class="mb-2">시공 <span class="gradient-text">Before / After</span></h2>
                    <p class="text-muted">사진을 클릭하면 크게 볼 수 있습니다</p>
                </div>
                <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(320px, 1fr)); gap: 2rem;">
                    <div class="glass-card" style="padding:0;overflow:hidden;cursor:pointer;" onclick="window.openProductGallery('assets/images/260428 GLE350 검정 광택/작업전-12.jpg','assets/images/260428 GLE350 검정 광택/작업후-12.jpg')">
                        <div style="display:grid;grid-template-columns:1fr 1fr;height:220px;">
                            <div style="position:relative;overflow:hidden;"><img src="assets/images/260428 GLE350 검정 광택/작업전-12.jpg" style="width:100%;height:100%;object-fit:cover;"><span style="position:absolute;top:8px;left:8px;background:rgba(0,0,0,0.75);color:#fff;padding:3px 10px;border-radius:4px;font-size:0.75rem;font-weight:700;">BEFORE</span></div>
                            <div style="position:relative;overflow:hidden;"><img src="assets/images/260428 GLE350 검정 광택/작업후-12.jpg" style="width:100%;height:100%;object-fit:cover;"><span style="position:absolute;top:8px;right:8px;background:var(--primary);color:#000;padding:3px 10px;border-radius:4px;font-size:0.75rem;font-weight:700;">AFTER</span></div>
                        </div>
                        <div style="padding:1.2rem;"><span style="color:var(--primary);font-size:0.8rem;font-weight:700;letter-spacing:2px;">BENZ GLE · DETAIL</span><h4 style="margin-top:0.3rem;">B필러 광택 · 유리막코팅</h4></div>
                    </div>
                    <div class="glass-card" style="padding:0;overflow:hidden;cursor:pointer;" onclick="window.openProductGallery('assets/images/260428 GLE350 검정 광택/작업전-15.jpg','assets/images/260428 GLE350 검정 광택/작업후-15.jpg')">
                        <div style="display:grid;grid-template-columns:1fr 1fr;height:220px;">
                            <div style="position:relative;overflow:hidden;"><img src="assets/images/260428 GLE350 검정 광택/작업전-15.jpg" style="width:100%;height:100%;object-fit:cover;"><span style="position:absolute;top:8px;left:8px;background:rgba(0,0,0,0.75);color:#fff;padding:3px 10px;border-radius:4px;font-size:0.75rem;font-weight:700;">BEFORE</span></div>
                            <div style="position:relative;overflow:hidden;"><img src="assets/images/260428 GLE350 검정 광택/작업후-15.jpg" style="width:100%;height:100%;object-fit:cover;"><span style="position:absolute;top:8px;right:8px;background:var(--primary);color:#000;padding:3px 10px;border-radius:4px;font-size:0.75rem;font-weight:700;">AFTER</span></div>
                        </div>
                        <div style="padding:1.2rem;"><span style="color:var(--primary);font-size:0.8rem;font-weight:700;letter-spacing:2px;">BENZ GLE · RESTORATION</span><h4 style="margin-top:0.3rem;">루프 스크래치 제거 · 광택</h4></div>
                    </div>
                    <div class="glass-card" style="padding:0;overflow:hidden;cursor:pointer;" onclick="window.openProductGallery('assets/images/260428 GLE350 검정 광택/작업전-07.jpg','assets/images/260428 GLE350 검정 광택/작업후-07.jpg')">
                        <div style="display:grid;grid-template-columns:1fr 1fr;height:220px;">
                            <div style="position:relative;overflow:hidden;"><img src="assets/images/260428 GLE350 검정 광택/작업전-07.jpg" style="width:100%;height:100%;object-fit:cover;"><span style="position:absolute;top:8px;left:8px;background:rgba(0,0,0,0.75);color:#fff;padding:3px 10px;border-radius:4px;font-size:0.75rem;font-weight:700;">BEFORE</span></div>
                            <div style="position:relative;overflow:hidden;"><img src="assets/images/260428 GLE350 검정 광택/작업후-07.jpg" style="width:100%;height:100%;object-fit:cover;"><span style="position:absolute;top:8px;right:8px;background:var(--primary);color:#000;padding:3px 10px;border-radius:4px;font-size:0.75rem;font-weight:700;">AFTER</span></div>
                        </div>
                        <div style="padding:1.2rem;"><span style="color:var(--primary);font-size:0.8rem;font-weight:700;letter-spacing:2px;">BENZ GLE · COATING</span><h4 style="margin-top:0.3rem;">후드 광택 · 유리막코팅</h4></div>
                    </div>
                    <div class="glass-card" style="padding:0;overflow:hidden;cursor:pointer;" onclick="window.openProductGallery('assets/images/260428 GLE350 검정 광택/작업전-01.jpg','assets/images/260428 GLE350 검정 광택/작업후-01.jpg')">
                        <div style="display:grid;grid-template-columns:1fr 1fr;height:220px;">
                            <div style="position:relative;overflow:hidden;"><img src="assets/images/260428 GLE350 검정 광택/작업전-01.jpg" style="width:100%;height:100%;object-fit:cover;"><span style="position:absolute;top:8px;left:8px;background:rgba(0,0,0,0.75);color:#fff;padding:3px 10px;border-radius:4px;font-size:0.75rem;font-weight:700;">BEFORE</span></div>
                            <div style="position:relative;overflow:hidden;"><img src="assets/images/260428 GLE350 검정 광택/작업후-01.jpg" style="width:100%;height:100%;object-fit:cover;"><span style="position:absolute;top:8px;right:8px;background:var(--primary);color:#000;padding:3px 10px;border-radius:4px;font-size:0.75rem;font-weight:700;">AFTER</span></div>
                        </div>
                        <div style="padding:1.2rem;"><span style="color:var(--primary);font-size:0.8rem;font-weight:700;letter-spacing:2px;">BENZ GLE · NEW CAR</span><h4 style="margin-top:0.3rem;">벤츠 GLE 신차 광택 · 유리막코팅</h4></div>
                    </div>
                    <div class="glass-card" style="padding:0;overflow:hidden;cursor:pointer;" onclick="window.openProductGallery('assets/images/260418 F150 페인트 날림제거/before-04.jpg','assets/images/260418 F150 페인트 날림제거/after-04.jpg')">
                        <div style="display:grid;grid-template-columns:1fr 1fr;height:220px;">
                            <div style="position:relative;overflow:hidden;"><img src="assets/images/260418 F150 페인트 날림제거/before-04.jpg" style="width:100%;height:100%;object-fit:cover;"><span style="position:absolute;top:8px;left:8px;background:rgba(0,0,0,0.75);color:#fff;padding:3px 10px;border-radius:4px;font-size:0.75rem;font-weight:700;">BEFORE</span></div>
                            <div style="position:relative;overflow:hidden;"><img src="assets/images/260418 F150 페인트 날림제거/after-04.jpg" style="width:100%;height:100%;object-fit:cover;"><span style="position:absolute;top:8px;right:8px;background:var(--primary);color:#000;padding:3px 10px;border-radius:4px;font-size:0.75rem;font-weight:700;">AFTER</span></div>
                        </div>
                        <div style="padding:1.2rem;"><span style="color:var(--primary);font-size:0.8rem;font-weight:700;letter-spacing:2px;">FORD F-150 · PAINT</span><h4 style="margin-top:0.3rem;">F-150 페인트 날림제거 · 광택</h4></div>
                    </div>
                    <div class="glass-card" style="padding:0;overflow:hidden;cursor:pointer;" onclick="window.openProductGallery('assets/images/260418 F150 페인트 날림제거/before-06.jpg','assets/images/260418 F150 페인트 날림제거/after-06.jpg')">
                        <div style="display:grid;grid-template-columns:1fr 1fr;height:220px;">
                            <div style="position:relative;overflow:hidden;"><img src="assets/images/260418 F150 페인트 날림제거/before-06.jpg" style="width:100%;height:100%;object-fit:cover;"><span style="position:absolute;top:8px;left:8px;background:rgba(0,0,0,0.75);color:#fff;padding:3px 10px;border-radius:4px;font-size:0.75rem;font-weight:700;">BEFORE</span></div>
                            <div style="position:relative;overflow:hidden;"><img src="assets/images/260418 F150 페인트 날림제거/after-06.jpg" style="width:100%;height:100%;object-fit:cover;"><span style="position:absolute;top:8px;right:8px;background:var(--primary);color:#000;padding:3px 10px;border-radius:4px;font-size:0.75rem;font-weight:700;">AFTER</span></div>
                        </div>
                        <div style="padding:1.2rem;"><span style="color:var(--primary);font-size:0.8rem;font-weight:700;letter-spacing:2px;">FORD F-150 · DETAIL</span><h4 style="margin-top:0.3rem;">F-150 도장면 복원 · 유리막코팅</h4></div>
                    </div>
                </div>
            </div>
        </section>
    `,
    certificates: `
        <div class="page-header">
            <h1 class="page-title">시공증명서</h1>
            <p class="page-desc">WARRANTY SEARCH</p>
        </div>
        <section class="section" style="padding-top: 0;">
            <div class="container">
                <div class="glass-card" style="max-width: 600px; margin: 0 auto; text-align: center;">
                    <h2 class="mb-4">정품 시공 조회</h2>
                    <p class="text-muted mb-8">고객님의 차대번호 마지막 5~6자리를 입력하여<br>쉴드광택 정품 시공 내역을 확인하세요.</p>
                    
                    <form id="cert-search-form" onsubmit="event.preventDefault();" style="display: flex; flex-wrap: wrap; gap: 1rem; margin-bottom: 2rem;">
                        <input type="text" id="cert-search-input" placeholder="차대번호 마지막 5~6자리 입력" style="flex: 1; min-width: 200px; padding: 1rem; border-radius: 4px; border: 1px solid var(--border-light); background: rgba(0,0,0,0.5); color: #fff; font-family: var(--font-body); outline: none; font-size: 1rem;">
                        <button type="submit" class="btn btn-primary" style="flex: 1; min-width: 120px;">조회하기</button>
                    </form>

                    <div id="cert-search-result" style="display: none; padding: 2rem; background: rgba(255,255,255,0.02); border-radius: 8px; border: 1px solid var(--border-gold);">
                        <div style="font-size: 3rem; margin-bottom: 1rem;">🛡️</div>
                        <h3 id="cert-result-title" class="gradient-text mb-4" style="font-size: 1.5rem;">정품 시공이 확인되었습니다</h3>
                        <div id="cert-results-container" style="display: flex; flex-direction: column; gap: 1rem;">
                            <!-- Results will be injected here dynamically -->
                        </div>
                    </div>
                    
                    <div id="cert-search-error" style="display: none; padding: 2rem; color: #ff6b6b;">
                        조회된 시공 내역이 없습니다. 입력하신 정보를 다시 확인해주세요.
                    </div>
                </div>
            </div>
        </section>
    `,
    partners: `
        <div class="page-header">
            <h1 class="page-title">전문점 소개</h1>
            <p class="page-desc">OUR PARTNERS</p>
        </div>
        <section class="section" style="padding-top: 0;">
            <div class="container text-center">
                <p class="text-muted mb-8">쉴드광택의 프리미엄 제품군을 사용하는 공식 파트너샵을 소개합니다.</p>
                
                <style>
                    .partner-grid {
                        display: grid;
                        grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
                        gap: 2.5rem;
                    }
                    .partner-card {
                        background: rgba(255, 255, 255, 0.02);
                        backdrop-filter: blur(10px);
                        -webkit-backdrop-filter: blur(10px);
                        border: 1px solid var(--border-light);
                        border-radius: 12px;
                        overflow: hidden;
                        transition: all var(--transition-normal);
                        display: flex;
                        flex-direction: column;
                        text-align: left;
                    }
                    .partner-card:hover {
                        transform: translateY(-5px);
                        border-color: var(--primary);
                        box-shadow: 0 10px 30px rgba(220, 165, 80, 0.1);
                        background: rgba(255, 255, 255, 0.04);
                    }
                    .partner-img {
                        height: 220px;
                        background-size: cover;
                        background-position: center;
                        border-bottom: 1px solid rgba(255, 255, 255, 0.05);
                    }
                    .partner-info {
                        padding: 2rem;
                        display: flex;
                        flex-direction: column;
                        flex: 1;
                    }
                </style>

                <div class="partner-grid">
                    ${partnersHTML}
                </div>
            </div>
        </section>
    `,
    login: `
        <div class="page-header">
            <h1 class="page-title">시스템 로그인</h1>
            <p class="page-desc">PARTNER & ADMIN LOGIN</p>
        </div>
        <section class="section" style="padding-top: 0;">
            <div class="container">
                <div class="glass-card" style="max-width: 400px; margin: 0 auto; text-align: center;">
                    <h2 class="mb-8 font-weight-bold" style="color: var(--primary);">접근 권한 확인</h2>
                    <form id="login-form" autocomplete="off" style="display: flex; flex-direction: column; gap: 1.5rem;">
                        <input type="text" id="login-id" placeholder="아이디" required style="padding: 1.2rem; border-radius: 4px; border: 1px solid var(--border-light); background: rgba(0,0,0,0.5); color: #fff; font-family: var(--font-body); outline: none; font-size: 1rem;">
                        <input type="password" id="login-pw" placeholder="비밀번호" required style="padding: 1.2rem; border-radius: 4px; border: 1px solid var(--border-light); background: rgba(0,0,0,0.5); color: #fff; font-family: var(--font-body); outline: none; font-size: 1rem;">
                        <button type="submit" class="btn btn-primary" style="margin-top: 1rem; padding: 1.2rem; font-size:1.1rem; width: 100%;">로그인</button>
                    </form>
                    <div id="login-error" style="display: none; margin-top: 1.5rem; color: #ff6b6b; font-size: 0.95rem;">
                        아이디 또는 비밀번호가 일치하지 않습니다.
                    </div>
                </div>
            </div>
        </section>
    `,
    admin: `
        <div class="page-header">
            <h1 class="page-title">관리자 대시보드</h1>
            <p class="page-desc">ADMIN & PARTNER DASHBOARD</p>
        </div>
        <section class="section" style="padding-top: 0;">
            <div class="container">
                <div class="glass-card" style="max-width: 700px; margin: 0 auto; margin-bottom: 3rem;">
                    <h2 class="mb-8 text-center" style="font-size: 1.8rem;" id="reg-form-title">신규 시공증명서 등록</h2>
                    
                    <form id="certificate-register-form" autocomplete="off" style="display: flex; flex-direction: column; gap: 2rem;">
                        <input type="hidden" id="reg-doc-id">
                        
                        <div>
                            <label style="display:block; margin-bottom:0.8rem; color: var(--text-muted); font-size:0.95rem;">시공 지점명</label>
                            <input type="text" id="reg-branch" placeholder="예: 쉴드광택 본사, 서울 파트너샵 등" required style="width: 100%; padding: 1.2rem; border-radius: 4px; border: 1px solid var(--border-light); background: rgba(0,0,0,0.5); color: #fff; font-family: var(--font-body); outline: none; font-size: 1rem;">
                        </div>

                        <div>
                            <label style="display:block; margin-bottom:0.8rem; color: var(--text-muted); font-size:0.95rem;">차대번호 마지막 5~6자리</label>
                            <input type="text" id="reg-vin" placeholder="예: 12345" required style="width: 100%; padding: 1.2rem; border-radius: 4px; border: 1px solid var(--border-light); background: rgba(0,0,0,0.5); color: #fff; font-family: var(--font-body); outline: none; font-size: 1rem;">
                        </div>

                        <div>
                            <label style="display:block; margin-bottom:0.8rem; color: var(--text-muted); font-size:0.95rem;">시공 차량</label>
                            <input type="text" id="reg-model" placeholder="예: Tesla Model 3" required style="width: 100%; padding: 1.2rem; border-radius: 4px; border: 1px solid var(--border-light); background: rgba(0,0,0,0.5); color: #fff; font-family: var(--font-body); outline: none; font-size: 1rem;">
                        </div>

                        <div>
                            <label style="display:block; margin-bottom:0.8rem; color: var(--text-muted); font-size:0.95rem;">시공 종류</label>
                            <select id="reg-type" required style="width: 100%; padding: 1.2rem; border-radius: 4px; border: 1px solid var(--border-light); background: rgba(0,0,0,0.5); color: #fff; font-family: var(--font-body); outline: none; appearance: none; font-size: 1rem; cursor: pointer;">
                                <option value="" disabled selected>코팅 종류를 선택하세요</option>
                                <option value="F5 도장채도 향상">F5 도장채도 향상</option>
                                <option value="G-Pro 도장경도 향상">G-Pro 도장경도 향상</option>
                                <option value="G-Top 발수력 및 슈팅력 향상">G-Top 발수력 및 슈팅력 향상</option>
                                <option value="G-Pro+F5 도장 경도+채도 향상">G-Pro+F5 도장 경도+채도 향상</option>
                                <option value="G-Pro+G-Top 도장 경도+발수력 향상">G-Pro+G-Top 도장 경도+발수력 향상</option>
                                <option value="G-Pro+F5+G-Top 도장 경도+채도+발수력 향상">G-Pro+F5+G-Top 도장 경도+채도+발수력 향상</option>
                                <option value="R-Alu 알루미늄 복원코팅">R-Alu 알루미늄 복원코팅</option>
                                <option value="Soft-Top 보호코팅">Soft-Top 보호코팅</option>
                                <option value="SeatCoat 시트오염보호코팅">SeatCoat 시트오염보호코팅</option>
                                <option value="유리발수코팅">유리발수코팅</option>
                            </select>
                        </div>

                        <div>
                            <label style="display:block; margin-bottom:0.8rem; color: var(--text-muted); font-size:0.95rem;">시공 일자</label>
                            <input type="date" id="reg-date" required style="width: 100%; padding: 1.2rem; border-radius: 4px; border: 1px solid var(--border-light); background: rgba(0,0,0,0.5); color: #fff; font-family: var(--font-body); outline: none; font-size: 1rem; cursor: pointer;">
                        </div>

                        <div style="margin-top: 1rem; display:flex; gap: 1rem;">
                            <button type="submit" id="reg-submit-btn" class="btn btn-primary" style="flex:2; padding: 1.2rem; font-size:1.1rem; border: none; cursor: pointer;">등록하기</button>
                            <button type="button" id="reg-cancel-btn" class="btn btn-outline" style="display:none; flex:1; padding: 1.2rem; cursor: pointer;">취소</button>
                            <button type="button" class="btn btn-outline" onclick="window.auth.signOut().then(() => { window.location.hash='#/'; alert('로그아웃 되었습니다.'); }).catch(console.error);" style="flex:1; padding: 1.2rem; cursor: pointer;">로그아웃</button>
                        </div>
                    </form>
                </div>

                <!-- Admin Certificate List -->
                <div class="glass-card" style="max-width: 900px; margin: 0 auto;">
                    <h2 class="mb-6 text-center" style="font-size: 1.5rem;">나의 등록 내역</h2>
                    <div style="overflow-x: auto;">
                        <table style="width: 100%; border-collapse: collapse; min-width: 700px;">
                            <thead style="border-bottom: 2px solid var(--border-gold); background: rgba(0,0,0,0.6);">
                                <tr>
                                    <th style="padding: 1rem; text-align: left; color: var(--primary);">차량종류</th>
                                    <th style="padding: 1rem; text-align: left; color: var(--primary);">차대번호</th>
                                    <th style="padding: 1rem; text-align: left; color: var(--primary);">시공일자</th>
                                    <th style="padding: 1rem; text-align: left; color: var(--primary);">지점명</th>
                                    <th style="padding: 1rem; text-align: right; color: var(--primary);">관리</th>
                                </tr>
                            </thead>
                            <tbody id="admin-cert-list" style="font-size: 0.95rem;">
                                <tr><td colspan="5" style="padding: 2rem; text-align: center; color: var(--text-muted);">로딩 중...</td></tr>
                            </tbody>
                        </table>
                    </div>
                </div>
            </div>
        </section>
    `,
    notfound: `
        <div class="hero">
            <div class="hero-content">
                <h1 class="hero-title">404</h1>
                <p class="hero-desc">존재하지 않는 페이지입니다.</p>
                <a href="#/" class="btn btn-primary">홈으로 돌아가기</a>
            </div>
        </div>
    `
};

window.AppPages = pages;
