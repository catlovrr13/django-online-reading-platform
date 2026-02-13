// import Entry from '@/pages/entry/EntryPage'
// import entryLayout from '@/components/layouts/EntryLayout'

// const entryRouter = [
//     {
//         path: '/',
//         Component: entryLayout,
//         children: [
//             {
//                 index: true,
//                 Component: Entry
//             }
//         ]
//     }
// ]

// export default entryRouter

import dashLayout from "@/components/layouts/DashboardLayout";
import Dashboard from "@/pages/home/Dashboard";

const dashRouter = [
    {
        path: '/dashboard',
        Component: dashLayout,
        children: [
            {
                index: true,
                Component: Dashboard
            },
        ]
    }
]

export default dashRouter