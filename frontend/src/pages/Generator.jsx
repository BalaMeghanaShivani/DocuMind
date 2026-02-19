import { useState, useRef } from 'react'
import { FileText, Mic, CheckCircle, Loader2, StopCircle } from 'lucide-react'
import { Button } from '@progress/kendo-react-buttons'
import Layout from '../components/Layout'
import { api } from '../services/api'

const STEPS = ['input', 'processing', 'preview', 'result']

export default function Generator() {
    return (
        <Layout title="New Document">
            <div className="bg-[var(--dm-bg-card)] rounded-xl border border-[var(--dm-border)] p-1 min-h-[600px] relative">
                <div className="p-6">
                    <GeneratorContent />
                </div>
            </div>
        </Layout>
    )
}

function GeneratorContent() {
    const [step, setStep] = useState('input')
    const [inputMode, setInputMode] = useState('text') // 'text' or 'voice'
    const [rawText, setRawText] = useState('')
    const [structuredData, setStructuredData] = useState(null)
    const [pdfPath, setPdfPath] = useState(null)
    const [error, setError] = useState(null)
    const [isRecording, setIsRecording] = useState(false)

    const mediaRecorderRef = useRef(null)
    const chunksRef = useRef([])

    // ── Voice Recording Logic ─────────────────────────────
    const startRecording = async () => {
        try {
            const stream = await navigator.mediaDevices.getUserMedia({ audio: true })
            mediaRecorderRef.current = new MediaRecorder(stream)
            chunksRef.current = []

            mediaRecorderRef.current.ondataavailable = (e) => {
                if (e.data.size > 0) chunksRef.current.push(e.data)
            }

            mediaRecorderRef.current.onstop = async () => {
                const blob = new Blob(chunksRef.current, { type: 'audio/webm' })
                await handleTranscribe(blob)
            }

            mediaRecorderRef.current.start()
            setIsRecording(true)
            setError(null)
        } catch (err) {
            console.error("Microphone error:", err)
            setError("Could not access microphone. Please check permissions.")
        }
    }

    const stopRecording = () => {
        if (mediaRecorderRef.current && isRecording) {
            mediaRecorderRef.current.stop()
            setIsRecording(false)
        }
    }

    const handleTranscribe = async (audioBlob) => {
        setStep('processing')
        try {
            const result = await api.transcribeAudio(audioBlob)
            setRawText(result.transcript)
            setStep('input') // Go back to input with transcribed text
            setInputMode('text') // Switch to text view to show result
        } catch (err) {
            setError(err.message)
            setStep('input')
        }
    }

    // ── Process text through backend ──────────────────────
    const handleProcess = async () => {
        if (!rawText.trim()) return
        setStep('processing')
        setError(null)
        try {
            const data = await api.processText(rawText)
            setStructuredData(data)
            setPdfPath(data.pdf_path)
            setStep('preview')
        } catch (err) {
            setError(err.message)
            setStep('input')
        }
    }

    const downloadPdf = () => {
        if (pdfPath) {
            // pdfPath usually comes as "output/meeting_notes_generated_enhanced.pdf"
            // We want just the filename: "meeting_notes_generated_enhanced.pdf"
            const filename = pdfPath.split('/').pop();
            const downloadUrl = `/api/download/${filename}`;

            // Trigger download
            const link = document.createElement('a');
            link.href = downloadUrl;
            link.setAttribute('download', filename);
            document.body.appendChild(link);
            link.click();
            link.remove();
        }
    }

    return (
        <div className="max-w-3xl mx-auto py-4">
            {/* Stepper */}
            <div className="flex justify-center mb-10">
                <div className="flex items-center gap-2">
                    {STEPS.map((s, i) => (
                        <div key={s} className={`w-3 h-3 rounded-full ${STEPS.indexOf(step) >= i ? 'bg-[var(--dm-primary)]' : 'bg-slate-700'}`} />
                    ))}
                </div>
            </div>

            {error && <div className="mb-6 p-4 rounded bg-red-500/10 text-red-400 border border-red-500/20">{error}</div>}

            {step === 'input' && (
                <div className="space-y-6 animate-in fade-in zoom-in duration-300">
                    <div className="text-center mb-8">
                        <h2 className="text-2xl font-bold mb-2">How should we start?</h2>
                        <p className="text-[var(--dm-text-muted)]">Choose an input method below.</p>
                    </div>

                    <div className="grid grid-cols-2 gap-4 mb-6">
                        <button
                            onClick={() => setInputMode('text')}
                            className={`p-6 rounded-xl border-2 flex flex-col items-center gap-3 transition-all ${inputMode === 'text' ? 'border-[var(--dm-primary)] bg-[var(--dm-primary)]/5' : 'border-[var(--dm-border)] bg-[var(--dm-bg-dark)] hover:border-[var(--dm-text-muted)]'}`}
                        >
                            <FileText size={32} className={inputMode === 'text' ? 'text-[var(--dm-primary)]' : 'text-[var(--dm-text-muted)]'} />
                            <span className={`font-semibold ${inputMode === 'text' ? '' : 'text-[var(--dm-text-muted)]'}`}>Text / Notes</span>
                        </button>
                        <button
                            onClick={() => setInputMode('voice')}
                            className={`p-6 rounded-xl border-2 flex flex-col items-center gap-3 transition-all ${inputMode === 'voice' ? 'border-[var(--dm-primary)] bg-[var(--dm-primary)]/5' : 'border-[var(--dm-border)] bg-[var(--dm-bg-dark)] hover:border-[var(--dm-text-muted)]'}`}
                        >
                            <Mic size={32} className={inputMode === 'voice' ? 'text-[var(--dm-primary)]' : 'text-[var(--dm-text-muted)]'} />
                            <span className={`font-semibold ${inputMode === 'voice' ? '' : 'text-[var(--dm-text-muted)]'}`}>Voice Memo</span>
                        </button>
                    </div>

                    {inputMode === 'text' ? (
                        <textarea
                            value={rawText}
                            onChange={e => setRawText(e.target.value)}
                            className="w-full h-48 rounded-xl bg-[var(--dm-bg-dark)] border border-[var(--dm-border)] p-4 focus:ring-2 ring-[var(--dm-primary)] outline-none resize-none transition-all placeholder:text-slate-600"
                            placeholder="Paste your meeting notes, PRD draft, or requirements here..."
                        />
                    ) : (
                        <div className="h-48 rounded-xl bg-[var(--dm-bg-dark)] border border-[var(--dm-border)] flex flex-col items-center justify-center gap-4">
                            {isRecording ? (
                                <>
                                    <div className="animate-pulse text-red-400 font-bold mb-2">Recording in progress...</div>
                                    <Button themeColor="error" size="large" onClick={stopRecording} icon="stop">
                                        <StopCircle className="mr-2" /> Stop Recording
                                    </Button>
                                </>
                            ) : (
                                <Button themeColor="primary" size="large" onClick={startRecording}>
                                    <Mic className="mr-2" /> Start Recording
                                </Button>
                            )}
                        </div>
                    )}

                    <div className="flex justify-end">
                        <Button themeColor="primary" size="large" onClick={handleProcess} disabled={!rawText.trim() || isRecording}>
                            Analyze Document
                        </Button>
                    </div>
                </div>
            )}

            {step === 'processing' && (
                <div className="text-center py-20 animate-in fade-in duration-500">
                    <Loader2 size={64} className="mx-auto text-[var(--dm-primary)] animate-spin mb-6" />
                    <h3 className="text-xl font-semibold mb-2">AI Agent Working...</h3>
                    <p className="text-[var(--dm-text-muted)]">Classifying, structuring, and generating your PDF.</p>
                </div>
            )}

            {step === 'preview' && (
                <div className="animate-in slide-in-from-bottom-4 duration-500">
                    <div className="flex justify-between items-center mb-6">
                        <div>
                            <h3 className="text-xl font-bold">{structuredData.title}</h3>
                            <span className="text-sm text-[var(--dm-text-muted)] uppercase tracking-wider font-medium">{structuredData.doc_type}</span>
                        </div>
                        <Button themeColor="primary" onClick={() => setStep('result')}>Confirm & Finish</Button>
                    </div>

                    <div className="bg-[var(--dm-bg-dark)] p-6 rounded-xl border border-[var(--dm-border)] overflow-auto max-h-[500px]">
                        <pre className="text-sm text-green-400 font-mono">{JSON.stringify(structuredData.structured_data, null, 2)}</pre>
                    </div>
                </div>
            )}

            {step === 'result' && (
                <div className="text-center py-20 animate-in zoom-in duration-300">
                    <CheckCircle size={80} className="mx-auto text-green-500 mb-6" />
                    <h2 className="text-3xl font-bold mb-4">Success!</h2>
                    <p className="text-[var(--dm-text-muted)] mb-8">Your PDF has been generated.</p>
                    <div className="flex justify-center gap-4">
                        <Button themeColor="primary" size="large" onClick={downloadPdf}>Download PDF</Button>
                        <Button size="large" onClick={() => { setStep('input'); setRawText(''); setStructuredData(null); }}>Create Another</Button>
                    </div>
                </div>
            )}
        </div>
    )
}

