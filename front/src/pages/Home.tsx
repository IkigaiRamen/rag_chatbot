import React, { useState } from "react";
import { askQuestion,type AskResponse } from "../services/ragApi";
import MessageBubble from "../components/MessageBubble";

interface ChatMessage {
  type: "user" | "assistant";
  message: string;
  sources?: any[];
}

const Home: React.FC = () => {
  const [question, setQuestion] = useState("");
  const [messages, setMessages] = useState<ChatMessage[]>([]);
  const [loading, setLoading] = useState(false);

  const handleAsk = async () => {
    if (!question.trim()) return;

    // Add user message
    setMessages((prev) => [...prev, { type: "user", message: question }]);
    setLoading(true);

    try {
      const res: AskResponse = await askQuestion(question);
      setMessages((prev) => [
        ...prev,
        { type: "assistant", message: res.answer, sources: res.sources },
      ]);
    } catch (err) {
      console.error(err);
      setMessages((prev) => [
        ...prev,
        { type: "assistant", message: "Error fetching answer." },
      ]);
    } finally {
      setLoading(false);
      setQuestion("");
    }
  };

  return (
    <div className="flex flex-col h-screen max-w-3xl mx-auto p-4">
      <h1 className="text-3xl font-bold mb-4 text-center">RAG Chat Assistant</h1>

      <div className="flex-1 overflow-y-auto p-2 space-y-2 bg-gray-50 rounded-lg shadow-inner">
        {messages.map((msg, idx) => (
          <MessageBubble key={idx} type={msg.type} message={msg.message} sources={msg.sources} />
        ))}
        {loading && (
          <div className="text-gray-500 italic mb-2">Assistant is typing...</div>
        )}
      </div>

      <div className="flex gap-2 mt-4">
        <input
          type="text"
          className="flex-1 border p-3 rounded-xl focus:outline-none focus:ring-2 focus:ring-blue-400"
          placeholder="Type your question..."
          value={question}
          onChange={(e) => setQuestion(e.target.value)}
          onKeyDown={(e) => e.key === "Enter" && handleAsk()}
        />
        <button
          className="bg-blue-600 text-white px-6 py-3 rounded-xl hover:bg-blue-700"
          onClick={handleAsk}
          disabled={loading}
        >
          Ask
        </button>
      </div>
    </div>
  );
};

export default Home;
