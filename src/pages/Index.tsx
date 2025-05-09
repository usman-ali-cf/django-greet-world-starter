
import React from 'react';
import Navbar from '@/components/Navbar';
import Hero from '@/components/Hero';
import Features from '@/components/Features';
import Template from '@/components/Template';
import AdminPanel from '@/components/AdminPanel';
import Footer from '@/components/Footer';
import { Button } from '@/components/ui/button';

const Index = () => {
  return (
    <div className="min-h-screen flex flex-col">
      <Navbar />
      <Hero />
      <Features />
      
      <div className="container mx-auto px-4 py-16">
        <div className="text-center mb-12">
          <h2 className="text-3xl font-bold mb-4 text-django-dark-green">Get Started with Django</h2>
          <p className="text-gray-600 max-w-3xl mx-auto">
            Getting started with Django is easy. Here's a simple "Hello World" example to get you going.
          </p>
        </div>
        
        <div className="grid md:grid-cols-3 gap-8">
          <div className="md:col-span-2">
            <Template />
          </div>
          <div>
            <AdminPanel />
            
            <div className="mt-8 p-6 bg-gray-50 rounded-lg border border-gray-200">
              <h3 className="font-bold text-xl mb-3 text-django-dark-green">Getting Started Steps</h3>
              <ol className="list-decimal list-inside space-y-2 text-gray-700">
                <li>Install Django: <code className="bg-gray-200 px-1 py-0.5 rounded">pip install django</code></li>
                <li>Create a project: <code className="bg-gray-200 px-1 py-0.5 rounded">django-admin startproject mysite</code></li>
                <li>Create an app: <code className="bg-gray-200 px-1 py-0.5 rounded">python manage.py startapp myapp</code></li>
                <li>Define models</li>
                <li>Create views and templates</li>
                <li>Run server: <code className="bg-gray-200 px-1 py-0.5 rounded">python manage.py runserver</code></li>
              </ol>
              
              <div className="mt-4">
                <Button className="w-full bg-django-light-green hover:bg-django-dark-green text-white">
                  <a href="https://docs.djangoproject.com/en/stable/intro/tutorial01/" target="_blank" rel="noopener noreferrer">
                    Follow the Tutorial
                  </a>
                </Button>
              </div>
            </div>
          </div>
        </div>
      </div>
      
      <Footer />
    </div>
  );
};

export default Index;
