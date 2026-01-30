import { motion } from 'framer-motion';
import { Plus, MessageSquare, Settings, Menu, X } from 'lucide-react';
import type { Conversation } from '@/types/chat';

interface ChatSidebarProps {
  conversations: Conversation[];
  currentConversationId: string | null;
  onNewChat: () => void;
  onSelectConversation: (id: string) => void;
  isOpen: boolean;
  onToggle: () => void;
}

const ChatSidebar = ({
  conversations,
  currentConversationId,
  onNewChat,
  onSelectConversation,
  isOpen,
  onToggle,
}: ChatSidebarProps) => {
  return (
    <>
      {/* Mobile overlay */}
      {isOpen && (
        <motion.div
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          exit={{ opacity: 0 }}
          className="fixed inset-0 bg-black/50 z-40 md:hidden"
          onClick={onToggle}
        />
      )}

      {/* Sidebar */}
      <motion.aside
        initial={false}
        animate={{ x: isOpen ? 0 : -280 }}
        transition={{ type: "spring", damping: 25, stiffness: 300 }}
        className={`fixed md:relative left-0 top-0 h-full w-[280px] bg-chat-sidebar border-r border-chat-border flex flex-col z-50 ${
          isOpen ? 'translate-x-0' : '-translate-x-full md:translate-x-0 md:w-0 md:border-0 md:overflow-hidden'
        }`}
      >
        {/* Header */}
        <div className="p-3 flex items-center justify-between">
          <button
            onClick={onToggle}
            className="p-2 text-chat-text-muted hover:text-chat-text hover:bg-chat-border/30 rounded-lg transition-colors"
          >
            <X className="w-5 h-5 md:hidden" />
            <Menu className="w-5 h-5 hidden md:block" />
          </button>
          <button
            onClick={onNewChat}
            className="p-2 text-chat-text-muted hover:text-chat-text hover:bg-chat-border/30 rounded-lg transition-colors"
          >
            <Plus className="w-5 h-5" />
          </button>
        </div>

        {/* New Chat Button */}
        <div className="px-3 mb-4">
          <button
            onClick={onNewChat}
            className="w-full flex items-center gap-3 px-3 py-3 rounded-lg border border-chat-border text-chat-text hover:bg-chat-border/30 transition-colors"
          >
            <Plus className="w-4 h-4" />
            <span className="text-sm">New chat</span>
          </button>
        </div>

        {/* Conversations List */}
        <div className="flex-1 overflow-y-auto scrollbar-thin px-3">
          {conversations.length > 0 && (
            <div className="mb-4">
              <p className="px-3 py-2 text-xs font-medium text-chat-text-muted uppercase tracking-wider">
                Recent
              </p>
              <div className="space-y-1">
                {conversations.map((conversation) => (
                  <button
                    key={conversation.id}
                    onClick={() => onSelectConversation(conversation.id)}
                    className={`w-full flex items-center gap-3 px-3 py-2 rounded-lg text-left transition-colors ${
                      currentConversationId === conversation.id
                        ? 'bg-chat-border/50 text-chat-text'
                        : 'text-chat-text-muted hover:text-chat-text hover:bg-chat-border/30'
                    }`}
                  >
                    <MessageSquare className="w-4 h-4 flex-shrink-0" />
                    <span className="text-sm truncate">{conversation.title}</span>
                  </button>
                ))}
              </div>
            </div>
          )}
        </div>

        {/* Footer */}
        <div className="p-3 border-t border-chat-border">
          <button className="w-full flex items-center gap-3 px-3 py-2 rounded-lg text-chat-text-muted hover:text-chat-text hover:bg-chat-border/30 transition-colors">
            <Settings className="w-4 h-4" />
            <span className="text-sm">Settings</span>
          </button>
        </div>
      </motion.aside>

      {/* Mobile toggle button when sidebar is closed */}
      {!isOpen && (
        <button
          onClick={onToggle}
          className="fixed top-4 left-4 p-2 text-chat-text-muted hover:text-chat-text bg-chat-sidebar border border-chat-border rounded-lg z-30 md:hidden"
        >
          <Menu className="w-5 h-5" />
        </button>
      )}
    </>
  );
};

export default ChatSidebar;
