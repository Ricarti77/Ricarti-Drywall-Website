// GET /api/uploads/config — tells the estimate page whether private uploads are switched on. No secrets returned.
import { enabled, MAX_BYTES, MAX_INDEX, TYPES } from './_rules.js';

export default function handler(req, res) {
  res.setHeader('Cache-Control', 'no-store');
  res.setHeader('X-Robots-Tag', 'noindex');
  if (req.method !== 'GET') { res.status(405).json({ error: 'method' }); return; }
  const on = enabled();
  res.status(200).json(on
    ? { enabled: true, storage: 'vercel-blob-private', maxBytes: MAX_BYTES, maxFiles: MAX_INDEX, types: Object.keys(TYPES) }
    : { enabled: false, reason: 'private-storage-not-configured' });
}
