import json
from pathlib import Path
from textwrap import dedent

root = Path(r"C:\Users\linds\OneDrive\Bureau\Hotel de toulouse")
(root / "css").mkdir(exist_ok=True, parents=True)
(root / "images").mkdir(exist_ok=True, parents=True)

site_url = "https://www.exemple.fr"

nav_html = '''
<nav aria-label="Navigation principale" class="site-nav">
  <div class="nav-brand"><a href="/">Hôtel de Toulouse</a></div>
  <ul class="nav-list">
    <li><a href="/">Accueil</a></li>
    <li><a href="/chambres/">Chambres</a></li>
    <li class="has-submenu">
      <a href="/qui-sommes-nous/">L'hôtel</a>
      <ul class="submenu">
        <li><a href="/qui-sommes-nous/">Qui sommes-nous</a></li>
        <li><a href="/restaurant/">Restaurant</a></li>
        <li><a href="/spa/">Spa</a></li>
        <li><a href="/galerie-photos/">Galerie photos</a></li>
      </ul>
    </li>
    <li><a href="/salle-seminaire-besancon/">Séminaires et réunions</a></li>
    <li><a href="/tourisme-activites/">Tourisme et activités</a></li>
    <li><a href="/acces-contact/">Accès et contact</a></li>
  </ul>
  <a class="button button-primary" href="/reservation/">Réserver une chambre</a>
</nav>
'''

footer_html = '''
<footer class="site-footer">
  <div class="footer-inner">
    <div>
      <p class="footer-brand">Hôtel de Toulouse, Besançon</p>
    </div>
    <ul class="footer-links">
      <li><a href="/">Accueil</a></li>
      <li><a href="/chambres/">Chambres</a></li>
      <li><a href="/qui-sommes-nous/">L'hôtel</a></li>
      <li><a href="/restaurant/">Restaurant</a></li>
      <li><a href="/spa/">Spa</a></li>
      <li><a href="/galerie-photos/">Galerie photos</a></li>
      <li><a href="/salle-seminaire-besancon/">Séminaires et réunions</a></li>
      <li><a href="/tourisme-activites/">Tourisme et activités</a></li>
      <li><a href="/acces-contact/">Accès et contact</a></li>
      <li><a href="/salle-seminaire-besancon/">Demander un devis séminaire</a></li>
      <li><a href="/mentions-legales/">Mentions légales</a></li>
    </ul>
  </div>
</footer>
'''

faq_content = {
    "home": [
        ("L'hôtel est-il en plein centre-ville de Besançon ?", "Oui, l'Hôtel de Toulouse est un hôtel indépendant 3 étoiles de charme en plein centre-ville de Besançon."),
        ("Combien de chambres proposez-vous ?", "L'hôtel compte 50 chambres réparties en 6 catégories."),
        ("Disposez-vous d'un parking et de bornes de recharge ?", "Oui, le parking privé et sécurisé est disponible sur réservation et 2 bornes de recharge pour véhicules électriques sont à disposition.")
    ],
    "contact": [
        ("Comment réserver une chambre ?", "Vous pouvez réserver en direct via notre formulaire dédié ou nous contacter pour votre demande de séjour."),
        ("L'hôtel possède-t-il un parking ?", "Oui, un parking privé et sécurisé est proposé sur réservation."),
        ("Proposez-vous des salles pour des événements professionnels ?", "Oui, nous disposons de 2 salles pour événements professionnels, jusqu'à 20 personnes.")
    ],
    "seminaire": [
        ("Combien de personnes peuvent accueillir vos salles ?", "Nos 2 salles pour événements professionnels accueillent jusqu'à 20 personnes."),
        ("Proposez-vous l'hébergement ?", "Oui, le séminaire peut s'accompagner d'un hébergement sur place."),
        ("Le parking est-il disponible pour les séminaires ?", "Oui, un parking privé et sécurisé est disponible sur place pour les clients.")
    ]
}


def make_page(title, description, h1, breadcrumb, body_html, canonical_path, noindex=False, jsonld=''):
    body_html = dedent(body_html).strip()
    noindex_tag = '<meta name="robots" content="noindex">\n' if noindex else ''
    return f'''<!doctype html>
<html lang="fr">
  <head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>{title}</title>
    <meta name="description" content="{description}">
    <link rel="canonical" href="{site_url}{canonical_path}">
    <meta property="og:title" content="{title}">
    <meta property="og:description" content="{description}">
    <meta property="og:url" content="{site_url}{canonical_path}">
    <meta property="og:type" content="website">
    <meta property="og:locale" content="fr_FR">
    {noindex_tag}
    <link rel="stylesheet" href="/css/style.css">
    {jsonld}
  </head>
  <body>
    <a class="skip-link" href="#contenu">Aller au contenu</a>
    <header>
      {nav_html}
    </header>
    <main id="contenu">
      {breadcrumb}
      <section class="page-header">
        <h1>{h1}</h1>
      </section>
      {body_html}
    </main>
    {footer_html}
  </body>
</html>
'''


def breadcrumb_html(current):
    items = [{"label": "Accueil", "url": "/"}, {"label": current, "url": None}]
    html = '<nav class="breadcrumb" aria-label="Fil d’Ariane"><ol>'
    for item in items:
        if item["url"]:
            html += '<li><a href="{url}">{label}</a></li>'.format(url=item["url"], label=item["label"])
        else:
            html += '<li aria-current="page">{label}</li>'.format(label=item["label"])
    html += '</ol></nav>'
    return html


def faq_schema(faq_list):
    data = {
        "@context": "https://schema.org",
        "@type": "FAQPage",
        "mainEntity": [
            {
                "@type": "Question",
                "name": q,
                "acceptedAnswer": {"@type": "Answer", "text": a},
            }
            for q, a in faq_list
        ],
    }
    return '<script type="application/ld+json">' + json.dumps(data, ensure_ascii=False) + '</script>'


def hotel_schema():
    data = {
        "@context": "https://schema.org",
        "@type": "Hotel",
        "name": "Hôtel de Toulouse",
        "starRating": {"@type": "Rating", "ratingValue": "3"},
        "numberOfRooms": "50",
        "address": {"@type": "PostalAddress", "addressLocality": "Besançon", "addressCountry": "FR"},
        "url": "https://www.exemple.fr/",
        "amenityFeature": [
            {"@type": "LocationFeatureSpecification", "name": "Parking privé et sécurisé sur réservation"},
            {"@type": "LocationFeatureSpecification", "name": "Bornes de recharge pour véhicules électriques (2)"},
            {"@type": "LocationFeatureSpecification", "name": "Petit déjeuner"},
            {"@type": "LocationFeatureSpecification", "name": "Terrasse"},
        ],
    }
    return '<script type="application/ld+json">' + json.dumps(data, ensure_ascii=False) + '</script>'


