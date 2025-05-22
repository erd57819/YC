<template>
  <div class="main-page">
    <section id="mainCarousel" class="carousel slide mb-5" data-bs-ride="carousel">
      <div class="carousel-indicators">
        <button type="button" data-bs-target="#mainCarousel" data-bs-slide-to="0" class="active" aria-current="true" aria-label="Slide 1"></button>
        <button type="button" data-bs-target="#mainCarousel" data-bs-slide-to="1" aria-label="Slide 2"></button>
        <button type="button" data-bs-target="#mainCarousel" data-bs-slide-to="2" aria-label="Slide 3"></button>
      </div>
      <div class="carousel-inner">
        <div class="carousel-item active">
          <img src="https://via.placeholder.com/1200x400/007bff/ffffff?text=Smart+Financial+Choices" class="d-block w-100" alt="Slide 1 - 스마트한 금융 선택">
          <div class="carousel-caption d-none d-md-block">
            <h5>스마트한 금융 상품 비교</h5>
            <p>나에게 꼭 맞는 예금, 적금을 찾아보세요.</p>
          </div>
        </div>
        <div class="carousel-item">
          <img src="https://via.placeholder.com/1200x400/6c757d/ffffff?text=Investment+Insights" class="d-block w-100" alt="Slide 2 - 투자 정보">
          <div class="carousel-caption d-none d-md-block">
            <h5>금/은 투자 정보 확인</h5>
            <p>안정적인 투자를 위한 현물 가격 변동을 한눈에!</p>
          </div>
        </div>
        <div class="carousel-item">
          <img src="https://via.placeholder.com/1200x400/28a745/ffffff?text=Personalized+Recommendations" class="d-block w-100" alt="Slide 3 - 맞춤 상품 추천">
          <div class="carousel-caption d-none d-md-block">
            <h5>나만을 위한 맞춤 추천</h5>
            <p>데이터 기반으로 최적의 금융 상품을 추천해 드립니다.</p>
          </div>
        </div>
      </div>
      <button class="carousel-control-prev" type="button" data-bs-target="#mainCarousel" data-bs-slide="prev">
        <span class="carousel-control-prev-icon" aria-hidden="true"></span>
        <span class="visually-hidden">Previous</span>
      </button>
      <button class="carousel-control-next" type="button" data-bs-target="#mainCarousel" data-bs-slide="next">
        <span class="carousel-control-next-icon" aria-hidden="true"></span>
        <span class="visually-hidden">Next</span>
      </button>
    </section>

    <section class="container text-center mb-5">
      <h2 class="mb-4">FinLife에 오신 것을 환영합니다!</h2>
      <p class="lead">
        FinLife는 여러분의 성공적인 재테크를 위한 맞춤형 금융 정보를 제공합니다. [cite: 6]
        다양한 예금 및 적금 상품을 비교하고, 금과 은 같은 현물 투자 정보를 확인하며,
        관심 있는 주식 정보를 검색하고, 가까운 은행을 찾는 것까지! [cite: 8]
        FinLife와 함께라면 금융 관리가 더 쉬워집니다.
      </p>
      <div class="row mt-5">
        <div class="col-md-3">
          <div class="feature-icon bg-primary text-white mb-3">
            <i class="bi bi-graph-up-arrow" style="font-size: 2rem;"></i> </div>
          <h5>금리 비교</h5>
          <p>최고의 조건으로 상품을 찾아보세요.</p>
        </div>
        <div class="col-md-3">
          <div class="feature-icon bg-success text-white mb-3">
            <i class="bi bi-gem" style="font-size: 2rem;"></i>
          </div>
          <h5>현물 투자</h5>
          <p>금/은 시세 변동을 확인하세요.</p>
        </div>
        <div class="col-md-3">
          <div class="feature-icon bg-info text-white mb-3">
            <i class="bi bi-geo-alt-fill" style="font-size: 2rem;"></i>
          </div>
          <h5>은행 찾기</h5>
          <p>내 주변 은행을 쉽게 검색하세요.</p>
        </div>
        <div class="col-md-3">
          <div class="feature-icon bg-warning text-white mb-3">
            <i class="bi bi-person-check-fill" style="font-size: 2rem;"></i>
          </div>
          <h5>맞춤 추천</h5>
          <p>나에게 맞는 상품을 추천받으세요.</p>
        </div>
      </div>
    </section>

    <section class="container mb-5">
      <h3 class="text-center mb-4">주요 서비스 바로가기</h3>
      <div class="row">
        <div class="col-md-4 mb-3">
          <div class="card h-100">
            <div class="card-body text-center">
              <h5 class="card-title">예금 & 적금 비교</h5>
              <p class="card-text">다양한 은행의 예금 및 적금 상품 금리를 한눈에 비교하세요.</p>
              <RouterLink :to="{ name: 'DepositListView' }" class="btn btn-primary">바로가기</RouterLink> </div>
          </div>
        </div>
        <div class="col-md-4 mb-3">
          <div class="card h-100">
            <div class="card-body text-center">
              <h5 class="card-title">커뮤니티</h5>
              <p class="card-text">금융 상품에 대한 생각과 정보를 다른 사용자들과 공유하세요.</p>
              <RouterLink :to="{ name: 'ArticleView' }" class="btn btn-secondary">게시판 가기</RouterLink>
            </div>
          </div>
        </div>
        <div class="col-md-4 mb-3">
          <div class="card h-100">
            <div class="card-body text-center">
              <h5 class="card-title">내 프로필</h5>
              <p class="card-text">가입한 상품 정보를 확인하고, 맞춤 추천을 받아보세요.</p>
              <RouterLink v-if="accountStore.isLogin" :to="{ name: 'ProfileView' }" class="btn btn-info">프로필 가기</RouterLink>
              <RouterLink v-else :to="{ name: 'LogInView' }" class="btn btn-info">로그인하고 이용하기</RouterLink>
            </div>
          </div>
        </div>
      </div>
    </section>
  </div>
</template>

<script setup>
import { RouterLink } from 'vue-router'
import { useAccountStore } from '@/stores/accounts'

const accountStore = useAccountStore()

// Bootstrap Icons를 사용하려면 index.html에 CDN 링크를 추가하거나 npm으로 설치해야 합니다.
// 예: <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap-icons@1.7.2/font/bootstrap-icons.css">
</script>

<style scoped>
.carousel-item img {
  height: 400px; /* 캐러셀 이미지 높이 조절 */
  object-fit: cover; /* 이미지가 비율을 유지하며 채우도록 설정 */
}
.carousel-caption {
  background-color: rgba(0, 0, 0, 0.5); /* 캡션 가독성 향상 */
  border-radius: .25rem;
  padding: 1rem;
}
.feature-icon {
  width: 4rem;
  height: 4rem;
  border-radius: .75rem;
  display: inline-flex;
  align-items: center;
  justify-content: center;
}
.card {
  transition: transform .2s;
}
.card:hover {
  transform: translateY(-5px);
  box-shadow: 0 4px 8px rgba(0,0,0,.12), 0 2px 4px rgba(0,0,0,.08);
}
</style>