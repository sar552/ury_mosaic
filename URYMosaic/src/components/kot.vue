<template>
  <div class="flex h-screen bg-gray-50">
    <!-- Alert Modal -->
    <div
      v-if="showModal"
      class="fixed inset-0 z-50 overflow-y-auto"
      style="background-color: rgba(0, 0, 0, 0.5);"
    >
      <div class="mt-20 flex items-center justify-center">
        <div class="w-full rounded-lg bg-white p-6 shadow-lg md:max-w-md">
          <p class="block text-left text-xl font-medium text-gray">
            <span class="w-3 h-3 rounded-full inline-block mr-1 bg-red-500"></span>
            Not Permitted
          </p>
          <hr class="border-gray-200 my-4" />
          <p class="text-left text-xl mt-6 font-medium text-gray-500">
            Log in to access this page.
          </p>
          <div class="flex justify-start">
            <button
              @click="redirectToLogin();"
              class="mt-8 rounded bg-blue-500 px-3 py-2 text-white hover:bg-blue-600"
            >
              Login
            </button>
          </div>
        </div>
      </div>
    </div>

    <!-- Column 1: NEW ORDERS -->
    <div class="flex-1 overflow-y-auto border-r border-gray-300">
      <div class="sticky top-0 bg-gradient-to-r from-yellow-500 to-yellow-600 text-white p-4 shadow-lg z-10">
        <h2 class="text-2xl font-bold">🔔 YANGI BUYURTMALAR</h2>
        <p class="text-sm opacity-90">Qabul qiling yoki rad eting</p>
        <div class="mt-2 text-lg font-semibold">
          {{ newOrders.length }} ta buyurtma
        </div>
      </div>
      
      <div class="p-4 space-y-4">
        <div
          v-for="kot in newOrders"
          :key="kot.name"
          class="bg-white rounded-lg shadow-lg border-2 border-yellow-400 p-4 hover:shadow-xl transition-all"
        >
          <div class="flex justify-between items-start mb-3">
            <div>
              <div class="text-sm font-medium text-gray-600">
                <span v-if="kot.tableortakeaway !== 'Takeaway'">Stol</span>
                <span class="text-2xl font-bold text-gray-900 ml-1">
                  {{ kot.tableortakeaway }}
                </span>
              </div>
              <div class="text-sm text-gray-500">
                Order: <span class="font-semibold text-gray-900">{{ kot.invoice ? kot.invoice.slice(-4) : 'N/A' }}</span>
                <span class="text-xs ml-2">({{ kot.user }})</span>
              </div>
            </div>
          </div>

          <div v-if="kot.comments" class="mb-3 p-2 bg-yellow-50 rounded text-sm text-gray-700 italic">
            💬 {{ kot.comments }}
          </div>

          <div class="space-y-2 mb-4">
            <div
              v-for="kotitem in kot.kot_items"
              :key="kotitem.name"
              class="flex justify-between items-center text-sm"
            >
              <span class="font-medium text-gray-800">{{ kotitem.item_name }}</span>
              <span class="bg-yellow-100 px-3 py-1 rounded-full font-bold text-yellow-800">
                × {{ kotitem.qty }}
              </span>
            </div>
          </div>

          <div class="flex gap-2">
            <button
              @click="acceptOrder(kot)"
              class="flex-1 bg-green-500 hover:bg-green-600 text-white font-bold py-3 px-4 rounded-lg transition-all transform hover:scale-105"
            >
              ✅ QABUL QILISH
            </button>
            <button
              @click="rejectOrder(kot)"
              class="flex-1 bg-red-500 hover:bg-red-600 text-white font-bold py-3 px-4 rounded-lg transition-all transform hover:scale-105"
            >
              ❌ RAD ETISH
            </button>
          </div>
        </div>

        <div v-if="newOrders.length === 0" class="text-center py-20">
          <div class="text-6xl mb-4">📭</div>
          <p class="text-xl text-gray-400 font-medium">Yangi buyurtmalar yo'q</p>
        </div>
      </div>
    </div>

    <!-- Column 2: PREPARING -->
    <div class="flex-1 overflow-y-auto border-r border-gray-300">
      <div class="sticky top-0 bg-gradient-to-r from-blue-500 to-blue-600 text-white p-4 shadow-lg z-10">
        <h2 class="text-2xl font-bold">👨‍🍳 TAYYORLANAYOTGAN</h2>
        <p class="text-sm opacity-90">Ishlash jarayonida</p>
        <div class="mt-2 text-lg font-semibold">
          {{ preparingOrders.length }} ta buyurtma
        </div>
      </div>
      
      <div class="p-4 space-y-4">
        <div
          v-for="kot in preparingOrders"
          :key="kot.name"
          :class="[
            'rounded-lg shadow-lg border-2 p-4 hover:shadow-xl transition-all',
            isOvertime(kot) ? 'bg-red-50 border-red-500 animate-pulse' : 'bg-white border-blue-400'
          ]"
        >
          <div class="flex justify-between items-start mb-3">
            <div>
              <div class="text-sm font-medium text-gray-600">
                <span v-if="kot.tableortakeaway !== 'Takeaway'">Stol</span>
                <span class="text-2xl font-bold text-gray-900 ml-1">
                  {{ kot.tableortakeaway }}
                </span>
              </div>
              <div class="text-sm text-gray-500">
                Order: <span class="font-semibold text-gray-900">{{ kot.invoice ? kot.invoice.slice(-4) : 'N/A' }}</span>
              </div>
            </div>
            <div :class="[
              'text-3xl font-bold',
              isOvertime(kot) ? 'text-red-600' : 'text-blue-600'
            ]">
              ⏱️ {{ kot.timeRemaining }}
            </div>
          </div>

          <div v-if="kot.comments" class="mb-3 p-2 bg-blue-50 rounded text-sm text-gray-700 italic">
            💬 {{ kot.comments }}
          </div>

          <div class="space-y-2 mb-4">
            <div
              v-for="kotitem in kot.kot_items"
              :key="kotitem.name"
              class="flex justify-between items-center text-sm cursor-pointer"
              @click="toggleItemStrikeThrough(kotitem, kot)"
            >
              <span 
                :class="[
                  'font-medium',
                  kotitem.striked ? 'line-through text-green-600' : 'text-gray-800'
                ]"
              >
                {{ kotitem.item_name }}
              </span>
              <span class="bg-blue-100 px-3 py-1 rounded-full font-bold text-blue-800">
                × {{ kotitem.qty }}
              </span>
            </div>
          </div>

          <button
            @click="serveOrder(kot)"
            class="w-full bg-green-500 hover:bg-green-600 text-white font-bold py-3 px-4 rounded-lg transition-all transform hover:scale-105"
          >
            ✓ TAYYOR BO'LDI
          </button>
        </div>

        <div v-if="preparingOrders.length === 0" class="text-center py-20">
          <div class="text-6xl mb-4">🍳</div>
          <p class="text-xl text-gray-400 font-medium">Tayyorlanayotgan buyurtmalar yo'q</p>
        </div>
      </div>
    </div>

    <!-- Column 3: HISTORY -->
    <div class="flex-1 overflow-y-auto bg-gray-50">
      <div class="sticky top-0 bg-gradient-to-r from-gray-600 to-gray-700 text-white p-4 shadow-lg z-10">
        <h2 class="text-2xl font-bold">📋 TARIX</h2>
        <p class="text-sm opacity-90">Tugallangan buyurtmalar</p>
        <div class="mt-2 text-lg font-semibold">
          {{ activities.length }} ta
        </div>
      </div>
      
      <div class="p-4 space-y-3">
        <div
          v-for="activity in activities"
          :key="activity.id"
          :class="[
            'p-4 rounded-lg border-l-4 shadow-sm transition-all',
            activity.type === 'served' ? 'bg-green-50 border-green-500' : '',
            activity.type === 'rejected' ? 'bg-red-50 border-red-500' : '',
            activity.type === 'cancelled' ? 'bg-orange-50 border-orange-500' : ''
          ]"
        >
          <div class="flex items-start justify-between mb-2">
            <span
              :class="[
                'px-3 py-1 rounded-full text-xs font-bold',
                activity.type === 'served' ? 'bg-green-500 text-white' : '',
                activity.type === 'rejected' ? 'bg-red-500 text-white' : '',
                activity.type === 'cancelled' ? 'bg-orange-500 text-white' : ''
              ]"
            >
              {{ activity.statusText }}
            </span>
            <span class="text-xs text-gray-500">{{ activity.time }}</span>
          </div>
          
          <div class="space-y-1 text-sm">
            <div class="font-semibold text-gray-800">
              Order: {{ activity.orderNumber }} | {{ activity.tableNumber }}
            </div>
            <div class="text-gray-600">
              <div v-for="(item, idx) in activity.items" :key="idx" class="flex justify-between">
                <span>{{ item.name }}</span>
                <span class="font-medium">× {{ item.qty }}</span>
              </div>
            </div>
          </div>
        </div>

        <div v-if="activities.length === 0" class="text-center py-20">
          <div class="text-6xl mb-4">📜</div>
          <p class="text-lg text-gray-400 font-medium">Tarix bo'sh</p>
        </div>
      </div>
    </div>

    <!-- Audio Alert -->
    <div
      v-if="showAudioAlertMessage"
      class="fixed top-20 left-1/2 transform -translate-x-1/2 bg-yellow-500 text-white px-6 py-3 rounded-lg shadow-lg z-50"
    >
      🔊 Audio notifications disabled. Click anywhere to enable.
    </div>

    <!-- Status Message -->
    <div
      v-if="statusMessage"
      :class="[
        'fixed bottom-10 right-10 p-4 rounded-lg shadow-lg text-white font-semibold',
        isOnline ? 'bg-green-500' : 'bg-red-500'
      ]"
    >
      {{ statusMessage }}
    </div>
  </div>
