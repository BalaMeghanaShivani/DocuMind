import { Bell, Search, User } from 'lucide-react'

export default function Header({ title }) {
    return (
        <header className="h-16 border-b border-[var(--dm-border)] bg-[var(--dm-bg-dark)] px-8 flex items-center justify-between sticky top-0 z-10">
            <h2 className="text-lg font-semibold text-[var(--dm-text-primary)]">{title}</h2>

            <div className="flex items-center gap-4">
                <div className="relative hidden md:block">
                    <Search size={16} className="absolute left-3 top-1/2 -translate-y-1/2 text-[var(--dm-text-muted)]" />
                    <input
                        type="text"
                        placeholder="Search documents..."
                        className="pl-9 pr-4 py-1.5 rounded-full bg-[var(--dm-bg-card)] border border-[var(--dm-border)] text-sm text-[var(--dm-text-primary)] focus:outline-none focus:ring-1 focus:ring-[var(--dm-primary)] w-64"
                    />
                </div>

                <button className="text-[var(--dm-text-muted)] hover:text-[var(--dm-text-primary)] transition-colors relative">
                    <Bell size={20} />
                    <span className="absolute top-0 right-0 w-2 h-2 bg-red-500 rounded-full border-2 border-[var(--dm-bg-dark)]"></span>
                </button>

                <div className="w-8 h-8 rounded-full bg-gradient-to-tr from-purple-500 to-indigo-500 flex items-center justify-center text-xs font-bold ring-2 ring-[var(--dm-bg-card)]">
                    JD
                </div>
            </div>
        </header>
    )
}
