import client from '../../../shared/api/client';
export const authApi = { login: (data) => client.post('token/', data), register: (data) => client.post('users/register/', data), me: () => client.get('users/me/') };
