// AllergiesContext.tsx
import React, { createContext, useContext, useState, ReactNode, useEffect } from 'react';
import { useAuth } from './AuthContext';

type Allergies = {
  Gluten: boolean;
  Lactose: boolean;
  Arachides: boolean;
  Végétarien: boolean;
};

type AllergiesContextType = {
  allergies: Allergies;
  toggleAllergie: (nom: keyof Allergies) => void;
  loading: boolean;
};

const AllergiesContext = createContext<AllergiesContextType | undefined>(undefined);

const allergyMap: Record<keyof Allergies, number> = {
  Gluten: 1,
  Lactose: 2,
  Arachides: 3,
  Végétarien: 4,
};

export const AllergiesProvider = ({ children }: { children: ReactNode }) => {
  const { user } = useAuth();
  console.log('🟢 AllergiesProvider user:', user);
  const [allergies, setAllergies] = useState<Allergies>({
    Gluten: false,
    Lactose: false,
    Arachides: false,
    Végétarien: false,
  });
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    if (!user?.id) {
      console.log('🔴 Aucun user.id, fetch allergies ignoré');
      return;
    }

    const fetchAllergies = async () => {
      setLoading(true);
      console.log('🔄 Chargement des allergies pour l’utilisateur :', user.id);

      try {
        const res = await fetch(`http://192.168.1.192:3000/user/${user.id}/allergies`);

        if (!res.ok) {
          console.error('❌ Erreur récupération allergies :', res.status);
          return;
        }

        const data = await res.json();
        console.log('✅ Allergies récupérées :', data);

        const allergiesState: Allergies = {
          Gluten: data.allergyIds.includes(allergyMap.Gluten),
          Lactose: data.allergyIds.includes(allergyMap.Lactose),
          Arachides: data.allergyIds.includes(allergyMap.Arachides),
          Végétarien: data.allergyIds.includes(allergyMap.Végétarien),
        };

        setAllergies(allergiesState);
      } catch (err) {
        console.error('❌ Erreur réseau lors du chargement des allergies :', err);
      } finally {
        setLoading(false);
      }
    };

    fetchAllergies();
  }, [user?.id]);

  const toggleAllergie = async (label: keyof Allergies) => {
    console.log('🔵 toggleAllergie user:', user);
    if (!user?.id) {
      console.warn('⚠️ Tentative de modification sans utilisateur connecté');
      return;
    }

    const allergyId = allergyMap[label];

    // Optimistic update
    setAllergies(prev => ({ ...prev, [label]: !prev[label] }));

    try {
      const response = await fetch('http://192.168.1.192:3000/user/toggle-allergy', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ userId: user.id, allergyId }),
      });

      const data = await response.json();

      if (!response.ok) {
        alert(data.message || 'Erreur lors de la mise à jour des allergies');
        // Revert changement
        setAllergies(prev => ({ ...prev, [label]: !prev[label] }));
      }
    } catch (e) {
      alert('Erreur réseau ou serveur');
      setAllergies(prev => ({ ...prev, [label]: !prev[label] }));
    }
  };

  return (
    <AllergiesContext.Provider value={{ allergies, toggleAllergie, loading }}>
      {children}
    </AllergiesContext.Provider>
  );
};

export const useAllergies = () => {
  const context = useContext(AllergiesContext);
  if (!context) {
    throw new Error('useAllergies must be used within an AllergiesProvider');
  }
  return context;
};
