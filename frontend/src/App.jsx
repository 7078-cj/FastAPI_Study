import { useEffect, useState, useRef } from 'react';
import './App.css';

function App() {
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState('');
  const [clientId, setClientId] = useState('1');
  const [connected, setConnected] = useState(false);
  const ws = useRef(null);
  const chatEndRef = useRef(null); // for scrolling

  // Scroll to bottom when messages change
  useEffect(() => {
    chatEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages]);

  useEffect(() => {
    if (ws.current) ws.current.close();

    ws.current = new WebSocket(`ws://127.0.0.1:8000/ws/${clientId}`);

    ws.current.onopen = () => setConnected(true);
    ws.current.onmessage = (event) => setMessages((prev) => [...prev, event.data]);
    ws.current.onclose = () => setConnected(false);
    ws.current.onerror = (error) => console.error('WebSocket error:', error);

    return () => ws.current.close();
  }, [clientId]);

  const sendMessage = () => {
    if (input.trim() && connected) {
      ws.current.send(input);
      setMessages((prev) => [...prev, `You (${clientId}): ${input}`]);
      setInput('');
    }
  };

  return (
    <div
      className="App"
      style={{
        maxWidth: '500px',
        margin: '20px auto',
        fontFamily: 'Arial, sans-serif',
        display: 'flex',
        flexDirection: 'column',
        height: '90vh',
        border: '1px solid #ccc',
        borderRadius: '10px',
        overflow: 'hidden',
        boxShadow: '0 4px 8px rgba(0,0,0,0.1)',
      }}
    >
      <header
        style={{
          padding: '15px',
          backgroundColor: '#0084FF',
          color: 'white',
          textAlign: 'center',
          fontWeight: 'bold',
          fontSize: '18px',
        }}
      >
        Messenger Chat
      </header>

      <div style={{ padding: '10px', backgroundColor: '#f0f0f0' }}>
        <label>
          Client ID:{' '}
          <input
            type="text"
            value={clientId}
            onChange={(e) => setClientId(e.target.value)}
            style={{ width: '50px', padding: '3px' }}
          />
        </label>
      </div>

      <div
        className="chat-box"
        style={{
          flex: 1,
          padding: '10px',
          display: 'flex',
          flexDirection: 'column',
          overflowY: 'auto',
          backgroundColor: '#e5ddd5',
        }}
      >
        {messages.map((msg, index) => {
          const isYou = msg.startsWith(`You (${clientId})`);
          return (
            <div
              key={index}
              style={{
                alignSelf: isYou ? 'flex-end' : 'flex-start',
                backgroundColor: isYou ? '#DCF8C6' : '#fff',
                color: '#000',
                padding: '8px 12px',
                borderRadius: '20px',
                marginBottom: '5px',
                maxWidth: '70%',
                wordWrap: 'break-word',
                boxShadow: '0 1px 2px rgba(0,0,0,0.1)',
              }}
            >
              {msg}
            </div>
          );
        })}
        <div ref={chatEndRef} />
      </div>

      <div
        style={{
          display: 'flex',
          padding: '10px',
          borderTop: '1px solid #ccc',
          backgroundColor: '#f0f0f0',
        }}
      >
        <input
          type="text"
          value={input}
          onChange={(e) => setInput(e.target.value)}
          onKeyDown={(e) => e.key === 'Enter' && sendMessage()}
          placeholder="Type a message..."
          style={{
            flex: 1,
            padding: '10px',
            borderRadius: '20px',
            border: '1px solid #ccc',
            outline: 'none',
          }}
        />
        <button
          onClick={sendMessage}
          style={{
            marginLeft: '10px',
            padding: '10px 20px',
            borderRadius: '20px',
            border: 'none',
            backgroundColor: '#0084FF',
            color: 'white',
            cursor: 'pointer',
            fontWeight: 'bold',
          }}
        >
          Send
        </button>
      </div>
    </div>
  );
}

export default App;
