import Entry from '@/pages/entry/EntryPage'
import entryLayout from '@/components/layouts/EntryLayout'

const entryRouter = [
    {
        path: '/',
        Component: entryLayout,
        children: [
            {
                index: true,
                Component: Entry
            }
        ]
    }
]

export default entryRouter