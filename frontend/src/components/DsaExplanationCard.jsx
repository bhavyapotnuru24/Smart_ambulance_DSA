import React, { useState } from 'react';
import { Cpu, ChevronDown, ChevronUp, Code2 } from 'lucide-react';

export default function DsaExplanationCard({ dsaData }) {
  const [expanded, setExpanded] = useState(true);

  if (!dsaData) return null;

  return (
    <div className="dsa-card">
      <div 
        style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', cursor: 'pointer' }}
        onClick={() => setExpanded(!expanded)}
      >
        <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem', fontSize: '1.05rem', fontWeight: '700', color: '#38bdf8' }}>
          <Cpu size={20} />
          <span>DSA-2 Execution Breakdown (Review 3 Demonstration)</span>
        </div>
        <button style={{ background: 'transparent', border: 'none', color: '#94a3b8', cursor: 'pointer' }}>
          {expanded ? <ChevronUp size={20} /> : <ChevronDown size={20} />}
        </button>
      </div>

      {expanded && (
        <div style={{ marginTop: '1rem', borderTop: '1px border #1e293b', paddingTop: '1rem' }}>
          <div className="grid-2">
            <div className="dsa-item">
              <div className="dsa-title">A. Road Network Graph</div>
              <div style={{ color: '#cbd5e1' }}>{dsaData.A_Graph_Representation}</div>
            </div>

            <div className="dsa-item">
              <div className="dsa-title">B. Dijkstra's Algorithm</div>
              <div style={{ color: '#cbd5e1' }}>{dsaData.B_Dijkstra_Algorithm}</div>
            </div>

            <div className="dsa-item">
              <div className="dsa-title">C. Priority Queue (heapq)</div>
              <div style={{ color: '#cbd5e1' }}>{dsaData.C_Priority_Queue}</div>
            </div>

            <div className="dsa-item">
              <div className="dsa-title">D. Dinic's Max Flow</div>
              <div style={{ color: '#cbd5e1' }}>{dsaData.D_Dinic_Max_Flow}</div>
            </div>

            <div className="dsa-item">
              <div className="dsa-title">E. Bipartite Matching</div>
              <div style={{ color: '#cbd5e1' }}>{dsaData.E_Bipartite_Matching}</div>
            </div>

            <div className="dsa-item">
              <div className="dsa-title">F. KMP String Matching</div>
              <div style={{ color: '#cbd5e1' }}>{dsaData.F_KMP_String_Matching}</div>
            </div>
          </div>

          <div style={{ marginTop: '0.75rem', padding: '0.5rem', background: 'rgba(56, 189, 248, 0.1)', borderRadius: '6px', fontSize: '0.8rem', color: '#7dd3fc', display: 'flex', alignItems: 'center', gap: '0.4rem' }}>
            <Code2 size={16} />
            <span>All DSA algorithms are natively implemented in Python in the backend (<code style={{ color: '#38bdf8' }}>backend/app/dsa/</code>).</span>
          </div>
        </div>
      )}
    </div>
  );
}
