# 🎨 React Embeddable Widget

A beautiful, customizable React widget for embedding the Mental Coach AI chatbot into any website.

## ✨ Features

- 🎨 Beautiful, modern UI
- 📱 Fully responsive (mobile-friendly)
- 🎯 Customizable colors and position
- 💬 Real-time streaming responses
- 💾 Conversation history support
- ♿ Accessible (ARIA labels, keyboard navigation)
- 🚀 Easy to integrate
- 🎭 Multiple position options

## 📦 Installation

### Option 1: NPM Package (Recommended)

```bash
npm install mental-coach-widget
```

### Option 2: Build from Source

```bash
cd integrations/react_widget
npm install
npm run build
```

The built files will be in the `dist/` directory.

## 🚀 Quick Start

### Basic Usage

```jsx
import React from 'react';
import MentalCoachWidget from 'mental-coach-widget';

function App() {
  return (
    <div>
      <h1>My Website</h1>
      <MentalCoachWidget 
        apiUrl="https://your-api.vercel.app"
        apiKey="optional-api-key"
      />
    </div>
  );
}
```

### HTML Integration (No Build Step)

If you don't use React, you can include the pre-built widget:

```html
<!DOCTYPE html>
<html>
<head>
  <title>My Website</title>
</head>
<body>
  <h1>Welcome to My Site</h1>
  
  <!-- Include React and ReactDOM -->
  <script crossorigin src="https://unpkg.com/react@18/umd/react.production.min.js"></script>
  <script crossorigin src="https://unpkg.com/react-dom@18/umd/react-dom.production.min.js"></script>
  
  <!-- Include the widget -->
  <script src="https://your-cdn.com/mental-coach-widget.js"></script>
  
  <!-- Initialize widget -->
  <script>
    ReactDOM.render(
      React.createElement(MentalCoachWidget, {
        apiUrl: 'https://your-api.vercel.app',
        apiKey: 'optional-key'
      }),
      document.getElementById('chatbot-widget')
    );
  </script>
  
  <div id="chatbot-widget"></div>
</body>
</html>
```

## ⚙️ Configuration Options

| Prop | Type | Default | Description |
|------|------|---------|-------------|
| `apiUrl` | string | `'http://localhost:8000'` | Your Mental Coach AI API URL |
| `apiKey` | string | `null` | Optional API key for authentication |
| `primaryColor` | string | `'#6366f1'` | Primary color for the widget (header, buttons) |
| `position` | string | `'bottom-right'` | Widget position: `'bottom-right'`, `'bottom-left'`, `'top-right'`, `'top-left'` |

### Example with Customization

```jsx
<MentalCoachWidget 
  apiUrl="https://your-api.vercel.app"
  apiKey="your-api-key"
  primaryColor="#ff6b6b"
  position="bottom-left"
/>
```

## 🎨 Styling

The widget comes with built-in styles, but you can customize it:

### Custom Colors

```jsx
<MentalCoachWidget 
  primaryColor="#your-color"
/>
```

### Custom CSS (Advanced)

You can override CSS classes:
- `.mental-coach-widget` - Main container
- `.widget-container` - Chat window
- `.widget-header` - Header section
- `.widget-messages` - Messages area
- `.widget-input-container` - Input area

## 📱 Responsive Design

The widget automatically adapts to mobile devices:
- On screens smaller than 480px, it becomes fullscreen
- Touch-friendly buttons and inputs
- Optimized for mobile interactions

## 🔒 Security

- API keys are sent securely via HTTPS
- No data is stored locally (except conversation ID)
- All API calls use proper authentication headers

## 🐛 Troubleshooting

### Widget not appearing

- Check that React and ReactDOM are loaded
- Verify the component is rendered
- Check browser console for errors

### API connection errors

- Verify `apiUrl` is correct
- Test API directly: `curl https://your-api.com/api/health`
- Check CORS settings on your API
- Verify API key if using authentication

### Styling issues

- Ensure CSS is loaded
- Check for conflicting styles
- Verify z-index (default: 10000)

## 📚 Examples

### Next.js

```jsx
// pages/_app.js or app/layout.js
import MentalCoachWidget from 'mental-coach-widget';

export default function App({ Component, pageProps }) {
  return (
    <>
      <Component {...pageProps} />
      <MentalCoachWidget 
        apiUrl={process.env.NEXT_PUBLIC_API_URL}
      />
    </>
  );
}
```

### Create React App

```jsx
// src/App.js
import MentalCoachWidget from 'mental-coach-widget';

function App() {
  return (
    <div className="App">
      {/* Your app content */}
      <MentalCoachWidget 
        apiUrl={process.env.REACT_APP_API_URL}
      />
    </div>
  );
}
```

### WordPress

1. Add to your theme's `footer.php`:
```php
<div id="chatbot-widget"></div>
<script>
  // Include React and widget scripts
  // Initialize widget
</script>
```

### Shopify

Add to your theme's `theme.liquid`:
```liquid
<div id="chatbot-widget"></div>
<script>
  // Include and initialize widget
</script>
```

## 🚀 Deployment

### Build for Production

```bash
npm run build
```

### CDN Deployment

1. Build the widget
2. Upload to your CDN
3. Include the script in your HTML

### Self-Hosted

1. Build the widget
2. Copy `dist/` files to your server
3. Include in your HTML/React app

## 📊 Performance

- Lightweight: ~50KB gzipped
- Fast initial load
- Lazy rendering (only renders when opened)
- Efficient re-renders

## 🔄 Updates

To update the widget:
1. Pull latest changes
2. Rebuild: `npm run build`
3. Deploy updated files

## 📝 License

MIT License - feel free to use in your projects!

## 🤝 Support

For issues or questions:
- Check the [Integration Guide](../../INTEGRATION_GUIDE.md)
- Review API documentation
- Check browser console for errors

---

**Happy Embedding! 🎉**
