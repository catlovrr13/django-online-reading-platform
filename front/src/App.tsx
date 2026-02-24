import { RouterProvider } from 'react-router'
import router from '@/routes/router'
import { Toaster } from './components/ui/sonner'
import { QueryClientProvider } from '@tanstack/react-query'
import { queryClient } from './lib/queryClient'
import { Provider } from 'react-redux'
import { CookiesProvider } from 'react-cookie'
import { store } from '@/hooks/redux/store'
import { ThemeProvider } from './components/theme-provider'
import { AuthRestore } from './components/AuthRestore'

function App() {


  return (
    <ThemeProvider defaultTheme="light" storageKey="ui-theme">
      <CookiesProvider>
        <Provider store={store}>
          <QueryClientProvider client={queryClient}>
            <AuthRestore>
              <RouterProvider router={router} />
              <Toaster />
            </AuthRestore>
          </QueryClientProvider>
        </Provider>
      </CookiesProvider>
    </ThemeProvider>
  )
}

export default App
