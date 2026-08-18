import client from '../../../shared/api/client';

const multipart = (data) => {
  const form = new FormData();
  Object.entries(data).forEach(([key, value]) => { if (value !== undefined && value !== null && value !== '') form.append(key, key === 'stack' ? JSON.stringify(value) : value); });
  return form;
};
export const communitiesApi = {
  list: (params, signal) => client.get('communities/', { params, signal }),
  get: (slug) => client.get(`communities/${slug}/`),
  posts: (slug) => client.get(`communities/${slug}/posts/`),
  members: (slug) => client.get(`communities/${slug}/members/`),
  join: (slug) => client.post(`communities/${slug}/join/`),
  leave: (slug) => client.post(`communities/${slug}/leave/`),
  setRole: (slug, username, role) => client.patch(`communities/${slug}/members/${username}/role/`, { role }),
  kick: (slug, username) => client.post(`communities/${slug}/members/${username}/kick/`),
  create: (data) => client.post('communities/', multipart(data), { headers: { 'Content-Type': 'multipart/form-data' } }),
  update: (slug, data) => client.patch(`communities/${slug}/`, multipart(data), { headers: { 'Content-Type': 'multipart/form-data' } }),
};
