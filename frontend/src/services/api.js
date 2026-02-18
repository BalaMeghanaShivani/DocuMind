import axios from 'axios';

const API = axios.create({
    baseURL: '/api', // Vite proxy will handle this
    headers: {
        'Content-Type': 'application/json',
    },
});

export const api = {
    // Check System Status
    getIntegrationStatus: async () => {
        try {
            const response = await API.get('/integrations/status');
            return response.data;
        } catch (error) {
            console.error('API Error (Status):', error);
            return { openai: 'error', deepgram: 'error', foxit: 'error', sanity: 'error' };
        }
    },

    // Fetch Documents
    getDocuments: async (type = null) => {
        try {
            const params = type ? { doc_type: type } : {};
            const response = await API.get('/documents', { params });
            return response.data || [];
        } catch (error) {
            console.error('API Error (Get Docs):', error);
            return [];
        }
    },

    // Fetch Open Tasks
    getOpenTasks: async () => {
        try {
            const response = await API.get('/documents/tasks');
            return response.data || [];
        } catch (error) {
            console.error('API Error (Tasks):', error);
            return [];
        }
    },

    // Process Text
    processText: async (text, sourceType = 'text') => {
        try {
            const response = await API.post('/process-text', { text, source_type: sourceType });
            return response.data;
        } catch (error) {
            throw new Error(error.response?.data?.detail || 'Processing failed');
        }
    },

    // Transcribe Audio
    transcribeAudio: async (audioBlob) => {
        const formData = new FormData();
        formData.append('file', audioBlob, 'recording.webm'); // Backend handles conversion if needed

        try {
            const response = await API.post('/transcribe-audio', formData, {
                headers: { 'Content-Type': 'multipart/form-data' },
            });
            return response.data;
        } catch (error) {
            throw new Error(error.response?.data?.detail || 'Transcription failed');
        }
    }
};
