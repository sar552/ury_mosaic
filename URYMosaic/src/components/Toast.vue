<template>
  <div class="toast-container">
    <transition-group name="toast" tag="div">
      <div
        v-for="toast in toasts"
        :key="toast.id"
        :class="['toast', `toast-${toast.type}`]"
      >
        <div class="toast-content">
          <span class="toast-icon">{{ getIcon(toast.type) }}</span>
          <span class="toast-message">{{ toast.message }}</span>
          <button class="toast-close" @click="removeToast(toast.id)">×</button>
        </div>
      </div>
    </transition-group>
  </div>
</template>

<script>
export default {
  name: "Toast",
  data() {
    return {
      toasts: [],
      nextId: 1,
    };
  },
  methods: {
    show(message, type = "success", duration = 5000) {
      const id = this.nextId++;
      const toast = { id, message, type };
      this.toasts.push(toast);

      setTimeout(() => {
        this.removeToast(id);
      }, duration);
    },
    removeToast(id) {
      const index = this.toasts.findIndex((t) => t.id === id);
      if (index !== -1) {
        this.toasts.splice(index, 1);
      }
    },
    getIcon(type) {
      const icons = {
        success: "✓",
        error: "✕",
        warning: "⚠",
        info: "ℹ",
      };
      return icons[type] || icons.info;
    },
    success(message, duration) {
      this.show(message, "success", duration);
    },
    error(message, duration) {
      this.show(message, "error", duration);
    },
    warning(message, duration) {
      this.show(message, "warning", duration);
    },
    info(message, duration) {
      this.show(message, "info", duration);
    },
  },
};
</script>

<style scoped>
.toast-container {
  position: fixed;
  top: 20px;
  right: 20px;
  z-index: 10000;
  display: flex;
  flex-direction: column;
  gap: 10px;
  max-width: 400px;
}

.toast {
  background: white;
  border-radius: 8px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
  overflow: hidden;
  min-width: 300px;
}

.toast-content {
  display: flex;
  align-items: center;
  padding: 16px;
  gap: 12px;
}

.toast-icon {
  width: 24px;
  height: 24px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: bold;
  flex-shrink: 0;
  font-size: 14px;
}

.toast-success .toast-icon {
  background: #28a745;
  color: white;
}

.toast-error .toast-icon {
  background: #dc3545;
  color: white;
}

.toast-warning .toast-icon {
  background: #ffc107;
  color: #212529;
}

.toast-info .toast-icon {
  background: #17a2b8;
  color: white;
}

.toast-message {
  flex: 1;
  color: #212529;
  font-size: 14px;
  font-weight: 500;
}

.toast-close {
  background: none;
  border: none;
  font-size: 24px;
  color: #6c757d;
  cursor: pointer;
  padding: 0;
  width: 24px;
  height: 24px;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
  transition: color 0.2s;
}

.toast-close:hover {
  color: #212529;
}

/* Animation */
.toast-enter-active {
  animation: slideIn 0.3s ease-out;
}

.toast-leave-active {
  animation: slideOut 0.3s ease-out;
}

@keyframes slideIn {
  from {
    transform: translateX(400px);
    opacity: 0;
  }
  to {
    transform: translateX(0);
    opacity: 1;
  }
}

@keyframes slideOut {
  from {
    transform: translateX(0);
    opacity: 1;
  }
  to {
    transform: translateX(400px);
    opacity: 0;
  }
}
</style>
