import React from "react";

interface AnswerCardProps {
  answer: string;
  sources: any[];
}

const AnswerCard: React.FC<AnswerCardProps> = ({ answer, sources }) => {
  return (
    <div className="border p-4 rounded-md shadow-md bg-white">
      <h2 className="text-lg font-semibold mb-2">Answer:</h2>
      <p className="mb-4">{answer}</p>
      {sources.length > 0 && (
        <>
          <h3 className="font-medium mb-1">Sources:</h3>
          <ul className="list-disc ml-5">
            {sources.map((s, idx) => (
              <li key={idx}>
                Doc: {s.doc_id}, Page: {s.page}, Text: {s.text?.slice(0, 60)}...
              </li>
            ))}
          </ul>
        </>
      )}
    </div>
  );
};

export default AnswerCard;