def breadcrumb_schema(current_path):
    path = current_path.strip('/').split('/') if current_path.strip('/') else []
    items = []
    url = site_url
    for index, segment in enumerate(path, start=1):
        url = f"{url.rstrip('/')}/{segment}"
        label = segment.replace('-', ' ').replace('_', ' ')
        items.append({"position": index, "name": label, "item": url})
    if not items:
        return ''
    data = {"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": [{"@type": "ListItem", "position": item["position"], "name": item["name"], "item": item["item"]} for item in items]}
    return '<script type="application/ld+json">' + json.dumps(data, ensure_ascii=False) + '</script>'

# SVG placeholders
svg_defs = {
    "hotel-toulouse-besancon-facade": '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 800 520"><rect width="800" height="520" fill="#eef2f0"/><rect x="60" y="120" width="680" height="290" rx="10" fill="#d7c7b5"/><rect x="120" y="170" width="110" height="170" rx="8" fill="#b49a7e"/><rect x="245" y="170" width="110" height="170" rx="8" fill="#c9b8a0"/><rect x="370" y="170" width="110" height="170" rx="8" fill="#b49a7e"/><rect x="495" y="170" width="110" height="170" rx="8" fill="#c9b8a0"/><rect x="620" y="170" width="90" height="170" rx="8" fill="#b49a7e"/><rect x="110" y="80" width="580" height="50" rx="4" fill="#7b6f63"/><rect x="260" y="35" width="280" height="55" rx="5" fill="#9a8b7a"/><text x="400" y="270" text-anchor="middle" font-size="42" fill="#2f2a27" font-family="Arial">Hôtel de Toulouse</text></svg>''',
    "chambre-hotel-toulouse-besancon": '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 800 520"><rect width="800" height="520" fill="#f5f1eb"/><rect x="70" y="120" width="660" height="300" rx="10" fill="#d7c7b5"/><rect x="125" y="250" width="260" height="80" rx="10" fill="#a68966"/><rect x="440" y="250" width="220" height="80" rx="10" fill="#b79f7d"/><rect x="180" y="170" width="440" height="100" rx="8" fill="#ece4dc"/><rect x="260" y="140" width="280" height="55" rx="6" fill="#c9b895"/><text x="400" y="430" text-anchor="middle" font-size="32" fill="#2f2a27" font-family="Arial">Chambre de charme</text></svg>''',
    "jardin-terrasse-hotel-toulouse-besancon": '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 800 520"><rect width="800" height="520" fill="#edf4ee"/><rect x="70" y="300" width="660" height="150" rx="18" fill="#87a77a"/><rect x="80" y="210" width="200" height="120" rx="12" fill="#d1b48a"/><rect x="300" y="190" width="200" height="140" rx="12" fill="#d9c3a4"/><rect x="520" y="210" width="200" height="120" rx="12" fill="#d1b48a"/><circle cx="550" cy="120" r="70" fill="#f6d694"/><text x="400" y="455" text-anchor="middle" font-size="32" fill="#1e2b22" font-family="Arial">Jardin et terrasse</text></svg>''',
    "chambres-hotel-toulouse-besancon": '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 800 520"><rect width="800" height="520" fill="#f4efe9"/><rect x="120" y="130" width="560" height="220" rx="12" fill="#d8c3a8"/><rect x="185" y="185" width="200" height="120" rx="10" fill="#b19d8b"/><rect x="430" y="185" width="190" height="120" rx="10" fill="#c7b09c"/><rect x="265" y="105" width="270" height="50" rx="6" fill="#8a7d70"/><text x="400" y="430" text-anchor="middle" font-size="30" fill="#2d2825" font-family="Arial">Chambre d'hôtel</text></svg>''',
    "plan-acces-hotel-toulouse-besancon": '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 800 520"><rect width="800" height="520" fill="#f2f5f8"/><rect x="80" y="90" width="640" height="340" rx="20" fill="#dfe8ef"/><path d="M160 360 L260 200 L400 270 L560 140 L670 300" stroke="#6d8ca3" stroke-width="18" fill="none" stroke-linecap="round"/><circle cx="260" cy="200" r="25" fill="#8aa7bb"/><circle cx="560" cy="140" r="25" fill="#8aa7bb"/><circle cx="400" cy="270" r="25" fill="#8aa7bb"/><text x="400" y="455" text-anchor="middle" font-size="30" fill="#243642" font-family="Arial">Plan d'accès</text></svg>''',
    "petit-dejeuner-hotel-toulouse-besancon": '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 800 520"><rect width="800" height="520" fill="#f8f3ea"/><rect x="120" y="160" width="560" height="220" rx="16" fill="#d4bf95"/><rect x="180" y="220" width="85" height="90" rx="10" fill="#f8e8c6"/><rect x="285" y="210" width="90" height="100" rx="10" fill="#f4d590"/><rect x="395" y="220" width="100" height="90" rx="10" fill="#f4e3af"/><rect x="520" y="205" width="110" height="105" rx="10" fill="#f9d9a9"/><text x="400" y="430" text-anchor="middle" font-size="28" fill="#312c29" font-family="Arial">Petit déjeuner</text></svg>''',
    "espace-bien-etre-hotel-toulouse-besancon": '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 800 520"><rect width="800" height="520" fill="#f3f0f7"/><rect x="160" y="150" width="480" height="220" rx="16" fill="#d7d1f0"/><circle cx="250" cy="250" r="80" fill="#e9e3ff"/><circle cx="550" cy="250" r="80" fill="#e9e3ff"/><rect x="320" y="210" width="130" height="130" rx="20" fill="#cfc5ef"/><text x="400" y="430" text-anchor="middle" font-size="28" fill="#2a2938" font-family="Arial">Espace bien-être</text></svg>''',
    "hotel-de-charme-besancon-interieur": '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 800 520"><rect width="800" height="520" fill="#f2efeb"/><rect x="120" y="110" width="560" height="240" rx="12" fill="#d8c2aa"/><rect x="170" y="170" width="460" height="120" rx="10" fill="#b89d82"/><rect x="220" y="145" width="150" height="35" rx="6" fill="#7d6858"/><rect x="430" y="145" width="150" height="35" rx="6" fill="#7d6858"/><text x="400" y="430" text-anchor="middle" font-size="28" fill="#2d231f" font-family="Arial">Hall d'accueil</text></svg>''',
    "salle-seminaire-hotel-toulouse-besancon": '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 800 520"><rect width="800" height="520" fill="#edf2f5"/><rect x="90" y="150" width="620" height="220" rx="12" fill="#cbd7de"/><rect x="170" y="200" width="460" height="120" rx="8" fill="#dfeaf2"/><rect x="220" y="250" width="100" height="70" rx="8" fill="#a0afbf"/><rect x="480" y="250" width="100" height="70" rx="8" fill="#a0afbf"/><text x="400" y="430" text-anchor="middle" font-size="28" fill="#1d2b34" font-family="Arial">Salle de séminaire</text></svg>''',
    "besancon-citadelle-panorama": '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 800 520"><rect width="800" height="520" fill="#e7f0f7"/><circle cx="650" cy="115" r="70" fill="#f4d36a"/><rect x="80" y="260" width="640" height="160" rx="12" fill="#9ab0b7"/><path d="M120 300 L260 200 L400 270 L540 180 L680 300" stroke="#5f7881" stroke-width="20" fill="none"/><text x="400" y="455" text-anchor="middle" font-size="28" fill="#20333d" font-family="Arial">Citadelle et Doubs</text></svg>''',
}

