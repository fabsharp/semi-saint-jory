---
layout: default
title: Accueil
description: "1ère édition du Semi-Marathon de Saint-Jory — 29 novembre 2026, Halle des Sports Allison Pineau."
---

<!-- ── HERO ──────────────────────────────────────────────────────────────── -->
<section class="hero">
  <div class="hero-bg-slideshow" aria-hidden="true">
    <div class="hero-bg-slide" style="background-image: url('{{ '/assets/images/header/km-1-3.1.webp' | relative_url }}');"></div>
    <div class="hero-bg-slide" style="background-image: url('{{ '/assets/images/header/km-1-3.2.webp' | relative_url }}');"></div>
    <div class="hero-bg-slide" style="background-image: url('{{ '/assets/images/header/km-1-3.3.webp' | relative_url }}');"></div>
  </div>
  <div class="hero-content">
    <p class="hero-edition">1ère édition</p>
    <h1>Semi-Marathon<br>Saint-Jory</h1>
    <p class="hero-subtitle">29 Novembre 2026 — <a href="{{ site.event.maps_url }}" target="_blank" rel="noopener">Halle des Sports Allison Pineau</a></p>

    <div id="countdown" class="countdown" data-target="2026-11-29T09:00:00"></div>

    <div class="hero-actions">
      <a href="{{ site.event.inscription_url }}" class="btn btn-primary" target="_blank" rel="noopener">S'inscrire</a>
      <a href="{{ '/parcours/' | relative_url }}" class="btn btn-outline">Voir le parcours</a>
    </div>

  </div>
</section>

<!-- ── POSTER + KEY FACTS ────────────────────────────────────────────────── -->
<section class="section">
  <div class="container poster-section">
    <div class="poster-wrap">
      <img src="{{ '/assets/images/poster.jpg' | relative_url }}" alt="Affiche officielle Semi-Marathon Saint-Jory 2026" class="poster-img">
    </div>
    <div class="poster-info">
      <p class="overline">29 Novembre 2026</p>
      <h2>Courez aux bords du canal</h2>
      <p>La première édition du Semi-Marathon de Saint-Jory vous invite à découvrir les paysages du Canal Latéral à la Garonne le temps d'une course inoubliable.</p>

      <ul class="fact-list">
        <li><span class="fact-icon">🏃</span> <strong>Semi-marathon</strong> — 21,1 km individuel</li>
        <li><span class="fact-icon">👥</span> <strong>Semi en relais</strong> — 10,5 km chacun</li>
        <li><span class="fact-icon">⭐</span> <strong>Saint-Jo'Kids</strong> — 600 m · 1 km · 2 km</li>
        <li><span class="fact-icon">📍</span> <a href="{{ site.event.maps_url }}" target="_blank" rel="noopener">Halle des Sports Allison Pineau, Saint-Jory</a></li>
      </ul>

      <a href="{{ site.event.inscription_url }}" class="btn btn-primary" target="_blank" rel="noopener">S'inscrire sur chrono-start.fr</a>
    </div>

  </div>
</section>

<!-- ── SPONSORS ──────────────────────────────────────────────────────────── -->
<section class="section section--alt">
  <div class="container">
    <h2 class="section-title">Nos partenaires</h2>
    <div class="sponsors-row">
      {% for sponsor in site.data.sponsors %}
        {% assign item_class = "sponsor-item" %}
        {% if sponsor.dark_bg %}{% assign item_class = item_class | append: " sponsor-item--dark" %}{% endif %}
        {% if sponsor.url %}
        <a class="{{ item_class }}" href="{{ sponsor.url }}" target="_blank" rel="noopener" aria-label="{{ sponsor.name }}">
          <img src="{{ '/assets/images/sponsors/' | append: sponsor.file | relative_url }}" alt="{{ sponsor.name }}" loading="lazy">
        </a>
        {% else %}
        <div class="{{ item_class }}">
          <img src="{{ '/assets/images/sponsors/' | append: sponsor.file | relative_url }}" alt="{{ sponsor.name }}" loading="lazy">
        </div>
        {% endif %}
      {% endfor %}
    </div>
  </div>
</section>
