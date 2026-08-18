import { Bell, Home, LogOut, Menu, Moon, Sun, UserRound, UsersRound } from 'lucide-react';
import { Link, NavLink, useNavigate } from 'react-router-dom';
import { useState } from 'react';
import { Avatar, Button } from '../shared/ui';
import { routes } from '../shared/config/routes';
import { useAuth } from '../features/auth/model/AuthContext';
import { useNotifications } from '../features/notifications/model/useNotifications';
import { useTheme } from '../shared/lib/theme.jsx';
import { SearchBox } from '../features/search/ui/SearchBox';

export function AppLayout({ children }) {
  const { user, logout } = useAuth();
  const { unread } = useNotifications();
  const [open, setOpen] = useState(() => (typeof window !== 'undefined' ? window.matchMedia('(min-width: 901px)').matches : true));
  const { dark, toggle } = useTheme();
  const navigate = useNavigate();
  const leave = () => { logout(); navigate(routes.login); };
  const toggleSidebar = () => setOpen((v) => !v);

  const nav = (
    <nav>
      <NavLink to={routes.feed} end><Home size={18}/> Лента</NavLink>
      <NavLink to={routes.communities}><UsersRound size={18}/> Сообщества</NavLink>
      <NavLink to={routes.notifications}><Bell size={18}/> Уведомления {unread > 0 && <b>{unread}</b>}</NavLink>
      <NavLink to={routes.profile(user?.username || '')}><UserRound size={18}/> Профиль</NavLink>
    </nav>
  );

  return (
    <div className="shell">
      <aside className={open ? 'sidebar' : 'sidebar sidebar--closed'}>
        <div className="sidebar__brand"><span className="wordmark">Devspace</span></div>
        {nav}
        <div className="sidebar__bottom">
          <Button variant="ghost" onClick={toggle}>{dark ? <Sun size={18}/> : <Moon size={18}/>} {dark ? 'Светлая тема' : 'Тёмная тема'}</Button>
          <Link className="account" to={routes.profile(user?.username)}><Avatar user={user}/><span><strong>{user?.first_name || user?.username}</strong><small>@{user?.username}</small></span></Link>
          <Button variant="ghost" onClick={leave}><LogOut size={18}/> Выйти</Button>
        </div>
      </aside>
      {open && <button className="backdrop" onClick={() => setOpen(false)} aria-label="Закрыть меню"/>}
      <div className={open ? 'workspace' : 'workspace workspace--full'}>
        <header className="topbar">
          <Button variant="ghost" onClick={toggleSidebar} aria-label={open ? 'Скрыть меню' : 'Показать меню'} aria-expanded={open}><Menu/></Button>
          <SearchBox/>
          <Link to={routes.notifications} className="notification-link" aria-label="Уведомления"><Bell size={19}/>{unread > 0 && <b>{unread}</b>}</Link>
        </header>
        <main className="content">{children}</main>
      </div>
    </div>
  );
}