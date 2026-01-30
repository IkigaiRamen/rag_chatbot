import { motion } from 'framer-motion';
import { Lightbulb, Code, BookOpen, Sparkles } from 'lucide-react';

interface WelcomeScreenProps {
  onSuggestionClick: (suggestion: string) => void;
}

const suggestions = [
  {
    icon: Lightbulb,
    text: "Explain quantum computing in simple terms",
    color: "from-amber-500 to-orange-500",
  },
  {
    icon: Code,
    text: "Write a Python function to reverse a string",
    color: "from-blue-500 to-cyan-500",
  },
  {
    icon: BookOpen,
    text: "Summarize the key points of machine learning",
    color: "from-purple-500 to-pink-500",
  },
  {
    icon: Sparkles,
    text: "Help me brainstorm ideas for a mobile app",
    color: "from-emerald-500 to-teal-500",
  },
];

const WelcomeScreen = ({ onSuggestionClick }: WelcomeScreenProps) => {
  return (
    <div className="flex-1 flex flex-col items-center justify-center p-8">
      <motion.div
        initial={{ opacity: 0, scale: 0.9 }}
        animate={{ opacity: 1, scale: 1 }}
        transition={{ duration: 0.5 }}
        className="text-center mb-12"
      >
        <div className="w-16 h-16 rounded-2xl bg-gradient-to-br from-emerald-500 to-teal-600 flex items-center justify-center mx-auto mb-6 shadow-lg shadow-emerald-500/20">
          <Sparkles className="w-8 h-8 text-white" />
        </div>
        <h1 className="text-3xl font-semibold text-chat-text mb-2">
          How can I help you today?
        </h1>
        <p className="text-chat-text-muted">
          Start a conversation or try one of these suggestions
        </p>
      </motion.div>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-3 w-full max-w-2xl">
        {suggestions.map((suggestion, index) => (
          <motion.button
            key={index}
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.3, delay: index * 0.1 }}
            onClick={() => onSuggestionClick(suggestion.text)}
            className="group flex items-start gap-3 p-4 rounded-xl bg-chat-input border border-chat-border hover:border-chat-text-muted/50 transition-all text-left"
          >
            <div className={`w-8 h-8 rounded-lg bg-gradient-to-br ${suggestion.color} flex items-center justify-center flex-shrink-0`}>
              <suggestion.icon className="w-4 h-4 text-white" />
            </div>
            <span className="text-sm text-chat-text group-hover:text-chat-text/90">
              {suggestion.text}
            </span>
          </motion.button>
        ))}
      </div>
    </div>
  );
};

export default WelcomeScreen;