for i in range(1, 7):
    svg_defs[f"chambre-categorie-{i}"] = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 800 520"><rect width="800" height="520" fill="#f5f1ec"/><rect x="90" y="120" width="620" height="260" rx="16" fill="#d4c1a7"/><rect x="155" y="185" width="200" height="120" rx="10" fill="#b89a7f"/><rect x="425" y="185" width="200" height="120" rx="10" fill="#c9b29c"/><rect x="260" y="120" width="280" height="46" rx="8" fill="#8a7f71"/><text x="400" y="430" text-anchor="middle" font-size="28" fill="#2b2725" font-family="Arial">Chambre de catégorie {i}</text></svg>'''
for i in range(1, 4):
    svg_defs[f"galerie-chambre-{i}"] = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 800 520"><rect width="800" height="520" fill="#efeae4"/><rect x="120" y="110" width="560" height="260" rx="12" fill="#d7c3a4"/><rect x="170" y="165" width="210" height="140" rx="10" fill="#b99578"/><rect x="430" y="165" width="190" height="140" rx="10" fill="#d0b9a2"/><text x="400" y="430" text-anchor="middle" font-size="28" fill="#2a2320" font-family="Arial">Chambre de l'Hôtel de Toulouse, vue {i}</text></svg>'''
    svg_defs[f"galerie-jardin-terrasse-{i}"] = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 800 520"><rect width="800" height="520" fill="#edf3ea"/><rect x="90" y="300" width="620" height="120" rx="18" fill="#92af83"/><rect x="150" y="185" width="150" height="120" rx="12" fill="#d4b58d"/><rect x="320" y="165" width="150" height="140" rx="12" fill="#d4c4a7"/><rect x="500" y="185" width="150" height="120" rx="12" fill="#d9b88d"/><text x="400" y="455" text-anchor="middle" font-size="26" fill="#1e2a22" font-family="Arial">Jardin et terrasse de l'Hôtel de Toulouse, vue {i}</text></svg>'''
    svg_defs[f"galerie-petit-dejeuner-salle-reunion-{i}"] = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 800 520"><rect width="800" height="520" fill="#f7f2e9"/><rect x="110" y="160" width="580" height="220" rx="16" fill="#d0b68e"/><rect x="190" y="210" width="120" height="120" rx="10" fill="#f5e6b0"/><rect x="340" y="205" width="120" height="120" rx="10" fill="#f1d49d"/><rect x="490" y="210" width="120" height="120" rx="10" fill="#f5e8c7"/><text x="400" y="430" text-anchor="middle" font-size="26" fill="#2d241f" font-family="Arial">Petit déjeuner et salle de réunion de l'Hôtel de Toulouse, vue {i}</text></svg>'''

for name, svg in svg_defs.items():
    (root / 'images' / f'{name}.svg').write_text(svg, encoding='utf-8')

home_content = '''
<section>
  <p>L'Hôtel de Toulouse est un hôtel indépendant 3 étoiles, en plein centre-ville de Besançon, de charme. Le site accueille une clientèle de séjours professionnels et touristiques, française et internationale.</p>
</section>
<section>
  <h2>Un hôtel en plein centre-ville de Besançon</h2>
  <p>Nous proposons un hébergement au cœur de la ville, avec un accueil attentif et des espaces pensés pour les séjours courts et longs.</p>
  <figure>
    <img src="https://images.unsplash.com/photo-1566073771259-6a8506099945?auto=format&fit=crop&w=1200&q=80" alt="Façade de l'Hôtel de Toulouse, hôtel 3 étoiles de charme en centre-ville de Besançon" width="1200" height="900" loading="eager">
  </figure>
</section>
<section>
  <h2>50 chambres de charme</h2>
  <h3>6 catégories pour tous les séjours</h3>
  <p>L'établissement compte 50 chambres réparties en 6 catégories, pour convenir à différents types de séjours.</p>
  <figure>
    <img src="https://images.unsplash.com/photo-1505693416388-ac5ce068fe85?auto=format&fit=crop&w=1200&q=80" alt="Chambre de l'Hôtel de Toulouse à Besançon avec literie confortable et décor de charme" width="1200" height="900" loading="lazy">
  </figure>
  <p><a href="/chambres/">Voir les chambres</a></p>
</section>
<section>
  <h2>Jardin, cour et petit déjeuner</h2>
  <p>Le jardin et la terrasse offrent un espace calme au centre de Besançon. Le petit-déjeuner est proposé à l'hôtel.</p>
  <figure>
    <img src="https://images.unsplash.com/photo-1494526585095-c41746248156?auto=format&fit=crop&w=1200&q=80" alt="Terrasse et jardin de l'Hôtel de Toulouse, un espace calme au centre de Besançon" width="1200" height="900" loading="lazy">
  </figure>
  <p><a href="/restaurant/">Découvrir le restaurant</a> · <a href="/galerie-photos/">Voir la galerie</a></p>
</section>
<section>
  <h2>Séjours professionnels et séminaires</h2>
  <p>Nous accueillons aussi des clients professionnels avec 2 salles pour événements professionnels, jusqu'à 20 personnes.</p>
  <p><a href="/salle-seminaire-besancon/">Découvrir les salles</a></p>
</section>
<section>
  <h2>Réserver en direct</h2>
  <p>Réservez votre chambre directement sur le site pour préparer un séjour simple et serein.</p>
  <p><a class="button button-primary" href="/reservation/">Réserver une chambre</a></p>
  <p><a href="/acces-contact/">Nous contacter</a> · <a href="/tourisme-activites/">Découvrir Besançon</a></p>
</section>
<section>
  <h2>Questions fréquentes</h2>
  <div class="faq-list">
    <h3>Question 1</h3>
    <p><strong>L'hôtel est-il en plein centre-ville de Besançon ?</strong> Oui, l'Hôtel de Toulouse est un hôtel indépendant 3 étoiles de charme en plein centre-ville de Besançon.</p>
    <h3>Question 2</h3>
    <p><strong>Combien de chambres proposez-vous ?</strong> L'hôtel compte 50 chambres réparties en 6 catégories.</p>
    <h3>Question 3</h3>
    <p><strong>Disposez-vous d'un parking et de bornes de recharge ?</strong> Oui, le parking privé et sécurisé est disponible sur réservation et 2 bornes de recharge pour véhicules électriques sont à disposition.</p>
  </div>
</section>
'''
root_index = make_page(
    'Hôtel Besançon centre-ville 3 étoiles | Hôtel de Toulouse',
    'Hôtel de Toulouse, hôtel 3 étoiles de charme en plein cœur de Besançon. 50 chambres, jardin, parking privé. Réservez en direct au meilleur tarif.',
    "Hôtel à Besançon : l'Hôtel de Toulouse, 3 étoiles de charme",
    '',
    home_content,
    '/',
    jsonld=hotel_schema() + faq_schema(faq_content['home']),
)
(root / 'index.html').write_text(root_index, encoding='utf-8')

