import React, { useState } from 'react';
import { useParams } from 'react-router-dom';
import { apiFetch } from '../utils/api';

const UploadUtilitiesPage: React.FC = () => {
  const { id } = useParams<{ id: string }>();
  const [selectedFile, setSelectedFile] = useState<File | null>(null);
  const [isUploading, setIsUploading] = useState(false);
  const [message, setMessage] = useState<{ text: string; type: 'success' | 'error' | 'info' } | null>(null);

  const handleFileChange = (event: React.ChangeEvent<HTMLInputElement>) => {
    const file = event.target.files?.[0];
    if (file) {
      // Validate file type
      if (!file.name.toLowerCase().endsWith('.xlsx') && !file.name.toLowerCase().endsWith('.xls')) {
        setMessage({ text: 'Please select an Excel file (.xlsx or .xls)', type: 'error' });
        return;
      }
      setSelectedFile(file);
      setMessage(null);
    }
  };

  const handleUpload = async () => {
    if (!selectedFile) {
      setMessage({ text: 'Please select a file first', type: 'error' });
      return;
    }

    setIsUploading(true);
    setMessage(null);

    try {
      const formData = new FormData();
      formData.append('file', selectedFile);

      const response = await apiFetch(`/api/progetti/${id}/carica_file_utenze`, {
        method: 'POST',
        body: formData,
        headers: {
          // Don't set Content-Type for FormData, let the browser set it
        },
      });

      if (response.status === 'confirmation_required') {
        // Handle confirmation case
        const confirmed = window.confirm(
          'Sono già presenti utenze per questo progetto. Vuoi sovrascriverle?'
        );
        
        if (confirmed) {
          await confirmUpload(response.data.tempFilePath);
        } else {
          setMessage({ text: 'Upload cancelled', type: 'info' });
        }
      } else {
        setMessage({ text: response.message || 'File uploaded successfully!', type: 'success' });
        setSelectedFile(null);
        // Reset file input
        const fileInput = document.getElementById('file-input') as HTMLInputElement;
        if (fileInput) fileInput.value = '';
      }
    } catch (error: any) {
      console.error('Upload error:', error);
      setMessage({ 
        text: error.message || 'Error uploading file. Please try again.', 
        type: 'error' 
      });
    } finally {
      setIsUploading(false);
    }
  };

  const confirmUpload = async (filePath: string) => {
    try {
      const response = await apiFetch(`/api/progetti/${id}/carica_file_utenze`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ 
          conferma: true, 
          file_path: filePath 
        }),
      });

      setMessage({ text: response.message || 'File uploaded successfully!', type: 'success' });
      setSelectedFile(null);
      // Reset file input
      const fileInput = document.getElementById('file-input') as HTMLInputElement;
      if (fileInput) fileInput.value = '';
    } catch (error: any) {
      console.error('Confirmation error:', error);
      setMessage({ 
        text: error.message || 'Error confirming upload.', 
        type: 'error' 
      });
    }
  };

  const handleDownloadTemplate = async () => {
    try {
      await apiFetch('/api/download_template');
      setMessage({ text: 'Template scaricato con successo!', type: 'success' });
    } catch (error: any) {
      console.error('Download error:', error);
      setMessage({ 
        text: error.message || 'Errore durante il download del template.', 
        type: 'error' 
      });
    }
  };

  return (
    <div className="bg-white rounded-lg shadow-md p-8 max-w-2xl mx-auto">
      {/* Title */}
      <h1 className="text-2xl font-bold text-gray-800 mb-4">
        Carica File Utenze
      </h1>

      {/* Description */}
      <p className="text-gray-600 mb-6">
        Seleziona un file Excel (.xlsx) per caricare le utenze relative al progetto ID: <strong>{id}</strong>
      </p>

      {/* File Input Section */}
      <div className="mb-6">
        <label htmlFor="file-input" className="flex items-center text-gray-700 font-medium mb-2">
          <span className="text-gray-400 mr-2">📂</span>
          Seleziona File Utenze (.xlsx):
        </label>
        <div className="flex items-center space-x-4">
          <input
            id="file-input"
            type="file"
            accept=".xlsx,.xls"
            onChange={handleFileChange}
            className="flex-1 px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent"
          />
          <button
            onClick={handleUpload}
            disabled={!selectedFile || isUploading}
            className="bg-red-600 hover:bg-red-700 disabled:bg-gray-400 text-white px-6 py-2 rounded-md font-medium flex items-center transition-colors"
          >
            <span className="mr-2">📤</span>
            {isUploading ? 'Caricamento...' : 'Carica File'}
          </button>
        </div>
      </div>

      {/* Download Template Button */}
      <div className="mb-6">
        <button
          onClick={handleDownloadTemplate}
          className="bg-red-600 hover:bg-red-700 text-white px-6 py-2 rounded-md font-medium flex items-center transition-colors"
        >
          <span className="mr-2">📥</span>
          Scarica Template
        </button>
      </div>

      {/* Message Display */}
      {message && (
        <div className={`p-4 rounded-md ${
          message.type === 'success' 
            ? 'bg-green-100 border border-green-400 text-green-700' 
            : message.type === 'error'
            ? 'bg-red-100 border border-red-400 text-red-700'
            : 'bg-blue-100 border border-blue-400 text-blue-700'
        }`}>
          {message.text}
        </div>
      )}

      {/* Loading Overlay */}
      {isUploading && (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
          <div className="bg-white rounded-lg p-6 text-center">
            <h4 className="text-lg font-medium mb-4">Elaborazione file…</h4>
            <div className="w-full h-2 bg-gray-200 rounded-full overflow-hidden">
              <div className="h-full bg-blue-600 animate-pulse" style={{ width: '100%' }}></div>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

export default UploadUtilitiesPage; 