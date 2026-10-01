import {
  categoryLabels,
  importanceLabels,
} from "../types/document";
import type { DocumentRecord } from "../types/document";

interface Props {
  documents: DocumentRecord[];
}

export default function DocumentTable({ documents }: Props) {
  if (documents.length === 0) {
    return <p>Nav dokumentu, ko parādīt.</p>;
  }

  return (
    <div className="table-container">
      <table>
        <thead>
          <tr>
            <th scope="col">Nosaukums un apraksts</th>
            <th scope="col">Atbildīgā struktūrvienība</th>
            <th scope="col">Izveides datums</th>
            <th scope="col">Faila tips</th>
            <th scope="col">Aptuvenais lasīšanas laiks</th>
            <th scope="col">Svarīguma līmenis</th>
            <th scope="col">Kategorija</th>
            <th scope="col">Aktīvs statuss</th>
          </tr>
        </thead>

        <tbody>
          {documents.map((document) => (
            <tr key={document.id}>
              <td>
                <a
                  href={document.url}
                  target="_blank"
                  rel="noopener noreferrer"
                >
                  {document.title}
                </a>
                <p className="description">{document.description}</p>
              </td>

              <td>{document.responsible_unit}</td>

              <td>
                {new Date(document.created_at).toLocaleDateString(
                  "lv-LV",
                  { timeZone: "UTC" },
                )}
              </td>

              <td>{document.file_type.toUpperCase()}</td>
              <td>{document.reading_time_minutes} min</td>
              <td>{importanceLabels[document.importance]}</td>
              <td>{categoryLabels[document.category]}</td>
              <td>{document.active ? "Jā" : "Nē"}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}