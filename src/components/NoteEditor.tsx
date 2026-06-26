interface Note {
  id: string;
  title: string;
  content: string;
  createdAt: string;
  updatedAt: string;
  colorTag: 'orange' | 'pink' | 'violet' | 'emerald' | 'none';
}

interface NoteEditorProps {
  activeNote: Note | null;
  onUpdateField: (field: keyof Pick<Note, 'title' | 'content' | 'colorTag'>, value: string) => void;
  onDeleteNote: (id: string) => void;
  onCreateNote: () => void;
  formatDate: (isoString: string) => string;
  tagColorMap: Record<Note['colorTag'], string>;
  tagLabelMap: Record<Note['colorTag'], string>;
}

export default function NoteEditor({
  activeNote,
  onUpdateField,
  onDeleteNote,
  onCreateNote,
  formatDate,
  tagColorMap,
  tagLabelMap
}: NoteEditorProps) {
  if (!activeNote) {
    return (
      <section className="flex-1 flex flex-col items-center justify-center p-8 text-center bg-surface-soft min-h-[400px] md:min-h-0">
        <div className="max-w-md p-6 bg-canvas border border-hairline rounded-lg shadow-sm">
          <div className="w-12 h-12 mx-auto mb-4 rounded-full bg-surface-card flex items-center justify-center text-muted">
            <svg className="w-6 h-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2.5} d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
            </svg>
          </div>
          <h3 className="font-semibold text-lg text-ink mb-1">No note selected</h3>
          <p className="text-xs text-muted mb-4">
            Select a note from the sidebar list or create a brand new one to get started.
          </p>
          <button
            onClick={onCreateNote}
            className="px-4 py-2 bg-primary hover:bg-primary-active text-on-primary font-medium text-xs rounded-md transition-colors cursor-pointer shadow-sm"
          >
            Create New Note
          </button>
        </div>
      </section>
    );
  }

  return (
    <section className="flex-1 flex flex-col bg-canvas min-h-[400px] md:min-h-0">
      <div className="flex-1 flex flex-col p-6 space-y-6">
        
        {/* Title & Metadata Control Row */}
        <div className="space-y-4">
          <input
            type="text"
            value={activeNote.title}
            onChange={(e) => onUpdateField('title', e.target.value)}
            placeholder="Note Title"
            className="w-full text-2xl md:text-3xl font-bold tracking-tight text-ink border-0 border-b border-transparent focus:border-hairline focus:outline-none pb-2"
            id="note-title-input"
          />

          <div className="flex flex-wrap items-center gap-4 text-xs text-muted pb-4 border-b border-hairline">
            <div className="flex items-center space-x-1">
              <span className="font-semibold">Last updated:</span>
              <span>{formatDate(activeNote.updatedAt)}</span>
            </div>
            <div className="flex items-center space-x-1">
              <span className="font-semibold">Created:</span>
              <span>{formatDate(activeNote.createdAt)}</span>
            </div>
          </div>
        </div>

        {/* Tag Picker Row */}
        <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4 py-2">
          <div className="flex items-center space-x-3">
            <span className="text-xs font-semibold uppercase tracking-wider text-muted">Tag:</span>
            <div className="flex flex-wrap gap-2">
              {(['none', 'orange', 'pink', 'violet', 'emerald'] as const).map((tag) => (
                <button
                  key={tag}
                  onClick={() => onUpdateField('colorTag', tag)}
                  className={`px-2.5 py-1 text-xs font-semibold rounded-md border transition-all cursor-pointer ${
                    activeNote.colorTag === tag
                      ? `${tagColorMap[tag]} ring-2 ring-primary/20 scale-105`
                      : 'bg-canvas text-muted hover:text-ink border-hairline'
                  }`}
                >
                  {tagLabelMap[tag]}
                </button>
              ))}
            </div>
          </div>

          <button
            onClick={() => onDeleteNote(activeNote.id)}
            className="inline-flex items-center text-xs font-semibold text-error hover:text-red-700 transition-colors self-start sm:self-center cursor-pointer"
            id="btn-delete-note"
          >
            <svg className="w-4 h-4 mr-1.5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16" />
            </svg>
            Delete Note
          </button>
        </div>

        {/* Note Content Textarea Editor */}
        <div className="flex-1 flex flex-col">
          <textarea
            value={activeNote.content}
            onChange={(e) => onUpdateField('content', e.target.value)}
            placeholder="Start typing your thoughts here..."
            className="w-full flex-1 resize-none bg-canvas text-ink text-sm md:text-base leading-relaxed focus:outline-none"
            id="note-content-textarea"
          />
        </div>

      </div>
    </section>
  );
}
