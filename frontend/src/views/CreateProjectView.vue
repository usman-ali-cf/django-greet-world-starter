<template>
  <div class="create-project">
    <h2>Create New Project</h2>
    <form @submit.prevent="handleSubmit" class="project-form">
      <div class="form-group">
        <label for="projectName">Project Name</label>
        <input 
          type="text" 
          id="projectName" 
          v-model="project.name" 
          required 
          placeholder="Enter project name"
        >
      </div>
      
      <div class="form-group">
        <label for="projectDescription">Description</label>
        <textarea 
          id="projectDescription" 
          v-model="project.description" 
          rows="4"
          placeholder="Enter project description"
        ></textarea>
      </div>
      
      <div class="form-actions">
        <button type="button" @click="$router.go(-1)" class="btn btn-secondary">
          Cancel
        </button>
        <button type="submit" class="btn btn-primary">
          Create Project
        </button>
      </div>
    </form>
  </div>
</template>

<script setup>
import { ref } from 'vue';
import { useRouter } from 'vue-router';
import { useProjectStore } from '@/stores/project';

const router = useRouter();
const projectStore = useProjectStore();

const project = ref({
  name: '',
  description: ''
});

const handleSubmit = async () => {
  try {
    await projectStore.createProject(project.value);
    // Force refresh the projects list when navigating back
    await projectStore.fetchProjects(true); // true to force refresh
    router.push('/projects');
  } catch (error) {
    console.error('Error creating project:', error);
    // Show error message to user
    alert('Failed to create project. Please try again.');
  }
};
</script>

<style scoped>
.create-project {
  max-width: 600px;
  margin: 0 auto;
  padding: 2rem;
}

h2 {
  color: #2c3e50;
  margin-bottom: 2rem;
  text-align: center;
}

.project-form {
  background: #fff;
  padding: 2rem;
  border-radius: 8px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

.form-group {
  margin-bottom: 1.5rem;
}

label {
  display: block;
  margin-bottom: 0.5rem;
  font-weight: 500;
  color: #2c3e50;
}

input[type="text"],
textarea {
  width: 100%;
  padding: 0.75rem;
  border: 1px solid #ddd;
  border-radius: 4px;
  font-size: 1rem;
  transition: border-color 0.3s;
}

input[type="text"]:focus,
textarea:focus {
  outline: none;
  border-color: #3498db;
  box-shadow: 0 0 0 2px rgba(52, 152, 219, 0.2);
}

.form-actions {
  display: flex;
  justify-content: flex-end;
  gap: 1rem;
  margin-top: 2rem;
}

.btn {
  padding: 0.75rem 1.5rem;
  border: none;
  border-radius: 4px;
  font-size: 1rem;
  font-weight: 500;
  cursor: pointer;
  transition: background-color 0.3s;
}

.btn-primary {
  background-color: #3498db;
  color: white;
}

.btn-primary:hover {
  background-color: #2980b9;
}

.btn-secondary {
  background-color: #f1f1f1;
  color: #2c3e50;
}

.btn-secondary:hover {
  background-color: #e0e0e0;
}
</style>
