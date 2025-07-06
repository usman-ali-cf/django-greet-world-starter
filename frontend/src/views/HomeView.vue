<template>
  <div class="home">
    <h1>Welcome to Electrical Project Manager</h1>
    <p class="subtitle">Manage your electrical projects with ease</p>
    
    <div class="actions">
      <router-link to="/projects" class="btn primary">View All Projects</router-link>
      <router-link to="/projects/new" class="btn secondary">Create New Project</router-link>
    </div>
    
    <div class="features">
      <div class="feature-card">
        <h3>Project Management</h3>
        <p>Create and manage all your electrical projects in one place.</p>
      </div>
      <div class="feature-card">
        <h3>Utility Configuration</h3>
        <p>Upload and configure utility data with ease.</p>
      </div>
      <div class="feature-card">
        <h3>I/O Assignment</h3>
        <p>Easily assign and manage I/O configurations.</p>
      </div>
    </div>
  </div>
</template>

<script setup>
// Component logic goes here
</script>

<style scoped>
.home {
  max-width: 1200px;
  margin: 0 auto;
  padding: 2rem;
  text-align: center;
}

h1 {
  font-size: 2.5rem;
  margin-bottom: 1rem;
  color: #2c3e50;
}

.subtitle {
  font-size: 1.2rem;
  color: #666;
  margin-bottom: 2rem;
}

.actions {
  display: flex;
  justify-content: center;
  gap: 1rem;
  margin: 2rem 0;
}

.btn {
  display: inline-block;
  padding: 0.8rem 1.5rem;
  border-radius: 4px;
  text-decoration: none;
  font-weight: 600;
  transition: all 0.3s ease;
}

.primary {
  background-color: #3498db;
  color: white;
  border: 2px solid #3498db;
}

.primary:hover {
  background-color: #2980b9;
  border-color: #2980b9;
}

.secondary {
  background-color: transparent;
  color: #3498db;
  border: 2px solid #3498db;
}

.secondary:hover {
  background-color: #f8f9fa;
}

.features {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
  gap: 2rem;
  margin-top: 3rem;
}

.feature-card {
  background: white;
  border-radius: 8px;
  padding: 2rem;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
  transition: transform 0.3s ease, box-shadow 0.3s ease;
}

.feature-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 5px 15px rgba(0, 0, 0, 0.1);
}

.feature-card h3 {
  color: #2c3e50;
  margin-bottom: 1rem;
}

.feature-card p {
  color: #666;
  line-height: 1.6;
}
</style>
