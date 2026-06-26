interface Note {
  id: string;
  title: string;
  content: string;
  createdAt: string;
  updatedAt: string;
  colorTag: 'orange' | 'pink' | 'violet' | 'emerald' | 'none';
}

interface NoteItemProps {
  note: Note;
  isActive: boolean;
  onSelect: (id: string) => void;
  formatDate: (isoString: string) => string;
  tagLabelMap: Record<Note['colorTag'], string>;
}

export default function NoteItem({ note, isActive, onSelect, formatDate, tagLabelMap }: NoteItemProps) {
  return (
    <div
      onClick={() => onSelect(note.id)}
      className={`p-4 rounded-lg border transition-all cursor-pointer relative ${
        isActive
          ? 'bg-canvas border-primary shadow-sm ring-1 ring-primary/10'
          : 'bg-canvas border-hairline hover:border-muted'
      }`}
    >
      <div className="flex items-start justify-between space-x-2 mb-1.5">
        <h3 className="font-semibold text-sm line-clamp-1 text-ink">
          {note.title.trim() || 'Untitled Note'}
        </h3>
        {note.colorTag !== 'none' && (
          <span className={`w-2.5 h-2.5 rounded-full shrink-0 ${
            note.colorTag === 'orange' ? 'bg-badge-orange' :
            note.colorTag === 'pink' ? 'bg-badge-pink' :
            note.colorTag === 'violet' ? 'bg-badge-violet' :
            'bg-badge-emerald'
          }`} />
        )}
      </div>
      
      <p className="text-xs text-muted line-clamp-2 mb-3">
        {note.content.trim() || 'No additional content'}
      </p>

      <div className="flex items-center justify-between text-[11px] text-muted-soft">
        <span>{formatDate(note.updatedAt)}</span>
        {note.colorTag !== 'none' && (
          <span className="px-2 py-0.5 rounded-full bg-surface-card border border-hairline text-muted font-medium">
            {tagLabelMap[note.colorTag]}
          </span>
        )}
      </div>
    </div>
  );
}
