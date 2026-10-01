import { useEffect, useState } from "react";
import DocumentFilters, {
  type FilterValues,
} from "./components/DocumentFilters";

import { getDocuments } from "./api/documents";
import DocumentTable from "./components/DocumentTable";
import type { DocumentRecord } from "./types/document";

const initialFilters: FilterValues = {
  search: "",
  importance: "",
  category: "",
  active: "",
  sort: "created_at",
  order: "desc",
};

export default function App() {
  const [documents, setDocuments] = useState<DocumentRecord[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");
  const [filters, setFilters] = useState<FilterValues>(initialFilters);

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
  const searchText = filters.search.trim().toLocaleLowerCase("lv");

const visibleDocuments = documents
  .filter((document) => {
    const matchesSearch =
      document.title.toLocaleLowerCase("lv").includes(searchText) ||
      document.description.toLocaleLowerCase("lv").includes(searchText);

    const matchesImportance =
      filters.importance === "" ||
      document.importance === filters.importance;

    const matchesCategory =
      filters.category === "" ||
      document.category === filters.category;

    const matchesActive =
      filters.active === "" ||
      document.active === (filters.active === "true");

    return (
      matchesSearch &&
      matchesImportance &&
      matchesCategory &&
      matchesActive
    );
  })
  .sort((first, second) => {
    let comparison: number;

    switch (filters.sort) {
      case "title":
        comparison = first.title.localeCompare(second.title, "lv");
        break;

      case "reading_time_minutes":
        comparison =
          first.reading_time_minutes - second.reading_time_minutes;
        break;

      default:
        comparison = first.created_at.localeCompare(second.created_at);
    }

    return filters.order === "asc" ? comparison : -comparison;
  });

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
    <DocumentFilters filters={filters} onChange={setFilters} />

    <button type="button" onClick={() => setFilters(initialFilters)}>
      Atiestatīt filtrus
    </button>

    <p>
      Parādīti {visibleDocuments.length} no {documents.length} dokumentiem
    </p>

    <DocumentTable documents={visibleDocuments} />
  </>
)}
    </main>
  );
}