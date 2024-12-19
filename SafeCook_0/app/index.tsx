import React from 'react';
import { Text, View } from "react-native";
import { Button } from 'react-native-paper';
import { useRouter } from 'expo-router';
import Icon from 'react-native-vector-icons/MaterialCommunityIcons'; // Importer l'icône

export default function Index() {
  const router = useRouter();

  return (
    <View
      style={{
        flex: 1,
        justifyContent: "space-between",
        alignItems: "center",
        paddingVertical: 60,
      }}
    >
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
            Accueil
          </Button>
        </View>
      </View>

      <View
        style={{
          flexDirection: "row",
          justifyContent: "center",
          width: "100%",
          marginBottom: 30,
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
          onPress={() => router.push('/recette')}
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
        contentStyle={{ flexDirection: 'row', alignItems: 'center' }} // Aligner l'icône si nécessaire
      >
        <Icon name="heart" size={20} color="white" /> {/* Icône en forme de cœur */}
      </Button>
      </View>
    </View>
  );
}
