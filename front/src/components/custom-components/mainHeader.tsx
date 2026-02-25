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
import { useSidebar } from '@/components/ui/sidebar'
import { Search, Menu } from 'lucide-react'
import { useState } from 'react'
import { motion, AnimatePresence } from 'framer-motion'

const StickyHeader = () => {
    const { theme } = useTheme()
    const headerColor = theme === 'dark' ? 'bg-neutral-900' : 'bg-white'
    const currentLogo = theme === 'dark' ? longlight : longdark
    const [mobileMenuOpen, setMobileMenuOpen] = useState(false)
    const { state } = useSidebar()
    const isSidebarOpen = state === 'expanded'

    return (
        <header className={`sticky top-0 z-50 ${headerColor} shadow-md w-full`}>
            <div className="mx-auto px-4 sm:px-6 lg:px-8">
                <nav className="flex items-center justify-between h-16">
                    {/* logo */}
                    <img
                        src={currentLogo}
                        alt='theonyxpub.'
                        className={`h-25 w-33 object-cover transition-transform duration-300 ease-in-out ${isSidebarOpen ? 'rotate-90' : ''}`}/>

                    {/* desktop view */}
                    <div className="hidden md:flex items-center content-center space-x-2 h-7">
                        <Tabs defaultValue="overview">
                            <TabsList variant="line">
                                <TabsTrigger value="overview" >Home</TabsTrigger>
                                <TabsTrigger value="analytics">Library</TabsTrigger>
                                <TabsTrigger value="reports">About us</TabsTrigger>
                            </TabsList>
                        </Tabs>
                        <Separator orientation="vertical"/>
                        <ThemeToggle/>
                        <Separator orientation="vertical"/>
                        <Popover>
                            <PopoverTrigger asChild>
                                <Button variant={'ghost'} size={'icon'}>
                                    <Search strokeWidth={2.4}/>
                                </Button>
                            </PopoverTrigger>
                            <PopoverContent className='p-0 w-max' align='end' sideOffset={25}>
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

                    {/* mobile view */}
                    <div className="flex md:hidden items-center space-x-2">
                        <Popover>
                            <PopoverTrigger asChild>
                                <Button variant={'ghost'} size={'icon'}>
                                    <Search strokeWidth={2.4}/>
                                </Button>
                            </PopoverTrigger>
                            <PopoverContent className='p-0 w-64' align='center' sideOffset={25}>
                                <InputGroup className='w-full'>
                                    <InputGroupAddon align={'inline-start'}>
                                        <Search/>
                                    </InputGroupAddon>
                                    <InputGroupInput placeholder="Search..."/>
                                </InputGroup>
                            </PopoverContent>
                        </Popover>
                        
                        <Separator orientation="vertical"/>

                        <ThemeToggle/>

                        <Separator orientation="vertical"/>
                        
                        <Button 
                            variant="ghost" 
                            size="icon"
                            onClick={() => setMobileMenuOpen(!mobileMenuOpen)}
                        >
                            <Menu className="h-5 w-5" strokeWidth={2.4} />
                        </Button>
                    </div>
                </nav>

                {/* mobile menu */}
                <AnimatePresence>
                    {mobileMenuOpen && (
                        <motion.div
                            initial={{ height: 0, opacity: 0 }}
                            animate={{ height: 'auto', opacity: 1 }}
                            exit={{ height: 0, opacity: 0 }}
                            transition={{ duration: 0.25, ease: "easeInOut" }}
                            className="md:hidden overflow-hidden"
                        >
                            <div className="py-4 border-t">
                                <Tabs defaultValue="home" className="w-full ">
                                    <TabsList variant="line" className="grid grid-cols-3 w-full">
                                        <TabsTrigger value="home" className="text-sm">Home</TabsTrigger>
                                        <TabsTrigger value="library" className="text-sm">Library</TabsTrigger>
                                        <TabsTrigger value="about-us" className="text-sm">About us</TabsTrigger>
                                    </TabsList>
                                </Tabs>
                            </div>
                        </motion.div>
                    )}
                </AnimatePresence>
            </div>
        </header>
    );
};

export default StickyHeader;