// components
import { Button } from '@/components/ui/button'
import { Input } from '@/components/ui/input'
import { Label } from '@/components/ui/label'
import { Header2 } from '@/components/custom-components/headers'

// function
import { useState, useEffect } from 'react'


interface LoginFormProps {
    onSwitchToRegister: () => void
}

function LoginForm({ onSwitchToRegister }: LoginFormProps) {
    const handleSubmit = (e: React.FormEvent) => {
        e.preventDefault()
        // login logic dito
        console.log('Login submitted')
    }

    const [email, setEmail] = useState<string>("")
    const [password, setPassword] = useState<string>("")
    const [hidden, setHidden] = useState<boolean>(true)

    const reset = () => {
        setEmail("")
        setPassword("")
    }

    useEffect(() => {
    console.log("on state change")
    setHidden(email || password ? false : true)
    }, [email, password])

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
                    <Label htmlFor="email">Email</Label>
                    <Input 
                        id="email" 
                        type="email" 
                        value={email}
                        placeholder="your@email.com"
                        required
                        onChange={e => setEmail(e.target.value)}
                    />
                </div>
                
                <div className="flex flex-col gap-2">
                    <Label htmlFor="password">Password</Label>
                    <Input 
                        id="password" 
                        type="password" 
                        value={password}
                        placeholder="••••••••"
                        required
                        onChange={e => setPassword(e.target.value)}
                    />
                </div>
                
                <Button type="submit" className="w-full mt-2" disabled={!email && !password}>
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
