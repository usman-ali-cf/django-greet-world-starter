
import React from 'react';

interface CodeBlockProps {
  code: string;
  language?: string;
  title?: string;
}

const CodeBlock: React.FC<CodeBlockProps> = ({ code, language = "python", title }) => {
  return (
    <div className="mb-6">
      {title && (
        <div className="bg-django-dark-green text-django-light-text px-4 py-2 text-sm font-medium rounded-t-md border-b border-gray-700">
          {title}
        </div>
      )}
      <pre className={`code-block ${title ? 'rounded-t-none' : ''}`}>
        <code>{code}</code>
      </pre>
    </div>
  );
};

export default CodeBlock;
