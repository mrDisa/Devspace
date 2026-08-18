import { useCallback, useEffect, useState } from 'react';
import { communitiesApi } from '../api/communitiesApi';
import { apiMessage } from '../../../shared/lib/format';

export function useCommunities({ query, sort }) { const [state, setState] = useState({ items: [], loading: true, error: '' }); const load = useCallback(async (signal) => { setState((old) => ({ ...old, loading: true, error: '' })); try { const { data } = await communitiesApi.list({ q: query, sort }, signal); setState({ items: data.results || data, loading: false, error: '' }); } catch (e) { if (e.code !== 'ERR_CANCELED') setState({ items: [], loading: false, error: apiMessage(e) }); } }, [query, sort]); useEffect(() => { const controller = new AbortController(); const timer = setTimeout(() => load(controller.signal), query ? 350 : 0); return () => { controller.abort(); clearTimeout(timer); }; }, [load, query]); return { ...state, reload: load }; }
