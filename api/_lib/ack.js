// Customer acknowledgement email in the visitor's language (EN, PT, ES, FR, IT). Kept deliberately short: it
// confirms receipt and the reference, repeats no project details, makes no promise about response times, and
// carries no links. The slogan stays in English in every language. Replies go to the office mailbox.
import { C, SANS, SERIF, esc, layout, paragraph } from './brand.js';

const T = {
  'en-CA': {
    refLabel: 'Your reference',
    subject: 'We received your estimate request — {ref}',
    hello: 'Hello {name},',
    body: [
      'Thank you for contacting Ricarti Drywall. We have received your estimate request.',
      'Your reference is {ref}. We will review the details and reply to this email address.',
      'If you would like to add anything, simply reply to this email and keep the reference in the subject line.',
    ],
    auto: 'This is an automatic confirmation. If you did not send this request, you can ignore this email.',
  },
  'pt-BR': {
    refLabel: 'Sua referência',
    subject: 'Recebemos seu pedido de orçamento — {ref}',
    hello: 'Olá, {name},',
    body: [
      'Obrigado por entrar em contato com a Ricarti Drywall. Recebemos seu pedido de orçamento.',
      'Sua referência é {ref}. Vamos analisar os detalhes e responder para este endereço de e-mail.',
      'Se quiser acrescentar alguma informação, basta responder a este e-mail mantendo a referência no assunto.',
    ],
    auto: 'Esta é uma confirmação automática. Se você não enviou este pedido, pode ignorar este e-mail.',
  },
  'es-419': {
    refLabel: 'Su referencia',
    subject: 'Recibimos su solicitud de presupuesto — {ref}',
    hello: 'Hola, {name}:',
    body: [
      'Gracias por comunicarse con Ricarti Drywall. Hemos recibido su solicitud de presupuesto.',
      'Su referencia es {ref}. Revisaremos los detalles y le responderemos a esta dirección de correo electrónico.',
      'Si desea agregar algo, simplemente responda a este correo y conserve la referencia en el asunto.',
    ],
    auto: 'Esta es una confirmación automática. Si usted no envió esta solicitud, puede ignorar este correo.',
  },
  'fr-CA': {
    refLabel: 'Votre référence',
    subject: 'Nous avons reçu votre demande de soumission — {ref}',
    hello: 'Bonjour {name},',
    body: [
      'Merci d’avoir communiqué avec Ricarti Drywall. Nous avons bien reçu votre demande de soumission.',
      'Votre numéro de référence est {ref}. Nous examinerons les détails et vous répondrons à cette adresse courriel.',
      'Pour ajouter des renseignements, répondez simplement à ce courriel en conservant la référence dans l’objet.',
    ],
    auto: 'Ceci est une confirmation automatique. Si vous n’avez pas envoyé cette demande, vous pouvez ignorer ce courriel.',
  },
  'it-IT': {
    refLabel: 'Il Suo riferimento',
    subject: 'Abbiamo ricevuto la Sua richiesta di preventivo — {ref}',
    hello: 'Gentile {name},',
    body: [
      'grazie per aver contattato Ricarti Drywall. Abbiamo ricevuto la Sua richiesta di preventivo.',
      'Il Suo codice di riferimento è {ref}. Esamineremo i dettagli e Le risponderemo a questo indirizzo email.',
      'Se desidera aggiungere qualcosa, risponda semplicemente a questa email mantenendo il riferimento nell’oggetto.',
    ],
    auto: 'Questa è una conferma automatica. Se non ha inviato Lei questa richiesta, può ignorare questa email.',
  },
};

export function buildAck(rec) {
  const t = T[rec.preferred_language] || T['en-CA'];
  const name = String(rec.contact.name || '').trim().split(/\s+/)[0].slice(0, 60);
  const fill = (s) => s.replace('{ref}', rec.id).replace('{name}', name);
  const hello = fill(t.hello);
  const lines = t.body.map(fill);
  const lang = (rec.preferred_language || 'en').slice(0, 2);
  let h = '<tr><td style="padding:34px 32px 0 32px"><p style="margin:0;font-family:' + SERIF + ';font-size:24px;line-height:30px;color:' + C.ink + '">' + esc(hello) + '</p></td></tr>';
  h += paragraph(esc(lines[0]), { pad: '16px 32px 0 32px' });
  h += '<tr><td style="padding:22px 32px 0 32px"><table role="presentation" cellpadding="0" cellspacing="0" border="0"><tr>'
    + '<td bgcolor="#FFFFFF" style="background:#FFFFFF;border:1px solid ' + C.line + ';border-left:3px solid ' + C.bronze + ';padding:14px 20px">'
    + '<p style="margin:0 0 4px 0;font-family:' + SANS + ';font-size:11px;letter-spacing:2px;text-transform:uppercase;color:' + C.bronze + ';font-weight:bold">' + esc(t.refLabel) + '</p>'
    + '<p style="margin:0;font-family:' + SERIF + ';font-size:22px;line-height:28px;color:' + C.ink + '">' + esc(rec.id) + '</p></td></tr></table></td></tr>';
  const afterRef = lines[1].includes(rec.id + '. ') ? lines[1].split(rec.id + '. ').slice(1).join(rec.id + '. ') : lines[1];   // the box already shows the reference
  h += paragraph(esc(afterRef), { pad: '22px 32px 0 32px' });
  h += paragraph(esc(lines[2]));
  const html = layout({ lang, title: fill(t.subject), preheader: lines[0], body: h, footerNote: esc(t.auto) });
  const text = [hello, '', ...lines, '', 'RICARTI DRYWALL', 'Perfection Starts Here!', '', t.auto].join('\n');
  return { subject: fill(t.subject), html, text };
}
