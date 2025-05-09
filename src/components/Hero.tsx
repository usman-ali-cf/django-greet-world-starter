
import React from 'react';
import { Button } from '@/components/ui/button';

const Hero = () => {
  return (
    <div className="django-gradient text-white py-20">
      <div className="container mx-auto px-4 text-center">
        <h1 className="text-4xl md:text-6xl font-bold mb-6">
          Hello World with Django
        </h1>
        <p className="text-xl md:text-2xl mb-8 max-w-3xl mx-auto">
          The web framework for perfectionists with deadlines. Django makes it easier to build better web apps more quickly and with less code.
        </p>
        <div className="flex justify-center space-x-4">
          <Button className="bg-white text-django-dark-green hover:bg-django-light-text">
            Get Started
          </Button>
          <Button className="bg-transparent border border-white hover:bg-white/10">
            Documentation
          </Button>
        </div>
      </div>
    </div>
  );
};

export default Hero;
