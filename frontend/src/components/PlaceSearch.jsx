import { useState, useRef, useEffect } from 'react';
import { searchPlaces } from '../api.js';

export default function PlaceSearch({ onSelect }) {
  const [query, setQuery] = useState('');
  const [results, setResults] = useState([]);
  const [open, setOpen] = useState(false);
  const [loading, setLoading] = useState(false);
  const timer = useRef(null);
  const ref = useRef(null);

  useEffect(() => {
    function onClickOutside(e) {
      if (ref.current && !ref.current.contains(e.target)) setOpen(false);
    }
    document.addEventListener('mousedown', onClickOutside);
    return () => document.removeEventListener('mousedown', onClickOutside);
  }, []);

  function handleInput(e) {
    const q = e.target.value;
    setQuery(q);
    clearTimeout(timer.current);
    if (q.trim().length < 2) { setResults([]); setOpen(false); return; }
    timer.current = setTimeout(async () => {
      setLoading(true);
      try {
        const data = await searchPlaces(q);
        setResults(data);
        setOpen(data.length > 0);
      } catch {}
      setLoading(false);
    }, 400);
  }

  function handleSelect(item) {
    onSelect({
      name: item.name || item.display_name.split(',')[0],
      address: item.display_name,
      latitude: parseFloat(item.lat),
      longitude: parseFloat(item.lon),
    });
    setQuery('');
    setResults([]);
    setOpen(false);
  }

  return (
    <div className="search-box" ref={ref}>
      <div className="field" style={{ marginBottom: 0 }}>
        <label>Search for a place</label>
        <input
          value={query}
          onChange={handleInput}
          placeholder="e.g. Eiffel Tower, Paris…"
          onFocus={() => results.length > 0 && setOpen(true)}
        />
      </div>
      {loading && <div style={{ fontSize: '0.8rem', color: 'var(--ink-soft)', padding: '6px 4px' }}>Searching…</div>}
      {open && results.length > 0 && (
        <div className="search-results">
          {results.map((item) => (
            <div key={item.place_id} className="search-result-item" onClick={() => handleSelect(item)}>
              <div className="search-result-name">
                📍 {item.name || item.display_name.split(',')[0]}
              </div>
              <div className="search-result-addr">{item.display_name}</div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}