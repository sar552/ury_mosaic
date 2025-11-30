<template>
  <div class="flex h-screen bg-gray-50">
    <!-- Toast Notifications -->
    <Toast ref="toast" />
    
    <!-- Alert Modal div start-->
    <div
      v-if="this.showModal"
      class="fixed inset-0 z-50 overflow-y-auto bg-gray-100"
    >
      <div class="mt-20 flex items-center justify-center">
        <div class="w-full rounded-lg bg-white p-6 shadow-lg md:max-w-md">
          <p
            class="block text-left text-xl font-medium text-gray dark:text-gray"
          >
            <span
              class="w-3 h-3 rounded-full inline-block mr-1 bg-red-500"
            ></span>
            Not Permitted
          </p>
          <hr class="border-gray-200" />

          <p class="text-left text-xl mt-6 font-medium text-gray-500">
            Log in to access this page.
          </p>

          <div class="flex justify">
            <button
              @click="
                this.showModal = false;
                this.redirectToLogin();
              "
              class="mt-8 rounded bg-blue-500 px-3 py-2 text-white hover:bg-blue-600"
            >
              Login
            </button>
          </div>
        </div>
      </div>
    </div>
    <!-- Alert Modal div end-->

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
                Order: <span class="font-semibold text-gray-900">{{ kot.invoice.slice(-4) }}</span>
                <span class="text-xs ml-2">({{ kot.user }})</span>
              </div>
            </div>
            <div class="text-sm text-gray-500">
              {{ formatTime(kot.time) }}
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
            isOvertime(kot) ? 'bg-red-50 border-red-500' : 'bg-white border-blue-400'
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
                Order: <span class="font-semibold text-gray-900">{{ kot.invoice.slice(-4) }}</span>
              </div>
            </div>
            <div :class="[
              'text-3xl font-bold',
              isOvertime(kot) ? 'text-red-600 animate-pulse' : 'text-blue-600'
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
              class="flex justify-between items-center text-sm"
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
    <div class="w-96 overflow-y-auto bg-gray-50">
      <div class="sticky top-0 bg-gradient-to-r from-gray-600 to-gray-700 text-white p-4 shadow-lg z-10">
        <h2 class="text-2xl font-bold">📋 TARIX</h2>
        <p class="text-sm opacity-90">Tugallangan buyurtmalar</p>
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

    <!-- Audio Alert Message -->
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
    <div
      v-if="this.showModal"
      class="fixed inset-0 z-10 overflow-y-auto bg-gray-100"
    >
      <div class="mt-20 flex items-center justify-center">
        <div class="w-full rounded-lg bg-white p-6 shadow-lg md:max-w-md">
          <p
            class="block text-left text-xl font-medium text-gray dark:text-gray"
          >
            <span
              class="w-3 h-3 rounded-full inline-block mr-1 bg-red-500"
            ></span>
            Not Permitted
          </p>
          <hr class="border-gray-200" />

          <p class="text-left text-xl mt-6 font-medium text-gray-500">
            Log in to access this page.
          </p>

          <div class="flex justify">
            <button
              @click="
                this.showModal = false;
                this.redirectToLogin();
              "
              class="mt-8 rounded bg-blue-500 px-3 py-2 text-white hover:bg-blue-600"
            >
              Login
            </button>
          </div>
        </div>
      </div>
    </div>
    <!-- Alert Modal div end-->

    <!-- Column 1: NEW ORDERS -->
        'right-10',
        'p-4',
        'rounded',
        'text-white',
        {
          'bg-green-500': isOnline,
          'bg-red-500': !isOnline,
        },
      ]"
      @transitionend="handleTransitionEnd"
    >
      {{ statusMessage }}
    </div>
    </div>

    <!-- Activity Panel (Right Side) -->
    <div class="w-96 bg-white border-l border-gray-300 overflow-y-auto shadow-lg">
      <div class="sticky top-0 bg-gradient-to-r from-blue-600 to-blue-700 text-white p-4 shadow-md z-10">
        <h2 class="text-xl font-bold">Buyurtmalar Tarixi</h2>
        <p class="text-sm opacity-90">Real vaqt yangilanishlar</p>
      </div>
      
      <div class="p-4 space-y-3">
        <div
          v-for="activity in activities"
          :key="activity.id"
          :class="[
            'p-4 rounded-lg border-l-4 shadow-sm transition-all duration-300 hover:shadow-md',
            activity.type === 'served' ? 'bg-green-50 border-green-500' : '',
            activity.type === 'confirmed' ? 'bg-blue-50 border-blue-500' : '',
            activity.type === 'cancelled' ? 'bg-red-50 border-red-500' : '',
            activity.type === 'new' ? 'bg-yellow-50 border-yellow-500' : ''
          ]"
        >
          <div class="flex items-start justify-between">
            <div class="flex-1">
              <div class="flex items-center gap-2 mb-2">
                <span
                  :class="[
                    'w-8 h-8 rounded-full flex items-center justify-center text-white font-bold text-sm',
                    activity.type === 'served' ? 'bg-green-500' : '',
                    activity.type === 'confirmed' ? 'bg-blue-500' : '',
                    activity.type === 'cancelled' ? 'bg-red-500' : '',
                    activity.type === 'new' ? 'bg-yellow-500' : ''
                  ]"
                >
                  {{ activity.type === 'served' ? '✓' : activity.type === 'confirmed' ? '✓' : activity.type === 'cancelled' ? '✕' : '🔔' }}
                </span>
                <span class="font-bold text-gray-800">{{ activity.statusText }}</span>
              </div>
              
              <div class="ml-10 space-y-1">
                <div class="flex items-center gap-2">
                  <span class="text-xs text-gray-500 font-medium">Order:</span>
                  <span class="font-semibold text-gray-900">{{ activity.orderNumber }}</span>
                </div>
                
                <div class="flex items-center gap-2">
                  <span class="text-xs text-gray-500 font-medium">{{ activity.tableLabel }}:</span>
                  <span class="font-semibold text-gray-900">{{ activity.tableNumber }}</span>
                </div>
                
                <div class="mt-2">
                  <span class="text-xs text-gray-500 font-medium">Items:</span>
                  <div class="mt-1 space-y-1">
                    <div
                      v-for="(item, idx) in activity.items"
                      :key="idx"
                      class="text-sm text-gray-700 flex justify-between"
                    >
                      <span>{{ item.name }}</span>
                      <span class="font-medium">× {{ item.qty }}</span>
                    </div>
                  </div>
                </div>
              </div>
            </div>
            
            <div class="text-xs text-gray-500 ml-2">
              {{ activity.time }}
            </div>
          </div>
        </div>
        
        <div v-if="activities.length === 0" class="text-center py-12 text-gray-400">
          <p class="text-lg">Hali hech qanday faoliyat yo'q</p>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { FrappeApp } from "frappe-js-sdk";
