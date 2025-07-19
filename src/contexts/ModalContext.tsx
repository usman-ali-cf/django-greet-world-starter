
import React, { createContext, useContext, useState, ReactNode } from 'react'

interface ModalContextType {
  showAlert: (message: string, title?: string) => Promise<void>
  showConfirm: (message: string, title?: string) => Promise<boolean>
}

const ModalContext = createContext<ModalContextType | undefined>(undefined)

export const useModal = () => {
  const context = useContext(ModalContext)
  if (!context) {
    throw new Error('useModal must be used within a ModalProvider')
  }
  return context
}

interface ModalProviderProps {
  children: ReactNode
}

export const ModalProvider: React.FC<ModalProviderProps> = ({ children }) => {
  const [alertModal, setAlertModal] = useState<{
    isOpen: boolean
    message: string
    title: string
    resolve?: () => void
  }>({
    isOpen: false,
    message: '',
    title: ''
  })

  const [confirmModal, setConfirmModal] = useState<{
    isOpen: boolean
    message: string
    title: string
    resolve?: (result: boolean) => void
  }>({
    isOpen: false,
    message: '',
    title: ''
  })

  const showAlert = (message: string, title: string = 'Avviso'): Promise<void> => {
    return new Promise((resolve) => {
      setAlertModal({
        isOpen: true,
        message,
        title,
        resolve
      })
    })
  }

  const showConfirm = (message: string, title: string = 'Conferma'): Promise<boolean> => {
    return new Promise((resolve) => {
      setConfirmModal({
        isOpen: true,
        message,
        title,
        resolve
      })
    })
  }

  const handleAlertClose = () => {
    if (alertModal.resolve) {
      alertModal.resolve()
    }
    setAlertModal(prev => ({ ...prev, isOpen: false }))
  }

  const handleConfirmClose = (result: boolean) => {
    if (confirmModal.resolve) {
      confirmModal.resolve(result)
    }
    setConfirmModal(prev => ({ ...prev, isOpen: false }))
  }

  return (
    <ModalContext.Provider value={{ showAlert, showConfirm }}>
      {children}
      
      {alertModal.isOpen && (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
          <div className="bg-white rounded-lg p-6 max-w-md w-full mx-4">
            <h2 className="text-xl font-semibold mb-4 text-[#032952]">
              {alertModal.title}
            </h2>
            <p className="mb-6 text-gray-700">
              {alertModal.message}
            </p>
            <div className="flex justify-end">
              <button
                onClick={handleAlertClose}
                className="px-4 py-2 bg-[#032952] text-white rounded hover:bg-[#021e3a] transition-colors"
              >
                OK
              </button>
            </div>
          </div>
        </div>
      )}

      {confirmModal.isOpen && (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
          <div className="bg-white rounded-lg p-6 max-w-md w-full mx-4">
            <h2 className="text-xl font-semibold mb-4 text-[#032952]">
              {confirmModal.title}
            </h2>
            <p className="mb-6 text-gray-700">
              {confirmModal.message}
            </p>
            <div className="flex justify-end gap-3">
              <button
                onClick={() => handleConfirmClose(false)}
                className="px-4 py-2 bg-gray-300 text-gray-700 rounded hover:bg-gray-400 transition-colors"
              >
                Annulla
              </button>
              <button
                onClick={() => handleConfirmClose(true)}
                className="px-4 py-2 bg-[#032952] text-white rounded hover:bg-[#021e3a] transition-colors"
              >
                Conferma
              </button>
            </div>
          </div>
        </div>
      )}
    </ModalContext.Provider>
  )
}
