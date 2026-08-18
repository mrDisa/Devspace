import { Component } from 'react';
import { Button } from './index';

export class ErrorBoundary extends Component {
  constructor(props) {
    super(props);
    this.state = { error: null };
  }

  static getDerivedStateFromError(error) {
    return { error };
  }

  componentDidCatch(error, info) {
    console.error('Render error caught by boundary:', error, info);
  }

  render() {
    if (this.state.error) {
      return (
        <div className="error-boundary">
          <p className="error-boundary__title">Что-то пошло не так</p>
          <p className="error-boundary__text">Страница не смогла отобразиться. Попробуйте обновить её — если ошибка повторится, дайте нам знать.</p>
          <Button onClick={() => { this.setState({ error: null }); window.location.reload(); }}>Обновить страницу</Button>
        </div>
      );
    }
    return this.props.children;
  }
}