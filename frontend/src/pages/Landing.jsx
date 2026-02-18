import { Link } from 'react-router-dom'
import { ArrowRight, FileText, Mic, Upload, Zap } from 'lucide-react'
import { Button } from '@progress/kendo-react-buttons'

export default function Landing() {
    return (
        <div className="min-h-screen bg-[var(--dm-bg-dark)] text-white overflow-hidden relative">
            {/* Background Gradients */}
            <div className="absolute top-0 left-0 w-full h-full overflow-hidden z-0 pointer-events-none">
                <div className="absolute top-[-10%] left-[-10%] w-[40%] h-[40%] bg-purple-600/20 rounded-full blur-[120px]" />
                <div className="absolute bottom-[-10%] right-[-10%] w-[40%] h-[40%] bg-indigo-600/20 rounded-full blur-[120px]" />
            </div>

            <nav className="relative z-10 px-8 py-6 flex justify-between items-center max-w-7xl mx-auto">
                <div className="flex items-center gap-2 font-bold text-xl">
                    <span className="text-2xl">🧠</span> DocuMind
                </div>
                <div className="flex gap-4">
                    <Link to="/generator">
                        <Button themeColor="primary" size="large" className="font-semibold px-6">
                            Launch App
                        </Button>
                    </Link>
                </div>
            </nav>

            <main className="relative z-10 max-w-5xl mx-auto px-6 pt-20 pb-32 text-center">
                <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-slate-800/50 border border-slate-700 text-xs font-medium text-slate-300 mb-8 backdrop-blur-sm">
                    <span className="w-2 h-2 rounded-full bg-green-400 animate-pulse" />
                    v1.0 Hackathon MVP
                </div>

                <h1 className="text-5xl md:text-7xl font-bold tracking-tight mb-6 bg-gradient-to-br from-white via-slate-200 to-slate-400 bg-clip-text text-transparent">
                    Turn Brain Dumps <br />
                    Into <span className="text-indigo-400">Professional Docs</span>
                </h1>

                <p className="text-lg md:text-xl text-slate-400 mb-10 max-w-2xl mx-auto leading-relaxed">
                    Stop formatting meeting notes and PRDs. Just talk or paste raw text,
                    and let our AI agent structure it into beautiful PDFs instantly.
                </p>

                <div className="flex flex-col sm:flex-row gap-4 justify-center items-center mb-20">
                    <Link to="/generator">
                        <button className="group flex items-center gap-2 px-8 py-4 rounded-xl bg-indigo-600 hover:bg-indigo-500 text-white font-semibold text-lg transition-all shadow-lg shadow-indigo-500/25 hover:shadow-indigo-500/40">
                            Start Generating
                            <ArrowRight size={20} className="group-hover:translate-x-1 transition-transform" />
                        </button>
                    </Link>
                    <a href="#how-it-works" className="px-8 py-4 rounded-xl hover:bg-slate-800/50 text-slate-300 font-medium transition-colors">
                        How it works
                    </a>
                </div>

                {/* Feature Grid */}
                <div className="grid md:grid-cols-3 gap-6 text-left">
                    <FeatureCard
                        icon={<Mic className="text-purple-400" />}
                        title="Voice to Text"
                        desc="Record meetings or upload audio. Deepgram transcribes it with 99% accuracy."
                    />
                    <FeatureCard
                        icon={<FileText className="text-blue-400" />}
                        title="AI Structuring"
                        desc="Our agent identifies action items, requirements, and summaries automatically."
                    />
                    <FeatureCard
                        icon={<Zap className="text-yellow-400" />}
                        title="Instant PDF"
                        desc="Export professional, branded PDFs ready for stakeholders in seconds."
                    />
                </div>
            </main>

            <footer className="relative z-10 border-t border-slate-800 py-12 text-center text-slate-500 text-sm">
                <p>&copy; 2026 DocuMind. Built for the Global AI Hackathon.</p>
            </footer>
        </div>
    )
}

function FeatureCard({ icon, title, desc }) {
    return (
        <div className="p-6 rounded-2xl bg-slate-900/50 border border-slate-800 hover:border-slate-700 transition-colors backdrop-blur-sm group">
            <div className="w-12 h-12 rounded-lg bg-slate-800 flex items-center justify-center mb-4 group-hover:scale-110 transition-transform">
                {icon}
            </div>
            <h3 className="text-lg font-semibold mb-2 text-slate-200">{title}</h3>
            <p className="text-slate-400 leading-relaxed">{desc}</p>
        </div>
    )
}
