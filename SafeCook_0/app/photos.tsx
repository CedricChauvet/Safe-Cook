import React from 'react';
import { View, Text, StyleSheet, TouchableOpacity } from 'react-native';
import { Button } from 'react-native-paper';
import { useRouter } from 'expo-router';
import Icon from 'react-native-vector-icons/MaterialCommunityIcons';

export default function PhotosPage() {
  const router = useRouter();


  return (
    <View style={styles.container}>
       <TouchableOpacity style={styles.iconButtonContent} onPress={() => console.log('photos cliquées')}>
        <Icon name="camera" size={50} color="green" />
      </TouchableOpacity>
    </View>
  );
}

const styles = StyleSheet.create({
    container: {
      flex: 1,
      justifyContent: "space-between",
      alignItems: "center",
      paddingVertical: 60,
      backgroundColor: '#f5f5f5',
    },

    buttonLabel: {
        color: 'white',
        fontWeight: 'bold',
        fontSize: 180, // Taille de la police augmentée
        height: 180
      },
      iconButtonContent: {
        height: 300,
        flexDirection: 'row',
        alignItems: 'center',
        padding: 10, // Padding ajouté pour agrandir le bouton
      },

}
)