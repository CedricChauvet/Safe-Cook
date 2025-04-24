// App.tsx ou le composant parent approprié
import React from 'react';
import { View } from 'react-native';
import { AllergiesProvider } from './contexts/AllergiesContext';
import HalfScreenModal from './AllergiesModal'; // importer les preference
// Importez d'autres composants selon vos besoins

const App = () => {
  const [modalVisible, setModalVisible] = React.useState(false);

  return (
    <AllergiesProvider>
      <View style={{ flex: 1 }}>
        {/* Votre contenu d'application */}
        
        {/* Exemple d'utilisation du modal */}
        <HalfScreenModal
          visible={modalVisible}
          onClose={() => setModalVisible(false)}
          title="Préférences alimentaires"
          toggleallergie1="Gluten"
          toggleallergie2="Lactose"
          toggleallergie3="Arachide"
          toggleVegetarien="Végétarien"
        />
        
        {/* Bouton pour ouvrir le modal, etc. */}
      </View>
    </AllergiesProvider>
  );
};

export default App;