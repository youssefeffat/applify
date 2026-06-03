<template>
  <div class="job-card skeleton-card">
    <div class="skeleton-header">
      <div class="skeleton-title pulse"></div>
      <div class="skeleton-company pulse"></div>
    </div>
    
    <div class="skeleton-location pulse"></div>
    
    <div class="job-card-tags">
      <div class="skeleton-tag pulse" style="width: 80px;"></div>
      <div class="skeleton-tag pulse" style="width: 100px;"></div>
      <div class="skeleton-tag pulse" style="width: 60px;"></div>
    </div>
  </div>
</template>
<style scoped>
.skeleton-card {
  position: relative;
  min-height: 200px;
  pointer-events: none;
}
.skeleton-title {
  height: 1.5rem;
  width: 70%;
  background: #e2e8f0;
  border-radius: 4px;
  margin-bottom: 0.5rem;
}
.skeleton-company {
  height: 1rem;
  width: 40%;
  background: #e2e8f0;
  border-radius: 4px;
}
.skeleton-location {
  height: 1rem;
  width: 30%;
  background: #e2e8f0;
  border-radius: 4px;
  margin: 1.5rem 0;
}
.skeleton-tag {
  height: 28px;
  background: #e2e8f0;
  border-radius: 14px;
}
.pulse {
  animation: pulse 1.5s infinite ease-in-out;
}
@keyframes pulse {
  0% { opacity: 0.7; }
  50% { opacity: 0.3; }
  100% { opacity: 0.7; }
}
</style>
