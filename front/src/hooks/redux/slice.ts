import { createSlice } from '@reduxjs/toolkit'

interface User {
    username: string
    token: string
    refresh: string
    first_name?: string
    last_name?: string
    email?: string
    subscription_type?: string
}

const loadUserFromStorage = (): User | null => {
    try {
        const userStr = localStorage.getItem('user')
        if (userStr) {
            return JSON.parse(userStr)
        }
    } catch (error) {
        console.error('Failed to load user from localStorage:', error)
    }
    return null
}

const initialState: { user: User | null } = {
    user: loadUserFromStorage()
}

const authSlice = createSlice({
    name: 'auth',
    initialState,
    reducers: {
        setUser: (state, action: { payload: User }) => {
            state.user = action.payload
            localStorage.setItem('user', JSON.stringify(action.payload))
        },
        reset: (state) => {
            state.user = null
            localStorage.removeItem('user')
        }
    }
})

export const { setUser, reset } = authSlice.actions

export default authSlice.reducer