import Masonry from "masonry-layout";
import io from "socket.io-client";
import Toast from "./Toast.vue";

let host = window.location.hostname;
let port = window.location.port;
let protocol = port ? "http" : "https";
let url = `${protocol}://${host}:${port}`;

// Socket.IO server alohida portda ishlaydi
let socketUrl = `${protocol}://${host}:9000`;
let socket = io(socketUrl);

const frappe = new FrappeApp(url);
export default {
  components: {
    Toast,
  },
  // inject: ["$auth", "$socket"],
  data() {
    return {
      kot: [],
      masonry: null,
      call: frappe.call(),
      production: "",
      branch: "",
      kot_channel: "",
      clickedItems: new Set(),
      struckThroughItems: {},
      loggeduser: "",
      showModal: false,
      kot_alert_time: "",
      showAudioAlertMessage: false,
      audio_alert: 0,
      isOnline: navigator.onLine,
      statusMessage: "",
      activities: [],
      activityIdCounter: 1,
      kotStatuses: {}, // Store KOT statuses: 'new', 'preparing', 'completed'
    };
  },
  computed: {
    newOrders() {
      return this.kot.filter(k => 
        !k.showDiv && 
        k.production === this.production &&
        this.getKotStatus(k.name) === 'new'
      );
    },
    preparingOrders() {
      return this.kot.filter(k => 
        !k.showDiv && 
        k.production === this.production &&
        this.getKotStatus(k.name) === 'preparing'
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
    
    formatTime(timeString) {
      try {
        const [hours, minutes] = timeString.split(':');
        return `${hours}:${minutes}`;
      } catch (e) {
        return timeString;
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
      this.$refs.toast.success(`✅ Buyurtma qabul qilindi - ${kot.tableortakeaway}`);
      
      // Play sound if enabled
      if (this.audio_alert === 1) {
        this.playAlertSound('/assets/ury_mosaic/sounds/accept.mp3');
      }
    },
    
    rejectOrder(kot) {
      // Call backend to cancel the order
      this.call
        .post("ury_mosaic.ury_mosaic.api.ury_kot_display.reject_kot", {
          name: kot.name,
          user: this.loggeduser,
        })
        .then((result) => {
          kot.showDiv = true;
          this.setKotStatus(kot.name, 'completed');
          
          // Add to history
          this.addActivity('rejected', 'RAD ETILDI', kot);
          
          this.$refs.toast.error(`❌ Buyurtma rad etildi - ${kot.tableortakeaway}`);
          
          this.removeAllItemsFromLocalStorage(kot);
        })
        .catch((error) => {
          console.error(error);
          this.$refs.toast.error("✕ Xatolik yuz berdi!");
        });
    },
    
    addActivity(type, statusText, kot) {
      const now = new Date();
      const activity = {
        id: this.activityIdCounter++,
        type: type,
        statusText: statusText,
        orderNumber: kot.invoice ? kot.invoice.slice(-4) : 'N/A',
        tableLabel: kot.tableortakeaway === 'Takeaway' ? 'Takeaway' : 'Stol',
        tableNumber: kot.tableortakeaway || 'N/A',
        items: kot.kot_items ? kot.kot_items.map(item => ({
          name: item.item_name,
          qty: item.qty || item.quantity
        })) : [],
        time: now.toLocaleTimeString('uz-UZ', { hour: '2-digit', minute: '2-digit' }),
        timestamp: now.getTime()
      };
      
      // Add to beginning of array
      this.activities.unshift(activity);
      
      // Keep only last 50 activities
      if (this.activities.length > 50) {
        this.activities = this.activities.slice(0, 50);
      }
      
      // Save to localStorage
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
          // Update counter to avoid ID conflicts
          if (this.activities.length > 0) {
            this.activityIdCounter = Math.max(...this.activities.map(a => a.id)) + 1;
          }
        }
      } catch (e) {
        console.error('Failed to load activities:', e);
        this.activities = [];
      }
    },
    
    playAlertSound(path) {
      var currentDomain = window.location.origin;
      var audio_path = currentDomain + path;
      const audio = new Audio(audio_path);
      audio.play();
    },
    auth() {
      return new Promise((resolve, reject) => {
        const auth = frappe.auth();
        auth
          .getLoggedInUser()
          .then((user) => {
            this.loggeduser = user;
            resolve();
          })
          .catch((error) => {
            console.error(error);
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
              this.kot_alert_time = result.message.kot_alert_time;
              this.audio_alert = result.message.audio_alert;
              this.kot_channel = `kot_update_${this.branch}_${this.production}`;
              this.kot = result.message.KOT;
              this.updateQtyColorTable();
              this.updateTimeRemaining();
              this.masonryLoading();
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
    rotateCard(kot) {
      this.masonryLoading();
      kot.isRotated = !kot.isRotated;
    },
    confirmOrder(kot) {
      const now = new Date();
      this.currentTime = now.toLocaleTimeString();
      this.call
        .post("ury_mosaic.ury_mosaic.api.ury_kot_display.confirm_cancel_kot", {
          name: kot.name,
          user: this.loggeduser,
        })
        .then((result) => {
          kot.showDiv = true;
          this.setKotStatus(kot.name, 'completed');

          this.removeAllItemsFromLocalStorage(kot);
          
          // Add to activity panel
          this.addActivity('cancelled', 'BEKOR QILINDI', kot);
          
          // Show success notification
          this.$refs.toast.success("✓ Buyurtma bekor qilindi!");
        })
        .catch((error) => {
          console.error(error);
          this.$refs.toast.error("✕ Xatolik yuz berdi!");
        });
    },
    async serveOrder(kot) {
      const now = new Date();
      this.currentTime = now.toLocaleTimeString();

      this.call
        .post("ury_mosaic.ury_mosaic.api.ury_kot_display.serve_kot", {
          name: kot.name,
          time: this.currentTime,
        })
        .then((result) => {
          kot.showDiv = true;
          this.setKotStatus(kot.name, 'completed');

          this.removeAllItemsFromLocalStorage(kot);
          
          // Add to activity panel
          this.addActivity('served', 'TAYYOR BO\'LDI', kot);
          
          // Show success notification
          this.$refs.toast.success("✓ Buyurtma tayyor bo'ldi!");
        })
        .catch((error) => {
          console.error(error);
          this.$refs.toast.error("✕ Xatolik yuz berdi!");
        });
    },

    async orderDelayNotify(kot) {
      const now = new Date();
      this.currentTime = now.toLocaleTimeString();

      this.call
        .post(
          "ury_mosaic.ury_mosaic.api.ury_kot_notification.order_delay_notification",
          {
            id: kot.name,
          }
        )
        .then((result) => {
          console.log("call backed ", result);
        })
        .catch((error) => console.error(error));
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
      if (type == "Order Modified") {
        kot.color = "bg-[#FFD493] border border-[#FFC700]";
      } else if (type == "Partially cancelled" || type == "Cancelled") {
        kot.color = "bg-[#FFD2D2] border border-[#FAA7A7]";
      } else if (restaurant_table === undefined || table_takeaway == 1) {
        kot.color = "bg-blue-100 border border-blue-200";
      } else {
        kot.color = "bg-white";
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
        kotitem.qty = qty - cancelled_qty;
      }
    },
    removeAllItemsFromLocalStorage(kot) {
      // Get all keys in local storage
      const keys = Object.keys(localStorage);
      // Remove keys that start with `${kot.name}_`
      keys.forEach((key) => {
        if (key.startsWith(`${kot.name}_`)) {
          localStorage.removeItem(key);
        }
      });
    },

    updateTimeRemaining() {
      // console.log("update time", this.kot_channel);
      this.kot.forEach((kot) => {
        kot.timeRemaining = this.calculateTimeRemaining(kot.time);

        const timeRemaining = kot.timeRemaining.split(":");
        const minutes =
          parseInt(timeRemaining[0]) * 60 + parseInt(timeRemaining[1]);

        if (
          minutes === this.kot_alert_time &&
          kot.type !== "Cancelled" &&
          kot.type !== "Partially cancelled"
        ) {
          this.orderDelayNotify(kot);
        }
        if (minutes >= this.kot_alert_time) {
          kot.timecolor = "text-[#DC0000]";
        } else {
          kot.timecolor = "text-black";
        }
      });
    },
    calculateTimeRemaining(targetTime) {
      const currentTime = new Date();
      const [targetHours, targetMinutes, targetSeconds] = targetTime.split(":");
      const targetDate = new Date(
        currentTime.getFullYear(),
        currentTime.getMonth(),
        currentTime.getDate(),
        targetHours,
        targetMinutes,
        targetSeconds
      );

      const timeDifference = currentTime - targetDate;
      const hoursRemaining = Math.floor(timeDifference / 3600000);
      const minutesRemaining = Math.floor((timeDifference % 3600000) / 60000);

      return `${hoursRemaining} : ${minutesRemaining}`;
    },
    fetchkotwithmasonry() {
      return this.fetchKOT().then(() => {
        this.masonryLoading();
      });
    },
    redirectToLogin() {
      var currentDomain = window.location.origin;
      window.location.href =
        currentDomain + "/login?redirect-to=URYMosaic/" + this.production;
    },
    masonryLoading() {
      this.$nextTick(() => {
        this.masonry = new Masonry(this.$el.querySelector(".grid"), {
          itemSelector: ".masonry-item",
          gutter: 28,

          // Other Masonry options can be added here
        });
        this.masonry.layout();
      });
    },
    hideAudioAlertMessage() {
      this.showAudioAlertMessage = false;
    },
    handleOnline() {
      this.isOnline = true;
      this.setStatusMessage("You are online");
      this.hideStatusMessageAfterDelay();
      this.fetchKOT();
      // Show toast notification
      if (this.$refs.toast) {
        this.$refs.toast.success("✓ Internet ulanish tiklandi");
      }
    },
    handleOffline() {
      this.isOnline = false;
      this.setStatusMessage("You are Offline");
      // Show toast notification
      if (this.$refs.toast) {
        this.$refs.toast.error("✕ Internet ulanish uzildi");
      }
    },
    setStatusMessage(message) {
      this.statusMessage = message;
    },
    hideStatusMessageAfterDelay() {
      setTimeout(() => {
        this.statusMessage = "";
      }, 3000);
    },
    handleTransitionEnd() {
      if (!this.isOnline) {
        // Reset the status message after transition end
        this.setStatusMessage("");
      }
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
    const self = this;

    // Load saved activities and statuses
    this.loadActivities();
    this.loadKotStatuses();

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
            this.kot.unshift(doc.kot);
            this.updateQtyColorTable();
            this.updateTimeRemaining();
            localStorage.setItem("kot_time", doc.kot.time);
            
            // Add to activity panel
            if (doc.kot.type === "Cancelled" || doc.kot.type === "Partially cancelled") {
              this.addActivity('cancelled', 'BEKOR QILINDI', doc.kot);
              this.$refs.toast.warning(`⚠ Buyurtma bekor qilindi - ${doc.kot.tableortakeaway || 'Takeaway'}`);
            } else if (doc.kot.type === "Order Modified") {
              this.$refs.toast.info(`ℹ Buyurtma o'zgartirildi - ${doc.kot.tableortakeaway || 'Takeaway'}`);
            } else {
              this.$refs.toast.info(`🔔 Yangi buyurtma - ${doc.kot.tableortakeaway || 'Takeaway'}`);
            }
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
<style>
.bg-gray-100 {
  background-color: rgba(0, 0, 0, 0.2);
}
</style>
