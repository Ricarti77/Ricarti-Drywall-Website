# Ricarti Drywall — portfolio content

`projects.json` is the single source for every project and photo on the site:
the "Selected Projects" portfolio, each project's gallery, and the site-wide photo album.
Nothing in the page code needs to change to add a project or swap a photo.

## Add or change a project
1. Put the photos in `/images` (web size: 900×1600 JPG, metadata stripped).
   Keep the original high-resolution files outside the public repository.
2. Add a cover: a 4:5 crop saved as `pf-<id>.jpg` (1000 px wide) and `pf-<id>-600.jpg` (600 px wide).
3. Add an entry to `projects` in `projects.json`. The order in the file is the order on the site.
4. Rebuild (`make.sh`). English and Portuguese pages, the gallery and the filters update automatically.

## Fields
| Field | Shown on site | Notes |
|---|---|---|
| `name` | yes | Street name only. **Never a house number.** |
| `location.neighbourhood`, `location.city` | yes, when filled | Leave `null` until confirmed. |
| `project_type` | yes, when filled | e.g. Custom home, Renovation. `null` until confirmed. |
| `services_performed` | yes, when filled | Only services Ricarti actually performed. `null` until confirmed. |
| `builder`, `client_type`, `year` | not yet | Kept for later; never shown unless confirmed and approved. |
| `documented_work` | yes ("Work documented") + filters | Only work visible in the project photos. Keys: `custom-homes`, `renovation`, `commercial`, `architectural`, `insulation`, `drywall-finishing`. |
| `cover` | yes | Cover file names + alt text in `en` and `pt`. |
| `photos` | gallery + album | Each photo: `file` + `caption` in `en` and `pt`. |
| `published` | — | `false` hides a project everywhere without deleting it. |

Filters appear only for categories that at least one published project supports.

## Future CMS
The file is plain JSON with a fixed structure, ready to be edited by a Git-based CMS
(for example Decap CMS or TinaCMS) without touching code. Not implemented yet.
