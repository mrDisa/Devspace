export const initials = (name = '?') => name.trim().slice(0, 1).toUpperCase();
export const relativeDate = (value) => {
  const delta = Math.max(0, Date.now() - new Date(value).getTime());
  const minutes = Math.floor(delta / 60000);
  if (minutes < 1) return 'только что';
  if (minutes < 60) return `${minutes} мин`;
  if (minutes < 1440) return `${Math.floor(minutes / 60)} ч`;
  return new Intl.DateTimeFormat('ru-RU', { day: 'numeric', month: 'short' }).format(new Date(value));
};
export const formatDate = (value) => {
  if (!value) return '—';
  const date = new Date(value);
  if (Number.isNaN(date.getTime())) return '—';
  return new Intl.DateTimeFormat('ru-RU', { day: 'numeric', month: 'long', year: 'numeric' }).format(date);
};
export const apiMessage = (error) => {
  const data = error?.response?.data;
  if (typeof data?.detail === 'string') return data.detail;
  if (data && typeof data === 'object') return Object.values(data).flat().join(' ');
  return 'Не удалось выполнить запрос. Проверьте подключение и повторите попытку.';
};