access_content = '''
<section>
  <h2>Nous trouver en centre-ville</h2>
  <p>L'Hôtel de Toulouse se trouve en plein centre-ville de Besançon, dans un environnement pratique pour profiter du centre historique et des services de la ville.</p>
  <figure>
    <img src="https://images.unsplash.com/photo-1502920514313-52581002a659?auto=format&fit=crop&w=1200&q=80" alt="Centre-ville de Besançon et accès à l'Hôtel de Toulouse, hôtel en centre-ville" width="1200" height="900" loading="lazy">
  </figure>
</section>
<section>
  <h2>Venir en voiture, en train ou à pied</h2>
  <h3>Parking privé et bornes de recharge</h3>
  <p>Le parking privé et sécurisé est disponible sur réservation. L'établissement propose également 2 bornes de recharge pour véhicules électriques.</p>
  <h3>Depuis la gare</h3>
  <p>Le centre-ville de Besançon peut être rejoint à pied depuis la gare, dans un parcours simple et pratique à l'arrivée de la ville.</p>
</section>
<section>
  <h2>Nous contacter</h2>
  <form>
    <label>Nom<input type="text" name="nom"></label>
    <label>E-mail<input type="email" name="email"></label>
    <label>Dates<input type="text" name="dates" placeholder="JJ/MM/AAAA"></label>
    <label>Message<textarea name="message"></textarea></label>
    <button type="submit">Envoyer</button>
    <!-- à connecter -->
  </form>
  <p><a href="/reservation/">Réserver une chambre</a> · <a href="/salle-seminaire-besancon/">Demander un devis séminaire</a></p>
</section>
<section>
  <h2>Questions fréquentes</h2>
  <div class="faq-list">
    <h3>Question 1</h3>
    <p><strong>Comment réserver une chambre ?</strong> Vous pouvez réserver en direct via notre formulaire dédié ou nous contacter pour votre demande de séjour.</p>
    <h3>Question 2</h3>
    <p><strong>L'hôtel possède-t-il un parking ?</strong> Oui, un parking privé et sécurisé est proposé sur réservation.</p>
    <h3>Question 3</h3>
    <p><strong>Proposez-vous des salles pour des événements professionnels ?</strong> Oui, nous disposons de 2 salles pour événements professionnels, jusqu'à 20 personnes.</p>
  </div>
</section>
'''
access_page = make_page(
    'Hôtel centre-ville Besançon : accès et contact | Toulouse',
    'Retrouvez l\'Hôtel de Toulouse en plein centre-ville de Besançon : adresse, plan d\'accès, parking et contact. Appelez-nous ou écrivez-nous pour réserver.',
    'Hôtel en centre-ville de Besançon : accès et contact',
    breadcrumb_html('Accès et contact'),
    access_content,
    '/acces-contact/',
    jsonld=faq_schema(faq_content['contact']) + breadcrumb_schema('/acces-contact/'),
)
(root / 'acces-contact').mkdir(exist_ok=True)
(root / 'acces-contact' / 'index.html').write_text(access_page, encoding='utf-8')

chambres_content = '''
<section>
  <h2>6 catégories de chambres</h2>
  <div class="category-grid">
    <article><h3>Chambre catégorie 1</h3><figure><img src="https://images.unsplash.com/photo-1505693416388-ac5ce068fe85?auto=format&fit=crop&w=1200&q=80" alt="Chambre de catégorie 1 de l'Hôtel de Toulouse à Besançon" width="1200" height="900" loading="lazy"></figure></article>
    <article><h3>Chambre catégorie 2</h3><figure><img src="https://images.unsplash.com/photo-1505693416388-ac5ce068fe85?auto=format&fit=crop&w=1200&q=80" alt="Chambre de catégorie 2 de l'Hôtel de Toulouse à Besançon" width="1200" height="900" loading="lazy"></figure></article>
    <article><h3>Chambre catégorie 3</h3><figure><img src="https://images.unsplash.com/photo-1505693416388-ac5ce068fe85?auto=format&fit=crop&w=1200&q=80" alt="Chambre de catégorie 3 de l'Hôtel de Toulouse à Besançon" width="1200" height="900" loading="lazy"></figure></article>
    <article><h3>Chambre catégorie 4</h3><figure><img src="https://images.unsplash.com/photo-1505693416388-ac5ce068fe85?auto=format&fit=crop&w=1200&q=80" alt="Chambre de catégorie 4 de l'Hôtel de Toulouse à Besançon" width="1200" height="900" loading="lazy"></figure></article>
    <article><h3>Chambre catégorie 5</h3><figure><img src="https://images.unsplash.com/photo-1505693416388-ac5ce068fe85?auto=format&fit=crop&w=1200&q=80" alt="Chambre de catégorie 5 de l'Hôtel de Toulouse à Besançon" width="1200" height="900" loading="lazy"></figure></article>
    <article><h3>Chambre catégorie 6</h3><figure><img src="https://images.unsplash.com/photo-1505693416388-ac5ce068fe85?auto=format&fit=crop&w=1200&q=80" alt="Chambre de catégorie 6 de l'Hôtel de Toulouse à Besançon" width="1200" height="900" loading="lazy"></figure></article>
  </div>
</section>
<section>
  <h2>Équipements et services</h2>
  <p>L'hôtel propose un petit-déjeuner, une terrasse, un espace jardin, ainsi qu'un parking privé et sécurisé sur réservation.</p>
  <p>La clientèle bénéficie d'un accueil adapté aux séjours professionnels et touristiques, française et internationale.</p>
</section>
<section>
  <h2>Pourquoi réserver en direct ?</h2>
  <p>Réserver directement votre chambre vous permet de préparer votre séjour facilement et en toute simplicité.</p>
  <p><a class="button button-primary" href="/reservation/">Réserver une chambre</a></p>
  <p><a href="/restaurant/">Découvrir le petit déjeuner</a> · <a href="/galerie-photos/">Voir la galerie photos</a></p>
</section>
'''
chambres_page = make_page(
    'Chambres d\'hôtel à Besançon centre | Hôtel de Toulouse',
    'Découvrez les 50 chambres de l\'Hôtel de Toulouse à Besançon, réparties en 6 catégories : charme, calme et confort en centre-ville. Réservez en ligne.',
    'Chambres d\'hôtel à Besançon : 50 chambres de charme',
    breadcrumb_html('Chambres'),
    chambres_content,
    '/chambres/',
    jsonld=breadcrumb_schema('/chambres/'),
)
(root / 'chambres').mkdir(exist_ok=True)
(root / 'chambres' / 'index.html').write_text(chambres_page, encoding='utf-8')

