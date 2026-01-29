import React from "react";

interface MessageBubbleProps {
  message: string;
  type: "user" | "assistant";
  sources?: any[];
}

const MessageBubble: React.FC<MessageBubbleProps> = ({ message, type, sources }) => {
  const isUser = type === "user";
  return (
    <div className={`flex ${isUser ? "justify-end" : "justify-start"} mb-4`}>
      <div
        className={`max-w-[80%] p-4 rounded-xl shadow-md break-words ${
          isUser ? "bg-blue-600 text-white rounded-br-none" : "bg-gray-100 text-gray-900 rounded-bl-none"
        }`}
      >
        <p>{message}</p>
        {!isUser && sources && sources.length > 0 && (
          <div className="mt-2 text-xs text-gray-500">
            Sources:
            <ul className="list-disc ml-5">
              {sources.map((s, idx) => (
                <li key={idx}>
                  Doc: {s.doc_id}, Page: {s.page}, Text: {s.text?.slice(0, 60)}...
                </li>
              ))}
            </ul>
          </div>
        )}
      </div>
    </div>
  );
};

export default MessageBubble;
