import React, { useState, useEffect } from 'react';
import { PlayCircle, CheckCircle, Loader2 } from 'lucide-react';

export default function App() {
  const [ticker, setTicker] = useState('AAPL');
  const [taskId, setTaskId] = useState(null);
  const [progress, setProgress] = useState(0);
  const [status, setStatus] = useState('idle');
  const [agent, setAgent] = useState('');

  const handleGenerate = async () => {
    // Mocking an API call to generate a report which returns a task ID
    // const res = await fetch('/api/v1/reports/generate', { method: 'POST', body: JSON.stringify({ ticker }) });
    // const data = await res.json();
    const mockTaskId = `task-${Date.now()}`;
    setTaskId(mockTaskId);
    setStatus('processing');
    setProgress(0);
  };

  useEffect(() => {
    if (taskId && status === 'processing') {
      const ws = new WebSocket(`ws://localhost:8000/ws/reports/stream/${taskId}`);
      
      ws.onmessage = (event) => {
        const data = JSON.parse(event.data);
        if (data.status === 'processing') {
          setProgress(data.progress);
          setAgent(data.current_agent);
        } else if (data.status === 'completed') {
          setStatus('completed');
          setProgress(100);
          setAgent('Report Generated Successfully!');
          ws.close();
        }
      };

      return () => ws.close();
    }
  }, [taskId, status]);

  return (
    <div className="min-h-screen bg-gray-900 text-white p-8">
      <div className="max-w-3xl mx-auto">
        <h1 className="text-3xl font-bold mb-8">AI Equity Research Analyst</h1>
        
        <div className="bg-gray-800 p-6 rounded-lg shadow-lg mb-8">
          <div className="flex gap-4 mb-4">
            <input 
              type="text" 
              value={ticker}
              onChange={(e) => setTicker(e.target.value)}
              className="bg-gray-700 text-white px-4 py-2 rounded focus:outline-none focus:ring-2 focus:ring-blue-500"
              placeholder="Enter Ticker (e.g. AAPL)"
            />
            <button 
              onClick={handleGenerate}
              disabled={status === 'processing'}
              className="bg-blue-600 hover:bg-blue-700 px-6 py-2 rounded flex items-center gap-2 font-medium transition disabled:opacity-50"
            >
              {status === 'processing' ? <Loader2 className="animate-spin" size={20} /> : <PlayCircle size={20} />}
              Generate Report
            </button>
          </div>

          {status !== 'idle' && (
            <div className="mt-8">
              <div className="flex justify-between mb-2">
                <span className="text-gray-400">Status: {agent}</span>
                <span className="font-medium">{progress}%</span>
              </div>
              <div className="w-full bg-gray-700 rounded-full h-2.5">
                <div 
                  className="bg-blue-500 h-2.5 rounded-full transition-all duration-500 ease-out" 
                  style={{ width: `${progress}%` }}
                ></div>
              </div>
            </div>
          )}

          {status === 'completed' && (
            <div className="mt-8 p-4 bg-green-900/30 border border-green-800 rounded flex items-center gap-3">
              <CheckCircle className="text-green-500" />
              <span className="text-green-100">Report is ready for review.</span>
              <button className="ml-auto text-sm bg-green-700 hover:bg-green-600 px-3 py-1 rounded">
                View Report
              </button>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}
