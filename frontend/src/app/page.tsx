'use client';

import { useEffect, useState } from 'react';
import { useRouter } from 'next/navigation';
import ChatInterface from '@/components/ChatInterface';
import { isAuthenticated } from '@/services/auth';
import { getConversation } from '@/services/api';
import { ChatMessage } from '@/types/chat';

export default function Home() {
  const router = useRouter();
  const [isAuthChecking, setIsAuthChecking] = useState(true);
  const [conversationId, setConversationId] = useState<number | null>(null);
  const [initialMessages, setInitialMessages] = useState<ChatMessage[]>([]);
  const [isLoadingHistory, setIsLoadingHistory] = useState(false);

  // Check authentication on mount
  useEffect(() => {
    const checkAuth = async () => {
      const authenticated = await isAuthenticated();

      if (!authenticated) {
        router.push('/login');
        return;
      }

      setIsAuthChecking(false);
    };

    checkAuth();
  }, [router]);

  // Load conversation history if conversationId exists
  useEffect(() => {
    const loadHistory = async () => {
      if (!conversationId) return;

      setIsLoadingHistory(true);
      try {
        const conversation = await getConversation(conversationId);

        // Convert messages to ChatMessage format
        const messages: ChatMessage[] = conversation.messages.map((msg) => ({
          id: msg.id,
          conversation_id: msg.conversation_id,
          role: msg.role,
          content: msg.content,
          created_at: msg.created_at,
        }));

        setInitialMessages(messages);
      } catch (error) {
        console.error('Failed to load conversation history:', error);
      } finally {
        setIsLoadingHistory(false);
      }
    };

    loadHistory();
  }, [conversationId]);

  // Handle new conversation creation
  const handleConversationCreated = (newConversationId: number) => {
    setConversationId(newConversationId);
  };

  // Show loading state while checking authentication
  if (isAuthChecking) {
    return (
      <main className="flex h-screen items-center justify-center">
        <div className="text-center">
          <div className="mb-4 text-4xl">⏳</div>
          <p className="text-gray-600">Loading...</p>
        </div>
      </main>
    );
  }

  // Show loading state while loading conversation history
  if (isLoadingHistory) {
    return (
      <main className="flex h-screen items-center justify-center">
        <div className="text-center">
          <div className="mb-4 text-4xl">💬</div>
          <p className="text-gray-600">Loading conversation...</p>
        </div>
      </main>
    );
  }

  return (
    <main className="h-screen">
      <ChatInterface
        conversationId={conversationId}
        initialMessages={initialMessages}
        onConversationCreated={handleConversationCreated}
      />
    </main>
  );
}
