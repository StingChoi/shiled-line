document.addEventListener('DOMContentLoaded', () => {
    
    // Set Current Year in Footer
    document.getElementById('year').textContent = new Date().getFullYear();

    // Elements
    const appContainer = document.getElementById('app');
    const header = document.querySelector('.header');
    const navLinks = document.querySelectorAll('.nav-link');
    const mobileBtn = document.querySelector('.mobile-menu-btn');
    const navList = document.querySelector('.nav-list');

    // pages object imported from pages.js
    const pages = window.AppPages;

    // --- Router Logic ---
    function navigate() {
        let hash = window.location.hash.substring(1); // remove '#'
        if (!hash || hash === '/') {
            hash = 'home';
        } else if (hash.startsWith('/')) {
            hash = hash.substring(1); // remove leading '/'
        }

        // --- RBAC Route Guards ---
        const user = window.auth ? window.auth.currentUser : null;
        if (hash === 'admin' && !user) {
            window.location.hash = '#/login';
            return;
        }
        
        if (hash === 'login' && user) {
            window.location.hash = '#/admin';
            return;
        }

        const view = pages[hash] || pages['notfound'];
        
        // Simple fade out/in effect
        appContainer.style.opacity = '0';
        
        setTimeout(() => {
            appContainer.innerHTML = view;
            window.scrollTo({ top: 0, behavior: 'instant' });
            appContainer.style.opacity = '1';
            updateNav(hash);
            
            // Re-trigger animation by resetting ID
            appContainer.style.animation = 'none';
            appContainer.offsetHeight; /* trigger reflow */
            appContainer.style.animation = null; 
            
            if (hash === 'admin' && window.loadAdminCertificates) {
                window.loadAdminCertificates();
            }

        }, 200);

        // Close mobile menu if open
        if (navList.classList.contains('active')) {
            navList.classList.remove('active');
        }
    }

    function updateNav(currentHash) {
        navLinks.forEach(link => {
            link.classList.remove('active');
            if (link.getAttribute('href') === '#/' + currentHash || (currentHash === 'home' && link.getAttribute('href') === '#/')) {
                link.classList.add('active');
            }
        });
    }

    // Handle initial load, auth state changes, and URL hash changes
    window.addEventListener('hashchange', navigate);

    if (window.auth) {
        window.auth.onAuthStateChanged((user) => {
            navigate();
        });
    } else {
        navigate();
    }

    // 시공증명서 조회 및 관리 모두 Firebase Firestore 단일 소스로 운영

    // --- Helpers ---
    function formatDateKorean(dateString) {
        if (!dateString) return '-';
        const parts = dateString.split('-');
        if (parts.length === 3) {
            return `${parts[0]}년 ${parts[1]}월 ${parts[2]}일`;
        }
        return dateString;
    }

    // UI Logic & Global Event Delegation
    
    // Admin Dashboard Global Functions
    window.deleteCertificate = async function(id) {
        if (!confirm("정말 삭제하시겠습니까?")) return;
        try {
            await window.db.collection('certificates').doc(id).delete();
            alert("삭제되었습니다.");
            window.loadAdminCertificates();
        } catch (err) {
            console.error("Delete failed:", err);
            alert("삭제 중 오류가 발생했습니다.");
        }
    };

    window.editCertificate = async function(id) {
        try {
            const doc = await window.db.collection('certificates').doc(id).get();
            if (!doc.exists) return;
            const data = doc.data();
            
            document.getElementById('reg-doc-id').value = id;
            document.getElementById('reg-branch').value = data.branch;
            document.getElementById('reg-vin').value = data.vin_number;
            document.getElementById('reg-model').value = data.car_type;
            document.getElementById('reg-type').value = data.coating_type;
            document.getElementById('reg-date').value = data.install_date;
            
            document.getElementById('reg-form-title').textContent = "시공증명서 수정";
            document.getElementById('reg-submit-btn').textContent = "수정(Update)";
            document.getElementById('reg-cancel-btn').style.display = "block";
            
            window.scrollTo({ top: 0, behavior: 'smooth' });
        } catch (err) {
            console.error("Edit load failed:", err);
            alert("데이터를 불러오는 중 오류가 발생했습니다.");
        }
    };
    
    window.loadAdminCertificates = async function() {
        const listBody = document.getElementById('admin-cert-list');
        if (!listBody) return;
        
        try {
            const snapshot = await window.db.collection('certificates').get();
            let docs = [];
            snapshot.forEach(doc => docs.push({ id: doc.id, ...doc.data() }));
            
            // Sort by createdAt desc locally (safe without composite index)
            docs.sort((a, b) => {
                const ta = a.createdAt && a.createdAt.toMillis ? a.createdAt.toMillis() : 0;
                const tb = b.createdAt && b.createdAt.toMillis ? b.createdAt.toMillis() : 0;
                return tb - ta;
            });
            
            if (docs.length === 0) {
                listBody.innerHTML = '<tr><td colspan="5" style="padding: 2rem; text-align: center; color: var(--text-muted);">등록된 시공증명서가 없습니다.</td></tr>';
                return;
            }
            
            let html = '';
            docs.forEach(data => {
                html += `
                    <tr style="border-bottom: 1px solid rgba(255,255,255,0.05); transition: background 0.3s;" onmouseover="this.style.background='rgba(255,255,255,0.02)';" onmouseout="this.style.background='transparent';">
                        <td style="padding: 1rem;">${data.car_type || '-'}</td>
                        <td style="padding: 1rem;">${data.vin_number || '-'}</td>
                        <td style="padding: 1rem;">${formatDateKorean(data.install_date)}</td>
                        <td style="padding: 1rem;">${data.branch || '-'}</td>
                        <td style="padding: 1rem; text-align: right; white-space: nowrap;">
                            <button class="btn btn-outline" style="padding: 0.4rem 0.8rem; font-size: 0.85rem; margin-right: 0.5rem;" onclick="window.editCertificate('${data.id}')">수정</button>
                            <button class="btn btn-primary" style="padding: 0.4rem 0.8rem; font-size: 0.85rem; border: none;" onclick="window.deleteCertificate('${data.id}')">삭제</button>
                        </td>
                    </tr>
                `;
            });
            listBody.innerHTML = html;
        } catch (err) {
            console.error("Failed to load certificates:", err);
            listBody.innerHTML = '<tr><td colspan="5" style="padding: 2rem; text-align: center; color: #ff6b6b;">목록을 불러올 수 없습니다.</td></tr>';
        }
    };

    document.addEventListener('submit', async (e) => {
        if (e.target && e.target.id === 'cert-search-form') {
            e.preventDefault();
            const inputVal = document.getElementById('cert-search-input').value.trim();
            const resultDiv = document.getElementById('cert-search-result');
            const errorDiv = document.getElementById('cert-search-error');
            
            if (!inputVal) return;

            try {
                // Fetch from Firestore
                const querySnapshot = await window.db.collection('certificates')
                    .where('vin_number', '==', inputVal)
                    .get();
                
                if (!querySnapshot.empty) {
                    const titleEl = document.getElementById('cert-result-title');
                    const resultsContainer = document.getElementById('cert-results-container');
                    
                    if (querySnapshot.docs.length > 1) {
                        titleEl.textContent = `${querySnapshot.docs.length}건의 정품 시공이 확인되었습니다`;
                    } else {
                        titleEl.textContent = '정품 시공이 확인되었습니다';
                    }

                    // Sort descending by install_date
                    const docs = querySnapshot.docs.map(doc => doc.data()).sort((a, b) => {
                        return new Date(b.install_date || 0) - new Date(a.install_date || 0);
                    });

                    let html = '';
                    docs.forEach(match => {
                        html += `
                        <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 1.5rem; text-align: left; background: rgba(0,0,0,0.3); padding: 1.5rem; border-radius: 4px; font-size: 1.05rem; border: 1px solid rgba(255,255,255,0.05);">
                            <div style="border-bottom: 1px solid rgba(255,255,255,0.1); padding-bottom: 0.5rem;">
                                <span class="text-muted" style="font-size: 0.85rem; display: block; margin-bottom: 0.3rem;">차대번호(일부)</span>
                                <div style="font-weight: 700;">${match.vin_number || '-'}</div>
                            </div>
                            <div style="border-bottom: 1px solid rgba(255,255,255,0.1); padding-bottom: 0.5rem;">
                                <span class="text-muted" style="font-size: 0.85rem; display: block; margin-bottom: 0.3rem;">시공 일자</span>
                                <div style="font-weight: 700;">${formatDateKorean(match.install_date)}</div>
                            </div>
                            <div>
                                <span class="text-muted" style="font-size: 0.85rem; display: block; margin-bottom: 0.3rem;">시공 차량</span>
                                <div style="font-weight: 700;">${match.car_type || '-'}</div>
                            </div>
                            <div>
                                <span class="text-muted" style="font-size: 0.85rem; display: block; margin-bottom: 0.3rem;">시공 종류</span>
                                <div style="font-weight: 700; color: var(--primary);">${match.coating_type || '-'}</div>
                            </div>
                            ${match.branch ? `
                            <div style="grid-column: 1 / -1; border-top: 1px solid rgba(255,255,255,0.1); padding-top: 1rem; margin-top: -0.5rem;">
                                <span class="text-muted" style="font-size: 0.85rem; display: block; margin-bottom: 0.3rem;">시공 지점명</span>
                                <div style="font-weight: 700;">${match.branch}</div>
                            </div>
                            ` : ''}
                        </div>
                        `;
                    });

                    resultsContainer.innerHTML = html;
                    
                    errorDiv.style.display = 'none';
                    resultDiv.style.display = 'block';
                    
                    // Simple animation
                    resultDiv.style.animation = 'none';
                    resultDiv.offsetHeight;
                    resultDiv.style.animation = 'fadeIn 0.5s ease forwards';
                } else {
                    resultDiv.style.display = 'none';
                    errorDiv.style.display = 'block';
                }
            } catch (err) {
                console.error("Failed to fetch certificates data", err);
                alert("데이터 조회 중 오류가 발생했습니다.");
            }
        }

        // --- Admin Login ---
        if (e.target && e.target.id === 'login-form') {
            e.preventDefault();
            const id = document.getElementById('login-id').value;
            const pw = document.getElementById('login-pw').value;
            const errorDiv = document.getElementById('login-error');

            window.auth.signInWithEmailAndPassword(id, pw)
                .then(() => {
                    errorDiv.style.display = 'none';
                    window.location.hash = '#/admin';
                })
                .catch((error) => {
                    console.error("Login failed:", error);
                    errorDiv.textContent = '아이디 또는 비밀번호가 일치하지 않습니다.';
                    errorDiv.style.display = 'block';
                });
        }

        // --- Admin Dashboard Registration ---
        if (e.target && e.target.id === 'certificate-register-form') {
            e.preventDefault();
            
            // Get form values
            const docId = document.getElementById('reg-doc-id').value;
            const branch = document.getElementById('reg-branch').value;
            const vin = document.getElementById('reg-vin').value;
            const model = document.getElementById('reg-model').value;
            const type = document.getElementById('reg-type').value;
            const dateStr = document.getElementById('reg-date').value;

            const certData = {
                branch: branch,
                vin_number: vin,
                car_type: model,
                coating_type: type,
                install_date: dateStr,
                uid: window.auth.currentUser ? window.auth.currentUser.uid : "unknown"
            };

            if (docId) {
                // Update
                certData.updatedAt = firebase.firestore.FieldValue.serverTimestamp();
                window.db.collection('certificates').doc(docId).update(certData)
                    .then(() => {
                        alert("시공증명서가 성공적으로 수정되었습니다.");
                        e.target.reset();
                        document.getElementById('reg-doc-id').value = '';
                        document.getElementById('reg-form-title').textContent = "신규 시공증명서 등록";
                        document.getElementById('reg-submit-btn').textContent = "등록하기";
                        document.getElementById('reg-cancel-btn').style.display = "none";
                        window.loadAdminCertificates();
                    })
                    .catch(error => {
                        console.error("Error updating document: ", error);
                        alert("수정 중 오류가 발생했습니다.");
                    });
            } else {
                // Create
                certData.createdAt = firebase.firestore.FieldValue.serverTimestamp();
                window.db.collection('certificates').add(certData)
                    .then(() => {
                        alert("시공증명서가 성공적으로 등록 및 저장되었습니다.");
                        e.target.reset(); // clear form inputs
                        window.loadAdminCertificates();
                    })
                    .catch(error => {
                        console.error("Error adding document: ", error);
                        alert("등록 중 오류가 발생했습니다. 권한이 없거나 네트워크를 확인하세요.");
                    });
            }
        }
    });

    // Scroll effect for header
    window.addEventListener('scroll', () => {
        if (window.scrollY > 50) {
            header.classList.add('scrolled');
        } else {
            header.classList.remove('scrolled');
        }
    });

    // Mobile menu toggle
    mobileBtn.addEventListener('click', () => {
        navList.classList.toggle('active');
    });

    // Cancel Edit Button
    document.addEventListener('click', (e) => {
        if (e.target && e.target.id === 'reg-cancel-btn') {
            const form = document.getElementById('certificate-register-form');
            if (form) form.reset();
            document.getElementById('reg-doc-id').value = '';
            document.getElementById('reg-form-title').textContent = "신규 시공증명서 등록";
            document.getElementById('reg-submit-btn').textContent = "등록하기";
            e.target.style.display = "none";
        }
    });

    // --- Global Audio Toggle ---
    const audioBtn = document.getElementById('audio-toggle-btn');
    const bgAudio = document.getElementById('bg-audio');
    
    if (audioBtn && bgAudio) {
        audioBtn.addEventListener('click', () => {
            if (bgAudio.paused) {
                bgAudio.play();
                audioBtn.classList.add('playing');
            } else {
                bgAudio.pause();
                audioBtn.classList.remove('playing');
            }
        });
    }

    // --- Gallery Modal Logic ---
    const modalHtml = `
        <div id="galleryModalOverlay" class="gallery-modal-overlay" onclick="window.closeProductGallery()">
            <div class="gallery-modal-content" onclick="event.stopPropagation()">
                <button class="gallery-modal-close" onclick="window.closeProductGallery()">&times;</button>
                <img id="galleryModalImg" class="gallery-modal-img" src="" alt="시공 상세 사진">
            </div>
        </div>
    `;
    document.body.insertAdjacentHTML('beforeend', modalHtml);

    const galleryModalOverlay = document.getElementById('galleryModalOverlay');
    const galleryModalImg = document.getElementById('galleryModalImg');

    window.openProductGallery = function(imageSrc, imageSrc2) {
        if (!galleryModalOverlay) return;
        const modalContent = galleryModalOverlay.querySelector('.gallery-modal-content');
        
        // Reset content
        modalContent.innerHTML = '<button class="gallery-modal-close" onclick="window.closeProductGallery()">&times;</button>';
        
        if (imageSrc2) {
            modalContent.innerHTML += `
                <div style="display: flex; gap: 4px; max-height: 90vh;">
                    <div style="flex: 1; position: relative;">
                        <span style="position: absolute; top: 1rem; left: 1rem; background: rgba(0,0,0,0.7); color: #fff; padding: 0.3rem 0.8rem; border-radius: 4px; font-weight: bold; font-size: 0.85rem; letter-spacing: 1px;">BEFORE</span>
                        <img src="${imageSrc}" class="gallery-modal-img" style="width: 100%; height: 100%; object-fit: cover;">
                    </div>
                    <div style="flex: 1; position: relative;">
                        <span style="position: absolute; top: 1rem; right: 1rem; background: var(--primary); color: #000; padding: 0.3rem 0.8rem; border-radius: 4px; font-weight: bold; font-size: 0.85rem; letter-spacing: 1px;">AFTER</span>
                        <img src="${imageSrc2}" class="gallery-modal-img" style="width: 100%; height: 100%; object-fit: cover;">
                    </div>
                </div>
            `;
        } else {
            modalContent.innerHTML += `<img src="${imageSrc}" class="gallery-modal-img">`;
        }
        
        galleryModalOverlay.classList.add('active');
    };

    window.closeProductGallery = function() {
        if (!galleryModalOverlay) return;
        galleryModalOverlay.classList.remove('active');
    };

    // Close on Escape key
    document.addEventListener('keydown', (e) => {
        if (e.key === 'Escape') {
            window.closeProductGallery();
        }
    });

});
