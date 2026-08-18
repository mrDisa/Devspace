import { useState } from 'react';
import { Check, ImagePlus } from 'lucide-react';
import { Avatar, Button, Card, Input, Textarea } from '../../../shared/ui';
import { profileApi } from '../api/profileApi';
import { apiMessage } from '../../../shared/lib/format';

export function ProfileEditForm({ user, onSaved }) {
  const [form, setForm] = useState({ first_name: user?.first_name || '', job: user?.job || '', bio: user?.bio || '' });
  const [avatarFile, setAvatarFile] = useState(null);
  const [preview, setPreview] = useState(user?.avatar || '');
  const [busy, setBusy] = useState(false);
  const [error, setError] = useState('');
  const [saved, setSaved] = useState(false);

  const set = (key) => (e) => { setForm({ ...form, [key]: e.target.value }); setSaved(false); };

  const pickAvatar = (e) => {
    const file = e.target.files?.[0];
    if (!file) return;
    setAvatarFile(file);
    setPreview(URL.createObjectURL(file));
    setSaved(false);
  };

  const submit = async (e) => {
    e.preventDefault();
    setBusy(true); setError(''); setSaved(false);
    try {
      const payload = { ...form };
      if (avatarFile) payload.avatar = avatarFile;
      const { data } = await profileApi.updateMe(payload);
      setSaved(true);
      onSaved?.(data);
    } catch (err) {
      setError(apiMessage(err));
    } finally {
      setBusy(false);
    }
  };

  return (
    <Card className="edit-form">
      <form onSubmit={submit}>
        <div className="edit-form__avatar">
          <Avatar user={{ avatar: preview, username: user?.username }} size="xl"/>
          <label className="button button--secondary edit-form__upload">
            <ImagePlus size={16}/> Изменить фото
            <input type="file" accept="image/*" onChange={pickAvatar} hidden/>
          </label>
        </div>
        <Input label="Отображаемое имя" value={form.first_name} onChange={set('first_name')} maxLength="60" placeholder="Как вас называть"/>
        <Input label="Должность / стек" value={form.job} onChange={set('job')} maxLength="60" placeholder="Например, Frontend-разработчик"/>
        <Textarea label="О себе" rows="4" value={form.bio} onChange={set('bio')} maxLength="280" placeholder="Расскажите, чем вы занимаетесь и что вам интересно…"/>
        {error && <p className="form-error" role="alert">{error}</p>}
        <div className="edit-form__footer">
          {saved && <span className="edit-form__saved"><Check size={15}/> Изменения сохранены</span>}
          <Button type="submit" loading={busy}>Сохранить изменения</Button>
        </div>
      </form>
    </Card>
  );
}
