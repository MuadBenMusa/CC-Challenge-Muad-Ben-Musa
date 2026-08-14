<script lang="ts">
  import { onMount } from "svelte";

  import Header from "./lib/components/Header.svelte";
  import ProjectTable from "./lib/components/ProjectTable.svelte";
  import { getProjects } from "./lib/api/projects";
  import type { Project, ProjectStatus } from "./lib/types/project";

  type StatusFilter = ProjectStatus | "";

  let projects: Project[] = [];
  let selectedStatus: StatusFilter = "";
  let loading = true;
  let error = "";

  async function loadProjects(): Promise<void> {
    loading = true;
    error = "";

    try {
      projects = await getProjects(selectedStatus || undefined);
    } catch {
      error = "Projekte konnten nicht geladen werden.";
    } finally {
      loading = false;
    }
  }

  onMount(loadProjects);
</script>

<Header />

<main class="page">
  <section class="toolbar">
    <div>
      <h1>Kanalprojekte</h1>
      <p>Projektübersicht für Reinigung, Inspektion und Sanierung.</p>
    </div>

    <label class="status-filter">
      <span>Status</span>

      <select bind:value={selectedStatus} onchange={loadProjects}>
        <option value="">Alle</option>
        <option value="open">Offen</option>
        <option value="in progress">In Bearbeitung</option>
        <option value="done">Erledigt</option>
      </select>
    </label>
  </section>

  <section class="workbench" aria-label="Projektliste">
    {#if loading}
      <p class="message">Projekte werden geladen...</p>
    {:else if error}
      <p class="message error">{error}</p>
    {:else if projects.length === 0}
      <p class="message">Keine Projekte für diesen Status gefunden.</p>
    {:else}
      <ProjectTable {projects} />
    {/if}
  </section>
</main>