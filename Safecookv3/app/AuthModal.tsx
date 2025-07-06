 
// AuthModal.tsx
import React, { useState } from 'react';
import { Button, Modal, StyleSheet, Text, TextInput, TouchableOpacity, View } from 'react-native';
import AsyncStorage from '@react-native-async-storage/async-storage';
import { useAuth } from './contexts/AuthContext'; 


type Props = {
  visible: boolean;
  onClose: () => void;
  onLoginSuccess: (email: string) => void;
};
export default function AuthModal({ visible, onClose, onLoginSuccess }: Props)
 {
  const [isSignUp, setIsSignUp] = useState(false);
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [showRgpdConsent, setShowRgpdConsent] = useState(false);
  const [hasConsented, setHasConsented] = useState(false);
  const { setUser } = useAuth();


const toggleForm = () => {
  if (!isSignUp) {
    // Si on passe de "login" à "signup", montrer d'abord le consentement
    setShowRgpdConsent(true);
  } else {
    setIsSignUp(false);
  }
};
const handleAuth = async () => {
  const endpoint = isSignUp
    ? 'https://backend-service-981813095604.europe-west1.run.app/auth/signup'
    : 'https://backend-service-981813095604.europe-west1.run.app/auth/signin';

  try {
    const response = await fetch(endpoint, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ email, password }),
    });

    const data = await response.json();

    if (!response.ok) {
      alert(data.message || 'Erreur de connexion');
      return;
    }

    console.log('✅ Auth OK :', data);
    alert(data.message);

    // Ici on adapte avec userId au lieu de user
    setUser({ id: data.userId, email });

    await AsyncStorage.setItem('user', JSON.stringify({ id: data.userId, email }));

    onLoginSuccess(email);

    // (optionnel) Stockage local
    await AsyncStorage.setItem('userEmail', email);

    onClose();
  } catch (error) {
    console.error('❌ Auth error:', error);
    alert('Erreur de réseau ou serveur.');
  }
};


return (
  <Modal visible={visible} animationType="slide" transparent={true}>
    <View style={styles.modalBackground}>
      <View style={styles.modalContent}>
        {showRgpdConsent ? (
          <>
      <Text style={styles.title}>Consentement RGPD</Text>
    <View style={{ marginBottom: 20 }}>
      <Text>Avant de créer un compte, veuillez prendre connaissance de notre politique de confidentialité :</Text>
      <View style={styles.bulletPoint}>
        <Text style={styles.bullet}>{'\u2022'}</Text>
        <Text style={styles.bulletText}>Nous stockons votre adresse email afin de gérer votre compte.</Text>
      </View>
      <View style={styles.bulletPoint}>
        <Text style={styles.bullet}>{'\u2022'}</Text>
        <Text style={styles.bulletText}>Les photos que vous prenez avec l’application sont également stockées. L'intention etant de collecter des données pour le modèle</Text>
      </View>
      <View style={styles.bulletPoint}>
        <Text style={styles.bullet}>{'\u2022'}</Text>
        <Text style={styles.bulletText}>
          <Text style={{ fontWeight: 'bold' }}>
            Nous ne collectons ni ne stockons les métadonnées associées à ces photos
          </Text>{' '}
          (telles que la localisation, la date, l’appareil, etc.).
        </Text>
      </View>
    </View>
            <Button
              title="J’accepte"
              onPress={() => {
                setHasConsented(true);
                setShowRgpdConsent(false);
                setIsSignUp(true);
              }}
            />
            <TouchableOpacity onPress={() => setShowRgpdConsent(false)}>
              <Text style={{ color: 'red', marginTop: 15, textAlign: 'center' }}>Annuler</Text>
            </TouchableOpacity>
          </>
        ) : (
          <>
            <Text style={styles.title}>{isSignUp ? 'Inscription' : 'Connexion'}</Text>
            <TextInput
              placeholder="Email"
              value={email}
              onChangeText={setEmail}
              style={styles.input}
            />
            <TextInput
              placeholder="Mot de passe"
              value={password}
              onChangeText={setPassword}
              secureTextEntry
              style={styles.input}
            />
            <Button title={isSignUp ? 'Créer un compte' : 'Se connecter'} onPress={handleAuth} />
            <TouchableOpacity onPress={toggleForm}>
              <Text style={styles.toggleText}>
                {isSignUp ? 'Déjà inscrit ? Se connecter' : 'Pas encore de compte ? S’inscrire'}
              </Text>
            </TouchableOpacity>
            <Button title="Fermer" onPress={onClose} />
          </>
        )}
      </View>
    </View>
  </Modal>
);
}

const styles = StyleSheet.create({
  modalBackground: {
    flex: 1,
    backgroundColor: 'rgba(0,0,0,0.3)',
    justifyContent: 'center',    // centre verticalement
    alignItems: 'center',        // centre horizontalement
  },
  modalContent: {
    backgroundColor: '#fff',
    padding: 30,
    borderRadius: 15,
    width: '85%',
    maxWidth: 400,
    alignItems: 'center',
    justifyContent: 'center',
    shadowColor: '#000',
    shadowOpacity: 0.25,
    shadowRadius: 5,
    elevation: 5,
  },
  title: {
    fontSize: 24,
    fontWeight: 'bold',
    marginBottom: 20,
    textAlign: 'center',
  },
  input: {
    borderBottomWidth: 1,
    marginBottom: 15,
    padding: 8,
    width: '100%',               // pour que les inputs prennent toute la largeur dispo
  },
  toggleText: {
    marginTop: 10,
    color: 'blue',
    textAlign: 'center',
  },
  bulletPoint: {
  flexDirection: 'row',
  alignItems: 'flex-start',
  marginVertical: 4,
  // width: '100%', // optionnel si tu veux forcer la largeur complète
},
bullet: {
  fontSize: 18,
  lineHeight: 22,
  marginRight: 8,
  width: 20, // fixe la largeur pour éviter que la puce bouge
},
bulletText: {
  flex: 1,
  fontSize: 14,
  lineHeight: 20,
},
});