reservation_content = '''
<section>
  <h2>Choisir vos dates et votre chambre</h2>
  <form>
    <label>Dates d'arrivée<input type="date" name="arrivee"></label>
    <label>Dates de départ<input type="date" name="depart"></label>
    <label>Nombre de voyageurs<input type="number" name="voyageurs" min="1" max="10"></label>
    <label>Nom<input type="text" name="nom"></label>
    <label>E-mail<input type="email" name="email"></label>
    <label>Message<textarea name="message"></textarea></label>
    <button type="submit">Envoyer ma demande</button>
    <!-- à connecter -->
  </form>
</section>
<section>
  <h2>Les avantages de la réservation directe</h2>
  <p>La réservation directe permet de préparer votre séjour et de contacter l'hôtel directement en fonction de vos besoins.</p>
</section>
<section>
  <h2>Un séjour professionnel ? Demandez un devis séminaire</h2>
  <p>Nous accueillons des événements professionnels et proposons 2 salles jusqu'à 20 personnes.</p>
  <p><a href="/salle-seminaire-besancon/">Demander un devis séminaire</a></p>
</section>
<section>
  <h2>Besoin d'aide ?</h2>
  <p>Pour toute question, vous pouvez nous écrire via le formulaire de contact ou nous appeler.</p>
  <p><a href="/acces-contact/">Accès et contact</a></p>
</section>
'''
reservation_page = make_page(
    'Réserver un hôtel à Besançon en direct | Hôtel de Toulouse',
    'Réservez votre chambre à l\'Hôtel de Toulouse, en plein centre de Besançon. Réservation en direct, simple et sécurisée : choisissez vos dates et partez serein.',
    'Réserver un hôtel à Besançon en direct',
    breadcrumb_html('Réservation'),
    reservation_content,
    '/reservation/',
    jsonld=breadcrumb_schema('/reservation/'),
)
(root / 'reservation').mkdir(exist_ok=True)
(root / 'reservation' / 'index.html').write_text(reservation_page, encoding='utf-8')

restaurant_content = '''
<section>
  <h2>Le petit déjeuner</h2>
  <p>L'hôtel propose un petit-déjeuner soigné, avec un accueil simple et agréable pour les clients qui se réveillent au cœur de Besançon.</p>
  <figure>
    <img src="https://images.unsplash.com/photo-1521017432531-fbd92d768814?auto=format&fit=crop&w=1200&q=80" alt="Petit déjeuner servi à l'Hôtel de Toulouse, hôtel de charme au centre de Besançon" width="1200" height="900" loading="lazy">
  </figure>
</section>
<section>
  <h2>Terrasse et jardin</h2>
  <p>La terrasse et le jardin offrent un espace de détente au centre de la ville, dans un cadre calme pendant votre séjour.</p>
</section>
<section>
  <h2>Où dîner à Besançon</h2>
  <p>Pour découvrir la ville et ses délices, nous vous conseillons de consulter l'Office de tourisme de Besançon.</p>
  <p><a href="https://www.besancon-tourisme.com" target="_blank" rel="noopener noreferrer">Office de tourisme de Besançon</a></p>
  <p><a href="/galerie-photos/">Voir la galerie photos</a></p>
</section>
'''
restaurant_page = make_page(
    'Restaurant et petit déjeuner à Besançon | Hôtel de Toulouse',
    'Petit déjeuner soigné à l\'Hôtel de Toulouse et adresses gourmandes à Besançon : découvrez notre offre de restauration en centre-ville. Réservez.',
    'Restaurant et petit déjeuner à l\'Hôtel de Toulouse',
    breadcrumb_html('Restaurant'),
    restaurant_content,
    '/restaurant/',
    jsonld=breadcrumb_schema('/restaurant/'),
)
(root / 'restaurant').mkdir(exist_ok=True)
(root / 'restaurant' / 'index.html').write_text(restaurant_page, encoding='utf-8')

