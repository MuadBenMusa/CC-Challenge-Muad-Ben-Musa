<script lang="ts">
  import type {
    Project,
    ProjectStatus,
    ProjectTask
  } from "../types/project";

  let { projects }: { projects: Project[] } = $props();

  function taskLabel(task: ProjectTask): string {
    const labels: Record<ProjectTask, string> = {
      cleaning: "Reinigung",
      inspection: "Inspektion",
      repair: "Sanierung"
    };

    return labels[task];
  }

  function statusLabel(status: ProjectStatus): string {
    const labels: Record<ProjectStatus, string> = {
      open: "Offen",
      "in progress": "In Bearbeitung",
      done: "Erledigt"
    };

    return labels[status];
  }

  function statusClass(status: ProjectStatus): string {
    return status.replace(" ", "-");
  }
</script>

<div class="table-wrapper">
  <table>
    <thead>
      <tr>
        <th>Datum</th>
        <th>Kunde</th>
        <th>Aufgabe</th>
        <th>Ort</th>
        <th>Beschreibung</th>
        <th>Status</th>
      </tr>
    </thead>

    <tbody>
      {#each projects as project}
        <tr>

          <td>{project.date}</td>

          <td>{project.customer_name}</td>

          <td>{taskLabel(project.task)}</td>

          <td>{project.location ?? "–"}</td>

          <td class="description">
            {project.description ?? "–"}
          </td>

          <td>
            <span class={`status-badge ${statusClass(project.status)}`}>
              {statusLabel(project.status)}
            </span>
          </td>
        </tr>
      {/each}
    </tbody>
  </table>
</div>