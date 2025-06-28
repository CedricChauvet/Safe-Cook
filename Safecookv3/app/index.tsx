import { MaterialCommunityIcons } from '@expo/vector-icons';
import { useRouter } from 'expo-router';
import React, { useState } from 'react';
import { Image, StyleSheet, Text, TouchableOpacity, View } from 'react-native';


import AllergiesModal from './AllergiesModal';
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

  /** Ouvre le modal des préférences alimentaires */
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
        <TouchableOpacity style={styles.iconAccount} onPress={openAllergyModal}>
          <MaterialCommunityIcons name="account" size={70} color="black" />
        </TouchableOpacity>

        {/* Modal des allergies */}
        <AllergiesModal
          visible={isModalVisible}
          onClose={closeAllergyModal}
          title="Mes habitudes alimentaires"
        />

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
});
