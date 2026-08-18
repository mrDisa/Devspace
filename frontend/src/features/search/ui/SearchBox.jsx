import { useEffect, useRef, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { FileText, Loader2, Search } from 'lucide-react';
import { searchApi } from '../api/searchApi';
import { Avatar } from '../../../shared/ui';
import { routes } from '../../../shared/config/routes';

const MIN_LENGTH = 2;
const EMPTY = { users: [], posts: [], communities: [], loading: false };

export function SearchBox() {
  const [query, setQuery] = useState('');
  const [open, setOpen] = useState(false);
  const [state, setState] = useState(EMPTY);
  const navigate = useNavigate();
  const rootRef = useRef(null);

  useEffect(() => {
    const trimmed = query.trim();
    if (trimmed.length < MIN_LENGTH) { setState(EMPTY); return; }
    const controller = new AbortController();
    const timer = setTimeout(() => {
      setState((s) => ({ ...s, loading: true }));
      searchApi.search(trimmed, controller.signal)
        .then(({ data }) => setState({ users: data.users || [], posts: data.posts || [], communities: data.communities || [], loading: false }))
        .catch((e) => { if (e.code !== 'ERR_CANCELED') setState({ ...EMPTY }); });
    }, 300);
    return () => { controller.abort(); clearTimeout(timer); };
  }, [query]);

  useEffect(() => {
    const onClick = (e) => { if (rootRef.current && !rootRef.current.contains(e.target)) setOpen(false); };
    document.addEventListener('mousedown', onClick);
    return () => document.removeEventListener('mousedown', onClick);
  }, []);

  const trimmed = query.trim();
  const hasResults = state.users.length || state.posts.length || state.communities.length;

  const goToFullResults = () => {
    if (!trimmed) return;
    navigate(`${routes.feed}?q=${encodeURIComponent(trimmed)}`);
    setOpen(false);
  };
  const goTo = (path) => { navigate(path); setOpen(false); setQuery(''); };

  return (
    <div className="topbar-search" ref={rootRef}>
      <label className="search">
        <Search size={17}/>
        <input
          value={query}
          placeholder="Поиск по людям, постам и сообществам"
          onChange={(e) => { setQuery(e.target.value); setOpen(true); }}
          onFocus={() => query && setOpen(true)}
          onKeyDown={(e) => {
            if (e.key === 'Enter') goToFullResults();
            if (e.key === 'Escape') setOpen(false);
          }}
        />
        {state.loading && <Loader2 size={15} className="search__spinner"/>}
      </label>
      {open && trimmed.length >= MIN_LENGTH && (
        <div className="search__dropdown" role="listbox">
          {!state.loading && !hasResults && <p className="search__hint">Ничего не найдено по «{trimmed}»</p>}

          {state.users.length > 0 && (
            <div className="search__group">
              <span className="search__group-title">Люди</span>
              {state.users.map((u) => (
                <button key={`u-${u.id}`} type="button" className="search__row" onClick={() => goTo(routes.profile(u.username))}>
                  <Avatar user={u} size="sm"/>
                  <span><strong>{u.first_name || u.username}</strong><small>@{u.username}</small></span>
                </button>
              ))}
            </div>
          )}

          {state.communities.length > 0 && (
            <div className="search__group">
              <span className="search__group-title">Сообщества</span>
              {state.communities.map((c) => (
                <button key={`c-${c.id}`} type="button" className="search__row" onClick={() => goTo(routes.community(c.slug))}>
                  <Avatar user={{ avatar: c.avatar, username: c.name }} size="sm"/>
                  <span><strong>{c.name}</strong><small>/c/{c.slug}</small></span>
                </button>
              ))}
            </div>
          )}

          {state.posts.length > 0 && (
            <div className="search__group">
              <span className="search__group-title">Публикации</span>
              {state.posts.map((p) => (
                <button key={`p-${p.id}`} type="button" className="search__row" onClick={() => goTo(routes.profile(p.author?.username))}>
                  <span className="search__row-icon"><FileText size={16}/></span>
                  <span><strong>{p.title}</strong><small>{(p.content || '').slice(0, 64)}</small></span>
                </button>
              ))}
            </div>
          )}

          {trimmed.length >= MIN_LENGTH && (
            <button type="button" className="search__all" onClick={goToFullResults}>
              Показать все результаты по «{trimmed}»
            </button>
          )}
        </div>
      )}
    </div>
  );
}
