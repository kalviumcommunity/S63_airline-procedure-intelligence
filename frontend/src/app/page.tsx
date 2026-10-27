'use client';

import React, { useState } from 'react';

export default function GroundDashboardPage() {
  const [station, setStation] = useState('KORD');
  const [fleet, setFleet] = useState('A321neo');
  const [query, setQuery] = useState('');

  return (
    <main style={{ padding: '24px', maxWidth: '800px', margin: '0 auto' }}>
      <header style={{ marginBottom: '24px', borderBottom: '1px solid #e2e8f0', paddingBottom: '16px' }}>
        <h1 style={{ fontSize: '24px', fontWeight: 800, margin: 0 }}>SkyOps Intelligence</h1>
        <p style={{ color: '#64748b', margin: '4px 0 0' }}>Ground Handling Operational Procedure Intelligence</p>
      </header>

      <section style={{ display: 'flex', gap: '12px', marginBottom: '20px' }}>
        <label>
          Station:
          <select value={station} onChange={(e) => setStation(e.target.value)} style={{ marginLeft: '8px', padding: '6px 10px' }}>
            <option value="KORD">KORD (Chicago O'Hare)</option>
            <option value="KJFK">KJFK (New York JFK)</option>
            <option value="KLAX">KLAX (Los Angeles)</option>
            <option value="KDFW">KDFW (Dallas/Ft. Worth)</option>
          </select>
        </label>
        <label>
          Fleet:
          <select value={fleet} onChange={(e) => setFleet(e.target.value)} style={{ marginLeft: '8px', padding: '6px 10px' }}>
            <option value="A321neo">Airbus A321neo</option>
            <option value="A320-200">Airbus A320-200</option>
            <option value="B737-800">Boeing 737-800</option>
            <option value="B787-9">Boeing 787-9</option>
          </select>
        </label>
      </section>

      <section style={{ marginBottom: '24px' }}>
        <input
          type="text"
          value={query}
          onChange={(e) => setQuery(e.target.value)}
          placeholder="Ask a ground operational procedure question..."
          style={{ width: '100%', padding: '12px', fontSize: '16px', borderRadius: '6px', border: '2px solid #cbd5e1', boxSizing: 'border-box' }}
        />
      </section>

      <div style={{ background: '#f8fafc', border: '1px solid #e2e8f0', borderRadius: '8px', padding: '16px' }}>
        <strong>Current Scope:</strong> Station: {station} | Fleet: {fleet}
      </div>
    </main>
  );
}

