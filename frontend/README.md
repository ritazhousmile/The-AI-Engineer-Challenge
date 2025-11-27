# 🎨 Mental Coach AI Frontend

Welcome to the frontend of your Mental Coach AI application! This is a modern, beautiful Next.js application that connects to your FastAPI backend to provide supportive mental coaching powered by AI.

## ✨ Features

- 💬 **Real-time Chat Interface** - Beautiful, responsive chat UI with smooth animations
- 🎨 **Modern Design** - Glassmorphism effects, gradient colors, and smooth transitions
- 🌓 **Dark Mode Support** - Automatically adapts to your system preferences
- 📱 **Responsive Layout** - Works perfectly on desktop, tablet, and mobile devices
- ⚡ **Fast & Optimized** - Built with Next.js 15 for optimal performance
- 🎯 **Type-Safe** - Written in TypeScript for better development experience

## 🚀 Getting Started

### Prerequisites

- Node.js 18+ installed on your system
- The FastAPI backend running on `http://localhost:8000`
- npm or yarn package manager

### Installation

1. **Navigate to the frontend directory:**
   ```bash
   cd frontend
   ```

2. **Install dependencies:**
   ```bash
   npm install
   ```
   or if you prefer yarn:
   ```bash
   yarn install
   ```

3. **Configure environment (optional):**
   
   If you need to change the backend API URL, copy `.env.example` to `.env.local`:
   ```bash
   cp .env.example .env.local
   ```
   Then edit `.env.local` to set your backend URL.

### Running the Development Server

Start the development server with hot-reload:

```bash
npm run dev
```

or with yarn:

```bash
yarn dev
```

The application will be available at **[http://localhost:3000](http://localhost:3000)** 🎉

### Building for Production

To create an optimized production build:

```bash
npm run build
```

Then start the production server:

```bash
npm run start
```

## 🎯 How to Use

1. **Start the Backend**: Make sure your FastAPI backend is running on port 8000
2. **Start the Frontend**: Run `npm run dev` in the frontend directory
3. **Open Your Browser**: Navigate to `http://localhost:3000`
4. **Start Chatting**: Type your message and click send or press Enter!

## 🎨 Tech Stack

- **[Next.js 15](https://nextjs.org/)** - React framework with App Router
- **[React 18](https://react.dev/)** - UI library
- **[TypeScript](https://www.typescriptlang.org/)** - Type safety
- **[Tailwind CSS](https://tailwindcss.com/)** - Utility-first CSS framework
- **[Axios](https://axios-http.com/)** - HTTP client for API calls

## 🛠️ Project Structure

```
frontend/
├── app/                    # Next.js App Router directory
│   ├── globals.css        # Global styles and Tailwind directives
│   ├── layout.tsx         # Root layout component
│   └── page.tsx           # Main chat interface page
├── public/                # Static assets
├── .env.example           # Environment variables example
├── next.config.js         # Next.js configuration
├── tailwind.config.js     # Tailwind CSS configuration
├── tsconfig.json          # TypeScript configuration
└── package.json           # Dependencies and scripts

```

## 🎨 Customization

### Changing Colors

Edit `tailwind.config.js` to customize the color scheme:

```javascript
theme: {
  extend: {
    colors: {
      primary: {
        // Your custom colors here
      },
    },
  },
}
```

### Modifying Animations

Check out `app/globals.css` for custom animations and effects. Feel free to add your own!

## 🐛 Troubleshooting

### "Failed to get a response" Error

- Make sure the FastAPI backend is running on `http://localhost:8000`
- Check that CORS is properly configured in the backend
- Verify your OPENAI_API_KEY is set in the backend environment

### Port Already in Use

If port 3000 is already in use, Next.js will automatically try the next available port (3001, 3002, etc.)

### Styles Not Loading

Try clearing the Next.js cache:
```bash
rm -rf .next
npm run dev
```

## 🚀 Deploying to Vercel

This application is optimized for deployment on Vercel:

1. Push your code to GitHub
2. Import your repository on [Vercel](https://vercel.com)
3. Vercel will automatically detect Next.js and configure the build settings
4. Add your environment variables in the Vercel dashboard
5. Deploy! 🎉

For the backend deployment, make sure to:
- Deploy your FastAPI backend (Vercel supports Python functions)
- Update the `NEXT_PUBLIC_API_URL` environment variable to point to your deployed backend

## 💡 Tips

- The chat interface includes suggested prompts when you first load the page
- Messages are cleared when you click "Clear Chat"
- The interface automatically scrolls to the latest message
- Dark mode is automatically detected from your system preferences

## 🤝 Contributing

Feel free to enhance this frontend! Some ideas:
- Add message persistence with localStorage
- Implement user authentication
- Add voice input functionality
- Create conversation history
- Add emoji reactions to messages

## 📝 License

This project is part of the AI Engineer Challenge. Feel free to use and modify as needed!

---

**Need help?** Check out the main [project README](../README.md) or reach out to the community!

Built with 💜 by aspiring AI Engineers