// components
import {
    Card,
    CardHeader,
    CardTitle,
    CardContent,
    CardDescription,
    CardFooter,
} from '@/components/ui/card'
import { Separator } from "@/components/ui/separator"
import { ThemeToggle } from '@/components/theme-toggle'
import { useTheme } from '@/components/theme-provider'
import { Header1, Header2, Header3 } from '@/components/custom-components/headers'
import { Button } from '@/components/ui/button'

// media
import regdark from '@/assets/media/regdark.svg'
import reglight from '@/assets/media/reglight.svg'

// function

function Entry() {
    // theme settings
    const { theme } = useTheme()
    const currentLogo = theme === 'dark' ? reglight : regdark
    
    return (
        <div className="w-full max-w-4xl px-4 sm:px-6 lg:px-8">
            <div className="absolute top-4 right-4">
                <ThemeToggle />
            </div>
            <Card className="w-full">
                <CardContent className="flex flex-col sm:flex-row h-full items-center gap-4 justify-center p-6">
                    <div className="w-full flex flex-col justify-center items-center p-5">
                        <img 
                            src={currentLogo} 
                            alt='theonyxpub.' 
                            className="h-25 w-33 object-cover mb-7"/>
                        <div className='w-full flex flex-col justify-center items-center p-5 gap-5'>
                            <Button type='button' className='w-25'>Log in</Button>
                            <Button type='button' className='w-25'>Register</Button>
                            <Button type='button' variant='link' className='opacity-45'>continue as guest</Button>
                        </div>
                    </div>
                    <Separator orientation="vertical" className="hidden sm:block h-24"/>
                    <Separator orientation="horizontal" className="block sm:hidden w-full"/>
                    <div className="w-full flex flex-col justify-end-safe content-start p-5 gap-2.5">
                        <Header2 text={"Enter the Onyx"}/>
                        <h2 className='font-medium'>This is where stories cut deeper. Create your account to unlock <i>The Onyx Pub’s</i> digital shelves—bold books, dark ink, and an online reader built for those who don’t just read, but consume every page. Sign up and cross the threshold.
                        </h2>
                    </div>
                </CardContent>
            </Card>
        </div>
    )
}

export default Entry

// {/* <Card className="w-full">
//                 <CardHeader className='justify-center'>
//                     <img 
//                         src={currentLogo} 
//                         alt='theonyxpub.' 
//                         className="h-25 w-33 object-cover"
//                     />
//                     {/* h-17.5 w-62.5  */}
//                 </CardHeader>
//                 <CardContent className="flex flex-col sm:flex-row h-full items-center gap-4 justify-center p-6">
//                     <div className="w-full flex flex-col justify-center items-center">heh
//                     </div>
//                         <Separator orientation="vertical"   className="hidden sm:block h-24"/>
//                         <Separator orientation="horizontal"     className="block sm:hidden w-full"/>
//                     <div className="w-full flex flex-col justify-center items-center">section 2</div>
//                 </CardContent>
//             </Card> */}