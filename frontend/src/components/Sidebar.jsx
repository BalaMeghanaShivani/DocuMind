import { Link, useLocation } from 'react-router-dom'
import { LayoutDashboard, FileText, Settings, PlusCircle, LogOut } from 'lucide-react'

export default function Sidebar() {
    const location = useLocation()
    const path = location.pathname

    const navItems = [
        { icon: LayoutDashboard, label: 'Dashboard', to: '/dashboard' },
        { icon: PlusCircle, label: 'Generator', to: '/generator' },
        { icon: Settings, label: 'Settings', to: '/settings' },
    ]

    return (
        <aside className="w-64 border-r border-[var(--dm-border)] bg-[var(--dm-bg-dark)] flex flex-col h-screen sticky top-0">
            {/* Logo */}
            <div className="p-6 border-b border-[var(--dm-border)]">
                <Link to="/" className="flex items-center gap-3 hover:opacity-80 transition-opacity">
                    <span className="text-2xl">🧠</span>
                    <h1 className="text-xl font-bold tracking-tight">DocuMind</h1>
                </Link>
            </div>

            {/* Nav */}
            <nav className="flex-1 p-4 space-y-1">
                {navItems.map((item) => {
                    const isActive = path === item.to
                    return (
                        <Link
                            key={item.to}
                            to={item.to}
                            className={`flex items-center gap-3 px-4 py-3 rounded-lg text-sm font-medium transition-colors ${isActive
                                    ? 'bg-[var(--dm-primary)]/10 text-[var(--dm-primary)]'
                                    : 'text-[var(--dm-text-muted)] hover:bg-[var(--dm-bg-card)] hover:text-[var(--dm-text-primary)]'
                                }`}
                        >
                            <item.icon size={18} />
                            {item.label}
                        </Link>
                    )
                })}
            </nav>

            {/* User Footer */}
            <div className="p-4 border-t border-[var(--dm-border)]">
                <button className="flex items-center gap-3 w-full px-4 py-3 rounded-lg text-sm font-medium text-[var(--dm-text-muted)] hover:bg-[var(--dm-bg-card)] hover:text-red-400 transition-colors">
                    <LogOut size={18} />
                    Sign Out
                </button>
            </div>
        </aside>
    )
}
