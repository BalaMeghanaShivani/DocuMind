# 🎨 DocuMind Frontend Design

## 📱 User Flow
1. **Input**: User lands on dashboard -> Selects "New Document" -> Uploads Audio OR Pastes Text.
2. **Processing**: System shows "Analyzing..." state (Deepgram + AI Agent).
3. **Preview**: User sees the *Structured Data* (not just text). They can edit extracted fields (e.g., fix a due date).
4. **Generation**: User clicks "Generate PDF" -> Backend builds PDF -> Foxit enhances it.
5. **Result**: User views PDF in browser and can download/save to Sanity.

## 🏗 Component Structure

### `App.jsx`
Main entry point. Holds state for `currentStep` (input | preview | result).

### 1. `InputSection.jsx`
- **Tabs**: [ Text Input ] | [ Voice Upload ]
- **Text Area**: For raw brain dumps.
- **File Uploader**: Drag & drop zone for `.mp3` / `.wav`.
- **Action**: `onProcess()` prop to trigger backend API.

### 2. `StructurePreview.jsx`
- **Props**: `data` (The JSON returned from Backend)
- **Edit Mode**: Simple inputs to modify the AI's deductions before finalizing.
- **Visuals**:
    - *Meeting Notes*: Card view for "Action Items".
    - *PRD*: Accordion view for "Requirements".
- **Action**: `onGeneratePDF()` to confirm structure.

### 3. `PDFResult.jsx`
- **PDF Viewer**: Embeds the generated PDF (using standard `<embed>` or Foxit Web SDK).
- **Actions**:
    - [ Download ]
    - [ Save to Knowledge Base ] (Triggers Sanity save)

### 4. `Sidebar.jsx`
- Navigation: Dashboard, Knowledge Base, Settings.
- Recent Docs list.

## 🔄 State Management (React Context or simple State)

```javascript
const [docState, setDocState] = useState({
  step: 'input', // input, processing, preview, done
  rawContent: '',
  structuredData: null,
  pdfUrl: null
});
```

## 🔌 API Integration Hooks
- `useTranscribe`: Handles Deepgram upload.
- `useStructure`: Calls AI agent endpoint.
- `usePDF`: Calls PDF generation + Foxit enhancement.
