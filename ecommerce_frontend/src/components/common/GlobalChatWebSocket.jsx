import { useCallback, useEffect } from "react";
import useWebSocket from "../../hooks/useWebSocket";
import { getWebSocketUrl } from "../../services/websocketService";
import { useAuthStore } from "../../stores/authStore";
import { useChatStore } from "../../stores/chatStore";
import { useNotificationStore } from "../../stores/notificationStore";

function GlobalChatWebSocket() {
  const user = useAuthStore((state) => state.user);

  const addIncomingMessage = useChatStore(
    (state) => state.addIncomingMessage
  );
  const setConnection = useChatStore(
    (state) => state.setConnection
  );
  const setSendMessage = useChatStore(
    (state) => state.setSendMessage
  );

  const addNotification = useNotificationStore(
    (state) => state.addNotification
  );

  const handleMessage = useCallback(
    (message) => {
      if (message.type !== "chat.message") {
        return;
      }

      // Do not generate notifications or alerts for your own sent messages
      if (user && message.sender_id === user.id) {
        addIncomingMessage(message, user.id);
        return;
      }

      addIncomingMessage(message, user?.id);

      addNotification({
        type: "chat",
        orderId: message.order_id,
        title: message.order_id ? `Order #ORD-${message.order_id} Concierge` : "Arise Customer Support",
        message:
          message.message?.length > 80
            ? `${message.message.slice(0, 80)}...`
            : message.message,
      });
    },
    [addIncomingMessage, addNotification, user]
  );

  const { isConnected, sendMessage } = useWebSocket({
    url: user ? getWebSocketUrl("/ws/chat") : null,
    onMessage: handleMessage,
    enabled: Boolean(user),
  });

  useEffect(() => {
    setConnection(isConnected);
    setSendMessage(sendMessage);

    return () => {
      setConnection(false);
      setSendMessage(null);
    };
  }, [isConnected, sendMessage, setConnection, setSendMessage]);

  return null;
}

export default GlobalChatWebSocket;
