import { useState, useEffect, useMemo, useTransition } from 'react'
import Header from './components/Header'
import Sidebar from './components/Sidebar'
import NoteEditor from './components/NoteEditor'
import {formatCount, formatDate} from "./utils/formState.ts"

interface Note {
  id: string;
  title: string;
  content: string;
  createdAt: string; // ISO string
  updatedAt: string; // ISO string
  colorTag: 'orange' | 'pink' | 'violet' | 'emerald' | 'none';
}

const STORAGE_KEY = 'noteworthy_notes_v1';

const DEFAULT_NOTES: Note[] = [
  {
    id: '1',
    title: '🚀 Getting Started with Noteworthy',
    content: 'Welcome to your new notes app!\n\nHere are a few things you can do:\n- Add a new note using the "New Note" button at the top.\n- Edit the title and body of any note on the right pane.\n- Categorize your thoughts by selecting a color tag.\n- Use the search bar to find notes quickly.\n- Filter your list using the category pills below the search.\n\nAll your notes are saved automatically in your browser\'s localStorage, so they will persist even if you refresh the page.',
    createdAt: new Date().toISOString(),
    updatedAt: new Date().toISOString(),
    colorTag: 'emerald'
  },
  {
    id: '2',
    title: '📝 Ideas for project expansion',
    content: '- Add markdown rendering support for beautiful text formatting.\n- Support light and dark theme mode switches.\n- Implement pinning/starring notes to keep key thoughts at the top.\n- Export notes as TXT or Markdown files.',
    createdAt: new Date(Date.now() - 3600000).toISOString(),
    updatedAt: new Date(Date.now() - 3600000).toISOString(),
    colorTag: 'violet'
  }
];

