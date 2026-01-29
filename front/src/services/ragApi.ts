import axios from "axios";

const API_URL = "http://localhost:8000/ask"; // backend endpoint

export interface AskResponse {
  question: string;
  answer: string;
  sources: any[];
  latency_seconds: number;
}

export const askQuestion = async (question: string, top_k = 3): Promise<AskResponse> => {
  const res = await axios.post(API_URL, { question, top_k });
  return res.data;
};
