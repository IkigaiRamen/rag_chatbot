import { useState, useRef, useEffect } from 'react';
import { motion } from 'framer-motion';
import { ArrowUp, Paperclip } from 'lucide-react';

interface ChatInputProps {
  onSend: (message: string) => void;
  isLoading: boolean;
}

const ChatInput = ({ onSend, isLoading }: ChatInputProps) => {
  const [message, setMessage] = useState('');
  const textareaRef = useRef<HTMLTextAreaElement>(null);

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (message.trim() && !isLoading) {
      onSend(message.trim());
      setMessage('');
    }
  };

  const handleKeyDown = (e: React.KeyboardEvent) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSubmit(e);
    }
  };

  useEffect(() => {
    if (textareaRef.current) {
      textareaRef.current.style.height = 'auto';
      textareaRef.current.style.height = `${Math.min(textareaRef.current.scrollHeight, 200)}px`;
    }
  }, [message]);

  return (
    <div className="p-4 border-t border-chat-border">
      <form onSubmit={handleSubmit} className="max-w-3xl mx-auto">
        <div className="relative bg-chat-input rounded-2xl border border-chat-border focus-within:border-chat-text-muted/50 transition-colors">
          <div className="flex items-end gap-2 p-3">
            <button
              type="button"
              className="p-2 text-chat-text-muted hover:text-chat-text transition-colors rounded-lg hover:bg-chat-border/30"
            >
              <Paperclip className="w-5 h-5" />
            </button>
            <textarea
              ref={textareaRef}
              value={message}
              onChange={(e) => setMessage(e.target.value)}
              onKeyDown={handleKeyDown}
              placeholder="Message RagGPT..."
              rows={1}
              className="flex-1 bg-transparent text-chat-text placeholder:text-chat-text-muted resize-none outline-none text-sm leading-relaxed max-h-[200px] py-2"
            />
            <motion.button
              type="submit"
              disabled={!message.trim() || isLoading}
              whileHover={{ scale: 1.05 }}
              whileTap={{ scale: 0.95 }}
              className={`p-2 rounded-lg transition-all ${
                message.trim() && !isLoading
                  ? 'bg-chat-text text-chat-bg hover:bg-chat-text/90'
                  : 'bg-chat-border text-chat-text-muted cursor-not-allowed'
              }`}
            >
              <ArrowUp className="w-5 h-5" />
            </motion.button>
          </div>
        </div>
        <p className="text-center text-xs text-chat-text-muted mt-3">
          RagGPT can make mistakes. Check important info.
        </p>
      </form>
    </div>
  );
};

export default ChatInput;
