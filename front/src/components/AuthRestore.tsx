import { useEffect } from 'react'
import { useDispatch, useSelector } from 'react-redux'
import { getUserProfile } from '@/api/authAPI'
import { setUser } from '@/hooks/redux/slice'
import type { RootState, AppDispatch } from '@/hooks/redux/store'
import { useCookies } from 'react-cookie'

export function AuthRestore({ children }: { children: React.ReactNode }) {
    const [cookies] = useCookies(['token'])
    const dispatch = useDispatch<AppDispatch>()
    const user = useSelector((state: RootState) => state.auth.user)

    useEffect(() => {
        const restoreAuth = async () => {
            const token = cookies.token
            if (token && user) {
                try {
                    const profile = await getUserProfile(token)
                    dispatch(setUser({
                        token,
                        refresh: user.refresh,
                        username: profile.username,
                        first_name: profile.first_name,
                        last_name: profile.last_name,
                        email: profile.email,
                        subscription_type: profile.subscription_type
                    }))
                } catch (error) {
                    console.error('Failed to restore user session:', error)
                    dispatch(setUser({ 
                        token: '', 
                        refresh: '', 
                        username: '' 
                    }))
                }
            }
        }

        restoreAuth()
    }, [])

    return <>{children}</>
}
