import React from 'react';
import { View, Text, StyleSheet } from 'react-native';
import { Button } from 'react-native-paper';
import { useRouter } from 'expo-router';
import Icon from 'react-native-vector-icons/MaterialCommunityIcons';

export default function PhotosPage() {
  const router = useRouter();


  return (
    <View style={styles.container}>
        <Button
                    mode="contained"
                    onPress={() => console.log('Favoris cliqué')}
                    buttonColor="green"
                    labelStyle={styles.buttonLabel}
                    contentStyle={styles.iconButtonContent}
                  >
                    <Icon name="photo" size={20} color="white" />
                  </Button>
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
      },
      iconButtonContent: {
        flexDirection: 'row',
        alignItems: 'center',
      },
}
)