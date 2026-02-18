import { useState, useEffect } from 'react'
import { Grid, GridColumn } from '@progress/kendo-react-grid'
import { Badge } from '@progress/kendo-react-indicators'
import { Loader2 } from 'lucide-react'
import Layout from '../components/Layout'
import { api } from '../services/api'

const TypeCell = (props) => {
    const typeLabels = {
        meeting_notes: 'Meeting Notes',
        prd: 'PRD',
        code_docs: 'Code Docs',
        general: 'General'
    }
    const typeColors = {
        meeting_notes: 'info',
        prd: 'warning',
        code_docs: 'success',
        general: 'neutral'
    }
    return (
        <td>
            <Badge themeColor={typeColors[props.dataItem.doc_type] || 'neutral'}>
                {typeLabels[props.dataItem.doc_type] || props.dataItem.doc_type}
            </Badge>
        </td>
    )
}

const DateCell = (props) => {
    return (
        <td>
            {new Date(props.dataItem._createdAt || Date.now()).toLocaleDateString()}
        </td>
    )
}

const StatusCell = (props) => {
    // For now, if it's in Sanity, it's "Completed" or "Generated"
    return (
        <td>
            <span className="inline-flex items-center gap-1.5 px-2.5 py-0.5 rounded-full text-xs font-medium bg-green-500/10 text-green-400">
                <span className="w-1.5 h-1.5 rounded-full bg-current" />
                Ready
            </span>
        </td>
    )
}

export default function Dashboard() {
    const [documents, setDocuments] = useState([])
    const [loading, setLoading] = useState(true)

    useEffect(() => {
        const fetchDocs = async () => {
            try {
                const docs = await api.getDocuments()
                setDocuments(docs)
            } catch (error) {
                console.error("Failed to load dashboard:", error)
            } finally {
                setLoading(false)
            }
        }
        fetchDocs()
    }, [])

    return (
        <Layout title="Dashboard">
            <div className="space-y-6">
                <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
                    <StatCard label="Total Documents" value={documents.length} />
                    <StatCard label="Avg Processing Time" value="1.2s" />
                    <StatCard label="System Status" value="Online" />
                </div>

                <div className="bg-[var(--dm-bg-card)] rounded-xl border border-[var(--dm-border)] overflow-hidden min-h-[400px]">
                    <div className="p-4 border-b border-[var(--dm-border)]">
                        <h3 className="font-semibold">Recent Documents</h3>
                    </div>

                    {loading ? (
                        <div className="flex justify-center items-center h-64 text-[var(--dm-text-muted)]">
                            <Loader2 className="animate-spin mr-2" /> Loading documents...
                        </div>
                    ) : documents.length === 0 ? (
                        <div className="flex justify-center items-center h-64 text-[var(--dm-text-muted)]">
                            No documents found. Create one in the Generator!
                        </div>
                    ) : (
                        <Grid data={documents} style={{ height: '400px', border: 'none' }}>
                            <GridColumn field="title" title="Title" />
                            <GridColumn field="doc_type" title="Type" cell={TypeCell} />
                            <GridColumn field="_createdAt" title="Created At" cell={DateCell} />
                            <GridColumn title="Status" cell={StatusCell} />
                        </Grid>
                    )}
                </div>
            </div>
        </Layout>
    )
}

function StatCard({ label, value }) {
    return (
        <div className="p-6 rounded-xl bg-[var(--dm-bg-card)] border border-[var(--dm-border)]">
            <p className="text-sm text-[var(--dm-text-muted)] mb-1">{label}</p>
            <p className="text-3xl font-bold">{value}</p>
        </div>
    )
}

