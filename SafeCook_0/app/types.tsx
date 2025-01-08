import React from 'react';
import { View, Text, FlatList, StyleSheet } from 'react-native';

// Importez les données JSON
import recettes from './data/recipes_mix1.json';

const Recette = () => {
  return (
    <View style={styles.container}>
      <Text style={styles.header}>Liste des Types</Text>
    </View>
  );
};

const styles = StyleSheet.create({
  container: {
    flex: 1,
    padding: 16,
    backgroundColor: '#fff',
  },
  header: {
    fontSize: 24,
    fontWeight: 'bold',
    marginBottom: 16,
  },
  card: {
    marginBottom: 16,
    padding: 16,
    borderRadius: 8,
    backgroundColor: '#f8f9fa',
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
  },
  subtitle: {
    fontSize: 16,
    fontWeight: '600',
    marginTop: 8,
  },
  text: {
    fontSize: 14,
    marginTop: 4,
  },
});

export default Recette;
