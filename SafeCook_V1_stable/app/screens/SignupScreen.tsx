import React, { useEffect, useState } from 'react';
import { SafeAreaView, StyleSheet, Alert } from 'react-native';
import AsyncStorage from '@react-native-async-storage/async-storage';
import SignupForm from '../components/SignupForm';

const SignupScreen: React.FC = () => {
  const [allergies, setAllergies] = useState<string[]>([]);


  useEffect(() => {
    const checkUser = async () => {
      try {
        const username = await AsyncStorage.getItem('@username');
        {/*const password = await AsyncStorage.getItem('@password');*/}
        if (username ) {
          Alert.alert(`Welcome back, ${username}!`);
        }
      } catch (e) {
        console.error(e);
      }
    };

    checkUser();
  }, []);

  const handleSignup = (allergies: string[]) => {
    setAllergies(allergies);
    // Vous pouvez également enregistrer les allergies dans AsyncStorage si nécessaire
    AsyncStorage.setItem('@allergies', JSON.stringify(allergies));

  };

  return (
    <SafeAreaView style={styles.container}>
      <SignupForm handleSignup={handleSignup} />
    </SafeAreaView>
  );
};

const styles = StyleSheet.create({
  container: {
    flex: 1,
    justifyContent: 'center',
    backgroundColor: '#fff', // Ajoutez une couleur de fond pour mieux voir
  },
});

export default SignupScreen;
