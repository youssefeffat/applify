<script setup>
/**
 * ApplicationStatusBadge — shows the current application status
 * with a premium pill design. Replaces action buttons when a job
 * is in a "locked" status (Applied, Interviewed, Accepted, Rejected).
 */
const props = defineProps({
  status: {
    type: String,
    required: true
  },
  size: {
    type: String,
    default: 'md'  // 'sm' | 'md' | 'lg'
  }
})

const STATUS_CONFIG = {
  Saved: {
    icon: '🔖',
    label: 'Saved',
    bg: '#f0f9ff',
    color: '#0369a1',
    border: '#bae6fd',
    glow: 'rgba(3,105,161,0.15)'
  },
  Applied: {
    icon: '📤',
    label: 'Applied',
    bg: '#eff6ff',
    color: '#1d4ed8',
    border: '#bfdbfe',
    glow: 'rgba(29,78,216,0.15)'
  },
  Interviewed: {
    icon: '🎯',
    label: 'Interviewed',
    bg: '#f5f3ff',
    color: '#6d28d9',
    border: '#ddd6fe',
    glow: 'rgba(109,40,217,0.15)'
  },
  Accepted: {
    icon: '✅',
    label: 'Accepted',
    bg: '#f0fdf4',
    color: '#15803d',
    border: '#86efac',
    glow: 'rgba(21,128,61,0.15)'
  },
  Rejected: {
    icon: '❌',
    label: 'Rejected',
    bg: '#fff1f2',
    color: '#be123c',
    border: '#fda4af',
    glow: 'rgba(190,18,60,0.15)'
  }
}

const SIZE_CONFIG = {
  sm: { padding: '3px 10px', fontSize: '0.72rem', iconSize: '0.8rem', gap: '5px', borderRadius: '20px' },
  md: { padding: '6px 14px', fontSize: '0.85rem', iconSize: '1rem', gap: '6px', borderRadius: '24px' },
  lg: { padding: '10px 20px', fontSize: '1rem', iconSize: '1.2rem', gap: '8px', borderRadius: '28px' }
}

const cfg = STATUS_CONFIG[props.status] || STATUS_CONFIG['Saved']
const sz = SIZE_CONFIG[props.size] || SIZE_CONFIG['md']
</script>

<template>
  <div
    :style="{
      display: 'inline-flex',
      alignItems: 'center',
      gap: sz.gap,
      padding: sz.padding,
      borderRadius: sz.borderRadius,
      background: cfg.bg,
      color: cfg.color,
      border: `1.5px solid ${cfg.border}`,
      fontWeight: 700,
      fontSize: sz.fontSize,
      letterSpacing: '0.02em',
      boxShadow: `0 2px 8px ${cfg.glow}`,
      userSelect: 'none',
      whiteSpace: 'nowrap'
    }"
  >
    <span :style="{ fontSize: sz.iconSize, lineHeight: 1 }">{{ cfg.icon }}</span>
    <span>{{ cfg.label }}</span>
  </div>
</template>
