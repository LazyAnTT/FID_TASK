import { useEffect, useState } from "react";

import { getDocuments } from "./api/documents";
import DocumentTable from "./components/DocumentTable";
import type { DocumentRecord } from "./types/document";

export default function App() {
  const [documents, setDocuments] = useState<DocumentRecord[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  useEffect(() => {
    const controller = new AbortController();

    async function loadDocuments() {
      try {
        const data = await getDocuments(controller.signal);

        if (!controller.signal.aborted) {
          setDocuments(data);
        }
      } catch {
        if (!controller.signal.aborted) {
          setError(
            "Neizdevās ielādēt dokumentus. Pārbaudiet, vai API darbojas.",
          );
        }
      } finally {
        if (!controller.signal.aborted) {
          setLoading(false);
        }
      }
    }

    loadDocuments();

    return () => controller.abort();
  }, []);

  return (
    <main>
      <h1>Dokumentu katalogs</h1>
      <p>Organizācijas dokumentu dati</p>

      {loading && <p role="status">Ielādē dokumentus...</p>}

      {error && (
        <p className="error" role="alert">
          {error}
        </p>
      )}

      {!loading && !error && (
        <>
          <p>Dokumentu skaits: {documents.length}</p>
          <DocumentTable documents={documents} />
        </>
      )}
    </main>
  );
}