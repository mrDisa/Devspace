import client from '../../../shared/api/client';

export const searchApi = {
  search: (q, signal) => client.get('search/', { params: { q }, signal }),
};
