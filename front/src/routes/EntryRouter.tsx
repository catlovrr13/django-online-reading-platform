import Entry from '@/pages/entry/EntryPage'
import Subscription from '@/pages/entry/Subscription'
import entryLayout from '@/components/layouts/EntryLayout'

const entryRouter = [
    {
        path: '/',
        Component: entryLayout,
        children: [
            {
                index: true,
                Component: Entry
            },
            {
                path: 'subscription',
                Component: Subscription
            }
        ]
    }
]

export default entryRouter