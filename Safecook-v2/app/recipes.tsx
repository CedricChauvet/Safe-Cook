import React from 'react';
import { View, Text, FlatList, StyleSheet, Image } from 'react-native';
import { useLocalSearchParams } from 'expo-router';
import BottomNavBar from './components/BottomNavBar';

const Recipes = () => {
  const params = useLocalSearchParams();
  // Analyser les recettes à partir des paramètres
  const recettesData = params.recettes ? JSON.parse(params.recettes) : [];

  return (
    <View style={styles.container}>
      <Text style={styles.header}>Liste des Recettes</Text>
      <FlatList
        data={recettesData}
        // Utiliser l'index comme clé si _id n'est pas disponible ou n'est pas une chaîne
        keyExtractor={(item, index) => {
          // S'assurer que item._id existe et peut être converti en chaîne
          if (item._id && typeof item._id !== 'object') {
            return item._id.toString();
          }
          // Sinon, utiliser l'index avec un préfixe
          return `recipe-${index}`;
        }}
        renderItem={({ item }) => (
          <View style={styles.card}>
            <Text style={styles.title}>{item.title}</Text>

            {/* Informations générales */}
            <Text style={styles.text}>Note : {item.rating} ⭐</Text>
            <Text style={styles.text}>
              Avis : {item.review_count >= 0 ? item.review_count : 'Aucun avis'}
            </Text>
            <Text style={styles.text}>Temps de préparation : {item.prep_time}</Text>
            <Text style={styles.text}>Difficulté : {item.difficulty}</Text>
            <Text style={styles.text}>Coût : {item.cost}</Text>
            <Text style={styles.text}>Portions : {item.servings}</Text>

            {/* Liste des ingrédients */}
            <Text style={styles.subtitle}>Ingrédients:</Text>
            {item.ingredients && item.ingredients.map((ing, ingIndex) => (
              <Text key={`ing-${ingIndex}`} style={styles.text}>- {ing}</Text>
            ))}

            {/* Instructions */}
            <Text style={styles.subtitle}>Instructions:</Text>
            <Text style={styles.text}>{item.steps ? item.steps.join('\n') : ''}</Text>
            <Image
              style={styles.photo}
              source={{ uri: item.photo }}
              resizeMode='cover'
/>
          </View>
        )}
      />
      <BottomNavBar />
    </View>
  );
};

const styles = StyleSheet.create({
  container: {
    flex: 1,
    padding: 10,
    backgroundColor: '#f3ddbbff',
  },
  header: {
    fontSize: 24,
    fontWeight: 'bold',
    marginBottom: 16,
    marginTop: 10,
    textAlign: 'center',
    color: '#793d1cff',
  },
  card: {
    marginBottom: 16,
    padding: 16,
    borderRadius: 8,
    backgroundColor: '#fffcf7',
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 2 },
    shadowOpacity: 0.2,
    shadowRadius: 2,
    elevation: 2,
  },
  title: {
    fontSize: 20,
    fontWeight: 'bold',
    marginBottom: 8,
    color: '#793d1cff',
  },
  subtitle: {
    fontSize: 16,
    fontWeight: '600',
    marginTop: 8,
    color: '#793d1cff',
  },
  text: {
    fontSize: 14,
    marginTop: 4,
  },
    photo: {
    width: '100%',
    height: 200,
    marginBottom: 0,
  },
});

export default Recipes;