// POST /api/uploads/sign — issues ONE short-lived presigned PUT URL for ONE file, into a PRIVATE Vercel Blob store.
// The browser uploads straight to storage; files never pass through this function, never reach GitHub,
// and are never publicly readable (private store: every read needs a token or a signed GET URL).
import { enabled, allowedOrigin, safeName, MAX_BYTES, MAX_INDEX, TYPES, ENQUIRY_ID } from './_rules.js';

export default async function handler(req, res) {
  res.setHeader('Cache-Control', 'no-store');
  res.setHeader('X-Robots-Tag', 'noindex');
  if (req.method !== 'POST') { res.status(405).json({ error: 'method' }); return; }
  if (!enabled()) { res.status(503).json({ error: 'uploads-not-enabled' }); return; }
  if (!allowedOrigin(req.headers.origin)) { res.status(403).json({ error: 'origin' }); return; }

  const b = typeof req.body === 'string' ? JSON.parse(req.body || '{}') : (req.body || {});
  const index = Number(b.index), size = Number(b.size);
  const { ext, file } = safeName(b.name);
  const type = TYPES[ext];
  if (!ENQUIRY_ID.test(String(b.enquiry || ''))) { res.status(400).json({ error: 'enquiry' }); return; }
  if (!Number.isInteger(index) || index < 1 || index > MAX_INDEX) { res.status(400).json({ error: 'index' }); return; }
  if (!type || (b.type && b.type !== type && !(ext === 'jpg' && b.type === 'image/jpeg'))) { res.status(415).json({ error: 'type' }); return; }
  if (!Number.isFinite(size) || size < 1 || size > MAX_BYTES) { res.status(413).json({ error: 'size' }); return; }

  const month = new Date().toISOString().slice(0, 7);
  const pathname = `enquiries/${month}/${b.enquiry}/${String(index).padStart(2, '0')}-${file}`;

  let blob;
  try { blob = await import('@vercel/blob'); } catch { res.status(503).json({ error: 'sdk-missing' }); return; }
  if (typeof blob.issueSignedToken !== 'function' || typeof blob.presignUrl !== 'function') { res.status(503).json({ error: 'sdk-too-old' }); return; }

  try {
    const validUntil = Date.now() + 10 * 60 * 1000;
    const token = await blob.issueSignedToken({
      pathname, operations: ['put'], allowedContentTypes: [type], maximumSizeInBytes: size, validUntil,
    });
    const { presignedUrl } = await blob.presignUrl(token, {
      operation: 'put', pathname, access: 'private', allowedContentTypes: [type], maximumSizeInBytes: size,
      addRandomSuffix: false, allowOverwrite: false, validUntil,
    });
    res.status(200).json({ url: presignedUrl, pathname, expires: validUntil });
  } catch (e) {
    console.error('sign failed', e && e.message);
    res.status(502).json({ error: 'storage' });
  }
}
