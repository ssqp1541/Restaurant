// 데이터 로딩 및 렌더링
let restaurantsData = [];

// 페이지 로드 시 데이터 불러오기
document.addEventListener('DOMContentLoaded', async () => {
    try {
        const response = await fetch('data/restaurants.json');
        if (!response.ok) {
            throw new Error('데이터를 불러올 수 없습니다.');
        }
        restaurantsData = await response.json();
        renderRestaurants();
    } catch (error) {
        console.error('Error loading data:', error);
        showError('데이터를 불러오는 중 오류가 발생했습니다.');
    }
    
    // 모달 이벤트 리스너 설정
    setupModal();
});

// 매장 카드 렌더링
function renderRestaurants() {
    const container = document.getElementById('restaurants-container');
    
    if (!restaurantsData || restaurantsData.length === 0) {
        container.innerHTML = `
            <div class="empty-state">
                <h2>등록된 맛집이 없습니다</h2>
                <p>데이터를 추가해주세요.</p>
            </div>
        `;
        return;
    }
    
    container.innerHTML = restaurantsData.map((restaurant, index) => 
        createRestaurantCard(restaurant, index)
    ).join('');
    
    // 이미지 클릭 이벤트 추가
    attachImageClickEvents();
}

// 매장 카드 HTML 생성
function createRestaurantCard(restaurant, index) {
    const menuImages = restaurant.menuImages.map((img, i) => 
        `<img src="${img}" alt="${restaurant.name} 메뉴 ${i + 1}" class="menu-image" data-index="${index}" data-image="${i}">`
    ).join('');
    
    const blogLinks = restaurant.blogLinks.map((blog, i) => 
        `<a href="${blog.url}" target="_blank" rel="noopener noreferrer" class="blog-link">${blog.title || `블로그 리뷰 ${i + 1}`}</a>`
    ).join('');
    
    const reviews = restaurant.reviews.map((review, i) => 
        `<div class="review-item">
            <div class="review-text">${review.text}</div>
            ${review.rating ? `<div class="review-rating">${'⭐'.repeat(review.rating)}</div>` : ''}
        </div>`
    ).join('');
    
    return `
        <div class="restaurant-card">
            <div class="restaurant-header">
                <h2 class="restaurant-name">${restaurant.name}</h2>
                <div class="restaurant-info">
                    ${restaurant.address ? `<span>📍 ${restaurant.address}</span>` : ''}
                    ${restaurant.phone ? `<span>📞 ${restaurant.phone}</span>` : ''}
                    ${restaurant.hours ? `<span>🕐 ${restaurant.hours}</span>` : ''}
                </div>
            </div>
            
            ${menuImages ? `
            <div class="menu-section">
                <h3 class="menu-title">대표 메뉴</h3>
                <div class="menu-images">
                    ${menuImages}
                </div>
            </div>
            ` : ''}
            
            ${blogLinks ? `
            <div class="blog-section">
                <h3 class="blog-title">Naver 블로그 리뷰</h3>
                <div class="blog-links">
                    ${blogLinks}
                </div>
            </div>
            ` : ''}
            
            ${reviews ? `
            <div class="reviews-section">
                <h3 class="reviews-title">고객 후기</h3>
                ${reviews}
            </div>
            ` : ''}
        </div>
    `;
}

// 이미지 클릭 이벤트 연결
function attachImageClickEvents() {
    const images = document.querySelectorAll('.menu-image');
    images.forEach(img => {
        img.addEventListener('click', function() {
            const restaurantIndex = parseInt(this.dataset.index);
            const imageIndex = parseInt(this.dataset.image);
            openModal(restaurantIndex, imageIndex);
        });
    });
}

// 모달 설정
function setupModal() {
    const modal = document.getElementById('image-modal');
    const closeBtn = document.querySelector('.modal-close');
    
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
function openModal(restaurantIndex, imageIndex) {
    const modal = document.getElementById('image-modal');
    const modalImg = document.getElementById('modal-image');
    const caption = document.querySelector('.modal-caption');
    
    const restaurant = restaurantsData[restaurantIndex];
    const imageSrc = restaurant.menuImages[imageIndex];
    
    modalImg.src = imageSrc;
    caption.textContent = `${restaurant.name} - 메뉴 ${imageIndex + 1}`;
    modal.style.display = 'block';
}

// 에러 표시
function showError(message) {
    const container = document.getElementById('restaurants-container');
    container.innerHTML = `
        <div class="empty-state">
            <h2>오류 발생</h2>
            <p>${message}</p>
        </div>
    `;
}

