<template>
  <div v-if="financialStore.savingProduct" class="detail-container">
    <h2 class="title">정기적금 상세</h2>

    <div class="detail-card">
      <div class="detail-row detail-margin-bottom">
        <div class="detail-col-3"><strong>공시 제출월</strong></div>
        <div class="detail-col-9">{{ financialStore.savingProduct.dcls_month }}</div>
      </div>
      <div class="detail-row detail-margin-bottom">
        <div class="detail-col-3"><strong>금융회사명</strong></div>
        <div class="detail-col-9">{{ financialStore.savingProduct.kor_co_nm }}</div>
      </div>
      <div class="detail-row detail-margin-bottom">
        <div class="detail-col-3"><strong>상품명</strong></div>
        <div class="detail-col-9">{{ financialStore.savingProduct.fin_prdt_nm }}</div>
      </div>
      <div class="detail-row detail-margin-bottom">
        <div class="detail-col-3"><strong>가입제한</strong></div>
        <div class="detail-col-9">{{ financialStore.savingProduct.join_deny }}</div>
      </div>
      <div class="detail-row detail-margin-bottom">
        <div class="detail-col-3"><strong>가입방법</strong></div>
        <div class="detail-col-9">{{ financialStore.savingProduct.join_way }}</div>
      </div>
      <div class="detail-row detail-margin-bottom">
        <div class="detail-col-3"><strong>우대조건</strong></div>
        <div class="detail-col-9" v-html="financialStore.savingProduct.spcl_cnd"></div>
      </div>
      <div class="detail-row detail-margin-bottom">
        <div class="detail-col-3"><strong>저축 기간 및 금리</strong></div>
        <div class="detail-col-9">
          <ul class="no-bullet-list">
            <li v-for="option in financialStore.savingProduct.options" :key="option.id">
              {{ option.save_trm }}개월 (유형: {{ option.rsrv_type_nm }}, 기본 {{ option.intr_rate }}%, 우대 {{ option.intr_rate2 }}%)
            </li>
          </ul>
        </div>
      </div>
      <div class="detail-row detail-margin-bottom">
        <div class="detail-col-3"><strong>만기 후 이자율</strong></div>
        <div class="detail-col-9" v-html="financialStore.savingProduct.mtrt_int"></div>
      </div>
      <div class="detail-row detail-margin-bottom">
        <div class="detail-col-3"><strong>최대 한도</strong></div>
        <div class="detail-col-9">{{ financialStore.savingProduct.max_limit }}</div>
      </div>

      <div class="text-align-end">
        <button class="custom-button custom-button-primary" @click="openJoinModal">가입</button>
      </div>
    </div>
  </div>
  <div v-else class="detail-container text-align-center">
    <p>상품 정보를 불러오는 중입니다...</p>
    <div class="loading-spinner">
      <span class="visually-hidden-text">Loading...</span>
    </div>
  </div>

  <div v-if="showModal" class="modal-overlay" @click.self="closeJoinModal">
    <div class="modal-content-custom">
      <div class="modal-header-custom">
        <h5 class="modal-title-custom">상품 가입하기</h5>
        <button type="button" class="modal-close-button" @click="closeJoinModal" aria-label="Close">X</button>
      </div>
      <div class="modal-body-custom">
        <form @submit.prevent="submitJoin">
          <div class="form-group detail-margin-bottom">
            <label for="principal" class="form-label-custom">월 납입액:</label>
            <input type="number" class="form-control-custom" id="principal" v-model.number="joinPayload.principal" required>
          </div>
          <div class="form-group detail-margin-bottom">
            <label for="maturity_at" class="form-label-custom">만기일:</label>
            <input type="date" class="form-control-custom" id="maturity_at" v-model="joinPayload.maturity_at">
          </div>
          <div class="form-group detail-margin-bottom">
            <label for="selectedOption" class="form-label-custom">저축 기간 선택:</label>
            <select class="form-control-custom" id="selectedOption" v-model="selectedOptionId" @change="updateAppliedRate">
              <option v-for="option in currentProductOptions" :value="option.id" :key="option.id">
                {{ option.save_trm }}개월 (유형: {{ option.rsrv_type_nm }}, 기본 {{ option.intr_rate }}%, 우대 {{ option.intr_rate2 }}%)
              </option>
            </select>
          </div>
          <div class="form-group detail-margin-bottom">
            <label for="appliedRate" class="form-label-custom">적용 금리:</label>
            <input type="text" class="form-control-custom" id="appliedRate" v-model="joinPayload.applied_rate" readonly>
          </div>
          <button type="submit" class="custom-button custom-button-primary">가입 확정</button>
        </form>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, watch } from 'vue';
import { useFinancialStore } from '@/stores/financials';
import { useRoute } from 'vue-router';

const financialStore = useFinancialStore();
const route = useRoute();

const showModal = ref(false); // 모달 표시 여부 제어용 ref

// 가입 폼 데이터
const joinPayload = ref({
  principal: 0,
  maturity_at: null,
  applied_rate: null,
});
const selectedOptionId = ref(null);

const currentProductOptions = computed(() => {
  return financialStore.savingProduct?.options || [];
});

const updateAppliedRate = () => {
  const selectedOption = currentProductOptions.value.find(
    (option) => option.id === selectedOptionId.value
  );
  if (selectedOption) {
    joinPayload.value.applied_rate = selectedOption.intr_rate2;
  } else {
    joinPayload.value.applied_rate = null;
  }
};

