
import React from 'react';

const Footer = () => {
  return (
    <footer className="bg-django-dark-green text-django-light-text py-8">
      <div className="container mx-auto px-4">
        <div className="flex flex-col md:flex-row justify-between">
          <div className="mb-6 md:mb-0">
            <h3 className="text-django-light-green font-bold text-lg mb-3">Django</h3>
            <p className="text-sm max-w-md">
              Django is a high-level Python web framework that encourages rapid development and clean, pragmatic design.
            </p>
          </div>
          
          <div className="grid grid-cols-2 md:grid-cols-3 gap-8">
            <div>
              <h4 className="font-semibold mb-3">Get Help</h4>
              <ul className="space-y-2 text-sm">
                <li><a href="https://docs.djangoproject.com/" className="hover:text-django-light-green">Documentation</a></li>
                <li><a href="https://forum.djangoproject.com/" className="hover:text-django-light-green">Django Forum</a></li>
                <li><a href="https://djangosnippets.org/" className="hover:text-django-light-green">Django Snippets</a></li>
                <li><a href="https://www.djangoproject.com/community/" className="hover:text-django-light-green">Mailing Lists</a></li>
              </ul>
            </div>
            
            <div>
              <h4 className="font-semibold mb-3">Resources</h4>
              <ul className="space-y-2 text-sm">
                <li><a href="https://www.djangoproject.com/download/" className="hover:text-django-light-green">Download</a></li>
                <li><a href="https://github.com/django/django" className="hover:text-django-light-green">GitHub</a></li>
                <li><a href="https://djangoproject.com/weblog/" className="hover:text-django-light-green">Django News</a></li>
                <li><a href="https://www.djangoproject.com/foundation/" className="hover:text-django-light-green">Django Software Foundation</a></li>
              </ul>
            </div>
          </div>
        </div>
        <div className="border-t border-gray-700 mt-8 pt-6 text-sm text-center text-gray-400">
          <p>&copy; {new Date().getFullYear()} Django Software Foundation and individual contributors. Django is a registered trademark of the Django Software Foundation.</p>
        </div>
      </div>
    </footer>
  );
};

export default Footer;
