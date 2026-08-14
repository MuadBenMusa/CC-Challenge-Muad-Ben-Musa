export type ProjectTask = "cleaning" | "inspection" | "repair"

export type ProjectStatus = "open" | "in progress" | "done";

export interface Project {
    customer_name: string;
    date: string;
    task: ProjectTask;
    location: string | null;
    description: string | null;
    status: ProjectStatus;
}