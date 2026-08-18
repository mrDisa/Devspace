import client from '../../../shared/api/client';
export const postInteractionsApi = {
  rate: (postId, value) => client.post(`posts/${postId}/rate/`, { value }),
  comments: (postId) => client.get(`posts/${postId}/comments/`),
  createComment: (postId, text) => client.post(`posts/${postId}/comments/`, { post: postId, text }),
  deleteComment: (id) => client.delete(`comments/${id}/`),
  likeComment: (postId, commentId) => client.post(`posts/${postId}/comments/${commentId}/like/`),
};
