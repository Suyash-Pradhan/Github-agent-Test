import NoteItem from './NoteItem';

interface Note {
  id: string;
  title: string;
  content: string;
  createdAt: string;
  updatedAt: string;
  colorTag: 'orange' | 'pink' | 'violet' | 'emerald' | 'none';
}

interface SidebarProps {
  notes: Note[];
  activeNoteId: string | null;
  onSelectNote: (id: string) => void;
  searchQuery: string;
  onSearchChange: (query: string) => void;
  selectedTagFilter: 'all' | Note['colorTag'];
  onTagFilterChange: (tag: 'all' | Note['colorTag']) => void;
  onCreateNote: () => void;
  formatDate: (isoString: string) => string;
  tagLabelMap: Record<Note['colorTag'], string>;
}

export default function Sidebar({
  notes,
  activeNoteId,
  onSelectNote,
  searchQuery,
  onSearchChange,
  selectedTagFilter,
  onTagFilterChange,
  onCreateNote,
  formatDate,
  tagLabelMap
}: SidebarProps) {
  return (
    <section className="w-full md:w-80 lg:w-96 border-r border-hairline flex flex-col bg-surface-soft shrink-0">
      {/* Search Box */}
      <div className="p-4 border-b border-hairline bg-canvas">
        <div className="relative">
          <span className="absolute inset-y-0 left-0 flex items-center pl-3 text-muted">
            <svg className="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path strokeLinecap="round" strokeLinejoin="round" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
            </svg>
          </span>
          <input
            type="text"
            value={searchQuery}
            onChange={(e) => onSearchChange(e.target.value)}
            placeholder="Search notes..."
            className="w-full pl-9 pr-4 py-2 bg-canvas text-ink text-sm rounded-md border border-hairline focus:border-primary focus:outline-none transition-colors"
            id="search-input"
          />
        </div>
      </div>

      {/* Filter Pills Category Switcher */}
      <div className="p-4 bg-canvas border-b border-hairline overflow-x-auto shrink-0 flex items-center space-x-2 scrollbar-none">
        {(['all', 'none', 'orange', 'pink', 'violet', 'emerald'] as const).map((tag) => (
          <button
            key={tag}
            onClick={() => onTagFilterChange(tag)}
            className={`px-3 py-1.5 text-xs font-semibold rounded-pill transition-colors cursor-pointer border shrink-0 ${
              selectedTagFilter === tag
                ? 'bg-primary text-on-primary border-primary'
                : 'bg-surface-card text-muted hover:text-ink border-hairline'
            }`}
          >
            {tag === 'all' ? 'All' : tagLabelMap[tag]}
          </button>
        ))}
      </div>

      {/* Notes List Scroll Container */}
      <div className="flex-1 overflow-y-auto p-4 space-y-3">
        {notes.length === 0 ? (
          <div className="text-center py-12 px-4">
            <p className="text-sm text-muted">No notes found.</p>
            <button
              onClick={onCreateNote}
              className="mt-3 text-xs font-semibold text-primary hover:underline cursor-pointer"
            >
              Create one now
            </button>
          </div>
        ) : (
          notes.map((note) => (
            <NoteItem
              key={note.id}
              note={note}
              isActive={note.id === activeNoteId}
              onSelect={onSelectNote}
              formatDate={formatDate}
              tagLabelMap={tagLabelMap}
            />
          ))
        )}
      </div>
    </section>
  );
}
