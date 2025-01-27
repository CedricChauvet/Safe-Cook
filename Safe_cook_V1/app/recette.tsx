import { useLocalSearchParams } from 'expo-router';
import { View, Text, FlatList, StyleSheet, Image} from 'react-native';
import { Picker } from '@react-native-picker/picker';
import React, { useState } from 'react';




const Recette = () => {
  // Importez les données JSON
  const { recette } = useLocalSearchParams();
  const [selectedIngredient, setSelectedIngredient] = useState('');

  let recettes = [];

  if (typeof recette === 'string') {
    recettes = JSON.parse(recette);
  } else if (Array.isArray(recette)) {
    recettes = recette.map(r => JSON.parse(r));
  }

  const item = recettes[0]; // Assuming you want to use the first recipe
  const [selectedInstruction, setSelectedInstruction] = useState(item.steps[0]);

  return (
    <View style={styles.container}>
      <Text style={styles.header}>Liste des Recettes</Text>
      <FlatList
        data={recettes}
        keyExtractor={(item) => item._id.toString()}
        renderItem={({ item }) => (
          <View style={styles.card} key={item._id.toString()}>
            <Text style={styles.title}>{item.title}</Text>

            {/* Informations générales */}
            {/*<Text style={styles.text}>Note : {item.rating} ⭐</Text>*/}
            {/*<Text style={styles.text}>
              Avis : {item.review_count >= 0 ? item.review_count : 'Aucun avis'}
            </Text>*/}
            <Text style={styles.text}>Temps de préparation : {item.prep_time}</Text>
            {/*<Text style={styles.text}>Difficulté : {item.difficulty}</Text>*/}
            {/*<Text style={styles.text}>Coût : {item.cost}</Text>*/}
            <Text style={styles.text}>Portions : {item.servings}</Text>

                <Image
                  style={styles.photo}
                  source={{uri: item.photo}}
                  resizeMode='cover'
                  onError={(error) => console.log("Erreur lors du chargement de l'image", error)}
                />

            {/* Liste des Ingrédients */}
            <Text style={styles.subtitle}>Ingrédients:</Text>
            <Picker
            selectedValue={selectedIngredient}
            onValueChange={(itemValue) => setSelectedIngredient(itemValue)}
          >
            {item.ingredients.map((ingredient: string, index: number) => (
              <Picker.Item key={index} label={ingredient} value={ingredient} />
            ))}
          </Picker>

            {/* Instructions */}
            <Text style={styles.subtitle}>Instructions:</Text>
            <Picker
              selectedValue={selectedInstruction}
              onValueChange={(itemValue) => setSelectedInstruction(itemValue)}
            >
              {item.steps.map((step: string, index: number) => (
                <Picker.Item key={index} label={step} value={step} />
              ))}
            </Picker>
          </View>
        )}
      />
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
  photo: {
    width: '100%',
    height: 200,
    marginBottom: 16,
  },
});

export default Recette;