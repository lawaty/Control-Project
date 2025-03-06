import React, { useState, useCallback } from 'react';
import ReactFlow, {
  addEdge,
  Background,
  Controls,
  Handle
} from 'reactflow';
import 'reactflow/dist/style.css';

const CustomNode = ({ data }) => {
  return (
    <div className="custom-node">
      <Handle type="target" position="left" style={{ background: '#555' }} />
      <div>{data.label}</div>
      <Handle type="source" position="right" style={{ background: '#555' }} />
    </div>
  );
};

const nodeTypes = { custom: CustomNode };

const SignalFlowGraph = ({ setTransferFunction }) => {
  const [nodes, setNodes] = useState([
    { id: '1', type: 'custom', position: { x: 50, y: 100 }, data: { label: 'Node 1' }, draggable: true },
    { id: '2', type: 'custom', position: { x: 300, y: 100 }, data: { label: 'Node 2' }, draggable: true },
  ]);

  const [edges, setEdges] = useState([
    { id: 'e1-2', source: '1', target: '2', label: 'Gain: 1', animated: true },
  ]);

  const [history, setHistory] = useState([{ nodes, edges }]);
  const [historyIndex, setHistoryIndex] = useState(0);

  const saveToHistory = useCallback((newNodes, newEdges) => {
    const updatedHistory = history.slice(0, historyIndex + 1);
    updatedHistory.push({ nodes: newNodes, edges: newEdges });
    setHistory(updatedHistory);
    setHistoryIndex(updatedHistory.length - 1);
  }, [history, historyIndex]);

  const onConnect = useCallback((connection) => {
    const gain = prompt('Enter gain for this connection:');
    if (gain !== null) {
      const newEdges = addEdge({ ...connection, label: `Gain: ${gain}`, animated: true }, edges);
      setEdges(newEdges);
      saveToHistory(nodes, newEdges);
    }
  }, [edges, nodes, saveToHistory]);

  const onNodeDragStop = (event, node) => {
    const updatedNodes = nodes.map((n) =>
      n.id === node.id ? { ...n, position: node.position } : n
    );
    setNodes(updatedNodes);
    saveToHistory(updatedNodes, edges);
  };

  const addNode = () => {
    const newNodeId = (nodes.length + 1).toString();
    const newNode = {
      id: newNodeId,
      type: 'custom',
      position: { x: Math.random() * 400, y: Math.random() * 400 },
      data: { label: `Node ${newNodeId}` },
      draggable: true
    };
    const newNodes = [...nodes, newNode];
    setNodes(newNodes);
    saveToHistory(newNodes, edges);
  };

  const undo = () => {
    if (historyIndex > 0) {
      const prevState = history[historyIndex - 1];
      setNodes(prevState.nodes);
      setEdges(prevState.edges);
      setHistoryIndex(historyIndex - 1);
    }
  };

  const redo = () => {
    if (historyIndex < history.length - 1) {
      const nextState = history[historyIndex + 1];
      setNodes(nextState.nodes);
      setEdges(nextState.edges);
      setHistoryIndex(historyIndex + 1);
    }
  };

  const calculateTransferFunction = () => {
    setTransferFunction('TF = (Y(s) / X(s)) = Σ(PkΔk) / Δ'); // Placeholder logic
  };

  return (
    <div className="card">
      <h2>Signal Flow Graph</h2>
      <button onClick={addNode}>Add Node</button>
      <button onClick={calculateTransferFunction}>Calculate Transfer Function</button>
      <button onClick={undo} disabled={historyIndex === 0}>Undo</button>
      <button onClick={redo} disabled={historyIndex === history.length - 1}>Redo</button>
      
      <div style={{ height: '500px', border: '1px solid #ccc', marginTop: '20px' }}>
        <ReactFlow
          nodes={nodes}
          edges={edges}
          onConnect={onConnect}
          onNodeDragStop={onNodeDragStop}
          fitView
          nodeTypes={nodeTypes}
        >
          <Background />
          <Controls />
        </ReactFlow>
      </div>
    </div>
  );
};

export default SignalFlowGraph;
