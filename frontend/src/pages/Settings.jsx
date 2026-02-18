import { useState, useEffect } from 'react'
import { Switch } from '@progress/kendo-react-inputs'
import { Badge } from '@progress/kendo-react-indicators'
import { CheckCircle, XCircle, RefreshCw } from 'lucide-react'
import Layout from '../components/Layout'
import { api } from '../services/api'

export default function Settings() {
    const [statuses, setStatuses] = useState(null)
    const [loading, setLoading] = useState(true)

    useEffect(() => {
        fetchStatus()
    }, [])

    const fetchStatus = async () => {
        setLoading(true)
        try {
            const data = await api.getIntegrationStatus()
            setStatuses(data)
        } catch (err) {
            console.error("Failed to fetch status", err)
        } finally {
            setLoading(false)
        }
    }

    return (
        <Layout title="Settings">
            <div className="max-w-3xl space-y-8">

                {/* Connected Services Section */}
                <section className="space-y-4">
                    <div className="border-b border-[var(--dm-border)] pb-2 mb-4 flex justify-between items-center">
                        <div>
                            <h3 className="text-lg font-semibold">Connected Services</h3>
                            <p className="text-sm text-[var(--dm-text-muted)]">System-level integrations configured via environment variables.</p>
                        </div>
                        <button onClick={fetchStatus} className="p-2 hover:bg-[var(--dm-bg-card)] rounded-full transition-colors">
                            <RefreshCw size={16} className={loading ? "animate-spin" : ""} />
                        </button>
                    </div>

                    <div className="grid gap-4">
                        <ServiceStatus
                            label="OpenAI (AI Agent)"
                            status={statuses?.openai}
                            desc="Powers document structuring and classification."
                        />
                        <ServiceStatus
                            label="Deepgram (Voice)"
                            status={statuses?.deepgram}
                            desc="Handles high-accuracy voice transcription."
                        />
                        <ServiceStatus
                            label="Foxit PDF SDK"
                            status={statuses?.foxit}
                            desc="Generates and enhances professional PDFs."
                        />
                        <ServiceStatus
                            label="Sanity CMS"
                            status={statuses?.sanity}
                            desc="Stores structured content and archives."
                        />
                    </div>
                </section>

                {/* Preferences */}
                <section className="space-y-4 pt-6">
                    <div className="border-b border-[var(--dm-border)] pb-2 mb-4">
                        <h3 className="text-lg font-semibold">Preferences</h3>
                        <p className="text-sm text-[var(--dm-text-muted)]">Customize your local experience.</p>
                    </div>

                    <div className="flex items-center justify-between p-4 bg-[var(--dm-bg-card)] rounded-lg border border-[var(--dm-border)]">
                        <div>
                            <p className="font-medium">Dark Mode</p>
                            <p className="text-sm text-[var(--dm-text-muted)]">Toggle application theme</p>
                        </div>
                        <Switch defaultChecked={true} onLabel={'ON'} offLabel={'OFF'} />
                    </div>

                    <div className="flex items-center justify-between p-4 bg-[var(--dm-bg-card)] rounded-lg border border-[var(--dm-border)]">
                        <div>
                            <p className="font-medium">Notifications</p>
                            <p className="text-sm text-[var(--dm-text-muted)]">Email alerts when documents are ready</p>
                        </div>
                        <Switch defaultChecked={false} />
                    </div>
                </section>
            </div>
        </Layout>
    )
}

function ServiceStatus({ label, status, desc }) {
    const isConnected = status === 'connected'

    return (
        <div className="flex items-center justify-between p-4 bg-[var(--dm-bg-card)] rounded-lg border border-[var(--dm-border)]">
            <div className="flex items-center gap-4">
                <div className={`p-2 rounded-lg ${isConnected ? 'bg-green-500/10 text-green-500' : 'bg-slate-700/50 text-slate-400'}`}>
                    {isConnected ? <CheckCircle size={24} /> : <XCircle size={24} />}
                </div>
                <div>
                    <h4 className="font-medium">{label}</h4>
                    <p className="text-sm text-[var(--dm-text-muted)]">{desc}</p>
                </div>
            </div>

            <Badge themeColor={isConnected ? 'success' : 'neutral'} shape="rounded">
                {status?.toUpperCase() || 'UNKNOWN'}
            </Badge>
        </div>
    )
}
