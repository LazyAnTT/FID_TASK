import {
  categoryLabels,
  importanceLabels,
} from "../types/document";

export interface FilterValues {
  search: string;
  importance: string;
  category: string;
  active: string;
  sort: string;
  order: string;
}

interface Props {
  filters: FilterValues;
  onChange: (filters: FilterValues) => void;
}

export default function DocumentFilters({ filters, onChange }: Props) {
  return (
    <div className="filters">
      <div className="search-field">
        <label htmlFor="search">Meklēt nosaukumā vai aprakstā</label>
        <input
          id="search"
          type="search"
          value={filters.search}
          onChange={(event) =>
            onChange({ ...filters, search: event.target.value })
          }
        />
      </div>

      <div>
        <label htmlFor="importance">Svarīguma līmenis</label>
        <select
          id="importance"
          value={filters.importance}
          onChange={(event) =>
            onChange({ ...filters, importance: event.target.value })
          }
        >
          <option value="">Visi</option>
          {Object.entries(importanceLabels).map(([value, label]) => (
            <option key={value} value={value}>
              {label}
            </option>
          ))}
        </select>
      </div>

      <div>
        <label htmlFor="category">Kategorija</label>
        <select
          id="category"
          value={filters.category}
          onChange={(event) =>
            onChange({ ...filters, category: event.target.value })
          }
        >
          <option value="">Visas</option>
          {Object.entries(categoryLabels).map(([value, label]) => (
            <option key={value} value={value}>
              {label}
            </option>
          ))}
        </select>
      </div>

      <div>
        <label htmlFor="active">Aktīvs statuss</label>
        <select
          id="active"
          value={filters.active}
          onChange={(event) =>
            onChange({ ...filters, active: event.target.value })
          }
        >
          <option value="">Visi</option>
          <option value="true">Jā</option>
          <option value="false">Nē</option>
        </select>
      </div>

      <div>
        <label htmlFor="sort">Kārtot pēc</label>
        <select
          id="sort"
          value={filters.sort}
          onChange={(event) =>
            onChange({ ...filters, sort: event.target.value })
          }
        >
          <option value="created_at">Izveides datuma</option>
          <option value="title">Nosaukuma</option>
          <option value="reading_time_minutes">Lasīšanas laika</option>
        </select>
      </div>

      <div>
        <label htmlFor="order">Secība</label>
        <select
          id="order"
          value={filters.order}
          onChange={(event) =>
            onChange({ ...filters, order: event.target.value })
          }
        >
          <option value="asc">Augoša</option>
          <option value="desc">Dilstoša</option>
        </select>
      </div>
    </div>
  );
}