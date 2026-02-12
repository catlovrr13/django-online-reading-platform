import longdark from '@/assets/media/longdark.svg'
import longlight from '@/assets/media/longlight.svg'

import { Button } from "@/components/ui/button"
import { Tabs, TabsList, TabsTrigger } from "@/components/ui/tabs"
import {
    Popover,
    PopoverContent,
    PopoverTrigger,
} from "@/components/ui/popover"
import {
    InputGroup,
    InputGroupAddon,
    InputGroupInput,
} from "@/components/ui/input-group"
import { Separator } from '@/components/ui/separator'

import { ThemeToggle } from '@/components/theme-toggle'
import { useTheme } from '@/components/theme-provider'
import { Search } from 'lucide-react'

const StickyHeader = () => {
    const { theme } = useTheme()
    const headerColor = theme === 'dark' ? 'bg-neutral-900' : 'bg-white'
    // const textColor = theme === 'dark' ? 'text-neutral-950' : 'text-stone-100'
    const currentLogo = theme === 'dark' ? longlight : longdark

    return (
        <header className={`sticky top-0 z-50 ${headerColor} shadow-md w-full`}>
            <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
                <nav className="flex items-center justify-between h-16">
                {/* logo */}
                <img 
                    src={currentLogo} 
                    alt='theonyxpub.' 
                    className="h-25 w-33 object-cover"/>
                {/* menu buttons */}
                <div className="flex items-center content-center space-x-2 h-7">
                    {/* <a href="#home" className="text-gray-600 hover:text-gray-900">Home</a>
                    <a href="#about" className="text-gray-600 hover:text-gray-900">About</a>
                    <a href="#contact" className="text-gray-600 hover:text-gray-900">Contact</a> */}
                    <Tabs defaultValue="overview">
                        <TabsList variant="line">
                            <TabsTrigger value="overview" >Home</TabsTrigger>
                            <TabsTrigger value="analytics">Library</TabsTrigger>
                            <TabsTrigger value="reports">About us</TabsTrigger>
                        </TabsList>
                    </Tabs>
                    <Separator orientation="vertical" className=''/>
                    <ThemeToggle/>
                    <Separator orientation="vertical" className=''/>
                    <Popover>
                        <PopoverTrigger asChild>
                            <Button variant={'ghost'} className=''>
                                <Search/>
                            </Button>
                        </PopoverTrigger>
                        <PopoverContent className='p-0 w-max' align='end' sideOffset={30}>
                            <InputGroup className='w-75'>
                                <InputGroupAddon align={'inline-start'}>
                                    <Search/>
                                </InputGroupAddon>
                                <InputGroupInput placeholder="Search..."/>
                                <InputGroupAddon align='inline-end' className=''>0 results</InputGroupAddon>
                            </InputGroup>
                        </PopoverContent>
                    </Popover>
                </div>
                </nav>
            </div>
        </header>
    );
};

export default StickyHeader;