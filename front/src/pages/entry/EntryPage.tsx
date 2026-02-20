// components
import {
    Card,
    CardContent,
} from '@/components/ui/card'
import { Separator } from "@/components/ui/separator"
import { ThemeToggle } from '@/components/theme-toggle'
import { useTheme } from '@/components/theme-provider'
import { Header2 } from '@/components/custom-components/headers'
import { Button } from '@/components/ui/button'
import LoginForm from './LoginForm'
import RegisterForm from './RegisterForm'

// media
import regdark from '@/assets/media/regdark.svg'
import reglight from '@/assets/media/reglight.svg'

// function
import { useState } from 'react'
import { useNavigate } from 'react-router'

// types
type ViewMode = 'initial' | 'login' | 'register'

function Entry() {
    // theme settings
    const { theme } = useTheme()
    const currentLogo = theme === 'dark' ? reglight : regdark
    
    // view mode state
    const [viewMode, setViewMode] = useState<ViewMode>('initial')

    const nav = useNavigate()
    const guestNav: any = () => {
        nav("/dashboard")
    }

    const renderContent = () => {
        switch (viewMode) {
            case 'login':
                return <LoginForm onSwitchToRegister={() => setViewMode('register')} />
            case 'register':
                return <RegisterForm onSwitchToLogin={() => setViewMode('login')} />
            default:
                return (
                    <>
                        <div className="w-full flex flex-col justify-center items-center p-5">
                            <img 
                                src={currentLogo} 
                                alt='theonyxpub.' 
                                className="h-25 w-33 object-cover mb-6"/>
                            <div className='w-full flex flex-col justify-center items-center p-5 gap-5'>
                                <Button 
                                    type='button' 
                                    className='w-25'
                                    onClick={() => setViewMode('login')}
                                >
                                    Log in
                                </Button>
                                <Button 
                                    type='button' 
                                    variant='link' 
                                    className='opacity-35 text-1xs'
                                    onClick={guestNav}
                                >
                                    Continue as guest
                                </Button>
                            </div>
                        </div>
                        <Separator orientation="vertical" className="hidden sm:block h-24"/>
                        <Separator orientation="horizontal" className="block sm:hidden w-full"/>
                        <div className="w-full flex flex-col justify-end-safe content-start p-5 gap-2">
                            <Header2 text={"Enter the Onyx"}/>
                            <h2 className='font-medium'>This is where stories cut deeper. Create your account to unlock <i>The Onyx Pub's</i> digital shelves—bold books, dark ink, and an online reader built for those who don't just read, but consume every page. Sign up and cross the threshold.
                            </h2>
                        </div>
                    </>
                )
        }
    }

    return (
        <div className="w-full max-w-4xl px-4 sm:px-6 lg:px-8">
            <div className="absolute top-4 right-4">
                <ThemeToggle />
            </div>
            <Card className="w-full">
                <CardContent className="flex flex-col sm:flex-row h-full items-center gap-4 justify-center p-6">
                    {/* {viewMode !== 'initial' && (
                        <>
                            <div className="w-full flex flex-col justify-center items-center p-5">
                                <img 
                                    src={currentLogo} 
                                    alt='theonyxpub.' 
                                    className="h-25 w-33 object-cover mb-6"
                                />
                                <Button 
                                    type='button' 
                                    variant='outline' 
                                    className='mt-4'
                                    onClick={() => setViewMode('initial')}
                                >
                                    ← Back
                                </Button>
                            </div>
                            <Separator orientation="vertical" className="hidden sm:block h-96"/>
                            <Separator orientation="horizontal" className="block sm:hidden w-full"/>
                        </>
                    )} */}
                    {viewMode === 'initial' ? (
                        renderContent()
                    ) : (
                        <div className="w-full flex flex-col justify-center p-5 gap-1">
                            {renderContent()}
                            <Button 
                                    type='button' 
                                    variant='link' 
                                    className='opacity-35 font-light'
                                    onClick={guestNav}
                                >
                                    Continue as guest
                                </Button>
                        </div>
                        
                    )}
                </CardContent>
            </Card>
        </div>
    )
}

export default Entry
