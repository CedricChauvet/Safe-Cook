import React from 'react';
import { Stack } from "expo-router";
import { AppBar, IconButton } from "@react-native-material/core";
import Icon from 'react-native-vector-icons/MaterialCommunityIcons';
import { View, Text } from 'react-native';
import { useRouter } from 'expo-router';

export default function RootLayout() {
  const router = useRouter(); // Add this line

  return (
    <>
      <Stack screenOptions={{ headerShown: false }}/>
      <AppBar
      title="Menu"
      style={{ backgroundColor: 'green' }}
      trailing={
        <View style={{ flex: 1, flexDirection: 'row', justifyContent: 'center', alignItems: 'center' }}>
        <IconButton
          icon={<Icon name="camera" size={30} color="white" />}
          onPress={() => router.push('/photos')}
        />
        <IconButton
          icon={<Icon name="book" size={30} color="white" />}
          onPress={() => router.push('/recette1')}
        />
        <IconButton
          icon={<Icon name="heart" size={30} color="white" />}
          onPress={() => console.log('Favoris')}
        />
        </View>
      }
      />
    </>
  );
}
