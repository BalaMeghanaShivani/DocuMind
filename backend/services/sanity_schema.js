// 📝 Sanity Schema: 'generatedDocument'
//
// This schema allows us to store not just the PDF file, but the verify
// atoms of data that make up the document (Action Items, Decisions, Requirements).

export default {
    name: 'generatedDocument',
    title: 'Generated Document',
    type: 'document',
    fields: [
        {
            name: 'title',
            title: 'Title',
            type: 'string',
        },
        {
            name: 'docType',
            title: 'Document Type',
            type: 'string',
            options: {
                list: [
                    { title: 'Meeting Notes', value: 'meeting_notes' },
                    { title: 'Product Requirements', value: 'prd' },
                    { title: 'Code Documentation', value: 'code_docs' },
                ],
            },
        },
        {
            name: 'createdAt',
            title: 'Created At',
            type: 'datetime',
        },

        // 🧠 Structured Content Fields
        // These allow us to query ACROSS documents.
        // e.g. *[_type == "generatedDocument"] { actionItems }
        {
            name: 'actionItems',
            title: 'Action Items',
            type: 'array',
            of: [
                {
                    type: 'object',
                    fields: [
                        { name: 'task', type: 'string', title: 'Task' },
                        { name: 'owner', type: 'string', title: 'Owner' },
                        { name: 'dueDate', type: 'string', title: 'Due Date' },
                        { name: 'status', type: 'string', title: 'Status', initialValue: 'open', options: { list: ['open', 'done'] } }
                    ]
                }
            ],
            hidden: ({ document }) => document?.docType !== 'meeting_notes'
        },
        {
            name: 'requirements',
            title: 'Requirements (PRD)',
            type: 'array',
            of: [{ type: 'string' }],
            hidden: ({ document }) => document?.docType !== 'prd'
        },

        // 📄 The Artifacts
        {
            name: 'summary',
            title: 'Summary',
            type: 'text',
            rows: 3
        },
        {
            name: 'pdfFile',
            title: 'Generated PDF',
            type: 'file',
        }
    ],
}
