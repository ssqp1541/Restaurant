/**
 * 이미지 라이트박스 모달 기능
 * Python Flask 환경에서 서버 사이드 렌더링을 사용하므로
 * 클라이언트 사이드에서는 모달 기능만 담당
 */

// 페이지 로드 시 모달 설정
document.addEventListener('DOMContentLoaded', () => {
    setupModal();
    attachImageClickEvents();
});

// 이미지 클릭 이벤트 연결
function attachImageClickEvents() {
    const images = document.querySelectorAll('.menu-image');
    images.forEach(img => {
        img.addEventListener('click', function() {
            const imageSrc = this.src;
            const imageAlt = this.alt;
            openModal(imageSrc, imageAlt);
        });
    });
}

// 모달 설정
function setupModal() {
    const modal = document.getElementById('image-modal');
    const closeBtn = document.querySelector('.modal-close');
    
    if (!modal || !closeBtn) {
        return;
    }
    
    closeBtn.addEventListener('click', () => {
        modal.style.display = 'none';
    });
    
    window.addEventListener('click', (e) => {
        if (e.target === modal) {
            modal.style.display = 'none';
        }
    });
    
    // ESC 키로 닫기
    document.addEventListener('keydown', (e) => {
        if (e.key === 'Escape' && modal.style.display === 'block') {
            modal.style.display = 'none';
        }
    });
}

// 모달 열기
function openModal(imageSrc, imageAlt) {
    const modal = document.getElementById('image-modal');
    const modalImg = document.getElementById('modal-image');
    const caption = document.querySelector('.modal-caption');
    
    if (!modal || !modalImg) {
        return;
    }
    
    modalImg.src = imageSrc;
    if (caption) {
        caption.textContent = imageAlt || '메뉴 이미지';
    }
    modal.style.display = 'block';
}

