import { CameraView, CameraType, useCameraPermissions } from 'expo-camera';
import { useState, useRef } from 'react';
import { Button, StyleSheet, Text, TouchableOpacity, View, ActivityIndicator } from 'react-native';
import * as ImageManipulator from 'expo-image-manipulator';
import ImageResizer from 'react-native-image-resizer';
import { Alert } from 'react-native';

export default function PhotosPage() {
  const [facing, setFacing] = useState<CameraType>('back');
  const [permission, requestPermission] = useCameraPermissions();
  const [photo, setPhoto] = useState(null);
  const [isUploading, setIsUploading] = useState(false);
  const cameraRef = useRef(null);

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

  async function uploadPhoto(photoUri) {
    try {
  

      console.log(photoUri)
      // Vérifier que l'URI existe
      if (!photoUri) {
        throw new Error('URI de photo manquant');
      }
  
      // Redimensionner et convertir l'image

      console.log('Traitement de l\'image...');

      console.log('Image traitée avec succès');
  
      // console.log('Image traitée avec succès:', {
      //   width: manipResult.width,
      //   height: manipResult.height,
      //   base64Length: manipResult.base64?.length
      // });
  
      // Vérifier que nous avons bien une chaîne base64

  
      setIsUploading(true);
  
      // Envoyer l'image
      console.log(photoUri.substring(0, 100));

      console.log('Envoi de l\'image...');
      const response = await fetch('http://176.139.25.235:5000/detect', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          image: photoUri,
        })
      });
      console.log('Réponse reçue');

      
      if (!response.ok) {
        throw new Error(`Erreur serveur: ${response.status}`);
      }
  
      const data = await response.json();
      //console.log(data);
      // Créer un message formaté avec les détails
      const message = 
        'Classes : ' + data.classes.join(', ') + '\n\n' +
        'Comptage : \n' + 
        Object.entries(data.class_counts)
          .map(([classe, count]) => `${classe}: ${count}`)
          .join('\n') + '\n\n' +
        'Fichier : ' + data.filename;

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
          quality: 0.9, // Slightly reduced to improve compatibility
          base64: true, // Recommended for memory efficiency
          exif: true, // Capture metadata for better image processing
          skipProcessing: false, // Better image handling
          width: 1024, // Optional: limit image dimensions
        });
        
        // Upload automatique après la prise de photo

        console.log('En cours de téléchargement de la photo...');
        await uploadPhoto(photo.base64);
        console.log('Photo téléchargée avec succès');
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