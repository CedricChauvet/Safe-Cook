import React from 'react';
import { View, StyleSheet, TouchableOpacity, Alert, Text } from "react-native";
import { useRouter, usePathname } from 'expo-router';
import { MaterialCommunityIcons } from '@expo/vector-icons';
import { setLatestRecipes } from '../tempData'; // Ajustez le chemin selon votre structure


const BottomNavBar = () => {
  const router = useRouter();
  const pathname = usePathname(); 
  

  // Déterminer quelle icône est active
  const isActive = (path: string) => {
    return pathname === path;
  };


  return (
  
            <View style={styles.navContainer}>
        <TouchableOpacity
          style={[styles.iconContainer, isActive('/photos') && styles.activeIcon]}
          onPress={() => router.push('/photos')}
        >
          <MaterialCommunityIcons 
            name="camera" 
            size={24} 
            color={isActive('/photos') ? "#793d1c" : "white"} 
          />
          {/* Exemple de texte dans un bouton */}
          <Text style={styles.iconText}>Camera</Text>
        </TouchableOpacity>
      
        <TouchableOpacity
          style={[styles.iconContainer, isActive('/') && styles.activeIcon]}
          onPress={() => {
            
            router.push('/');  // Naviguer vers la page d'accueil
          }}
        >
          <MaterialCommunityIcons 
            name="home" 
            size={40} 
            color={isActive('/') ? "#793d1c" : "white"} 
          />
          {/* Exemple de texte dans un bouton */}
          <Text style={styles.iconText}>Home</Text>
        </TouchableOpacity>

        <TouchableOpacity
  style={[styles.iconContainer, isActive('/recipes-V2') && styles.activeIcon]}
  onPress={() => {
    // Stocker les données dans tempData

    // Naviguer sans passer de paramètres
    router.push('/recipes-V2');
  }}
  

>
  <MaterialCommunityIcons 
    name="pasta" 
    size={24} 
    color={isActive('/recipes-V2') ? "#793d1c" : "white"} 
  />
  <Text style={styles.iconText}>Recipes</Text>
</TouchableOpacity>
    </View>

  );
};

const styles = StyleSheet.create({
  navContainer: {
    flexDirection: "row",
    justifyContent: "space-around",
    alignItems: "center",
    backgroundColor: '#efd5b0ff',
    borderRadius: 0,
    padding: 15,
    width: "100%",
    marginBottom: 0,
    shadowColor: "#000",
  },
  iconContainer: {
    padding: 10,
    alignItems: 'center',
    justifyContent: 'center',
    borderRadius: 50,
  },
  activeIcon: {
    backgroundColor: 'rgba(255, 255, 255, 0.8)',
    transform: [{ scale: 1.1 }],
  },
  iconText: {
    color: 'white',
    fontSize: 12,
    marginTop: 5,
  }
});

export default BottomNavBar;
