import { forwardRef } from 'react';
import { initials } from '../lib/format';

export function Button({ variant = 'primary', loading, children, className = '', ...props }) { return <button className={`button button--${variant} ${className}`} disabled={loading || props.disabled} {...props}>{loading ? 'Загрузка…' : children}</button>; }
export const Input = forwardRef(function Input({ label, error, ...props }, ref) { return <label className="field">{label && <span>{label}</span>}<input ref={ref} {...props}/>{error && <small className="field__error">{error}</small>}</label>; });
export function Textarea({ label, ...props }) { return <label className="field">{label && <span>{label}</span>}<textarea {...props}/></label>; }
export function Card({ className = '', children }) { return <section className={`card ${className}`}>{children}</section>; }
const AVATAR_SIZES = { sm: 28, md: 36, lg: 56, xl: 96 };

export function Avatar({ user, size = 'md' }) {
  const px = AVATAR_SIZES[size] || AVATAR_SIZES.md;
  return (
    <span
      className={`avatar avatar--${size}`}
      style={{
        width: px,
        height: px,
        minWidth: px,
        minHeight: px,
        borderRadius: '50%',
        overflow: 'hidden',
        display: 'grid',
        placeItems: 'center',
        flexShrink: 0,
        background: 'var(--surface-soft)',
        color: 'var(--accent)',
        fontWeight: 750,
      }}
    >
      {user?.avatar ? (
        <img
          src={user.avatar}
          alt=""
          style={{ width: '100%', height: '100%', objectFit: 'cover', display: 'block' }}
        />
      ) : (
        initials(user?.username || user?.first_name)
      )}
    </span>
  );
}
export function Badge({ children, tone = 'neutral' }) { return <span className={`badge badge--${tone}`}>{children}</span>; }
export function Tabs({ items, value, onChange }) { return <div className="tabs" role="tablist">{items.map((item) => <button key={item.value} role="tab" aria-selected={value === item.value} className={value === item.value ? 'tabs__item tabs__item--active' : 'tabs__item'} onClick={() => onChange(item.value)}>{item.label}</button>)}</div>; }
export function Skeleton({ className = '' }) { return <span className={`skeleton ${className}`} aria-hidden="true"/>; }
export function EmptyState({ title, description, action }) { return <div className="state state--empty"><h2>{title}</h2><p>{description}</p>{action}</div>; }
export function ErrorState({ error, onRetry }) { return <div className="state state--error" role="alert"><h2>Не удалось загрузить данные</h2><p>{error}</p>{onRetry && <Button variant="secondary" onClick={onRetry}>Повторить</Button>}</div>; }
