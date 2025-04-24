import React, { useState } from 'react';
import { Text, View, StyleSheet, Image, TouchableOpacity } from 'react-native';
import { useRouter } from 'expo-router';
import { MaterialCommunityIcons } from '@expo/vector-icons';
import BottomNavBar from './components/BottomNavBar'; // Importer la barre de navigation
import AllergiesModal from './AllergiesModal'; // Importer le modal des préférences
import { AllergiesProvider } from './contexts/AllergiesContext'; // Assure-toi que le chemin est correct
import recettes from './data/demo-day.json'; 

// Définir le composant MainContent à l'intérieur du même fichier
export default function Index() {
  const router = useRouter();
  const [modalVisible, setModalVisible] = useState(false);
  return (
    <AllergiesProvider>
    <View style={styles.container}>
      {/* Section utilisateur (icône de compte) */}
      <TouchableOpacity
        style={styles.iconAccount}
        onPress={() => setModalVisible(true)}
      >
        <MaterialCommunityIcons name="account" size={70} color="black" />
      </TouchableOpacity>

      {/* Modal des allergies */}
      <AllergiesModal
        visible={modalVisible}
        onClose={() => setModalVisible(false)}
        title="Mes habitudes alimentaires">
      </AllergiesModal>
      
      {/* Titre de l'application */}
      <View>
        <Text style={styles.title}>SafeCook</Text>
      </View>

      {/* Image de l'application */}
      <Image
        style={styles.tinyLogo}
        source={require('../assets/images/garcon-safecook.png')}
      />
      
      <TouchableOpacity
        style={styles.button}
        onPress={() => router.push({
            pathname: 'recipes-V2',
            params: { recettes: JSON.stringify(recettes) }
          })}>
        <MaterialCommunityIcons name="food-variant" size={70} color="black" />
        <Text>Toutes les recettes</Text>
      </TouchableOpacity>
      
      {/* Composant de barre de navigation */}
      <BottomNavBar />
    </View>
    </AllergiesProvider>
  );
};

// Le composant principal qui enveloppe MainContent avec le provider

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
}});