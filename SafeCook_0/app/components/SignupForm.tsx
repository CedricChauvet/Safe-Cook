import React, { useState, useEffect } from 'react';
import {
    View,
    Text,
    TextInput,
    Button,
    StyleSheet,
    Alert,
  } from 'react-native';
import AsyncStorage from '@react-native-async-storage/async-storage';

interface SignupFormProps {
  handleSignup: (allergies: string[]) => void;
}

const SignupForm: React.FC<SignupFormProps> = ({ handleSignup }) => {


  const onSignupPress = () => {
    handleSignup(allergies.split(',').map(allergy => allergy.trim()));
  };

  const [name, setName] = useState<string>('');
  const [email, setEmail] = useState<string>('');
  {/*const [password, setPassword] = useState<string>('');*/} // Ne pas afficher pour  le moment
  const [allergies, setAllergies] = useState<string>(''); // Nouvel état pour les allergies

  useEffect(() => {
    const loadSignupData = async () => {
      try {
        const storedName = await AsyncStorage.getItem('@username');
        const storedEmail = await AsyncStorage.getItem('@email');
        {/*const storedPassword = await AsyncStorage.getItem('@password');*/}
        const storedAllergies = await AsyncStorage.getItem('@allergies');

        if (storedName) setName(storedName);
        if (storedEmail) setEmail(storedEmail);
        {/*if (storedPassword) setPassword(storedPassword);*/}
        if (storedAllergies) setAllergies(storedAllergies);
      } catch (e) {
        console.error(e);
      }
    };

    loadSignupData();
  }, []);

    const handleSignupInternal = async () => {
      if (!name || !email ) {
        Alert.alert('Erreur', 'Tous les champs sont obligatoires');
        return;
      }

    try {
      await AsyncStorage.setItem('@username', name);
      await AsyncStorage.setItem('@email', email);
      {/*await AsyncStorage.setItem('@password', password);*/}
      await AsyncStorage.setItem('@allergies', allergies); // Enregistrer les allergies
      Alert.alert('Succès', `Bienvenue ${name}!`);
    } catch (e) {
      console.error(e);
      Alert.alert('Erreur', 'Échec de l\'enregistrement des données');
    }
  };



  return (
    <View style={styles.container}>
      <Text style={styles.title}>Inscription</Text>
      <TextInput
        style={styles.input}
        placeholder="Nom"
        value={name}
        onChangeText={setName}
        placeholderTextColor="black"
      />
      <TextInput
        style={styles.input}
        placeholder="Email"
        value={email}
        onChangeText={setEmail}
        placeholderTextColor="black"
        keyboardType="email-address"
      />
      {/*<TextInput
        style={styles.input}
        placeholder="Mot de passe"
        value={password}
        onChangeText={setPassword}
        placeholderTextColor="#FFFFFF"
        secureTextEntry
      />*/}
      <TextInput
        style={styles.input}
        placeholder="Allergies alimentaires"
        value={allergies}
        onChangeText={setAllergies}
        placeholderTextColor="black"
      />
      <Button title="S'inscrire" onPress={handleSignupInternal} />
      <View style={styles.dataContainer}>
        <Text style={styles.dataText}>Nom: {name}</Text>
        <Text style={styles.dataText}>Email: {email}</Text>
        <Text style={styles.dataText}>Allergies: {allergies}</Text>
      </View>
    </View>
  );
};

const styles = StyleSheet.create({
  container: {
    flex: 1,
    justifyContent: 'center',
    padding: 20,
    backgroundColor: 'white', // Couleur de fond pour visualisation
  },
  title: {
    fontSize: 40,
    color: 'black',
    marginBottom: 20,
    textAlign: 'center',
  },
  input: {
    height: 80,
    borderColor: 'black',
    borderWidth: 1,
    marginBottom: 12,
    paddingHorizontal: 10,
  },
  dataContainer: {
    marginTop: 20,
  },
  dataText: {
    fontSize: 16,
    color: 'black',
  },
});

export default SignupForm;
