import React, { useState, useEffect } from 'react';
import { useParams } from 'react-router-dom';
import { apiFetch } from '../utils/api';
import './ConfigurePowerUtilitiesPage.css';

interface PowerUtility {
  id_potenza: number;
  nome: string;
  potenza: number;
  tensione: number;
  descrizione: string;
  elaborato: string | number;  // Can be '1'/'0' from DB or 1/0 from frontend
}

interface StartupOption {
  id_opzione: number;
  descrizione: string;
}

const ConfigurePowerUtilitiesPage: React.FC = () => {
  const { id } = useParams<{ id: string }>();
  const [powerUtilities, setPowerUtilities] = useState<PowerUtility[]>([]);
  const [startupOptions, setStartupOptions] = useState<StartupOption[]>([]);
  const [selectedUtility, setSelectedUtility] = useState<PowerUtility | null>(null);
  const [selectedOption, setSelectedOption] = useState<number | null>(null);
  const [loading, setLoading] = useState(true);
  const [processingStatus, setProcessingStatus] = useState<string>('');

  // Load data on component mount
  useEffect(() => {
    if (id) {
      loadPowerUtilities();
      loadStartupOptions();
    }
  }, [id]);

  const loadPowerUtilities = async () => {
    try {
      const response = await apiFetch(`/api/potenza?id_prg=${id}`);
      setPowerUtilities(response.utenze || []);
      setLoading(false);
    } catch (error) {
      console.error('Error loading power utilities:', error);
      setLoading(false);
    }
  };

  const loadStartupOptions = async () => {
    try {
      const response = await apiFetch('/api/opzioni_avviamento');
      setStartupOptions(response.opzioni || []);
    } catch (error) {
      console.error('Error loading startup options:', error);
      setStartupOptions([]);
    }
  };

  const handleUtilityClick = async (utility: PowerUtility) => {
    setSelectedUtility(utility);
    
    try {
      // Load current startup option for this utility
      const response = await apiFetch(`/api/get_opzione_potenza?id_potenza=${utility.id_potenza}`);
      setSelectedOption(response.id_opzione_avviamento || null);
    } catch (error) {
      console.error('Error loading utility startup option:', error);
      setSelectedOption(null);
    }
  };

  const handleOptionChange = (optionId: number) => {
    setSelectedOption(optionId);
  };

  const handleUpdate = async () => {
    if (!selectedUtility) {
      alert('Seleziona prima un\'utenza di potenza.');
      return;
    }

    if (!selectedOption) {
      alert('Seleziona un\'opzione di avviamento.');
      return;
    }

    setProcessingStatus('Aggiornamento in corso...');

    try {
      const response = await apiFetch('/api/assegna_avviamento', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          id_prg: parseInt(id!),
          id_potenza: selectedUtility.id_potenza,
          opzione_avviamento: selectedOption
        })
      });

      if (response.status === 'success') {
        setProcessingStatus('Aggiornamento completato con successo!');
        
        // Reload utilities to update the processed status
        await loadPowerUtilities();
        
        // Find next utility to select
        const currentIndex = powerUtilities.findIndex(u => u.id_potenza === selectedUtility.id_potenza);
        if (currentIndex !== -1 && currentIndex < powerUtilities.length - 1) {
          const nextUtility = powerUtilities[currentIndex + 1];
          await handleUtilityClick(nextUtility);
        }
        
        setTimeout(() => setProcessingStatus(''), 3000);
      } else {
        setProcessingStatus('Errore durante l\'aggiornamento');
        setTimeout(() => setProcessingStatus(''), 3000);
      }
    } catch (error) {
      console.error('Error updating startup option:', error);
      setProcessingStatus('Errore durante l\'aggiornamento');
      setTimeout(() => setProcessingStatus(''), 3000);
    }
  };

  if (loading) {
    return <div className="text-center p-8">Caricamento...</div>;
  }

  return (
    <div style={{ overflowX: 'auto', width: '100%', height: 'calc(100vh - 64px)', overflowY: 'auto' }}>
      <div className="configure-power-utilities-page">
        {/* Processing Status */}
        {processingStatus && (
          <div className="configure-processing-status">
            {processingStatus}
          </div>
        )}

        {/* Main Content */}
        <div className="configure-power-utilities-layout">
          {/* Left Section - Power Utilities List */}
          <div className="configure-power-utilities-left">
            <div className="configure-power-utilities-header">
              <h1 className="configure-power-utilities-title">Lista Utenze di Potenza</h1>
              <button
                onClick={loadPowerUtilities}
                className="configure-update-button"
              >
                Aggiorna
              </button>
            </div>

            <div className="configure-table-container">
              <div className="configure-table-wrapper">
                <table className="configure-table" style={{ borderSpacing: 0, width: '100%' }}>
                  <thead>
                    <tr>
                      <th style={{ padding: '6px 10px' }}>Elaborato</th>
                      <th style={{ padding: '6px 10px' }}>Nome</th>
                      <th style={{ padding: '6px 10px' }}>Tensione</th>
                      <th style={{ padding: '6px 10px' }}>Descrizione</th>
                      <th style={{ padding: '6px 10px' }}>Potenza</th>
                    </tr>
                  </thead>
                  <tbody>
                    {powerUtilities.length === 0 ? (
                      <tr>
                        <td colSpan={5} className="configure-table td" style={{ textAlign: 'center', color: '#6b7280' }}>
                          Nessuna utenza di potenza trovata.
                        </td>
                      </tr>
                    ) : (
                      powerUtilities.map((utility) => (
                        <tr
                          key={utility.id_potenza}
                          onClick={() => handleUtilityClick(utility)}
                          className={`configure-table tbody tr ${
                            selectedUtility?.id_potenza === utility.id_potenza ? 'selected' : ''
                          }`}
                        >
                          <td className="configure-table td" style={{ padding: '4px 8px' }}>
                            <span className={`configure-checkbox ${utility.elaborato === '1' || utility.elaborato === 1 ? 'checked' : 'unchecked'}`}>
                              {utility.elaborato === '1' || utility.elaborato === 1 ? '✓' : ''}
                            </span>
                          </td>
                          <td className="configure-table td utility-name" style={{ padding: '4px 8px' }}>
                            {utility.nome}
                          </td>
                          <td className="configure-table td" style={{ padding: '4px 8px' }}>
                            {utility.tensione}V
                          </td>
                          <td className="configure-table td" style={{ padding: '4px 8px' }}>
                            {utility.descrizione}
                          </td>
                          <td className="configure-table td" style={{ padding: '4px 8px' }}>
                            {utility.potenza} kW
                          </td>
                        </tr>
                      ))
                    )}
                  </tbody>
                </table>
              </div>
            </div>
          </div>

          {/* Right Section - Startup Configuration */}
          <div className="configure-power-utilities-right">
            <div className="configure-startup-panel">
              <h2 className="configure-startup-title">Configurazione Avviamento</h2>
              
              <div className="configure-startup-options">
                {startupOptions.map((option) => (
                  <label key={option.id_opzione} className="configure-radio-option">
                    <input
                      type="radio"
                      name="startupOption"
                      value={option.id_opzione}
                      checked={selectedOption === option.id_opzione}
                      onChange={() => handleOptionChange(option.id_opzione)}
                      className="configure-radio-input"
                    />
                    <span className="configure-radio-label">
                      {option.descrizione}
                    </span>
                  </label>
                ))}
              </div>

              <button
                onClick={handleUpdate}
                disabled={!selectedUtility || !selectedOption}
                className="configure-confirm-startup-button"
              >
                Conferma Avviamento
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default ConfigurePowerUtilitiesPage; 