gallery_content = '''
<section>
  <h2>Les chambres</h2>
  <div class="gallery-grid">
    <figure><img src="https://images.unsplash.com/photo-1505693416388-ac5ce068fe85?auto=format&fit=crop&w=1200&q=80" alt="Chambre de l'Hôtel de Toulouse à Besançon, vue 1" width="1200" height="900" loading="lazy"></figure>
    <figure><img src="https://images.unsplash.com/photo-1505693416388-ac5ce068fe85?auto=format&fit=crop&w=1200&q=80" alt="Chambre de l'Hôtel de Toulouse à Besançon, vue 2" width="1200" height="900" loading="lazy"></figure>
    <figure><img src="https://images.unsplash.com/photo-1505693416388-ac5ce068fe85?auto=format&fit=crop&w=1200&q=80" alt="Chambre de l'Hôtel de Toulouse à Besançon, vue 3" width="1200" height="900" loading="lazy"></figure>
  </div>
</section>
<section>
  <h2>Jardin, terrasse et cour</h2>
  <div class="gallery-grid">
    <figure><img src="https://images.unsplash.com/photo-1494526585095-c41746248156?auto=format&fit=crop&w=1200&q=80" alt="Jardin et terrasse de l'Hôtel de Toulouse à Besançon, vue 1" width="1200" height="900" loading="lazy"></figure>
    <figure><img src="https://images.unsplash.com/photo-1494526585095-c41746248156?auto=format&fit=crop&w=1200&q=80" alt="Jardin et terrasse de l'Hôtel de Toulouse à Besançon, vue 2" width="1200" height="900" loading="lazy"></figure>
    <figure><img src="https://images.unsplash.com/photo-1494526585095-c41746248156?auto=format&fit=crop&w=1200&q=80" alt="Jardin et terrasse de l'Hôtel de Toulouse à Besançon, vue 3" width="1200" height="900" loading="lazy"></figure>
  </div>
</section>
<section>
  <h2>Petit déjeuner et salles de réunion</h2>
  <div class="gallery-grid">
    <figure><img src="https://images.unsplash.com/photo-1552664730-d307ca884978?auto=format&fit=crop&w=1200&q=80" alt="Petit déjeuner et salle de réunion de l'Hôtel de Toulouse à Besançon, vue 1" width="1200" height="900" loading="lazy"></figure>
    <figure><img src="https://images.unsplash.com/photo-1552664730-d307ca884978?auto=format&fit=crop&w=1200&q=80" alt="Petit déjeuner et salle de réunion de l'Hôtel de Toulouse à Besançon, vue 2" width="1200" height="900" loading="lazy"></figure>
    <figure><img src="https://images.unsplash.com/photo-1552664730-d307ca884978?auto=format&fit=crop&w=1200&q=80" alt="Petit déjeuner et salle de réunion de l'Hôtel de Toulouse à Besançon, vue 3" width="1200" height="900" loading="lazy"></figure>
  </div>
</section>
<p><a class="button button-primary" href="/reservation/">Réserver une chambre</a></p>
'''
gallery_page = make_page(
    'Galerie photos de l\'hôtel à Besançon | Hôtel de Toulouse',
    'Parcourez les photos de l\'Hôtel de Toulouse à Besançon : chambres, jardin, terrasse, petit déjeuner et salles de réunion. Découvrez l\'hôtel et réservez.',
    'Photos de l\'hôtel à Besançon : la galerie de l\'Hôtel de Toulouse',
    breadcrumb_html('Galerie photos'),
    gallery_content,
    '/galerie-photos/',
    jsonld=breadcrumb_schema('/galerie-photos/'),
)
(root / 'galerie-photos').mkdir(exist_ok=True)
(root / 'galerie-photos' / 'index.html').write_text(gallery_page, encoding='utf-8')

spa_content = '''
<section>
  <h2>Notre projet bien-être</h2>
  <p>Le projet d'espace bien-être de l'Hôtel de Toulouse s'inscrit dans une logique de confort et de relaxation à Besançon, dans le centre-ville.</p>
  <figure>
    <img src="https://images.unsplash.com/photo-1515377905703-c4788e51af15?auto=format&fit=crop&w=1200&q=80" alt="Ambiance détente à l'Hôtel de Toulouse, hôtel avec projet d'espace bien-être à Besançon" width="1200" height="900" loading="lazy">
  </figure>
</section>
<section>
  <h2>Hôtel spa en Bourgogne-Franche-Comté</h2>
  <p>Le spa est actuellement un projet, qui peut être envisagé comme un prolongement du séjour à l'hôtel dans une logique de détente et de bien-être.</p>
</section>
<section>
  <h2>Prolonger son séjour à Besançon</h2>
  <p>Nous vous invitons à nous contacter pour découvrir les possibilités de séjour et d'organisation à l'Hôtel de Toulouse.</p>
  <p><a href="/acces-contact/">Nous contacter</a> · <a href="/chambres/">Voir les chambres</a></p>
</section>
'''
spa_page = make_page(
    'Hôtel spa Besançon : espace bien-être | Hôtel de Toulouse',
    'Un espace bien-être à l\'Hôtel de Toulouse, en centre-ville de Besançon : découvrez notre projet de spa et prolongez votre séjour. Contactez-nous.',
    'Hôtel spa à Besançon : un espace bien-être en centre-ville',
    breadcrumb_html('Spa'),
    spa_content,
    '/spa/',
    jsonld=breadcrumb_schema('/spa/'),
)
(root / 'spa').mkdir(exist_ok=True)
(root / 'spa' / 'index.html').write_text(spa_page, encoding='utf-8')

about_content = '''
<section>
  <h2>Une histoire et une architecture à Besançon</h2>
  <p>L'Hôtel de Toulouse est un hôtel de charme en plein centre de Besançon, avec un accueil attentionné et une ambiance accueillante.</p>
  <figure>
    <img src="https://images.unsplash.com/photo-1551882547-ff40c63fe5fa?auto=format&fit=crop&w=1200&q=80" alt="Hall d'accueil de l'Hôtel de Toulouse, hôtel de charme à Besançon" width="1200" height="900" loading="lazy">
  </figure>
</section>
<section>
  <h2>La cour, la Traction et la Tour Eiffel</h2>
  <p>Le projet de l'hôtel s'appuie sur un cadre de charme au centre de la ville, avec un espace jardin et une atmosphère de séjour agréable.</p>
</section>
<section>
  <h2>Le jardin</h2>
  <p>Le jardin fait partie des espaces ouverts à la clientèle et contribue au calme de l'établissement en plein centre-ville.</p>
</section>
<section>
  <h2>Un accueil attentif</h2>
  <p>La clientèle apprécie un accueil attentionné, adapté aux séjours professionnels et touristiques à Besançon.</p>
  <p><a class="button button-primary" href="/reservation/">Réserver une chambre</a> · <a href="/galerie-photos/">Voir la galerie</a></p>
</section>
'''
about_page = make_page(
    'Hôtel de charme Bourgogne-Franche-Comté | Hôtel de Toulouse',
    'Histoire, architecture et accueil de l\'Hôtel de Toulouse, hôtel de charme en plein centre de Besançon. Découvrez notre identité et réservez votre séjour.',
    'Hôtel de charme en Bourgogne-Franche-Comté : l\'Hôtel de Toulouse',
    breadcrumb_html('Qui sommes-nous'),
    about_content,
    '/qui-sommes-nous/',
    jsonld=breadcrumb_schema('/qui-sommes-nous/'),
)
(root / 'qui-sommes-nous').mkdir(exist_ok=True)
(root / 'qui-sommes-nous' / 'index.html').write_text(about_page, encoding='utf-8')

