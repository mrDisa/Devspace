import { ChevronLeft } from 'lucide-react';
import { Link } from 'react-router-dom';
import { useAuth } from '../features/auth/model/AuthContext';
import { ProfileEditForm } from '../features/profile/ui/ProfileEditForm';
import { routes } from '../shared/config/routes';

export function ProfileEditPage() {
  const { user, refreshUser } = useAuth();
  if (!user) return null;

  return (
    <>
      <Link className="back-link" to={routes.profile(user.username)}><ChevronLeft size={16}/> К профилю</Link>
      <header className="page-heading">
        <div>
          <p className="eyebrow">НАСТРОЙКИ</p>
          <h1>Редактирование профиля</h1>
          <p>Обновите имя, должность, описание и аватар — эти данные видны всем на платформе.</p>
        </div>
      </header>
      <ProfileEditForm user={user} onSaved={refreshUser}/>
    </>
  );
}
