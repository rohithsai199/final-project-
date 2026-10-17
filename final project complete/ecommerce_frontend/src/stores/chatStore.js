import { create } from "zustand";
import api from "../services/api";

export const useChatStore = create((set, get) => ({
  messages: [],
  unreadByOrder: {},
  unreadCount: 0,
  isConnected: false,
  sendMessage: null,

  setConnection: (isConnected) => set({ isConnected }),

  setSendMessage: (sendMessage) => set({ sendMessage }),

  setUnreadCount: (unreadCount) => set({ unreadCount }),

  // 1. Sync unread counts from backend on page load / mount
  syncUnreadCounts: async (userId, adminId = 1) => {
    if (!userId) return;
    try {
      const res = await api.get(`/chat/history/${adminId}`);
      if (Array.isArray(res.data)) {
        const lastReadGeneral = Number(
          (typeof window !== "undefined" && localStorage.getItem(`chat_read_ts_${userId}`)) || 0
        );
        const orderReadMap = JSON.parse(
          (typeof window !== "undefined" && localStorage.getItem(`chat_order_read_ts_${userId}`)) || "{}"
        );

        let totalUnread = 0;
        const unreadByOrder = {};

        res.data.forEach((msg) => {
          // Only messages sent from admin/support to this user count as unread
          if (msg.sender_id !== userId) {
            const msgTime = new Date(msg.created_at).getTime();
            if (msgTime > lastReadGeneral) {
              totalUnread += 1;
            }
            if (msg.order_id) {
              const lastOrderRead = Number(orderReadMap[msg.order_id] || 0);
              if (msgTime > lastOrderRead) {
                unreadByOrder[msg.order_id] = (unreadByOrder[msg.order_id] || 0) + 1;
              }
            }
          }
        });

        set({
          unreadCount: totalUnread,
          unreadByOrder,
        });
      }
    } catch (err) {
      console.warn("syncUnreadCounts failed:", err);
    }
  },

  // 2. Reactively handle new incoming message
  addIncomingMessage: (message, currentUserId) =>
    set((state) => {
      const isFromOther = currentUserId ? message.sender_id !== currentUserId : true;
      const newUnreadCount = isFromOther ? state.unreadCount + 1 : state.unreadCount;
      const newUnreadByOrder =
        isFromOther && message.order_id != null
          ? {
              ...state.unreadByOrder,
              [message.order_id]: (state.unreadByOrder[message.order_id] || 0) + 1,
            }
          : state.unreadByOrder;

      return {
        messages: [...state.messages, message],
        unreadCount: newUnreadCount,
        unreadByOrder: newUnreadByOrder,
      };
    }),

  addLocalMessage: (message) =>
    set((state) => ({
      messages: [...state.messages, message],
    })),

  markOrderRead: (orderId, userId) =>
    set((state) => {
      if (userId && typeof window !== "undefined") {
        const orderReadMap = JSON.parse(localStorage.getItem(`chat_order_read_ts_${userId}`) || "{}");
        orderReadMap[orderId] = Date.now();
        localStorage.setItem(`chat_order_read_ts_${userId}`, JSON.stringify(orderReadMap));
      }
      const orderUnread = state.unreadByOrder[orderId] || 0;
      return {
        unreadCount: Math.max(0, state.unreadCount - orderUnread),
        unreadByOrder: {
          ...state.unreadByOrder,
          [orderId]: 0,
        },
      };
    }),

  markGeneralRead: (userId) =>
    set((state) => {
      if (userId && typeof window !== "undefined") {
        localStorage.setItem(`chat_read_ts_${userId}`, String(Date.now()));
      }
      return {
        unreadCount: 0,
      };
    }),

  reset: () =>
    set({
      messages: [],
      unreadByOrder: {},
      unreadCount: 0,
      isConnected: false,
      sendMessage: null,
    }),
}));
