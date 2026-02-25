// components
import { Button } from '@/components/ui/button'
import { Input } from '@/components/ui/input'
import { Label } from '@/components/ui/label'
import { Header2 } from '@/components/custom-components/headers'
// import { toast } from 'sonner'
import {
    InputGroup,
    InputGroupAddon,
    InputGroupButton,
    InputGroupInput
} from "@/components/ui/input-group"
import {toast} from 'sonner'

// media
import { EyeIcon, EyeOffIcon } from 'lucide-react'

// function
import { useState, useEffect } from 'react'
import { useDispatch } from 'react-redux';
import { loginUser, getUserProfile } from '@/api/authAPI'
import { useMutation } from '@tanstack/react-query'
import { useCookies } from 'react-cookie'
import { setUser } from '@/hooks/redux/slice'
import { useNavigate } from 'react-router'


interface LoginFormProps {
    onSwitchToRegister: () => void
}

function LoginForm({ onSwitchToRegister }: LoginFormProps) {
    const [_, setCookie] = useCookies()
    const dispatch = useDispatch()
    const nav = useNavigate()

    const loginMutate = useMutation({
        mutationFn: async ({data}: {data: {username: string, password: string} }) => {
            const loginResult = await loginUser(data)
            const profile = await getUserProfile(loginResult.token)
            return { ...loginResult, profile }
        },
        onSuccess: (res) => {
            setCookie("token", res.token,
                {
                    expires: new Date(new Date().setDate(new Date().getDate() + 1))
                }
            )
            dispatch(setUser({
                token: res.token,
                refresh: res.refresh,
                username: res.profile.username,
                first_name: res.profile.first_name,
                last_name: res.profile.last_name,
                email: res.profile.email,
                subscription_type: res.profile.subscription_type
            }))
            nav('/dashboard')
            toast.success('Login successful', {position: 'bottom-center'})
        },
        onError: (err) => {
            toast.error(err.message)
        }
    })

    const handleSubmit = (e: React.FormEvent) => {
        e.preventDefault()
        loginMutate.mutate({ data: { username, password } })
    }

    const [username, setUsername] = useState<string>("")
    const [password, setPassword] = useState<string>("")
    const [hidden, setHidden] = useState<boolean>(true)


    const [peek, setPeek] = useState<boolean>(false)

    const reset = () => {
        setUsername("")
        setPassword("")
    }

    useEffect(() => {
    console.log("on state change")
    setHidden(username || password ? false : true)
    }, [username, password])

    return (
        <div className="w-full flex flex-col gap-6">
            <div className="flex flex-col gap-2">
                <Header2 text="Welcome Back" />
                <p className="text-sm opacity-70">
                    Sign in to continue your journey through The Onyx Pub
                </p>
            </div>
            
            <form onSubmit={handleSubmit} className="flex flex-col gap-4">
                <div className="flex flex-col gap-2">
                    <Label htmlFor="username">Username</Label>
                    <Input
                        id="username"
                        type="text"
                        value={username}
                        placeholder="your_username"
                        required
                        onChange={e => setUsername(e.target.value)}
                    />
                </div>
                
                <div className="flex flex-col gap-2">
                    <Label htmlFor="password">Password</Label>
                    <InputGroup>
                        <InputGroupInput 
                        id='password'
                        type={!peek ? 'password' : 'text'}
                        placeholder='••••••••'
                        value={password} 
                        onChange={e => setPassword(e.target.value)}/>
                        <InputGroupAddon align="inline-end">
                            <InputGroupButton onClick={()=>setPeek(!peek)}>
                                {peek ? <EyeIcon/> : <EyeOffIcon/>}
                            </InputGroupButton>
                        </InputGroupAddon>
                    </InputGroup>
                </div>
                
                <Button type="submit" className="w-full mt-2" disabled={!username && !password}>
                    Log In
                </Button>
                <Button variant="ghost" type='button' className={hidden ? 'hidden' : 'w-full'} onClick={reset}>
                    Reset
                </Button>
                
                <div className="flex flex-col gap-2 items-center mt-2">
                    <Button 
                        type="button" 
                        variant="link" 
                        className="opacity-50 text-xs"
                    >
                        Forgot password?
                    </Button>
                    
                    <div className="flex items-center gap-2 text-sm">
                        <span className="opacity-70 text-1xs">Don't have an account?</span>
                        <Button 
                            type="button" 
                            variant="link" 
                            onClick={onSwitchToRegister}
                            className="p-0 h-auto font-semibold"
                        >
                            Register
                        </Button>
                    </div>
                </div>
            </form>
        </div>
    )
}

export default LoginForm
