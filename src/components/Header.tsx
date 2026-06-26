interface HeaderProps {
  onCreateNote: () => void;
}

export default function Header({ onCreateNote }: HeaderProps) {
  return (
    <header className="sticky top-0 z-30 flex items-center justify-between h-16 px-6 bg-canvas border-b border-hairline">
      <div className="flex items-center space-x-3">
        <div className="w-8 h-8 rounded-full bg-primary flex items-center justify-center text-on-primary font-bold">
          N
        </div>
        <span className="text-xl font-bold tracking-tight font-sans">Noteworthy</span>
      </div>

      <div className="flex items-center space-x-4">
        <button
          onClick={onCreateNote}
          className="flex items-center px-4 py-2 bg-primary hover:bg-primary-active text-on-primary font-medium text-sm rounded-md transition-colors shadow-sm cursor-pointer"
          id="btn-new-note"
        >
          <svg className="w-4 h-4 mr-2" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={2.5}>
            <path strokeLinecap="round" strokeLinejoin="round" d="M12 4v16m8-8H4" />
          </svg>
          New Note
        </button>
      </div>
    </header>
  );
}
