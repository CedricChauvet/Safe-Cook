import { MaterialCommunityIcons } from '@expo/vector-icons';
import { useRouter } from 'expo-router';
import AsyncStorage from '@react-native-async-storage/async-storage';
import React, { useState } from 'react';
import { Image, StyleSheet, Text, TouchableOpacity, View } from 'react-native';


import AllergiesModal from './AllergiesModal';
import AuthModal from './AuthModal'; // adapte le chemin si nécessaire
import BottomNavBar from './components/BottomNavBar';
import { AllergiesProvider } from './contexts/AllergiesContext';
import recettes from './data/demo-day.json';
import { setLatestRecipes } from './tempData';

/**
 * Composant principal affichant l'accueil de l'application SafeCook.
 * Gère l'accès au modal des préférences alimentaires et à la navigation vers les recettes.
 */
export default function IndexScreen() {
  const router = useRouter();
  const [isModalVisible, setIsModalVisible] = useState(false);
  const [isAuthModalVisible, setAuthModalVisible] = useState(false);
  const [userEmail, setUserEmail] = useState<string | null>(null);
  /** Ouvre le modal des préférences alimentaires */

  const handleLoginSuccess = (email: string) => {
  setUserEmail(email);
  setAuthModalVisible(false); // ferme le modal après succès
};
  const openAllergyModal = () => setIsModalVisible(true);

  /** Ferme le modal des préférences alimentaires */
  const closeAllergyModal = () => setIsModalVisible(false);

  /** Gère la navigation vers l’écran des recettes */
  const handleShowAllRecipes = () => {
    setLatestRecipes(recettes); // Sauvegarde globale
    router.push('recipes-V2');  // Navigation
  };

  return (
    <AllergiesProvider>
      <View style={styles.container}>
        {/* Bouton icône utilisateur */}
            <View style={styles.topRightButtons}>
        <TouchableOpacity style={styles.iconButton} onPress={openAllergyModal}>
          <MaterialCommunityIcons name="food-off" size={40} color="black" />
        </TouchableOpacity>
        <TouchableOpacity style={styles.iconButton} onPress={() => setAuthModalVisible(true)}>
          <MaterialCommunityIcons name="account" size={40} color="black" />
        </TouchableOpacity>
      </View>
        {/* Modal des allergies */}
        <AllergiesModal
          visible={isModalVisible}
          onClose={closeAllergyModal}
          title="Mes habitudes alimentaires"
        />
       <AuthModal
  visible={isAuthModalVisible}
  onClose={() => setAuthModalVisible(false)}
  onLoginSuccess={handleLoginSuccess} // 👈 ajoute ceci
/>
             <Text style={{ marginBottom: 10, fontSize: 16 }}>
          {userEmail ? `Bonjour ${userEmail}` : 'Veuillez vous connecter'}
        </Text>
        

        {/* Titre principal */}
        <Text style={styles.title}>SafeCook</Text>

        {/* Image mascotte */}
        <Image
          style={styles.tinyLogo}
          source={require('../assets/images/garcon-safecook.png')}
        />

        {/* Bouton "Toutes les recettes" */}
        <TouchableOpacity style={styles.button} onPress={handleShowAllRecipes}>
          <MaterialCommunityIcons name="food-variant" size={70} color="black" />
          <Text>Toutes les recettes</Text>
        </TouchableOpacity>

        {/* Barre de navigation en bas */}
        <BottomNavBar />
      </View>
    </AllergiesProvider>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    justifyContent: 'space-between',
    alignItems: 'center',
    paddingVertical: 0,
    backgroundColor: '#f3ddbbff',
  },
  title: {
    fontSize: 40,
    color: '#793d1cff',
    fontWeight: 'bold',
    marginTop: -100,
  },
  iconAccount: {
    alignSelf: 'flex-end',
    marginLeft: 'auto',
  },
  tinyLogo: {
    width: 200,
    height: 200,
    borderRadius: 100,
    backgroundColor: 'green',
  },
  button: {
    backgroundColor: '#f3ddbbff',
    padding: 10,
    borderRadius: 10,
    alignItems: 'center',
  },

  topRightButtons: {
  flexDirection: 'row',         // ← aligne horizontalement
  justifyContent: 'flex-end',   // ← aligne à droite
  width: '100%',                // ← prend toute la largeur en haut
  paddingHorizontal: 10,
  paddingTop: 50,               // ← un peu d’espace avec le haut
  gap: 12,                      // ← espace entre les boutons (React Native >= 0.71)
},

iconButton: {
  padding: 8,
  backgroundColor: '#fff',
  borderRadius: 8,
  elevation: 2,
}
});
