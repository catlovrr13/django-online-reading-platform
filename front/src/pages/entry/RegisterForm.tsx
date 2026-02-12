// components
import { Button } from '@/components/ui/button'
import { Input } from '@/components/ui/input'
import { Label } from '@/components/ui/label'
import { Header2 } from '@/components/custom-components/headers'
import { toast } from 'sonner'
import {
    InputGroup,
    InputGroupAddon,
    InputGroupButton,
    InputGroupInput
} from "@/components/ui/input-group"

// media
import { EyeIcon, EyeOffIcon } from 'lucide-react'

// function
import { useState, useEffect } from 'react'


interface RegisterFormProps {
    onSwitchToLogin: () => void
}

function RegisterForm({ onSwitchToLogin }: RegisterFormProps) {
    const handleSubmit = (e: React.FormEvent) => {
        e.preventDefault()
        
        
        console.log('Register submitted')
    }

    const register = (getValue?: string) => {
        // const formData = {
        //     username: username,
        //     password: password,
        //     email: email
        // }

        // if (username && email && password) {
        //     loginMutate.mutate({data: formData})
        // }

        if (password !== confirm) {
            toast.warning("Password does not match", {position: "bottom-center"})
        }
    }

    const [username, setUsername] = useState<string>("")
    const [email, setEmail] = useState<string>("")
    const [password, setPassword] = useState<string>("")
    const [confirm, setConfirm] = useState<string>("")
    const [hidden, setHidden] = useState<boolean>(true)

    const [peek, setPeek] = useState<boolean>(false)
    const [peekCon, setPeekCon] = useState<boolean>(false)

    const reset = () => {
        setEmail("")
        setPassword("")
        setUsername("")
        setConfirm("")
    }

    useEffect(() => {
    setHidden(email || password || username ? false : true)
    }, [email, password, username])

    return (
        <div className="w-full flex flex-col gap-6">
            <div className="flex flex-col gap-2">
                <Header2 text="Enter the Onyx" />
                <p className="text-sm opacity-70">
                    Create your account to unlock The Onyx Pub's digital shelves
                </p>
            </div>
            
            <form onSubmit={handleSubmit} className="flex flex-col gap-4">
                <div className="flex flex-col gap-2">
                    <Label htmlFor="register-username">Username</Label>
                    <Input 
                        id="register-username" 
                        type="text" 
                        value={username}
                        placeholder="Choose a username"
                        required
                        onChange={e => setUsername(e.target.value)}
                    />
                </div>
                
                <div className="flex flex-col gap-2">
                    <Label htmlFor="register-email">Email</Label>
                    <Input 
                        id="register-email" 
                        type="email" 
                        value={email}
                        placeholder="your@email.com"
                        required
                        onChange={e => setEmail(e.target.value)}
                    />
                </div>
                
                <div className="flex flex-col gap-2">
                    <Label htmlFor="register-password">Password</Label>
                    <InputGroup>
                        <InputGroupInput 
                        id='register-password'
                        type={!peek ? 'password' : 'text'}
                        placeholder='Enter a password'
                        value={password} 
                        onChange={e => setPassword(e.target.value)}/>
                        <InputGroupAddon align="inline-end">
                            <InputGroupButton onClick={()=>setPeek(!peek)}>
                                {peek ? <EyeIcon/> : <EyeOffIcon/>}
                            </InputGroupButton>
                        </InputGroupAddon>
                    </InputGroup>
                </div>
                
                <div className="flex flex-col gap-2">
                    <Label htmlFor="confirm-password">Confirm Password</Label>
                    <InputGroup>
                        <InputGroupInput 
                        id='confirm-password'
                        type={!peekCon ? 'password' : 'text'}
                        placeholder='Confirm your password'
                        value={confirm} 
                        onChange={e => setConfirm(e.target.value)}/>
                        <InputGroupAddon align="inline-end">
                            <InputGroupButton onClick={()=>setPeekCon(!peekCon)}>
                                {peekCon ? <EyeIcon/> : <EyeOffIcon/>}
                            </InputGroupButton>
                        </InputGroupAddon>
                    </InputGroup>
                </div>
                
                <Button type="submit" className="w-full mt-2" onClick={()=> register("value")} disabled={!username || !email || !password}>
                    Create Account
                </Button>
                <Button variant="ghost" type='button' className={hidden ? 'hidden' : 'w-full'} onClick={reset}>
                    Reset
                </Button>
                
                <div className="flex items-center justify-center gap-2 text-sm mt-2">
                    <span className="opacity-70">Already have an account?</span>
                    <Button 
                        type="button" 
                        variant="link" 
                        onClick={onSwitchToLogin}
                        className="p-0 h-auto font-semibold"
                    >
                        Log In
                    </Button>
                </div>
            </form>
        </div>
    )
}

export default RegisterForm
