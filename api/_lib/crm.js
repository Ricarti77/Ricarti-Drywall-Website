// CRM preparation. Builds the normalized enquiry record and the mappings a future GoHighLevel / JobTread connector
// would send. NOTHING is sent to any CRM: dispatch() only runs when CRM_PROVIDER is set AND the owner has approved
// and configured that integration (Task 012 and later).
import { parseLocation, route } from './region.js';

export function record(d, extra) {
  const location = parseLocation(d.project.location);
  const routing = route(location);
  const [first, ...rest] = d.contact.name.split(/\s+/);
  return {
    schema: 'ricarti.enquiry.v2', id: d.id, received_at: new Date().toISOString(),
    customer_type: d.customer_type, classification: d.customer_type === 'builder' ? 'b2b-builder' : 'b2c-homeowner',
    contact: { ...d.contact, first_name: first || '', last_name: rest.join(' ') },
    project: { ...d.project, location, routing }, services: d.services, preferred_language: d.preferred_language,
    consent: { marketing_opt_in: d.marketing_opt_in, privacy_notice: 'shown', captured_at: new Date().toISOString(), source: 'website-estimate-form' },
    lead_source: d.lead_source, attachments: d.attachments, attachments_not_received: d.attachments_not_received,
    delivery: extra || {},
  };
}

// GoHighLevel (LeadConnector API v2) shapes. Field names to be confirmed against the purchased plan in Task 012.
export function toGoHighLevel(rec) {
  const tags = ['website-enquiry', rec.classification, 'region-' + rec.project.routing.region, 'lang-' + rec.preferred_language,
    ...rec.services.map((s) => 'service-' + s), rec.consent.marketing_opt_in ? 'marketing-opt-in' : 'marketing-no-consent'];
  return {
    contact: {
      firstName: rec.contact.first_name, lastName: rec.contact.last_name, email: rec.contact.email, phone: rec.contact.phone,
      companyName: rec.contact.company, address1: rec.project.location.raw, city: rec.project.location.city, state: rec.project.location.province,
      postalCode: rec.project.location.postal_code, country: rec.project.location.country || 'CA', source: 'Website estimate form', tags,
      customFields: { enquiry_reference: rec.id, customer_type: rec.customer_type, project_type: rec.project.type, timeline: rec.project.timeline,
        preferred_language: rec.preferred_language, marketing_consent: rec.consent.marketing_opt_in ? 'yes' : 'no', marketing_consent_at: rec.consent.captured_at },
    },
    opportunity: {
      name: rec.id + ' · ' + (rec.customer_type === 'builder' ? (rec.contact.company || rec.contact.name) : rec.contact.name),
      pipelineKey: rec.customer_type === 'builder' ? 'builders' : 'homeowners', regionKey: rec.project.routing.region,
      stage: 'new-enquiry', status: 'open', source: 'website',
    },
    note: rec.project.description,
  };
}

// JobTread: customer + job draft, for when an approved estimate becomes a job (future).
export function toJobTread(rec) {
  return { customer: { name: rec.contact.company || rec.contact.name, type: rec.customer_type, email: rec.contact.email, phone: rec.contact.phone },
    job: { name: rec.id, address: rec.project.location.raw, city: rec.project.location.city, province: rec.project.location.province,
      postalCode: rec.project.location.postal_code, description: rec.project.description } };
}

export async function dispatch(rec) {
  const provider = (process.env.CRM_PROVIDER || '').trim();
  if (!provider) return { crm: 'disabled' };
  return { crm: 'not-implemented', provider };   // connectors are added only after owner approval (Task 012)
}
