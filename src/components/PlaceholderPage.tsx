
import React from 'react'
import {
  Box,
  Card,
  CardContent,
  Typography,
  Container,
  Chip
} from '@mui/material'
import { Construction } from '@mui/icons-material'
import underConstruction from '../img/under_construction.png'

interface PlaceholderPageProps {
  pageName: string
}

const PlaceholderPage: React.FC<PlaceholderPageProps> = ({ pageName }) => {
  return (
    <Container maxWidth="md" sx={{ py: 8 }}>
      <Card elevation={0} sx={{ border: '1px solid #e0e0e0', textAlign: 'center' }}>
        <CardContent sx={{ p: 6 }}>
          <Construction sx={{ fontSize: 64, color: '#ff9800', mb: 2 }} />
          
          <Typography variant="h4" component="h2" gutterBottom sx={{ fontWeight: 600, mb: 2 }}>
            Pagina in fase di sviluppo
          </Typography>
          
          <Typography variant="h6" color="text.secondary" sx={{ mb: 4 }}>
            Stiamo lavorando per offrirti presto un'interfaccia completa per{' '}
            <Chip 
              label={pageName}
              variant="outlined"
              sx={{ 
                fontWeight: 600,
                bgcolor: '#f5f5f5',
                fontSize: '1rem',
                height: 'auto',
                py: 0.5
              }}
            />
          </Typography>
          
          <Box 
            sx={{ 
              maxWidth: 400, 
              mx: 'auto',
              '& img': {
                width: '100%',
                height: 'auto',
                borderRadius: 2,
                opacity: 0.8
              }
            }}
          >
            <img 
              src={underConstruction} 
              alt="In costruzione"
            />
          </Box>
        </CardContent>
      </Card>
    </Container>
  )
}

export default PlaceholderPage
