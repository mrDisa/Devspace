import { useCallback, useEffect, useState } from 'react';
import { useNavigate, useParams } from 'react-router-dom';
import { Calendar, FileText, Lock, Settings, Tag, Users } from 'lucide-react';
import { Avatar, Badge, Button, Card, EmptyState, ErrorState, Skeleton } from '../shared/ui';
import { communitiesApi } from '../features/communities/api/communitiesApi';
import { apiMessage, formatDate } from '../shared/lib/format';
import { PostCard } from '../entities/post/PostCard';
import { routes } from '../shared/config/routes';

const ROLE_LABEL = { owner: 'Владелец', admin: 'Администратор', moderator: 'Модератор', member: 'Участник' };

export function CommunityPage() {
  const { slug } = useParams();
  const navigate = useNavigate();
  const [state, setState] = useState({ community: null, posts: [], members: [], loading: true, error: '' });

  const load = useCallback(async () => {
    setState((s) => ({ ...s, loading: true, error: '' }));
    try {
      const [{ data: community }, { data: rawPosts }, { data: rawMembers }] = await Promise.all([
        communitiesApi.get(slug),
        communitiesApi.posts(slug),
        communitiesApi.members(slug),
      ]);
      setState({ community, posts: rawPosts.results || rawPosts, members: rawMembers.results || rawMembers, loading: false, error: '' });
    } catch (e) {
      setState({ community: null, posts: [], members: [], loading: false, error: apiMessage(e) });
    }
  }, [slug]);
  useEffect(() => { load(); }, [load]);

  if (state.loading) return <div className="community-layout"><div><Skeleton className="community-hero-skeleton"/><Skeleton className="line"/><Skeleton className="line"/></div><Skeleton className="community-aside-skeleton"/></div>;
  if (state.error) return <ErrorState error={state.error} onRetry={load}/>;

  const c = state.community;
  const manager = ['owner', 'admin', 'moderator'].includes(c.current_role);
  const membership = async () => { if (c.is_joined) await communitiesApi.leave(slug); else await communitiesApi.join(slug); load(); };

  return (
    <>
      <section className="community-hero">
        {c.banner ? <img className="community-hero__banner" src={c.banner} alt=""/> : <div className="community-hero__banner community-hero__banner--placeholder"/>}
        <div className="community-hero__content">
          <Avatar user={{ avatar: c.avatar, username: c.name }} size="xl"/>
          <div className="community-hero__info">
            <p className="eyebrow">СООБЩЕСТВО</p>
            <h1>{c.name}</h1>
            <p>{c.description || 'У сообщества пока нет описания.'}</p>
            <div className="community-hero__stats">
              <span><Users size={16}/>{c.member_count ?? 0} участников</span>
              <span><FileText size={16}/>{c.post_count ?? 0} постов</span>
              {c.current_role && <Badge tone={c.current_role}>{ROLE_LABEL[c.current_role] || c.current_role}</Badge>}
              {c.is_private && <Badge tone="neutral"><Lock size={11}/> приватное</Badge>}
            </div>
          </div>
          <div className="community-hero__actions">
            {manager && <Button variant="secondary" onClick={() => navigate(routes.communityManage(slug))}><Settings size={16}/> Управление</Button>}
            <Button variant={c.is_joined ? 'secondary' : 'primary'} onClick={membership}>{c.is_joined ? 'Покинуть' : 'Вступить'}</Button>
          </div>
        </div>
      </section>

      <div className="community-layout">
        <section className="feed-list">
          <header className="section-heading"><h2>Публикации</h2></header>
          {state.posts.length
            ? state.posts.map((post) => <PostCard key={post.id} post={post}/>)
            : <EmptyState title="Публикаций пока нет" description="Когда участники начнут обсуждение, записи появятся здесь."/>}
        </section>

        <aside className="community-aside">
          <Card className="aside-card">
            <h3>О сообществе</h3>
            <ul className="aside-list">
              {c.category && <li><Tag size={15}/> {c.category}</li>}
              <li><Calendar size={15}/> создано {formatDate(c.created_at)}</li>
              <li><Lock size={15}/> {c.is_private ? 'Приватное сообщество' : 'Открытое сообщество'}</li>
            </ul>
            {c.owner && <div className="aside-owner"><span className="aside-list__label">Владелец</span><div className="author"><Avatar user={c.owner} size="sm"/><span><strong>{c.owner.first_name || c.owner.username}</strong><small>@{c.owner.username || ''}</small></span></div></div>}
          </Card>

          <Card className="aside-card">
            <h3>Участники <span className="muted">· {c.member_count ?? 0}</span></h3>
            {state.members.length ? (
              <ul className="member-preview">
                {state.members.slice(0, 6).map((member, i) => (
                  <li key={member.user?.id ?? i}>
                    <Avatar user={member.user} size="sm"/>
                    <span><strong>@{member.user?.username || 'неизвестно'}</strong></span>
                    <Badge tone={member.role}>{ROLE_LABEL[member.role] || member.role}</Badge>
                  </li>
                ))}
              </ul>
            ) : <p className="muted">Пока никто не вступил.</p>}
            {manager && <Button variant="ghost" className="aside-card__link" onClick={() => navigate(routes.communityManage(slug))}>Все участники и роли</Button>}
          </Card>
        </aside>
      </div>
    </>
  );
}