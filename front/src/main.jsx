import { createRoot } from 'react-dom/client'
import './index.css'
import App from './App.jsx'
import Books from './pages/Books.jsx'
import { createBrowserRouter, Outlet } from 'react-router'
import { RouterProvider } from 'react-router'
import Profile from './pages/Profile.jsx'
import MainLayout from './pages/MainLayout.jsx'

const router = createBrowserRouter([
    {
        path: '',
        element: <MainLayout />,
    },
    {
        path: 'profile',
        element: <Profile />,
    },
    {
        path: 'books',
        element: <Books />
    }
])

createRoot(document.getElementById('root')).render(
    <RouterProvider router={router} />
)
