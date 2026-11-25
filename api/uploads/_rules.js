// Shared limits for enquiry uploads. Keep in step with /estimate (build/estimate.js).
export const MAX_BYTES = 50 * 1024 * 1024;        // per file
export const MAX_INDEX = 20;                       // files per enquiry (index 1..20)
export const TYPES = {
  pdf: 'application/pdf', jpg: 'image/jpeg', jpeg: 'image/jpeg', png: 'image/png',
  webp: 'image/webp', heic: 'image/heic', heif: 'image/heif',
};
export const ENQUIRY_ID = /^RD-\d{6}-[A-Z2-9]{5}$/;

// Uploads are off unless the owner has created a PRIVATE Vercel Blob store, connected it to this project
// (which adds BLOB_READ_WRITE_TOKEN, or BLOB_STORE_ID for OIDC) and set RD_UPLOADS_ENABLED=true.
export function enabled() {
  const on = String(process.env.RD_UPLOADS_ENABLED || '').toLowerCase() === 'true';
  const cred = !!(process.env.BLOB_READ_WRITE_TOKEN || process.env.BLOB_STORE_ID);
  return on && cred;
}

// Only pages on our own domains may ask for upload URLs.
export function allowedOrigin(origin) {
  if (!origin) return false;
  try {
    const h = new URL(origin).hostname;
    const extra = String(process.env.RD_ALLOWED_HOSTS || '').split(',').map((s) => s.trim()).filter(Boolean);
    return h === 'ricartidrywall.ca' || h === 'www.ricartidrywall.ca' || /^ricarti-drywall-website-[a-z0-9-]+\.vercel\.app$/.test(h) || extra.includes(h);
  } catch { return false; }
}

export function safeName(name) {
  const base = String(name || 'file').normalize('NFKD').replace(/[̀-ͯ]/g, '');
  const m = /\.([a-z0-9]+)$/i.exec(base);
  const ext = m ? m[1].toLowerCase() : '';
  const stem = base.replace(/\.[^.]*$/, '').replace(/[^A-Za-z0-9._-]+/g, '-').replace(/^-+|-+$/g, '').slice(0, 60) || 'file';
  return { ext, file: stem + (ext ? '.' + ext : '') };
}