export default function App() {
  // Lazy state initialization to read from localStorage without computing on every render
  const [notes, setNotes] = useState<Note[]>(() => {
    try {
      const stored = localStorage.getItem(STORAGE_KEY);
      return stored ? JSON.parse(stored) : DEFAULT_NOTES;
    } catch (e) {
      console.error('Failed to parse notes from localStorage:', e);
      return DEFAULT_NOTES;
    }
  });

  const [activeNoteId, setActiveNoteId] = useState<string | null>(() => {
    const stored = localStorage.getItem(STORAGE_KEY);
    try {
      const initialNotes = stored ? JSON.parse(stored) as Note[] : DEFAULT_NOTES;
      return initialNotes.length > 0 ? initialNotes[0].id : null;
    } catch {
      return DEFAULT_NOTES.length > 0 ? DEFAULT_NOTES[0].id : null;
    }
  });

  const [searchQuery, setSearchQuery] = useState('');
  const [selectedTagFilter, setSelectedTagFilter] = useState<'all' | Note['colorTag']>('all');
  const [, startTransition] = useTransition();

  // Save notes to localStorage whenever they change
  useEffect(() => {
    localStorage.setItem(STORAGE_KEY, JSON.stringify(notes));
  }, [notes]);

  // Derived state: active note object
  const activeNote = useMemo(() => {
    return notes.find(note => note.id === activeNoteId) || null;
  }, [notes, activeNoteId]);

  // Derived state: filtered and searched notes
  const filteredNotes = useMemo(() => {
    return notes.filter(note => {
      const matchesSearch =
        note.title.toLowerCase().includes(searchQuery.toLowerCase()) ||
        note.content.toLowerCase().includes(searchQuery.toLowerCase());
      const matchesTag = selectedTagFilter === 'all' || note.colorTag === selectedTagFilter;
      return matchesSearch && matchesTag;
    });
  }, [notes, searchQuery, selectedTagFilter]);

  // Handler: create a new note
  const handleCreateNote = () => {
    const newNote: Note = {
      id: crypto.randomUUID(),
      title: 'Untitled Note',
      content: '',
      createdAt: new Date().toISOString(),
      updatedAt: new Date().toISOString(),
      colorTag: 'none'
    };
    setNotes(prev => [newNote, ...prev]);
    setActiveNoteId(newNote.id);
  };

  // Handler: update active note field
  const handleUpdateNoteField = (field: keyof Pick<Note, 'title' | 'content' | 'colorTag'>, value: string) => {
    if (!activeNoteId) return;
    setNotes(prev =>
      prev.map(note =>
        note.id === activeNoteId
          ? { ...note, [field]: value, updatedAt: new Date().toISOString() }
          : note
      )
    );
  };

  // Handler: delete a note
  const handleDeleteNote = (id: string) => {
    setNotes(prev => {
      const remaining = prev.filter(note => note.id !== id);
      if (activeNoteId === id) {
        setActiveNoteId(remaining.length > 0 ? remaining[0].id : null);
      }
      return remaining;
    });
  };

  // Format date helper
  // const formatDate = (isoString: string) => {
  //   const date = new Date(isoString);
  //   return date.toLocaleDateString(undefined, {
  //     month: 'short',
  //     day: 'numeric',
  //     hour: '2-digit',
  //     minute: '2-digit'
  //   });
  // };

  // Map tag names to color classes for pills
  const tagColorMap = {
    none: 'bg-surface-strong text-ink border-hairline',
    orange: 'bg-badge-orange/20 text-ink border-badge-orange/40',
    pink: 'bg-badge-pink/20 text-ink border-badge-pink/40',
    violet: 'bg-badge-violet/20 text-ink border-badge-violet/40',
    emerald: 'bg-badge-emerald/20 text-ink border-badge-emerald/40',
  };

  const tagLabelMap = {
    none: 'No Tag',
    orange: 'Work',
    pink: 'Personal',
    violet: 'Ideas',
    emerald: 'Todo',
  };

  return (
    <div className="flex flex-col min-h-screen bg-canvas text-ink font-sans selection:bg-primary selection:text-on-primary">
      {/* Top Header Component */}
      <Header onCreateNote={handleCreateNote} />

      {/* Main Workspace split */}
      <main className="flex-1 flex flex-col md:flex-row max-w-350 w-full mx-auto">

        {/* Left Panel: Sidebar Component */}
        <Sidebar
          notes={filteredNotes}
          activeNoteId={activeNoteId}
          onSelectNote={setActiveNoteId}
          searchQuery={searchQuery}
          onSearchChange={(query) => startTransition(() => setSearchQuery(query))}
          selectedTagFilter={selectedTagFilter}
          onTagFilterChange={setSelectedTagFilter}
          onCreateNote={handleCreateNote}
          formatDate={formatDate}
          tagLabelMap={tagLabelMap}
        />

        {/* Right Panel: Detail Editor Component */}
        <NoteEditor
          activeNote={activeNote}
          onUpdateField={handleUpdateNoteField}
          onDeleteNote={handleDeleteNote}
          onCreateNote={handleCreateNote}
          formatDate={formatDate}
          tagColorMap={tagColorMap}
          tagLabelMap={tagLabelMap}
        />
        

        // somewhere in JSX:
        <p>Followers: {formatCount(1500)}</p>       {/* shows 1.5k — correct-ish */}
        <p>Joined: {formatDate("2026-06-28")}</p>   {/* shows 2024-2-15 — wrong month */}
      </main>

      {/* Dark Footer */}
      <footer className="bg-surface-dark text-on-dark-soft text-xs py-4 px-6 mt-auto border-t border-surface-dark-elevated">
        <div className="max-w-350 mx-auto flex flex-col sm:flex-row items-center justify-between gap-2">
          <div className="flex items-center space-x-2">
            <span className="font-bold text-on-dark">Noteworthy</span>
            <span className="text-muted-soft">|</span>
            <span>{notes.length} {notes.length === 1 ? 'note' : 'notes'} stored locally</span>
          </div>
          <div className="flex items-center space-x-1.5 text-muted-soft">
            <div className="w-1.5 h-1.5 rounded-full bg-success animate-pulse" />
            <span>Autosaved in local storage</span>
          </div>
        </div>
      </footer>
    </div>
  );
}
