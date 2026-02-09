import { RouterProvider } from 'react-router'
import router from '@/routes/router'
import { Toaster } from './components/ui/sonner'
import { QueryClientProvider } from '@tanstack/react-query'
import { queryClient } from './lib/queryClient'
import { Provider } from 'react-redux'
import { CookiesProvider } from 'react-cookie'
import { store } from '@/hooks/redux/store'

function App() {


  return (
    <CookiesProvider>
      <Provider store={store}>
        <QueryClientProvider client={queryClient}>
          <RouterProvider router={router} />
          <Toaster />
        </QueryClientProvider>
      </Provider>
    </CookiesProvider>
  )
}

export default App
