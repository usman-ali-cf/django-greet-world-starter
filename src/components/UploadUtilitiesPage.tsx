
import React, { useState } from 'react';
import { useParams } from 'react-router-dom';
import { apiFetch } from '../utils/api';
import {
  Box,
  Card,
  CardContent,
  Typography,
  Button,
  Container,
  Alert,
  LinearProgress,
  Paper,
  Divider,
  Stack
} from '@mui/material';
import {
  CloudUpload,
  Download,
  Description
} from '@mui/icons-material';

const UploadUtilitiesPage: React.FC = () => {
  const { id } = useParams<{ id: string }>();
  const [selectedFile, setSelectedFile] = useState<File | null>(null);
  const [isUploading, setIsUploading] = useState(false);
  const [message, setMessage] = useState<{ text: string; type: 'success' | 'error' | 'info' } | null>(null);

  const handleFileChange = (event: React.ChangeEvent<HTMLInputElement>) => {
    const file = event.target.files?.[0];
    if (file) {
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
        headers: {},
      });

      if (response.status === 'confirmation_required') {
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
    <Container maxWidth="md" sx={{ py: 4 }}>
      <Card elevation={0} sx={{ border: '1px solid #e0e0e0' }}>
        <CardContent sx={{ p: 4 }}>
          <Typography variant="h4" component="h1" gutterBottom sx={{ fontWeight: 600, mb: 2 }}>
            Carica File Utenze
          </Typography>
          
          <Typography variant="body1" color="text.secondary" sx={{ mb: 4, fontSize: '1.1rem' }}>
            Seleziona un file Excel (.xlsx) per caricare le utenze relative al progetto ID: <strong>{id}</strong>
          </Typography>

          <Divider sx={{ mb: 4 }} />

          <Stack spacing={3}>
            <Paper 
              elevation={0} 
              sx={{ 
                p: 3, 
                border: '2px dashed #e0e0e0',
                borderRadius: 2,
                textAlign: 'center',
                bgcolor: '#fafafa'
              }}
            >
              <CloudUpload sx={{ fontSize: 48, color: '#9e9e9e', mb: 2 }} />
              <Typography variant="h6" gutterBottom>
                Seleziona File Utenze
              </Typography>
              <Typography variant="body2" color="text.secondary" sx={{ mb: 2 }}>
                Formati supportati: .xlsx, .xls
              </Typography>
              
              <input
                id="file-input"
                type="file"
                accept=".xlsx,.xls"
                onChange={handleFileChange}
                style={{ display: 'none' }}
              />
              <label htmlFor="file-input">
                <Button
                  variant="outlined"
                  component="span"
                  startIcon={<Description />}
                  sx={{ mr: 2 }}
                >
                  Scegli File
                </Button>
              </label>
              
              <Button
                variant="contained"
                onClick={handleUpload}
                disabled={!selectedFile || isUploading}
                startIcon={<CloudUpload />}
                sx={{ 
                  bgcolor: '#1976d2',
                  '&:hover': { bgcolor: '#1565c0' }
                }}
              >
                {isUploading ? 'Caricamento...' : 'Carica File'}
              </Button>
              
              {selectedFile && (
                <Typography variant="body2" sx={{ mt: 2, color: '#2e7d32' }}>
                  File selezionato: {selectedFile.name}
                </Typography>
              )}
            </Paper>

            <Box sx={{ textAlign: 'center' }}>
              <Button
                variant="outlined"
                onClick={handleDownloadTemplate}
                startIcon={<Download />}
                size="large"
                sx={{ 
                  borderColor: '#1976d2',
                  color: '#1976d2',
                  '&:hover': { borderColor: '#1565c0', bgcolor: '#f3f7ff' }
                }}
              >
                Scarica Template
              </Button>
            </Box>

            {message && (
              <Alert severity={message.type} sx={{ mt: 2 }}>
                {message.text}
              </Alert>
            )}

            {isUploading && (
              <Box sx={{ mt: 2 }}>
                <Typography variant="body2" color="text.secondary" gutterBottom>
                  Elaborazione file in corso...
                </Typography>
                <LinearProgress />
              </Box>
            )}
          </Stack>
        </CardContent>
      </Card>
    </Container>
  );
};

export default UploadUtilitiesPage;