</template>

<script>
import { FrappeApp } from "frappe-js-sdk";
import io from "socket.io-client";

let host = window.location.hostname;
let port = window.location.port;
let protocol = window.location.protocol.replace(':', ''); // Use actual protocol from window
let portPart = port ? `:${port}` : '';
let url = `${protocol}://${host}${portPart}`;
let socketUrl = `${protocol}://${host}:9000`;
let socket = io(socketUrl);

const frappe = new FrappeApp(url);

export default {
  data() {
    return {
      kot: [],
      call: frappe.call(),
      production: "",
      branch: "",
      kot_channel: "",
      loggeduser: "",
      showModal: false,
      kot_alert_time: 15,
      showAudioAlertMessage: false,
      audio_alert: 0,
      isOnline: navigator.onLine,
      statusMessage: "",
      activities: [],
      activityIdCounter: 1,
      kotStatuses: {},
    };
  },
  computed: {
    newOrders() {
      return this.kot.filter(k => 
        !k.showDiv && 
        k.production === this.production &&
        this.getKotStatus(k.name) === 'new' &&
        k.type !== 'Cancelled' &&
        k.type !== 'Partially cancelled'
      );
    },
    preparingOrders() {
      return this.kot.filter(k => 
        !k.showDiv && 
        k.production === this.production &&
        this.getKotStatus(k.name) === 'preparing' &&
        k.type !== 'Cancelled' &&
        k.type !== 'Partially cancelled'
      );
    },
  },
  methods: {
    getKotStatus(kotName) {
      return this.kotStatuses[kotName] || 'new';
    },
    
    setKotStatus(kotName, status) {
      this.kotStatuses[kotName] = status;
      this.saveKotStatuses();
    },
    
    saveKotStatuses() {
      try {
        localStorage.setItem('kot_statuses', JSON.stringify(this.kotStatuses));
      } catch (e) {
        console.error('Failed to save KOT statuses:', e);
      }
    },
    
    loadKotStatuses() {
      try {
        const saved = localStorage.getItem('kot_statuses');
        if (saved) {
          this.kotStatuses = JSON.parse(saved);
        }
      } catch (e) {
        console.error('Failed to load KOT statuses:', e);
        this.kotStatuses = {};
      }
    },
    
    isOvertime(kot) {
      if (!kot.timeRemaining) return false;
      const timeRemaining = kot.timeRemaining.split(":");
      const minutes = parseInt(timeRemaining[0]) * 60 + parseInt(timeRemaining[1]);
      return minutes >= this.kot_alert_time;
    },
    
    acceptOrder(kot) {
      this.setKotStatus(kot.name, 'preparing');
      kot.acceptedTime = new Date().toISOString();
      this.showNotification('success', `✅ Qabul qilindi - ${kot.tableortakeaway}`);
    },
    
    rejectOrder(kot) {
      // Confirm before rejecting
      if (!confirm(`Buyurtmani rad etishni tasdiqlaysizmi?\nStol: ${kot.tableortakeaway}\nOrder: ${kot.invoice ? kot.invoice.slice(-4) : 'N/A'}`)) {
        return;
      }

      this.call
        .post("ury_mosaic.ury_mosaic.api.ury_kot_display.reject_kot", {
          name: kot.name,
          user: this.loggeduser,
        })
        .then((result) => {
          console.log('Reject result:', result);
          
          kot.showDiv = true;
          this.setKotStatus(kot.name, 'completed');
          this.addActivity('rejected', 'RAD ETILDI', kot);
          
          // Show detailed message
          if (result && result.message) {
            if (result.message.invoice_cancelled) {
              this.showNotification('success', `✓ Buyurtma va invoice bekor qilindi - ${kot.tableortakeaway}`);
            } else {
              this.showNotification('success', `✓ Buyurtma rad etildi - ${kot.tableortakeaway}`);
            }
          } else {
            this.showNotification('success', `❌ Rad etildi - ${kot.tableortakeaway}`);
          }
          
          this.removeAllItemsFromLocalStorage(kot);
        })
        .catch((error) => {
          console.error('Reject error:', error);
          this.showNotification('error', `✕ Xatolik: ${error.message || 'Rad etishda xatolik'}`);
        });
    },
    
    serveOrder(kot) {
      const now = new Date();
      const currentTime = now.toLocaleTimeString();

      this.call
        .post("ury_mosaic.ury_mosaic.api.ury_kot_display.serve_kot", {
          name: kot.name,
          time: currentTime,
        })
        .then((result) => {
          kot.showDiv = true;
          this.setKotStatus(kot.name, 'completed');
          this.removeAllItemsFromLocalStorage(kot);
          this.addActivity('served', 'TAYYOR BO\'LDI', kot);
          this.showNotification('success', "✓ Tayyor bo'ldi!");
        })
        .catch((error) => {
          console.error(error);
          this.showNotification('error', "✕ Xatolik yuz berdi!");
        });
    },
    
    confirmOrder(kot) {
      const now = new Date();
      const currentTime = now.toLocaleTimeString();
      
      this.call
        .post("ury_mosaic.ury_mosaic.api.ury_kot_display.confirm_cancel_kot", {
          name: kot.name,
          user: this.loggeduser,
        })
        .then((result) => {
          kot.showDiv = true;
          this.setKotStatus(kot.name, 'completed');
          this.removeAllItemsFromLocalStorage(kot);
          this.addActivity('cancelled', 'BEKOR QILINDI', kot);
          this.showNotification('success', "✓ Tasdiqlandi!");
        })
        .catch((error) => {
          console.error(error);
          this.showNotification('error', "✕ Xatolik yuz berdi!");
        });
    },
    
    addActivity(type, statusText, kot) {
      const now = new Date();
      const activity = {
        id: this.activityIdCounter++,
        type: type,
        statusText: statusText,
        orderNumber: kot.invoice ? kot.invoice.slice(-4) : 'N/A',
        tableNumber: kot.tableortakeaway || 'N/A',
        items: kot.kot_items ? kot.kot_items.map(item => ({
          name: item.item_name,
          qty: item.qty || item.quantity
        })) : [],
        time: now.toLocaleTimeString('uz-UZ', { hour: '2-digit', minute: '2-digit' }),
        timestamp: now.getTime()
      };
      
      this.activities.unshift(activity);
      
      if (this.activities.length > 50) {
        this.activities = this.activities.slice(0, 50);
      }
      
      this.saveActivities();
    },
    
    saveActivities() {
      try {
        localStorage.setItem('kot_activities', JSON.stringify(this.activities));
      } catch (e) {
        console.error('Failed to save activities:', e);
      }
    },
    
    loadActivities() {
      try {
        const saved = localStorage.getItem('kot_activities');
        if (saved) {
          this.activities = JSON.parse(saved);
          if (this.activities.length > 0) {
            this.activityIdCounter = Math.max(...this.activities.map(a => a.id)) + 1;
          }
        }
      } catch (e) {
        console.error('Failed to load activities:', e);
        this.activities = [];
      }
    },
    
    showNotification(type, message) {
      // Simple console notification for now
      console.log(`[${type}] ${message}`);
    },
    
    playAlertSound(path) {
      const currentDomain = window.location.origin;
      const audio_path = currentDomain + path;
      const audio = new Audio(audio_path);
      audio.play().catch(e => console.log('Audio play failed:', e));
    },
    
    auth() {
      return new Promise((resolve, reject) => {
        const auth = frappe.auth();
        auth
          .getLoggedInUser()
          .then((user) => {
            console.log("Logged in user:", user);
            if (!user) {
              console.error("No user found");
              this.showModal = true;
              reject(new Error("No user"));
              return;
            }
            this.loggeduser = user;
            this.showModal = false;
            resolve();
          })
          .catch((error) => {
            console.error("Auth error:", error);
            this.showModal = true;
            reject(error);
          });
      });
    },
    
    fetchKOT() {
      return new Promise((resolve, reject) => {
        try {
          this.call
            .get("ury_mosaic.ury_mosaic.api.ury_kot_display.kot_list", {})
            .then((result) => {
              this.branch = result.message.Branch;
              this.kot_alert_time = result.message.kot_alert_time || 15;
              this.audio_alert = result.message.audio_alert;
              this.kot_channel = `kot_update_${this.branch}_${this.production}`;
              this.kot = result.message.KOT;
              this.updateQtyColorTable();
              this.updateTimeRemaining();
              resolve();
            })
            .catch((error) => {
              console.error(error);
              reject(error);
            });
        } catch (error) {
          reject(error);
        }
      });
    },
    
    toggleItemStrikeThrough(kotitem, kot) {
      kotitem.striked = !kotitem.striked;
      localStorage.setItem(
        `${kot.name}_${kotitem.name}_strike`,
        JSON.stringify(kotitem.striked)
      );
    },
    
    updateColorandTable(kot, restaurant_table, type, table_takeaway) {
      if (restaurant_table === undefined) {
        kot.tableortakeaway = "Takeaway";
      } else {
        if (table_takeaway == 1) {
          kot.tableortakeaway = "Takeaway";
        } else {
          kot.tableortakeaway = restaurant_table;
        }
      }
    },
    
    updateQtyColorTable() {
      this.kot.forEach((kot) => {
        this.updateColorandTable(
          kot,
          kot.restaurant_table,
          kot.type,
          kot.table_takeaway
        );

        kot.kot_items.forEach((kotitem) => {
          const savedState = localStorage.getItem(
            `${kot.name}_${kotitem.name}_strike`
          );
          if (savedState) {
            kotitem.striked = JSON.parse(savedState);
          }
          this.calculateQty(
            kotitem,
            kotitem.quantity,
            kot.type,
            kotitem.cancelled_qty
          );
        });
      });
    },
    
    calculateQty(kotitem, qty, type, cancelled_qty) {
      kotitem.qty = qty;
      if (type == "Partially cancelled" || type == "Cancelled") {
        kotitem.qty = qty - (cancelled_qty || 0);
      }
    },
    
    removeAllItemsFromLocalStorage(kot) {
      const keys = Object.keys(localStorage);
      keys.forEach((key) => {
        if (key.startsWith(`${kot.name}_`)) {
          localStorage.removeItem(key);
        }
      });
    },
    
    updateTimeRemaining() {
      this.kot.forEach((kot) => {
        if (this.getKotStatus(kot.name) === 'preparing') {
          kot.timeRemaining = this.calculateTimeRemaining(kot.acceptedTime || kot.time);
        }
      });
    },
    
    calculateTimeRemaining(targetTime) {
      const currentTime = new Date();
      let targetDate;
      
      if (targetTime.includes('T')) {
        targetDate = new Date(targetTime);
      } else {
        const [targetHours, targetMinutes, targetSeconds] = targetTime.split(":");
        targetDate = new Date(
          currentTime.getFullYear(),
          currentTime.getMonth(),
          currentTime.getDate(),
          targetHours,
          targetMinutes,
          targetSeconds
        );
      }

      const timeDifference = currentTime - targetDate;
      const hoursRemaining = Math.floor(timeDifference / 3600000);
      const minutesRemaining = Math.floor((timeDifference % 3600000) / 60000);

      return `${hoursRemaining}:${minutesRemaining.toString().padStart(2, '0')}`;
    },
    
    redirectToLogin() {
      const currentDomain = window.location.origin;
      const currentPath = window.location.pathname;
      window.location.href = currentDomain + "/login?redirect-to=" + currentPath.substring(1);
    },
    
    hideAudioAlertMessage() {
      this.showAudioAlertMessage = false;
    },
    
    handleOnline() {
      this.isOnline = true;
      this.statusMessage = "You are online";
      this.hideStatusMessageAfterDelay();
      this.fetchKOT();
    },
    
    handleOffline() {
      this.isOnline = false;
      this.statusMessage = "You are Offline";
    },
    
    hideStatusMessageAfterDelay() {
      setTimeout(() => {
        this.statusMessage = "";
      }, 3000);
    },
  },
  
  mounted() {
    window.addEventListener("online", this.handleOnline);
    window.addEventListener("offline", this.handleOffline);
    document.addEventListener("click", this.hideAudioAlertMessage);
    
    const currentUrl = window.location.href;
    const parts = currentUrl.split("/");
    const production = parts[parts.length - 1];
    const decodedProduction = decodeURIComponent(production);
    this.production = decodedProduction;
    
    this.loadActivities();
    this.loadKotStatuses();
    
    const self = this;
    this.auth()
      .then(() => {
        self.fetchKOT().then(() => {
          if (this.audio_alert === 1) {
            this.showAudioAlertMessage = true;
          }
          
          socket.on(this.kot_channel, (doc) => {
            if (this.audio_alert === 1) {
              this.playAlertSound(doc.audio_file);
            }
            
            let kottime = localStorage.getItem("kot_time");
            if (doc.last_kot_time !== null) {
              if (doc.last_kot_time !== kottime) {
                self.fetchKOT();
              }
            }
            
            // Check if this order already exists (update scenario)
            const existingKotIndex = this.kot.findIndex(k => k.name === doc.kot.name);
            
            if (existingKotIndex !== -1) {
              // Update existing order
              const existingKot = this.kot[existingKotIndex];
              
              // Check if order was cancelled
              if ((doc.kot.type === "Cancelled" || doc.kot.type === "Partially cancelled") &&
                  (existingKot.type !== "Cancelled" && existingKot.type !== "Partially cancelled")) {
                // Order just got cancelled - move to history
                this.setKotStatus(doc.kot.name, 'completed');
                this.kot[existingKotIndex] = doc.kot;
                this.kot[existingKotIndex].showDiv = true;
                this.addActivity('cancelled', 'BEKOR QILINDI (ORDER PANELDAN)', doc.kot);
                this.showNotification('warning', `⚠ Buyurtma bekor qilindi - ${doc.kot.tableortakeaway}`);
              } else {
                // Regular update
                this.kot[existingKotIndex] = doc.kot;
              }
            } else {
              // New order - add to beginning
              this.kot.unshift(doc.kot);
              
              // If new order comes already cancelled
              if (doc.kot.type === "Cancelled" || doc.kot.type === "Partially cancelled") {
                this.setKotStatus(doc.kot.name, 'completed');
                doc.kot.showDiv = true;
                this.addActivity('cancelled', 'BEKOR QILINDI (ORDER PANELDAN)', doc.kot);
                this.showNotification('warning', `⚠ Buyurtma bekor qilindi - ${doc.kot.tableortakeaway}`);
              }
            }
            
            this.updateQtyColorTable();
            this.updateTimeRemaining();
            localStorage.setItem("kot_time", doc.kot.time);
          });
        });
      })
      .catch((error) => {
        console.error("Authentication error:", error);
        this.showModal = true;
      });
    
    setInterval(this.updateTimeRemaining, 60000);
  },
  
  beforeDestroy() {
    window.removeEventListener("online", this.handleOnline);
    window.removeEventListener("offline", this.handleOffline);
    document.removeEventListener("click", this.hideAudioAlertMessage);
  },
};
</script>

<style scoped>
@keyframes pulse {
  0%, 100% {
    opacity: 1;
  }
  50% {
    opacity: 0.7;
  }
}

.animate-pulse {
  animation: pulse 2s cubic-bezier(0.4, 0, 0.6, 1) infinite;
}
</style>