// 라우트 파라미터(id) 변경 감지하여 상품 상세 정보 다시 불러오기
watch(() => route.params.id, (newId) => {
  if (newId) {
    financialStore.fetchSavingProductDetail(newId);
  }
}, { immediate: true }); // 컴포넌트 마운트 시 즉시 실행

const openJoinModal = () => {
  // 모달 열기 전에 가입 폼 데이터 초기화
  joinPayload.value = {
    principal: 0,
    maturity_at: null,
    applied_rate: null,
  };
  // 기본적으로 첫 번째 옵션을 선택하도록 설정
  if (currentProductOptions.value.length > 0) {
    selectedOptionId.value = currentProductOptions.value[0].id;
    updateAppliedRate(); // 선택된 옵션에 따라 적용 금리 업데이트
  }
  showModal.value = true; // 모달 열기
};

const closeJoinModal = () => {
  showModal.value = false; // 모달 닫기
};

const submitJoin = async () => {
  try {
    const selectedOption = currentProductOptions.value.find(
      (option) => option.id === selectedOptionId.value
    );
    // 만기일이 설정되지 않았다면, 선택된 저축 기간을 기반으로 만기일 계산
    if (selectedOption && selectedOption.save_trm && !joinPayload.value.maturity_at) {
      const today = new Date();
      const maturityDate = new Date(today.getFullYear(), today.getMonth() + selectedOption.save_trm, today.getDate());
      joinPayload.value.maturity_at = maturityDate.toISOString().split('T')[0];
    }

    await financialStore.subscribeSavingProduct(route.params.id, joinPayload.value);
    closeJoinModal(); // 가입 성공 후 모달 닫기
  } catch (error) {
    console.error('가입 요청 실패:', error);
    // 에러 메시지는 financials.js 스토어에서 이미 처리됨
  }
};
</script>

<style scoped>
/* 상세 페이지 전체 컨테이너 */
.detail-container {
  max-width: 960px;
  margin: 40px auto;
  padding: 0 15px;
}

/* 제목 스타일 */
.title {
  margin-bottom: 30px;
  font-size: 2em;
  color: #333;
}

/* 상세 정보 카드 스타일 */
.detail-card {
  border: 1px solid #ddd;
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  background-color: #fff;
  padding: 30px;
}

/* 행(Row) 스타일 */
.detail-row {
  display: flex;
  flex-wrap: wrap;
  margin-left: -15px;
  margin-right: -15px;
}

/* 컬럼(Column) 스타일 */
.detail-col-3 {
  flex: 0 0 25%;
  max-width: 25%;
  padding-left: 15px;
  padding-right: 15px;
  box-sizing: border-box;
}

.detail-col-9 {
  flex: 0 0 75%;
  max-width: 75%;
  padding-left: 15px;
  padding-right: 15px;
  box-sizing: border-box;
}

/* 하단 마진 유틸리티 */
.detail-margin-bottom {
  margin-bottom: 15px;
}

/* 텍스트 정렬 */
.text-align-end {
  text-align: right;
}

.text-align-center {
  text-align: center;
}

/* 커스텀 버튼 스타일 */
.custom-button {
  padding: 10px 20px;
  border: none;
  border-radius: 5px;
  cursor: pointer;
  font-size: 1em;
  transition: background-color 0.3s ease;
}

.custom-button-primary {
  background-color: #007bff;
  color: white;
}

.custom-button-primary:hover {
  color: #333;
}

/* 목록 스타일 제거 */
.no-bullet-list {
  list-style: none;
  padding-left: 0;
  margin-bottom: 0;
}

/* 로딩 스피너 애니메이션 */
.loading-spinner {
  display: inline-block;
  width: 40px;
  height: 40px;
  border: 4px solid rgba(0, 123, 255, 0.2);
  border-top-color: #007bff;
  border-radius: 50%;
  animation: spin 1s linear infinite;
}

@keyframes spin {
  to {
    transform: rotate(360deg);
  }
}

.visually-hidden-text {
  position: absolute;
  width: 1px;
  height: 1px;
  margin: -1px;
  padding: 0;
  overflow: hidden;
  clip: rect(0, 0, 0, 0);
  white-space: nowrap;
  border: 0;
}

/* --- 모달 스타일 --- */
.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-color: rgba(0, 0, 0, 0.5);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 1000;
}

.modal-content-custom {
  background-color: #fff;
  padding: 20px;
  border-radius: 8px;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
  width: 90%;
  max-width: 500px;
  position: relative;
}

.modal-header-custom {
  display: flex;
  justify-content: space-between;
  align-items: center;
  border-bottom: 1px solid #eee;
  padding-bottom: 10px;
  margin-bottom: 20px;
}

.modal-title-custom {
  font-size: 1.5em;
  margin: 0;
}

.modal-close-button {
  background: none;
  border: none;
  font-size: 1.5em;
  cursor: pointer;
  color: #aaa;
}

.modal-close-button:hover {
  color: #333;
}

.modal-body-custom {
  /* 추가적인 모달 본문 스타일 */
}

.form-group {
  margin-bottom: 15px;
}

.form-label-custom {
  display: block;
  margin-bottom: 5px;
  font-weight: bold;
}

.form-control-custom {
  width: calc(100% - 20px);
  padding: 8px 10px;
  border: 1px solid #ccc;
  border-radius: 4px;
  box-sizing: border-box;
}

.form-control-custom:focus {
  border-color: #007bff;
  outline: none;
  box-shadow: 0 0 0 0.2rem rgba(0, 123, 255, 0.25);
}
</style>