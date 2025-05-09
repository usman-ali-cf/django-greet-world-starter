
import React from 'react';
import { Button } from '@/components/ui/button';
import CodeBlock from './CodeBlock';

const Template = () => {
  const templateCode = `# myapp/templates/myapp/hello.html
{% extends "base.html" %}

{% block title %}Hello, World!{% endblock %}

{% block content %}
<h1>Hello, World!</h1>
<p>Welcome to my first Django app!</p>
{% endblock %}`;

  const viewCode = `# myapp/views.py
from django.shortcuts import render

def hello_world(request):
    return render(request, 'myapp/hello.html')`;

  const urlsCode = `# myapp/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.hello_world, name='hello_world'),
]`;

  return (
    <div className="py-12">
      <div className="container mx-auto px-4">
        <h2 className="text-3xl font-bold mb-6 text-django-dark-green">Django Template System</h2>
        
        <div className="grid gap-10 md:grid-cols-2">
          <div>
            <h3 className="text-xl font-semibold mb-4">Template Structure</h3>
            <CodeBlock 
              code={templateCode} 
              title="myapp/templates/myapp/hello.html" 
            />
            <p className="text-gray-700 mb-6">
              Django's template system provides a powerful way to define the presentation layer of your web application.
              Templates contain the static parts of the desired HTML output as well as some special syntax describing how dynamic content will be inserted.
            </p>
            <Button className="bg-django-light-green hover:bg-django-dark-green text-white">
              <a href="https://docs.djangoproject.com/en/stable/topics/templates/" target="_blank" rel="noopener noreferrer">
                Learn More About Templates
              </a>
            </Button>
          </div>
          
          <div>
            <h3 className="text-xl font-semibold mb-4">View & URL Configuration</h3>
            <CodeBlock 
              code={viewCode} 
              title="myapp/views.py" 
            />
            <CodeBlock 
              code={urlsCode} 
              title="myapp/urls.py" 
            />
            <p className="text-gray-700">
              Views handle the logic of your application, while the URL patterns define how users navigate to different parts of your site.
            </p>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Template;
