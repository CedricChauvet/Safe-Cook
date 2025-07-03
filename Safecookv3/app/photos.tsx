import { CameraType, CameraView, useCameraPermissions } from 'expo-camera';
import { useRouter } from 'expo-router';
import React, { useRef, useState } from 'react';
import {
  ActivityIndicator,
  Alert,
  Button,
  StyleSheet,
  Text,
  TouchableOpacity,
  View,
} from 'react-native';

import BottomNavBar from './components/BottomNavBar';
import { useAllergies } from './contexts/AllergiesContext';
import { useAuth } from './contexts/AuthContext';
import { setLatestRecipes } from './tempData';

/**
 * Écran principal pour prendre une photo et détecter des éléments
 * en fonction des allergies renseignées par l'utilisateur.
 */
export default function PhotosPage() {
  const router = useRouter();
  const [facing, setFacing] = useState<CameraType>('back');
  const [permission, requestPermission] = useCameraPermissions();
  const [isUploading, setIsUploading] = useState(false);
  const cameraRef = useRef<any>(null);
  const { allergies } = useAllergies();
  const { user } = useAuth();

  if (!permission) return <View />;

  if (!permission.granted) {
    return (
      <View style={styles.container}>
        <Text style={styles.message}>We need your permission to show the camera</Text>
        <Button onPress={requestPermission} title="Grant permission" />
      </View>
    );
  }

  const prepareFormData = (fileUri: string, imageType: string) => {
    const formData = new FormData();
    const activeAllergies = Object.keys(allergies).filter(key => allergies[key]);

    formData.append('photo', {
      uri: fileUri,
      type: `image/${imageType}`,
      name: `photo.${imageType}`,
    });

    formData.append('allergies', JSON.stringify(activeAllergies));

    // Récupération dynamique du userId
    const userId = user?.id;
    console.log('🟢 User ID used for upload:', userId);

    if (!userId) {
      Alert.alert('Erreur', 'Utilisateur non connecté. Veuillez vous connecter.');
      throw new Error('Utilisateur non connecté');
    }

    formData.append('user_id', userId.toString());

    return { formData, activeAllergies };
  };

  const formatDetectionMessage = (data: any, allergies: string[]): string => {
    return (
      'Classes : ' + data.classes.join(', ') + '\n\n' +
      'Comptage :\n' +
      Object.entries(data.class_counts)
        .map(([label, count]) => `${label}: ${count}`)
        .join('\n') + '\n\n' +
      'Fichier : ' + data.filename + '\n\n' +
      'Allergies actives : ' + (allergies.length > 0 ? allergies.join(', ') : 'Aucune')
    );
  };

const uploadPhoto = async (fileUri: string, allergies: Allergies, imageType = 'jpg') => {
  if (!fileUri) throw new Error('URI de photo manquant');
  setIsUploading(true);

  const activeAllergies = Object.keys(allergies).filter(key => allergies[key]);

  const formData = new FormData();
  formData.append('photo', {
    uri: fileUri,
    type: `image/${imageType}`,
    name: `photo.${imageType}`,
  });
  formData.append('allergies', JSON.stringify(activeAllergies));
  formData.append('user_id', '123456'); // à adapter dynamiquement

  try {
    const response = await fetch('http://192.168.1.192:5000/detect', {
      method: 'POST',
      body: formData,
    });

    if (!response.ok) {
      console.error(await response.text());
      throw new Error(`Erreur serveur: ${response.status}`);
    }

    const data = await response.json();
    Alert.alert('Résultats de détection', formatDetectionMessage(data, activeAllergies));
    return data;

  } catch (error) {
    console.error('Erreur lors de l\'upload :', error);
    throw new Error('Erreur lors de l\'envoi de l\'image');

  } finally {
    setIsUploading(false);
  }
};





const takePicture = async () => {
  if (!cameraRef.current) return;

  try {
    const photo = await cameraRef.current.takePictureAsync({
      quality: 1,
      base64: false,
      exif: false,
      imageType: 'jpg',
    });

    const data = await uploadPhoto(photo.uri, allergies, 'jpg');
    setLatestRecipes(data.to_json);

    setTimeout(() => {
      router.push('recipes-V2');
    });

  } catch (error) {
    console.error('Erreur lors de la prise de photo :', error);
    throw new Error('Erreur lors de la prise de photo');
  }
};

  return (
    <View style={styles.container}>
      <CameraView style={styles.camera} ref={cameraRef} type={facing}>
        <View style={styles.buttonContainer}>
          <TouchableOpacity style={styles.button} onPress={takePicture} disabled={isUploading}>
            {isUploading
              ? <ActivityIndicator size="large" color="#ffffff" />
              : <Text style={styles.text}>snap</Text>}
          </TouchableOpacity>
        </View>
      </CameraView>
      <BottomNavBar />
    </View>
  );
}

const styles = StyleSheet.create({
  container: { flex: 1, justifyContent: 'center' },
  message: { textAlign: 'center', paddingBottom: 10 },
  camera: { flex: 1 },
  buttonContainer: {
    flex: 1,
    flexDirection: 'row',
    backgroundColor: 'transparent',
    margin: 64,
  },
  button: {
    flex: 1,
    alignSelf: 'flex-end',
    alignItems: 'center',
  },
  text: {
    fontSize: 24,
    fontWeight: 'bold',
    color: 'white',
  },
});
