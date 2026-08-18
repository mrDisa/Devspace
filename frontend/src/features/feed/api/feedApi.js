import client from '../../../shared/api/client';
export const feedApi = { list: () => client.get('feed/'), following: () => client.get('feed/follows/'), create: (data) => client.post('posts/', data), like: (id) => client.post(`posts/${id}/like/`), search: (q) => client.get(`search/?q=${encodeURIComponent(q)}`) };
