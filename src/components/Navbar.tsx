
import React from 'react';
import { Link } from 'react-router-dom';

const Navbar = () => {
  return (
    <nav className="bg-django-green text-django-light-text py-4 shadow-md">
      <div className="container mx-auto px-4 flex justify-between items-center">
        <div className="flex items-center space-x-2">
          <div className="text-django-light-green font-bold text-xl">Django</div>
        </div>
        
        <div className="hidden md:flex space-x-6">
          <NavLink href="https://docs.djangoproject.com/" label="Documentation" />
          <NavLink href="https://www.djangoproject.com/download/" label="Downloads" />
          <NavLink href="https://www.djangoproject.com/weblog/" label="News" />
          <NavLink href="https://www.djangoproject.com/community/" label="Community" />
          <NavLink href="https://code.djangoproject.com/" label="Code" />
          <NavLink href="https://www.djangoproject.com/foundation/" label="About" />
        </div>
        
        <div className="md:hidden">
          <button className="text-django-light-text">
            <svg xmlns="http://www.w3.org/2000/svg" className="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 6h16M4 12h16M4 18h16" />
            </svg>
          </button>
        </div>
      </div>
    </nav>
  );
};

const NavLink = ({ href, label }: { href: string; label: string }) => {
  return (
    <a 
      href={href} 
      target="_blank" 
      rel="noopener noreferrer"
      className="hover:text-django-light-green transition-colors duration-300"
    >
      {label}
    </a>
  );
};

export default Navbar;
