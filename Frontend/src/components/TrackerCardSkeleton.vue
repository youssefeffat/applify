<template>
  <div class="tracker-card skeleton-card">
    <div class="skeleton-title pulse"></div>
    <div class="skeleton-company pulse"></div>
    <div class="skeleton-meta pulse"></div>
    <div class="skeleton-date pulse"></div>
  </div>
</template>
<style scoped>
.skeleton-card {
  background: white;
  border-radius: var(--radius-md);
  padding: 1rem;
  border: 1px solid var(--border-gray);
  margin-bottom: 1rem;
  pointer-events: none;
}
.skeleton-title {
  height: 1.1rem;
  width: 80%;
  background: #e2e8f0;
  border-radius: 4px;
  margin-bottom: 0.5rem;
}
.skeleton-company {
  height: 0.9rem;
  width: 50%;
  background: #e2e8f0;
  border-radius: 4px;
  margin-bottom: 1rem;
}
.skeleton-meta {
  height: 0.8rem;
  width: 40%;
  background: #e2e8f0;
  border-radius: 4px;
  margin-bottom: 0.5rem;
}
.skeleton-date {
  height: 0.8rem;
  width: 60%;
  background: #e2e8f0;
  border-radius: 4px;
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
