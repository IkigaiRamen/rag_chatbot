import { motion } from 'framer-motion';
import ReactMarkdown from 'react-markdown';
import { User, Sparkles } from 'lucide-react';
import type { Message } from '@/types/chat';

interface ChatMessageProps {
  message: Message;
}

const ChatMessage = ({ message }: ChatMessageProps) => {
  const isUser = message.role === 'user';

  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.3, ease: "easeOut" }}
      className={`flex gap-4 px-4 py-6 ${isUser ? 'bg-transparent' : 'bg-chat-message-ai/50'}`}
    >
      <div className="flex-shrink-0">
        <div
          className={`w-8 h-8 rounded-lg flex items-center justify-center ${
            isUser
              ? 'bg-chat-message-user text-primary-foreground'
              : 'bg-gradient-to-br from-emerald-500 to-teal-600 text-white'
          }`}
        >
          {isUser ? <User className="w-4 h-4" /> : <Sparkles className="w-4 h-4" />}
        </div>
      </div>
      <div className="flex-1 min-w-0">
        <p className="text-sm font-medium text-chat-text mb-1">
          {isUser ? 'You' : 'RagGPT'}
        </p>
        <div className="prose prose-invert prose-sm max-w-none text-chat-text leading-relaxed">
          <ReactMarkdown
            components={{
              p: ({ children }) => <p className="mb-3 last:mb-0">{children}</p>,
              code: ({ children, className }) => {
                const isInline = !className;
                return isInline ? (
                  <code className="bg-chat-input px-1.5 py-0.5 rounded text-sm font-mono text-emerald-400">
                    {children}
                  </code>
                ) : (
                  <code className="block bg-chat-input p-4 rounded-lg overflow-x-auto text-sm font-mono">
                    {children}
                  </code>
                );
              },
              pre: ({ children }) => (
                <pre className="bg-chat-input rounded-lg overflow-hidden my-3">
                  {children}
                </pre>
              ),
              ul: ({ children }) => <ul className="list-disc list-inside mb-3 space-y-1">{children}</ul>,
              ol: ({ children }) => <ol className="list-decimal list-inside mb-3 space-y-1">{children}</ol>,
              li: ({ children }) => <li className="text-chat-text">{children}</li>,
              h1: ({ children }) => <h1 className="text-xl font-bold mb-3 mt-4">{children}</h1>,
              h2: ({ children }) => <h2 className="text-lg font-bold mb-2 mt-4">{children}</h2>,
              h3: ({ children }) => <h3 className="text-base font-bold mb-2 mt-3">{children}</h3>,
              a: ({ href, children }) => (
                <a href={href} className="text-emerald-400 hover:underline" target="_blank" rel="noopener noreferrer">
                  {children}
                </a>
              ),
              blockquote: ({ children }) => (
                <blockquote className="border-l-2 border-chat-border pl-4 italic text-chat-text-muted my-3">
                  {children}
                </blockquote>
              ),
            }}
          >
            {message.content}
          </ReactMarkdown>
        </div>
      </div>
    </motion.div>
  );
};

export default ChatMessage;