seminaire_content = '''
<section>
  <h2>Deux salles pour vos événements professionnels</h2>
  <h3>Réunion de travail</h3>
  <p>Deux salles sont disponibles pour accueillir des réunions professionnelles, dans un cadre calme et accessible.</p>
  <h3>Séminaire avec hébergement</h3>
  <p>Les équipes peuvent organiser un séminaire avec hébergement en fonction des besoins de leur séjour à Besançon.</p>
  <figure>
    <img src="https://images.unsplash.com/photo-1552664730-d307ca884978?auto=format&fit=crop&w=1200&q=80" alt="Salle de séminaire de l'Hôtel de Toulouse à Besançon, installée pour une réunion de 20 personnes" width="1200" height="900" loading="lazy">
  </figure>
</section>
<section>
  <h2>Séminaire en Bourgogne-Franche-Comté : hébergement et parking</h2>
  <p>Le centre-ville de Besançon et l'hôtel offrent un cadre adapté aux événements professionnels. Un parking privé et sécurisé est disponible sur place.</p>
</section>
<section>
  <h2>Demander un devis séminaire</h2>
  <form>
    <label>Nom<input type="text" name="nom"></label>
    <label>Société<input type="text" name="societe"></label>
    <label>E-mail<input type="email" name="email"></label>
    <label>Téléphone<input type="tel" name="telephone"></label>
    <label>Date<input type="date" name="date"></label>
    <label>Nombre de personnes<input type="number" name="personnes" min="1" max="20"></label>
    <label>Message<textarea name="message"></textarea></label>
    <button type="submit">Demander un devis</button>
    <!-- à connecter -->
  </form>
</section>
<section>
  <h2>Questions fréquentes</h2>
  <div class="faq-list">
    <h3>Question 1</h3>
    <p><strong>Combien de personnes peuvent accueillir vos salles ?</strong> Nos 2 salles pour événements professionnels accueillent jusqu'à 20 personnes.</p>
    <h3>Question 2</h3>
    <p><strong>Proposez-vous l'hébergement ?</strong> Oui, le séminaire peut s'accompagner d'un hébergement sur place.</p>
    <h3>Question 3</h3>
    <p><strong>Le parking est-il disponible pour les séminaires ?</strong> Oui, un parking privé et sécurisé est disponible sur place pour les clients.</p>
  </div>
  <p><a href="/acces-contact/">Nous contacter</a></p>
</section>
'''
seminaire_page = make_page(
    'Salle séminaire Besançon : réunions jusqu\'à 20 | Toulouse',
    '2 salles de séminaire et de réunion à Besançon pour 20 personnes maximum, avec hébergement et parking sur place. Demandez votre devis séminaire en ligne.',
    'Salle séminaire à Besançon : réunions jusqu\'à 20 personnes',
    breadcrumb_html('Séminaires et réunions'),
    seminaire_content,
    '/salle-seminaire-besancon/',
    jsonld=faq_schema(faq_content['seminaire']) + breadcrumb_schema('/salle-seminaire-besancon/'),
)
(root / 'salle-seminaire-besancon').mkdir(exist_ok=True)
(root / 'salle-seminaire-besancon' / 'index.html').write_text(seminaire_page, encoding='utf-8')

travel_content = '''
<section>
  <h2>La Citadelle de Besançon</h2>
  <p>La Citadelle de Besançon est une visite emblématique de la ville. Elle peut être découverte lors d'un séjour à l'hôtel.</p>
  <p><a href="https://www.citadelle.com" target="_blank" rel="noopener noreferrer">Citadelle de Besançon</a></p>
</section>
<section>
  <h2>Le centre historique à pied</h2>
  <p>Le centre historique de Besançon est accessible à pied, pour profiter de la ville et de ses rues dans un cadre agréable.</p>
</section>
<section>
  <h2>Musées et culture</h2>
  <p>Besançon offre des musées et des lieux culturels à découvrir pendant le séjour, à proximité du centre-ville.</p>
</section>
<section>
  <h2>Balades au bord du Doubs</h2>
  <p>Les balades au bord du Doubs offrent un cadre de détente et de découverte autour de la ville.</p>
</section>
<section>
  <h2>Séjourner à l'Hôtel de Toulouse</h2>
  <p>Le centre-ville de Besançon, les parcours touristiques et le calme de l'hôtel offrent un séjour agréable à la ville.</p>
  <figure>
    <img src="https://images.unsplash.com/photo-1502920514313-52581002a659?auto=format&fit=crop&w=1200&q=80" alt="Vue sur la Citadelle de Besançon et la boucle du Doubs" width="1200" height="900" loading="lazy">
  </figure>
  <p><a href="/acces-contact/">Accès et contact</a> · <a href="/chambres/">Découvrir les chambres</a> · <a href="/restaurant/">Le petit déjeuner</a></p>
  <p><a href="https://www.besancon-tourisme.com" target="_blank" rel="noopener noreferrer">Office de tourisme de Besançon</a></p>
</section>
'''
travel_page = make_page(
    'Séjour à Besançon : Citadelle et visites | Hôtel de Toulouse',
    'Préparez votre séjour à Besançon : Citadelle, centre historique, musées et balades au bord du Doubs, à pied depuis l\'Hôtel de Toulouse. Nos conseils.',
    'Séjour à Besançon : que visiter et que faire ?',
    breadcrumb_html('Tourisme et activités'),
    travel_content,
    '/tourisme-activites/',
    jsonld=breadcrumb_schema('/tourisme-activites/'),
)
(root / 'tourisme-activites').mkdir(exist_ok=True)
(root / 'tourisme-activites' / 'index.html').write_text(travel_page, encoding='utf-8')

legal_content = '''
<section>
  <h2>Éditeur</h2>
  <p>Site édité par l'Hôtel de Toulouse. À compléter.</p>
</section>
<section>
  <h2>Hébergeur</h2>
  <p>À compléter.</p>
</section>
<section>
  <h2>Données personnelles</h2>
  <p>À compléter.</p>
</section>
<p><a href="/">Retour à l'accueil</a></p>
'''
legal_page = make_page(
    'Mentions légales | Hôtel de Toulouse Besançon',
    'Mentions légales du site de l\'Hôtel de Toulouse à Besançon : éditeur, hébergeur et protection des données personnelles.',
    'Mentions légales',
    breadcrumb_html('Mentions légales'),
    legal_content,
    '/mentions-legales/',
    noindex=True,
)
(root / 'mentions-legales').mkdir(exist_ok=True)
(root / 'mentions-legales' / 'index.html').write_text(legal_page, encoding='utf-8')

(root / 'robots.txt').write_text('User-agent: *\nAllow: /\nSitemap: https://www.exemple.fr/sitemap.xml\n', encoding='utf-8')

