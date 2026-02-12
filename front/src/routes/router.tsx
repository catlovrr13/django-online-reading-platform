import { createBrowserRouter } from 'react-router';
import entryRouter from './EntryRouter';
import dashRouter from './DashboardRouter';

const router = createBrowserRouter([...entryRouter, ...dashRouter])

export default router