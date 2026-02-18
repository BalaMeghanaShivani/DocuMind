import Sidebar from './Sidebar'
import Header from './Header'

export default function Layout({ children, title = 'DocuMind' }) {
    return (
        <div className="flex min-h-screen bg-[var(--dm-bg-dark)] text-[var(--dm-text-primary)] font-sans selection:bg-[var(--dm-primary)] selection:text-white">
            <Sidebar />
            <div className="flex-1 flex flex-col min-w-0">
                <Header title={title} />
                <main className="flex-1 p-8 overflow-y-auto">
                    {children}
                </main>
            </div>
        </div>
    )
}