sitemap_urls = [
    '/', '/chambres/', '/reservation/', '/salle-seminaire-besancon/', '/restaurant/', '/spa/', '/qui-sommes-nous/', '/galerie-photos/', '/tourisme-activites/', '/acces-contact/'
]
xml = '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
for u in sitemap_urls:
    xml += f'  <url><loc>{site_url}{u}</loc></url>\n'
xml += '</urlset>\n'
(root / 'sitemap.xml').write_text(xml, encoding='utf-8')

llms = '''# Hôtel de Toulouse

L'Hôtel de Toulouse est un hôtel indépendant 3 étoiles, de charme, en plein centre-ville de Besançon. Nous accueillons des séjours professionnels et touristiques, avec 50 chambres réparties en 6 catégories, un petit-déjeuner, une terrasse, un jardin et un parking privé et sécurisé sur réservation.

- / : Accueil de l'hôtel, présentation générale et réservation.
- /chambres/ : 50 chambres réparties en 6 catégories.
- /reservation/ : formulaire de demande de réservation directe.
- /salle-seminaire-besancon/ : 2 salles pour événements professionnels jusqu'à 20 personnes.
- /restaurant/ : petit déjeuner et espace de restauration.
- /spa/ : projet d'espace bien-être.
- /qui-sommes-nous/ : identité de l'établissement et accueil.
- /galerie-photos/ : galerie de chambres, jardin, terrasse, petit déjeuner et salles.
- /tourisme-activites/ : conseils pour visiter Besançon.
- /acces-contact/ : accès, parking, contact et demande d'information.
'''
(root / 'llms.txt').write_text(llms, encoding='utf-8')

css = '''
:root {
  --bg: #f5f3f0;
  --surface: #ffffff;
  --ink: #1d1d1b;
  --muted: #5f625d;
  --line: #d8d0c7;
  --primary: #4d5d4c;
  --primary-strong: #334132;
  --focus: #0d5ed7;
}

* { box-sizing: border-box; }
html { scroll-behavior: smooth; }
body {
  margin: 0;
  font-family: Arial, Helvetica, sans-serif;
  background: var(--bg);
  color: var(--ink);
  line-height: 1.6;
}
a { color: var(--primary-strong); }
a:hover, a:focus-visible { text-decoration-thickness: 2px; }
img { max-width: 100%; height: auto; display: block; }
figure { margin: 0 0 1.5rem; }

.skip-link {
  position: absolute;
  left: -9999px;
  top: 0;
}
.skip-link:focus {
  left: 1rem;
  top: 1rem;
  background: #fff;
  padding: .8rem 1rem;
  z-index: 50;
}

.site-nav {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 1rem;
  padding: 1rem 2rem;
  background: #fff;
  border-bottom: 1px solid var(--line);
}
.nav-brand a {
  text-decoration: none;
  font-weight: 700;
  font-size: 1.1rem;
}
.nav-list {
  list-style: none;
  display: flex;
  flex-wrap: wrap;
  align-items: center;
  gap: 1rem;
  margin: 0;
  padding: 0;
}
.nav-list > li { position: relative; }
.nav-list a {
  text-decoration: none;
  color: var(--ink);
}
.has-submenu .submenu {
  position: absolute;
  left: 0;
  top: 100%;
  display: none;
  min-width: 180px;
  list-style: none;
  margin: 0;
  padding: .5rem 0;
  background: #fff;
  border: 1px solid var(--line);
  box-shadow: 0 8px 18px rgba(0,0,0,.08);
}
.has-submenu:hover .submenu,
.has-submenu:focus-within .submenu {
  display: block;
}
.submenu a { display: block; padding: .5rem 1rem; }
.button,
button {
  display: inline-block;
  border: none;
  border-radius: 999px;
  padding: .85rem 1.3rem;
  text-decoration: none;
  cursor: pointer;
  font-weight: 700;
}
.button-primary, button {
  background: var(--primary);
  color: #fff;
}

main {
  max-width: 1100px;
  margin: 0 auto;
  padding: 2rem 1rem 3rem;
}
.page-header {
  margin-bottom: 2rem;
}
h1 {
  font-size: clamp(2rem, 4vw, 3rem);
  line-height: 1.1;
  margin: 0 0 1rem;
}
h2 {
  font-size: clamp(1.5rem, 3vw, 2.25rem);
  margin-top: 2.5rem;
  margin-bottom: 1rem;
}
h3 {
  font-size: 1.2rem;
  margin-top: 1.25rem;
  margin-bottom: .75rem;
}
section {
  margin-bottom: 2.5rem;
  background: rgba(255,255,255,0.35);
  padding: 1.5rem;
  border: 1px solid var(--line);
}

.breadcrumb {
  margin-bottom: 1rem;
}
.breadcrumb ol {
  list-style: none;
  display: flex;
  flex-wrap: wrap;
  gap: .5rem;
  padding: 0;
  margin: 0;
  color: var(--muted);
}
.breadcrumb li:not(:last-child)::after { content: "/"; margin-left: .5rem; }

form {
  display: grid;
  gap: 1rem;
  max-width: 700px;
}
label {
  display: grid;
  gap: .4rem;
  font-weight: 600;
}
input, textarea, select, button {
  font: inherit;
}
input, textarea, select {
  width: 100%;
  padding: .8rem .9rem;
  border: 1px solid var(--line);
  background: #fff;
}
input:focus-visible, textarea:focus-visible, select:focus-visible, a:focus-visible, button:focus-visible {
  outline: 3px solid var(--focus);
  outline-offset: 2px;
}
textarea { min-height: 150px; resize: vertical; }

.gallery-grid, .category-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
  gap: 1rem;
}
.gallery-grid figure,
.category-grid article {
  margin: 0;
  padding: .75rem;
  background: #fff;
  border: 1px solid var(--line);
}

.site-footer {
  background: #fff;
  border-top: 1px solid var(--line);
  padding: 2rem 1rem;
}
.footer-inner {
  max-width: 1100px;
  margin: 0 auto;
}
.footer-links {
  list-style: none;
  padding: 0;
  margin: 1rem 0 0;
  display: flex;
  flex-wrap: wrap;
  gap: .75rem 1.2rem;
}
.footer-brand {
  font-weight: 700;
  margin: 0;
}

@media (max-width: 760px) {
  .site-nav {
    flex-direction: column;
    align-items: flex-start;
  }
  .nav-list {
    flex-direction: column;
    align-items: flex-start;
  }
  .has-submenu .submenu {
    position: static;
    display: block;
    border: none;
    box-shadow: none;
    padding-left: 1rem;
  }
  section { padding: 1rem; }
}
'''
(root / 'css' / 'style.css').write_text(css, encoding='utf-8')

print(f"Site généré dans {root}")
