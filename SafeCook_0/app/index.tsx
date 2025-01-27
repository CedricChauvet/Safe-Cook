import React, { useEffect } from 'react';
import { Text, View, StyleSheet, TouchableOpacity, Image} from "react-native";
import { Button } from 'react-native-paper';
import { useRouter } from 'expo-router';
import Icon from 'react-native-vector-icons/MaterialCommunityIcons';
import AsyncStorage from '@react-native-async-storage/async-storage';
import veganMixJson from './data/vegan_mix/0safe-cook.vegan_mix.json';
import sanshuileMixJson from './data/sans_huile_mix/0safe-cook.sans_huile_mix.json';

import { AppRegistry } from 'react-native';
import SignupScreen from './screens/SignupScreen';
import appJson from '../app.json';  // Importation de tout le fichier

const safecook = appJson.expo.name;  // Extraction du 'name' depuis 'expo'


AppRegistry.registerComponent(safecook, () => SignupScreen);

export default function Index() {
  const router = useRouter();

  useEffect(() => {
    // Function to store data
    const storeData = async (value: string) => {
      try {
        await AsyncStorage.setItem('@storage_Key', value);
      } catch (e) {
        // saving error
        console.error(e);
      }
    };

    // Function to retrieve data
    const getData = async () => {
      try {
        const value = await AsyncStorage.getItem('@storage_Key');
        if (value !== null) {
          // value previously stored
          console.log(value);
        }
      } catch (e) {
        // error reading value
        console.error(e);
      }
    };

    // Example usage
    storeData('some value');
    getData();
  }, []);

  return (

    <View style={styles.container}>

      // SignupScreen

      {/* Header Section */}
      <View style={styles.header}>
      <Text style={styles.title}>SafeCook</Text>
      <Image
          source={require('../assets/images/Logo_SafeCook.png')} // Mettez le chemin correct de votre image ici
          style={styles.logo}
        />
        <TouchableOpacity style={styles.signupButton} onPress={() => router.push('./screens/SignupScreen')}>
          <Text style={styles.signupButtonText}>S'inscrire</Text>
        </TouchableOpacity>

      </View>

      {/* Main Buttons Section */}
      <View style={styles.buttonGroup}>
          <View style={styles.row}>
          <View style={styles.container}>
                 <TouchableOpacity style={styles.iconButtonContent} onPress={() => router.push({
                      pathname: '/recette', // Assurez-vous que ce chemin correspond à l'emplacement de votre fichier recette.tsx
                      params: { recette: JSON.stringify(sanshuileMixJson) }
                    })}>
                  <Text style={styles.text}>Sans huile Mix</Text>
                </TouchableOpacity>
              </View>
              <View style={styles.container}>
                 <TouchableOpacity style={styles.iconButtonContent} onPress={() =>  router.push({
                      pathname: '/recette', // Assurez-vous que ce chemin correspond à l'emplacement de votre fichier recette.tsx
                      params: { recette: JSON.stringify(veganMixJson) }
                    })}>
                  <Text style={styles.text}>Vegan Mix</Text>
                </TouchableOpacity>
              </View>
        </View>
      </View>
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    justifyContent: "center",
    alignItems: "center",
    paddingVertical: 60,
    backgroundColor: '#f5f5f5',
  },
  header: {
    justifyContent: "center",
    alignItems: "center",
    flex: 1,
  },
  logo: {
    width: 300,
    height: 300,
    marginBottom: 10,
  },
  title: {
    fontSize: 60,
    color: 'green',
    fontWeight: 'bold',
  },
  text: {
    fontSize: 18,
    color: 'white',
    fontWeight: 'bold',
  },
  buttonGroup: {
    width: "100%",
    alignItems: "center",
  },
  row: {
    flexDirection: "row",
    justifyContent: "center",
  },
  buttonLabel: {
    color: 'white',
    fontWeight: 'normal',
    fontSize:10,
  },
  iconButtonContent: {
    borderRadius: 30,
    backgroundColor: 'green',
    flexDirection: 'row',
    alignItems: 'center',
    padding: 20,
    margin: 10,
  },
  signupButton: {
    backgroundColor: 'green', // Couleur de fond du bouton
    padding: 10,
    borderRadius: 60,
    marginTop: 10,
  },
  signupButtonText: {
    color: 'white', // Couleur du texte du bouton
    fontSize: 20,
    fontWeight: 'bold',
  },
});
