import client from '../../../shared/api/client';
export const notificationsApi = { list: () => client.get('notifications/'), readAll: () => client.patch('notifications/read_all/') };
