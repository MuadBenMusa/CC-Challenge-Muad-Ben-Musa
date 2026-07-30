<script lang="ts">
  import Header from "./lib/Header.svelte";

  const apiBaseUrl = import.meta.env.VITE_API_BASE_URL ?? "http://localhost:8000";
</script>

<Header />

<main class="page">
  <section class="toolbar">
    <div>
      <h1>Kanalprojekte</h1>
      <p>Projektuebersicht fuer Reinigung, Inspektion und Sanierung.</p>
    </div>
    <span class="api-pill">{apiBaseUrl}</span>
  </section>

  <section class="workbench" aria-label="Projektliste">
    <div class="empty-state">
      <h2>Projektliste implementieren</h2>
      <p>
        Lade die Projekte direkt von der FastAPI, sortiere sie nach Datum und
        ergaenze einen Statusfilter.
      </p>
    </div>
  </section>
</main>

