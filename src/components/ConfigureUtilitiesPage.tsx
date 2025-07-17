import React, { useState, useEffect } from 'react';
import { useParams } from 'react-router-dom';
import { apiFetch } from '../utils/api';
import './ConfigureUtilitiesPage.css';

interface Utility {
  id_utenza: number;
  nome_utenza: string;
  descrizione: string;
  categoria: string;
  tipo_comando: string;
  tensione: string;
  zona: string;
  DI: number;
  DO: number;
  AI: number;
  AO: number;
  FDI: number;
  FDO: number;
  elaborata: number;
}

interface Category {
  id_categoria: number;
  categoria: string;
}

interface Subcategory {
  id_sottocategoria: number;
  sottocategoria: string;
}

interface Option {
  id_opzione: number;
  opzione: string;
}

interface Detail {
  tipo: string;
  descrizione: string;
  simboli?: string[];
}

const ConfigureUtilitiesPage: React.FC = () => {
  const { id } = useParams<{ id: string }>();
  const [utilities, setUtilities] = useState<Utility[]>([]);
  const [categories, setCategories] = useState<Category[]>([]);
  const [subcategories, setSubcategories] = useState<Subcategory[]>([]);
  const [options, setOptions] = useState<Option[]>([]);
  const [details, setDetails] = useState<Detail[]>([]);
  const [selectedUtility, setSelectedUtility] = useState<Utility | null>(null);
  const [selectedCategory, setSelectedCategory] = useState<Category | null>(null);
  const [selectedSubcategory, setSelectedSubcategory] = useState<Subcategory | null>(null);
  const [selectedOption, setSelectedOption] = useState<Option | null>(null);
  const [loading, setLoading] = useState(true);
  const [processingStatus, setProcessingStatus] = useState<string>('');
  const cellWidth = 75;

  // Load utilities on component mount
  useEffect(() => {
    if (id) {
      loadUtilities();
      loadCategories();
    }
  }, [id]);

  const loadUtilities = async () => {
    try {
      const response = await apiFetch(`/api/aggiorna_tabella?id_prg=${id}`);
      setUtilities(response.utenze || []);
    } catch (error) {
      console.error('Error loading utilities:', error);
    }
  };

  const loadCategories = async () => {
    try {
      // Mock categories for now - replace with actual API call
      const mockCategories: Category[] = [
        { id_categoria: 1, categoria: 'Sensore' },
        { id_categoria: 2, categoria: 'Attuatore' },
        { id_categoria: 3, categoria: 'Comando operatore' },
        { id_categoria: 4, categoria: 'Segnalazione' },
        { id_categoria: 5, categoria: 'Dispositivo di sicurezza' }
      ];
      setCategories(mockCategories);
      setLoading(false);
    } catch (error) {
      console.error('Error loading categories:', error);
      setLoading(false);
    }
  };

  const loadSubcategories = async (categoryId: number) => {
    try {
      const response = await apiFetch(`/api/sottocategorie?id_categoria=${categoryId}`);
      setSubcategories(response);
      setOptions([]); // Reset options when category changes
    } catch (error) {
      console.error('Error loading subcategories:', error);
      setSubcategories([]);
    }
  };

  const loadOptions = async (subcategoryId: number) => {
    try {
      const response = await apiFetch(`/api/opzioni?id_sottocategoria=${subcategoryId}`);
      setOptions(response);
    } catch (error) {
      console.error('Error loading options:', error);
      setOptions([]);
    }
  };

  const loadDetails = async (utilityId: number, categoryId: number, subcategoryId: number, optionId: number) => {
    try {
      const response = await apiFetch(`/api/dettagli?id_utenza=${utilityId}&id_categoria=${categoryId}&id_sottocategoria=${subcategoryId}&id_opzione=${optionId}&id_prg=${id}`);
      setDetails(response.dettagli || []);
    } catch (error) {
      console.error('Error loading details:', error);
      setDetails([]);
    }
  };

  const handleUtilityClick = async (utility: Utility) => {
    setSelectedUtility(utility);
    
    try {
      // Load current selection for this utility
      const response = await apiFetch(`/api/selezione_utenza?id_utenza=${utility.id_utenza}`);
      const selection = response.selezione;
      
      if (selection) {
        // Find and select the category
        const category = categories.find(c => c.id_categoria === selection.id_cat);
        if (category) {
          await handleCategoryClick(category);
        }
        
        // Find and select the subcategory
        const subcategory = subcategories.find(s => s.id_sottocategoria === selection.id_sottocat);
        if (subcategory) {
          await handleSubcategoryClick(subcategory);
        }
        
        // Find and select the option
        const option = options.find(o => o.id_opzione === selection.id_opzione);
        if (option) {
          await handleOptionClick(option);
        }
      }
    } catch (error) {
      console.error('Error loading utility selection:', error);
    }
  };

  const handleCategoryClick = async (category: Category) => {
    setSelectedCategory(category);
    setSelectedSubcategory(null);
    setSelectedOption(null);
    setDetails([]);
    await loadSubcategories(category.id_categoria);
  };

  const handleSubcategoryClick = async (subcategory: Subcategory) => {
    setSelectedSubcategory(subcategory);
    setSelectedOption(null);
    setDetails([]);
    await loadOptions(subcategory.id_sottocategoria);
  };

  const handleOptionClick = async (option: Option) => {
    setSelectedOption(option);
    
    if (selectedUtility && selectedCategory && selectedSubcategory) {
      await loadDetails(
        selectedUtility.id_utenza,
        selectedCategory.id_categoria,
        selectedSubcategory.id_sottocategoria,
        option.id_opzione
      );
    }
  };

  const handleConfirm = async () => {
    if (!selectedUtility) {
      alert('Seleziona prima un\'utenza.');
      return;
    }

    try {
      await apiFetch('/api/conferma', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({})
      });

      // Reload utilities to update the processed status
      await loadUtilities();
      
      // Find next utility to select
      const currentIndex = utilities.findIndex(u => u.id_utenza === selectedUtility.id_utenza);
      if (currentIndex !== -1 && currentIndex < utilities.length - 1) {
        const nextUtility = utilities[currentIndex + 1];
        await handleUtilityClick(nextUtility);
      }
      
      alert('Conferma completata con successo!');
    } catch (error) {
      console.error('Error confirming:', error);
      alert('Errore durante la conferma. Riprova più tardi.');
    }
  };

  const handlePreProcessAll = async () => {
    setProcessingStatus('Elaborazione in corso...');
    
    try {
      const response = await apiFetch('/api/preelabora_utenze', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({})
      });
      
      setProcessingStatus(response.message || 'Pre-elaborazione completata');
      await loadUtilities();
      
      setTimeout(() => setProcessingStatus(''), 3000);
    } catch (error) {
      console.error('Error pre-processing:', error);
      setProcessingStatus('Errore durante la pre-elaborazione');
      setTimeout(() => setProcessingStatus(''), 3000);
    }
  };

  if (loading) {
    return <div className="text-center p-8">Caricamento...</div>;
  }

  return (
    <div style={{ overflowX: 'auto', width: '100%', height: 'calc(100vh - 64px)', overflowY: 'auto' }}>
      <div className="configure-utilities-page" style={{ minWidth: 1100 }}>
        {/* Header Section */}
        <div className="configure-utilities-header">
          <h1 className="configure-utilities-title">Elenco Utenze</h1>
          <button
            onClick={handlePreProcessAll}
            className="pre-process-button"
          >
            <span className="pre-process-icon">⚙️</span>
            Pre-elabora Tutte
          </button>
        </div>

        {/* Processing Status */}
        {processingStatus && (
          <div className="configure-processing-status">
            {processingStatus}
          </div>
        )}

        {/* Main Content */}
        <div className="configure-utilities-layout">
          {/* Left Side - Panels */}
          <div className="configure-panels">
            {/* Categories Panel */}
            <div className="configure-panel">
              <h4 className="configure-panel-title">Categorie</h4>
              <div className="configure-panel-content">
                {categories.map((category) => (
                  <div
                    key={category.id_categoria}
                    onClick={() => handleCategoryClick(category)}
                    className={`configure-panel-item ${
                      selectedCategory?.id_categoria === category.id_categoria ? 'selected' : ''
                    }`}
                  >
                    {category.categoria}
                  </div>
                ))}
              </div>
            </div>

            {/* Subcategories Panel */}
            <div className="configure-panel">
              <h4 className="configure-panel-title">Sottocategorie</h4>
              <div className="configure-panel-content">
                {subcategories.length === 0 ? (
                  <p className="configure-panel-placeholder">Seleziona una categoria</p>
                ) : (
                  subcategories.map((subcategory) => (
                    <div
                      key={subcategory.id_sottocategoria}
                      onClick={() => handleSubcategoryClick(subcategory)}
                      className={`configure-panel-item ${
                        selectedSubcategory?.id_sottocategoria === subcategory.id_sottocategoria ? 'selected' : ''
                      }`}
                    >
                      {subcategory.sottocategoria}
                    </div>
                  ))
                )}
              </div>
            </div>

            {/* Options Panel */}
            <div className="configure-panel">
              <h4 className="configure-panel-title">Opzioni</h4>
              <div className="configure-panel-content">
                {options.length === 0 ? (
                  <p className="configure-panel-placeholder">Seleziona una sottocategoria</p>
                ) : (
                  options.map((option) => (
                    <div
                      key={option.id_opzione}
                      onClick={() => handleOptionClick(option)}
                      className={`configure-panel-item ${
                        selectedOption?.id_opzione === option.id_opzione ? 'selected' : ''
                      }`}
                    >
                      {option.opzione}
                    </div>
                  ))
                )}
              </div>
            </div>

            {/* Details Panel */}
            <div className="configure-panel">
              <h4 className="configure-panel-title">Dettagli</h4>
              <div className="configure-details-content">
                {details.length === 0 ? (
                  <p className="configure-panel-placeholder">Seleziona un'opzione per vedere i dettagli</p>
                ) : (
                  details.map((detail, index) => (
                    <div key={index} className="configure-detail-item">
                      <div className="configure-detail-type">{detail.tipo}:</div>
                      <div className="configure-detail-description">{detail.descrizione}</div>
                      {detail.simboli && detail.simboli.length > 0 && (
                        <div className="configure-detail-symbols">
                          {detail.simboli.map((symbol, symbolIndex) => (
                            <img
                              key={symbolIndex}
                              src={`/static/img/${symbol}.png`}
                              alt={symbol}
                              className="configure-detail-symbol"
                            />
                          ))}
                        </div>
                      )}
                    </div>
                  ))
                )}
              </div>
            </div>
          </div>

          {/* Right Side - Table */}
          <div style={{ flex: 1, overflowX: 'auto' }}>
            <div className="configure-table-container">
              <div className="configure-table-wrapper">
                <table className="configure-utilities-table" style={{ borderSpacing: 0, width: '100%' }}>
                  <thead>
                    <tr>
                      <th style={{ padding: '4px 8px', width: cellWidth }}>Elaborata</th>
                      <th style={{ padding: '4px 8px', width: cellWidth }}>Nome Utenza</th>
                      <th style={{ padding: '4px 8px', width: cellWidth }}>Descrizione</th>
                      <th style={{ padding: '4px 8px', width: cellWidth }}>Categoria</th>
                      <th style={{ padding: '4px 8px', width: cellWidth }}>Tipo Comando</th>
                      <th style={{ padding: '4px 8px', width: cellWidth }}>Tensione</th>
                      <th style={{ padding: '4px 8px', width: cellWidth }}>Zona</th>
                      <th style={{ padding: '4px 8px', width: cellWidth }}>DI</th>
                      <th style={{ padding: '4px 8px', width: cellWidth }}>DO</th>
                      <th style={{ padding: '4px 8px', width: cellWidth }}>AI</th>
                      <th style={{ padding: '4px 8px', width: cellWidth }}>AO</th>
                      <th style={{ padding: '4px 8px', width: cellWidth }}>FDI</th>
                      <th style={{ padding: '4px 8px', width: cellWidth }}>FDO</th>
                    </tr>
                  </thead>
                  <tbody>
                    {utilities.length === 0 ? (
                      <tr>
                        <td colSpan={13} className="configure-table td" style={{ textAlign: 'center', color: '#6b7280' }}>
                          Nessuna utenza trovata. Carica un file utenze per iniziare.
                        </td>
                      </tr>
                    ) : (
                      utilities.map((utility) => (
                        <tr
                          key={utility.id_utenza}
                          onClick={() => handleUtilityClick(utility)}
                          className={`configure-table tbody tr ${
                            selectedUtility?.id_utenza === utility.id_utenza ? 'selected' : ''
                          }`}
                        >
                          <td className="configure-table td" style={{ padding: '4px 8px', width: cellWidth }}>
                            <span className={`configure-checkbox ${utility.elaborata ? 'checked' : 'unchecked'}`}>
                              {utility.elaborata ? '\u2713' : ''}
                            </span>
                          </td>
                          <td className="configure-table td utility-name" style={{ padding: '4px 8px', width: cellWidth }}>
                            {utility.nome_utenza}
                          </td>
                          <td className="configure-table td" style={{ padding: '4px 8px', width: cellWidth }}>{utility.descrizione}</td>
                          <td className="configure-table td" style={{ padding: '4px 8px', width: cellWidth }}>{utility.categoria}</td>
                          <td className="configure-table td" style={{ padding: '4px 8px', width: cellWidth }}>{utility.tipo_comando}</td>
                          <td className="configure-table td" style={{ padding: '4px 8px', width: cellWidth }}>{utility.tensione}</td>
                          <td className="configure-table td" style={{ padding: '4px 8px', width: cellWidth }}>{utility.zona}</td>
                          <td className="configure-table td" style={{ padding: '4px 8px', width: cellWidth }}>{utility.DI}</td>
                          <td className="configure-table td" style={{ padding: '4px 8px', width: cellWidth }}>{utility.DO}</td>
                          <td className="configure-table td" style={{ padding: '4px 8px', width: cellWidth }}>{utility.AI}</td>
                          <td className="configure-table td" style={{ padding: '4px 8px', width: cellWidth }}>{utility.AO}</td>
                          <td className="configure-table td" style={{ padding: '4px 8px', width: cellWidth }}>{utility.FDI}</td>
                          <td className="configure-table td" style={{ padding: '4px 8px', width: cellWidth }}>{utility.FDO}</td>
                        </tr>
                      ))
                    )}
                  </tbody>
                </table>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default ConfigureUtilitiesPage;