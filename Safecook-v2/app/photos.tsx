import React from 'react';

import { useRouter } from 'expo-router';
import Icon from 'react-native-vector-icons/MaterialCommunityIcons';
import { CameraView, CameraType, useCameraPermissions } from 'expo-camera';
import { useState, useRef } from 'react';
import { Button, StyleSheet, Text, TouchableOpacity, View, ActivityIndicator } from 'react-native';
import { Alert } from 'react-native';
import { useAllergies } from './contexts/AllergiesContext'; 
import BottomNavBar from './components/BottomNavBar'; // Importer la barre de navigation
import { setLatestRecipes } from './tempData'; //Pour Sauvegarder les données globalement


export default function PhotosPage() {
  const router = useRouter();
  const [facing, setFacing] = useState<CameraType>('back');
  const [permission, requestPermission] = useCameraPermissions();
  const [photo, setPhoto] = useState(null);
  const [isUploading, setIsUploading] = useState(false);
  const cameraRef = useRef(null);

  const { allergies } = useAllergies(); // Utilisation du contexte pour récupérer les allergies
  console.log('État des allergies dans PhotosPage:', allergies);
  if (!permission) {
    return <View />;
  }

  if (!permission.granted) {
    return (
      <View style={styles.container}>
        <Text style={styles.message}>We need your permission to show the camera</Text>
        <Button onPress={requestPermission} title="grant permission" />
      </View>
    );
  }

  async function uploadPhoto(fileUri: string, imageType = 'jpg') {
    try {


      console.log(fileUri)
      // Vérifier que l'URI existe
      if (!fileUri) {
        throw new Error('URI de photo manquant');
  
      }
      const formData = new FormData();
      formData.append('photo', {
        uri: fileUri,
        type: `image/${imageType}`,
        name: `photo.${imageType}`
      });
      
      console.log('Image traitée avec succès');
      console.log('Type de fileUri:', typeof fileUri);
      console.log('URI complet:', fileUri);
      console.log('FormData contenu:', JSON.stringify(formData));
      setIsUploading(true);
      // Créer un objet avec les allergies actives
      const allergiesActives = Object.keys(allergies).filter(key => allergies[key]);
      formData.append('allergies', JSON.stringify(allergiesActives));

      // Envoyer l'image
      console.log(fileUri.substring(0, 100));

      console.log('Envoi de l\'image...');
<<<<<<< HEAD
      const response = await fetch('http://192.168.1.96:5000/detect', {
=======
      const response = await fetch('http://172.18.240.1:5000/detect', {
>>>>>>> e34d36bc427b39ab2e5768c144aa630198056de3
        method: 'POST',
        body: formData,

      });
      console.log('Réponse reçue');


      if (!response.ok) {
        throw new Error(`Erreur serveur: ${response.status}`);
      }

      const data = await response.json();

      // Créer un message formaté avec les détails
      const message =
        'Classes : ' + data.classes.join(', ') + '\n\n' +
        'Comptage : \n' +
        Object.entries(data.class_counts)
          .map(([classe, count]) => `${classe}: ${count}`)
          .join('\n') + '\n\n' +
        'Fichier : ' + data.filename + '\n\n' +
        'Allergies actives : ' + 
        (allergiesActives.length > 0 ? allergiesActives.join(', ') : 'Aucune');

      Alert.alert(
        'Résultats de détection',
        message
      );

      return data;

    } catch (error) {
      // console.error('Erreur détaillée:', error);
      throw new Error('Erreur lors de l\'envoi de l\'image');
    } finally {
      setIsUploading(false);
    }
  }




  async function takePicture() {
    if (cameraRef.current) {
      try {
        const photo = await cameraRef.current.takePictureAsync({
          quality: 1,
          base64: false, // Ne convertit pas en base64
          exif: false,
          imageType: 'jpg',
          
        });
        // Upload automatique après la prise de photo

        console.log('En cours de téléchargement de la photo...');
        const data = await uploadPhoto(photo.uri, 'jpg');
        console.log('Photo téléchargée avec succès');

        setLatestRecipes(data.to_json);
        setTimeout(() => {
          router.push('recipes-V2');  // 2. Navigation
        }); // Petit délai pour s'assurer que les données sont sauvegardées

      } catch (error) {
        // console.error('Error taking picture:', error);
        throw new Error('Erreur lors de la prise de photo');
      }
    }
  }

  return (
    
    <View style={styles.container}>
      <CameraView
        style={styles.camera}
        ref={cameraRef}
        type={facing}
      >
        <View style={styles.buttonContainer}>
          <TouchableOpacity
            style={styles.button}
            onPress={takePicture}
            disabled={isUploading}
          >
            {isUploading ? (
              <ActivityIndicator size="large" color="#ffffff" />
            ) : (
              <Text style={styles.text}>snap</Text>
            )}
          </TouchableOpacity>
        </View>
      </CameraView>
      <BottomNavBar />
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    justifyContent: 'center',
  },
  message: {
    textAlign: 'center',
    paddingBottom: 10,
  },
  camera: {
    flex: 1,
  },
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