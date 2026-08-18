import { useState } from 'react';
import { Heart, MessageCircle, MoreHorizontal } from 'lucide-react';
import { Link } from 'react-router-dom';
import { Avatar, Badge, Button, Card } from '../../shared/ui';
import { relativeDate } from '../../shared/lib/format';
import { routes } from '../../shared/config/routes';
import { CommentThread, Rating } from '../../features/interactions/ui/PostInteractions';

export function PostCard({ post, onLike, onRate }) {
  const [commentsOpen, setCommentsOpen] = useState(false); const author = post.author || {};
  return (
    <Card className="post-card">
      <div className="post-card__head">
        <Link className="author" to={routes.profile(author.username)}>
          <Avatar user={author}/>
          <span><strong>{author.first_name || author.username}</strong><small>@{author.username} · {relativeDate(post.created_at)}</small></span>
        </Link>
        <Button variant="ghost" aria-label="Действия с постом"><MoreHorizontal size={18}/></Button>
      </div>
      <Link to={routes.profile(author.username)} className="post-card__body">
        <h2>{post.title}</h2>
        <p>{post.content}</p>
        {post.community && <Badge>community #{post.community}</Badge>}
      </Link>
      <div className="post-card__actions">
        <div className="post-card__reactions">
          <Button variant={post.is_liked ? 'active' : 'ghost'} onClick={() => onLike?.(post)} aria-label="Нравится"><Heart size={17}/> {post.likes_count || 0}</Button>
          <Button variant={commentsOpen ? 'active' : 'ghost'} onClick={() => setCommentsOpen(!commentsOpen)} aria-expanded={commentsOpen}><MessageCircle size={17}/> {post.comments_count || 0}</Button>
        </div>
        <Rating post={post} onChange={(data) => onRate?.(post.id, data)}/>
      </div>
      {commentsOpen && <CommentThread postId={post.id}/>}
    </Card>
  );
}
