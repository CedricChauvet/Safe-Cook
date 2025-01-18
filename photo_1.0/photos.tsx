// Import des dépendances nécessaires
import { CameraView, CameraType, useCameraPermissions } from 'expo-camera';
import { useState, useRef } from 'react';
import { Button, StyleSheet, Text, TouchableOpacity, View, ActivityIndicator } from 'react-native';
// Ces imports ne sont pas utilisés, ils peuvent être supprimés
import * as ImageManipulator from 'expo-image-manipulator';
import ImageResizer from 'react-native-image-resizer';

export default function PhotosPage() {
  // État pour gérer l'orientation de la caméra (avant/arrière)
  const [facing, setFacing] = useState<CameraType>('back');
  // Gestion des permissions de la caméra avec Expo
  const [permission, requestPermission] = useCameraPermissions();
  // Ces états ne semblent pas être utilisés dans le composant actuel
  const [photo, setPhoto] = useState(null);
  // État pour gérer l'indicateur de chargement
  const [isUploading, setIsUploading] = useState(false);
  // Référence à la caméra pour pouvoir prendre des photos
  const cameraRef = useRef(null);

  // Gestion des permissions de la caméra
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

  // Fonction pour envoyer la photo au serveur
  async function uploadPhoto(photoUri) {
    try {
      if (!photoUri) {
        throw new Error('URI de photo manquant');
      }

      setIsUploading(true);
      
      // Envoi de l'image au serveur
      const response = await fetch('http://176.139.25.235:5000/detect', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          image: 'data:image/jpeg;base64,' + photoUri,
        })
      });

      if (!response.ok) {
        throw new Error(`Erreur serveur: ${response.status}`);
      }

      const data = await response.json();
      
      // Affichage des données reçues en developpement
      console.log(data);
      
      return data;

    } catch (error) {
      throw new Error('Erreur lors de l\'envoi de l\'image');
    } finally {
      setIsUploading(false);
    }
  }

  // Fonction pour prendre une photo
  async function takePicture() {
    if (cameraRef.current) {
      try {
        // Configuration optimisée pour la prise de photo
        const photo = await cameraRef.current.takePictureAsync({
          quality: 0.1,      // Qualité réduite pour optimiser la taille
          base64: true,      // Nécessaire pour l'envoi en base64
          exif: false,       // Pas besoin des données EXIF
          width: 640,        // Dimensions réduites
          height: 640
        });

        await uploadPhoto(photo.base64);
      } catch (error) {
        throw new Error('Erreur lors de la prise de photo');
      }
    }
  }

  // Rendu du composant
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
            disabled={isUploading}  // Désactive le bouton pendant l'upload
          >
            {isUploading ? (
              <ActivityIndicator size="large" color="#ffffff" />
            ) : (
              <Text style={styles.text}>snap</Text>
            )}
          </TouchableOpacity>
        </View>
      </CameraView>
    </View>
  );
}