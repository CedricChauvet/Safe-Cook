import React from 'react';
import { View, Text, ScrollView } from 'react-native';
import { Button } from 'react-native-paper';
import { useRouter } from 'expo-router';

export default function RecettePage() {
  const router = useRouter();

  const recettes = [
    {
      id: 1,
      nom: 'Poulet rôti',
      description: 'Un délicieux poulet rôti avec des herbes de Provence'
    },
    {
      id: 2,
      nom: 'Salade César',
      description: 'Salade classique avec poulet grillé et croûtons'
    },
    {
      id: 3,
      nom: 'Lasagnes',
      description: 'Lasagnes traditionnelles à la bolognaise'
    }
  ];

  return (
    <View style={{
      flex: 1,
      padding: 20,
      backgroundColor: '#f0f0f0'
    }}>
      <Text style={{
        fontSize: 24,
        fontWeight: 'bold',
        color: 'green',
        textAlign: 'center',
        marginBottom: 20
      }}>
        Nos Recettes
      </Text>

      <ScrollView>
        {recettes.map((recette) => (
          <View
            key={recette.id}
            style={{
              backgroundColor: 'white',
              borderRadius: 10,
              padding: 15,
              marginBottom: 15,
              shadowColor: '#000',
              shadowOffset: { width: 0, height: 2 },
              shadowOpacity: 0.1,
              shadowRadius: 4,
              elevation: 3
            }}
          >
            <Text style={{
              fontSize: 18,
              fontWeight: 'bold',
              color: 'green',
              marginBottom: 10
            }}>
              {recette.nom}
            </Text>
            <Text style={{ color: 'gray' }}>
              {recette.description}
            </Text>
            <Button
              mode="contained"
              onPress={() => console.log(`Détails de ${recette.nom}`)}
              buttonColor="green"
              style={{ marginTop: 10 }}
            >
              Voir la recette
            </Button>
          </View>
        ))}
      </ScrollView>

      <Button
        mode="outlined"
        onPress={() => router.back()}
        style={{
          marginTop: 20,
          borderColor: 'green'
        }}
        labelStyle={{ color: 'green' }}
      >
        Retour
      </Button>
    </View>
  );
}
