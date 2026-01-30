export interface AskResponse {
    answer: string;
    sources: any[];
    latency_seconds: number;
  }
  
  export async function askRag(question: string): Promise<AskResponse> {
    const res = await fetch('http://127.0.0.1:8000/ask', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        question,
        top_k: 3,
      }),
    });
  
    if (!res.ok) {
      throw new Error('Failed to fetch RAG response');
    }
  
    return res.json();
  }
  