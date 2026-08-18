import client from '../../../shared/api/client';

const multipart = (data) => {
  const form = new FormData();
  Object.entries(data).forEach(([key, value]) => {
    if (value !== undefined && value !== null && value !== '') form.append(key, value);
  });
  return form;
};

export const profileApi = {
  get: (username) => client.get(`users/${username}/`),
  posts: (id) => client.get(`posts/user/${id}/`),
  follow: (id) => client.post('interactions/', { following: id }),
  unfollow: (id) => client.delete(`interactions/${id}/`),
  updateMe: (data) => client.patch('users/me/', multipart(data), { headers: { 'Content-Type': 'multipart/form-data' } }),
};
