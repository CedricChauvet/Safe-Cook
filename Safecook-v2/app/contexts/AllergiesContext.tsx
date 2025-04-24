import React, { createContext, useContext, useState, useEffect, ReactNode } from 'react';
import AsyncStorage from '@react-native-async-storage/async-storage';

type Allergies = {
  Gluten: boolean;
  Lactose: boolean;
  Arachides: boolean;
  Végétarien: boolean;
};

type AllergiesContextType = {
  allergies: Allergies;
  toggleAllergie: (nom: keyof Allergies) => void;
};

const AllergiesContext = createContext<AllergiesContextType | undefined>(undefined);

export const AllergiesProvider = ({ children }: { children: ReactNode }) => {
  const [allergies, setAllergies] = useState<Allergies>({
    Gluten: false,
    Lactose: false,
    Arachides: false,
    Végétarien: false,
  });

  // Charger les allergies depuis AsyncStorage au démarrage
  useEffect(() => {
    const loadAllergies = async () => {
      try {
        const savedAllergies = await AsyncStorage.getItem('allergies');
        if (savedAllergies) {
          console.log('Allergies chargées depuis AsyncStorage:', JSON.parse(savedAllergies));
          setAllergies(JSON.parse(savedAllergies));
        }
      } catch (error) {
        console.error('Erreur lors du chargement des allergies:', error);
      }
    };
    
    loadAllergies();
  }, []);

  const toggleAllergie = async (nom: keyof Allergies) => {
    try {
      const newAllergies = {
        ...allergies,
        [nom]: !allergies[nom],
      };
      
      setAllergies(newAllergies);
      
      // Sauvegarder les allergies dans AsyncStorage
      await AsyncStorage.setItem('allergies', JSON.stringify(newAllergies));
      console.log('Allergies sauvegardées dans AsyncStorage:', newAllergies);
    } catch (error) {
      console.error('Erreur lors de la sauvegarde des allergies:', error);
    }
  };
  
  return (
    <AllergiesContext.Provider value={{ allergies, toggleAllergie }}>
      {children}
    </AllergiesContext.Provider>
  );
};

// Hook personnalisé pour accéder facilement au contexte
export const useAllergies = () => {
  const context = useContext(AllergiesContext);
  if (!context) {
    throw new Error('useAllergies must be used within an AllergiesProvider');
  }
  return context;
};