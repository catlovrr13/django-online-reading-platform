import { Button } from '@/components/ui/button'
import { Input } from '@/components/ui/input'
import { Label } from '@/components/ui/label'
import { Header2 } from '@/components/custom-components/headers'

interface RegisterFormProps {
    onSwitchToLogin: () => void
}

function RegisterForm({ onSwitchToLogin }: RegisterFormProps) {
    const handleSubmit = (e: React.FormEvent) => {
        e.preventDefault()
        // Handle register logic here
        console.log('Register submitted')
    }

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
                        placeholder="Choose a username"
                        required
                    />
                </div>
                
                <div className="flex flex-col gap-2">
                    <Label htmlFor="register-email">Email</Label>
                    <Input 
                        id="register-email" 
                        type="email" 
                        placeholder="your@email.com"
                        required
                    />
                </div>
                
                <div className="flex flex-col gap-2">
                    <Label htmlFor="register-password">Password</Label>
                    <Input 
                        id="register-password" 
                        type="password" 
                        placeholder="Create a strong password"
                        required
                    />
                </div>
                
                <div className="flex flex-col gap-2">
                    <Label htmlFor="confirm-password">Confirm Password</Label>
                    <Input 
                        id="confirm-password" 
                        type="password" 
                        placeholder="Confirm your password"
                        required
                    />
                </div>
                
                <Button type="submit" className="w-full mt-2">
                    Create Account
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
