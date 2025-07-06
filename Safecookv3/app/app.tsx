// App.tsx
import React from 'react';
import { View, Button } from 'react-native';
import { AllergiesProvider } from './contexts/AllergiesContext';
import AllergiesModal from './AllergiesModal';
import { AuthProvider, useAuth } from './contexts/AuthContext';
import AuthModal from './AuthModal';
const AppContent = () => {
  const [modalVisible, setModalVisible] = React.useState(false);
  const [authModalVisible, setAuthModalVisible] = React.useState(false);
  const { user, loading } = useAuth();

  const openAllergiesModal = () => {
    if (!user) {
      setAuthModalVisible(true);
    } else {
      setModalVisible(true);
    }
  };

  const handleLoginSuccess = (email: string) => {
    setAuthModalVisible(false);
    setModalVisible(true);
  };

  if (loading) {
    return null;
  }

  return (
    <View style={{ flex: 1, justifyContent: 'center', alignItems: 'center' }}>
      <Button title="Modifier mes allergies" onPress={openAllergiesModal} />

      <AllergiesModal
        visible={modalVisible}
        onClose={() => setModalVisible(false)}
        title="Préférences alimentaires"
      />

      <AuthModal
        visible={authModalVisible}
        onClose={() => setAuthModalVisible(false)}
        onLoginSuccess={handleLoginSuccess}
      />
    </View>
  );
};

// ✅ CORRECT ORDER
const App = () => (
  <AuthProvider>
    <AllergiesProvider>
      <AppContent />
    </AllergiesProvider>
  </AuthProvider>
);

export default App;