import React from 'react';
import { Text, View } from "react-native";
import { Button } from 'react-native-paper';

export default function Index() {
  return (
    <View
      style={{
        flex: 1,
        justifyContent: "space-between", // Distribue l'espace entre les sections
        alignItems: "center",
        paddingVertical: 60, // Ajoute de l'espace vertical
      }}
    >
      {/* Texte et bouton centré */}
      <View>
        <Text style={{ fontSize: 60, color: 'green', fontWeight: 'bold' }}>SafeCook</Text>
        <View
          style={{
            flex: 1,
            justifyContent: "center",
          }}
        >
          <Button
            mode="contained"
            onPress={() => console.log('Bouton cliqué')}
            buttonColor="green"
            labelStyle={{ color: 'white', fontWeight: 'bold' }}
          >
            Acceuil
          </Button>
        </View>
      </View>

      {/* Trois boutons alignés en bas */}
      <View
        style={{
          flexDirection: "row",       // Aligne les boutons horizontalement
          justifyContent: "center", // Espace égal entre les boutons
          width: "100%",              // Prend toute la largeur de l'écran
          marginBottom: 30,             // Remonte les boutons
        }}
      >
        <Button
          mode="contained"
          onPress={() => console.log('Bouton 1 cliqué')}
          buttonColor="green"
          labelStyle={{ color: 'white' }}
        >
          Photos
        </Button>
        <Button
          mode="contained"
          onPress={() => console.log('Bouton 2 cliqué')}
          buttonColor="green"
          labelStyle={{ color: 'white' }}
        >
          Recettes
        </Button>
        <Button
          mode="contained"
          onPress={() => console.log('Bouton 3 cliqué')}
          buttonColor="green"
          labelStyle={{ color: 'white' }}
        >
          coeur
        </Button>
      </View>
    </View>
  );
}
