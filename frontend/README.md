# Sentinel Frontend

A performant, production-ready React/Next.js frontend for the Sentinel AI system.

## Features

**High Performance** - Next.js 14, optimized rendering, lazy loading
**Beautiful UI** - Tailwind CSS, responsive design, dark mode ready
**Real-time Metrics** - Session tracking, correction rates, confidence trends
**Type-Safe** - Full TypeScript support
**Persistent State** - Zustand with localStorage
**Production Ready** - Error handling, loading states, accessibility

## Quick Start

### Prerequisites
- Node.js 18+ and npm/yarn
- Backend running on `http://localhost:8000`

### Installation

```bash
cd frontend
npm install
```

### Configuration

```bash
cp .env.example .env.local
# Edit .env.local if backend is on different URL
```

### Development

```bash
npm run dev
```

Open [http://localhost:3000](http://localhost:3000) in your browser.

### Build for Production

```bash
npm run build
npm start
```

## Architecture

### Directory Structure

```
src/
  app/              Next.js app router pages
  components/       Reusable React components
  config/           Configuration (API, constants)
  hooks/            Custom React hooks
  store/            Zustand state management
  utils/            Utility functions
  styles/           Global CSS
```

### Key Components

- **ChatContainer** - Main chat interface layout
- **ChatMessage** - Individual message with confidence badge
- **ChatInput** - Textarea with auto-resize and keyboard shortcuts
- **ConfidenceBadge** - Visual confidence indicator (confident/cautious/guessing)
- **SessionMetrics** - Real-time session statistics

### State Management

Using Zustand with middleware:
- `persist` - Saves chat history to localStorage
- `devtools` - Redux DevTools integration

### API Integration

```typescript
// Configured in src/config/api.ts
apiClient.post('/chat')            // Send message
apiClient.post('/correct')         // Record correction
apiClient.get('/session/{id}/summary')  // Get metrics
```

## Performance Optimizations

1. **Code Splitting** - Next.js automatic route-based splitting
2. **Image Optimization** - Next.js Image component (future)
3. **Font Optimization** - System fonts, no external loads
4. **CSS** - Tailwind purging, minimal bundle
5. **State** - Zustand minimal runtime
6. **API** - Axios with timeout and interceptors

### Web Vitals

- LCP (Largest Contentful Paint) < 2.5s
- FID (First Input Delay) < 100ms
- CLS (Cumulative Layout Shift) < 0.1

## Features

### Chat Interface

- Real-time message display with streaming support
- Auto-scrolling to latest message
- Markdown-aware message rendering
- Keyboard shortcuts (Shift+Enter for new line)

### Confidence Display

- Color-coded badges (green/amber/red)
- Confidence score as percentage
- Expandable reasoning explanation
- Visual distinction from user messages

### Learning Signals

- "This response is wrong" button on assistant messages
- Inline correction modal
- Automatic session tracking
- Real-time metric updates

### Session Management

- Automatic session ID generation
- LocalStorage persistence
- Session history across browser sessions
- Clear chat functionality

## Keyboard Shortcuts

| Shortcut | Action |
|----------|--------|
| Enter | Send message |
| Shift + Enter | New line |
| Escape | Clear input |

## Testing

```bash
npm run test
npm run test:watch
```

## Deployment

### Vercel (Recommended)

```bash
npm install -g vercel
vercel
```

### Docker

```dockerfile
FROM node:18-alpine AS builder
WORKDIR /app
COPY package*.json ./
RUN npm ci
COPY . .
RUN npm run build

FROM node:18-alpine
WORKDIR /app
COPY --from=builder /app/.next ./.next
COPY --from=builder /app/package*.json ./
RUN npm ci --only=production
EXPOSE 3000
CMD ["npm", "start"]
```

### Environment Variables

```
NEXT_PUBLIC_API_URL=https://api.example.com
```

## Browser Support

- Chrome/Edge 90+
- Firefox 88+
- Safari 14+
- Mobile browsers (iOS Safari, Chrome Mobile)

## Troubleshooting

### API Connection Errors

1. Ensure backend is running on configured URL
2. Check CORS headers from backend
3. Verify `NEXT_PUBLIC_API_URL` in `.env.local`

### State Not Persisting

- Check browser's localStorage is enabled
- Clear localStorage if corrupted: `localStorage.clear()`

### Performance Issues

- Check Network tab in DevTools for slow requests
- Profile with React DevTools
- Check for console errors

## License

MIT
