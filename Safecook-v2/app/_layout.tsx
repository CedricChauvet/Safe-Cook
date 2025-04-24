// Dans App.tsx ou à la racine de ton projet
import React from 'react';
import { AllergiesProvider } from './contexts/AllergiesContext'; // Assure-toi du bon chemin
import { Stack } from 'expo-router';

export default function App() {
  return (
    <AllergiesProvider>
      <Stack
        screenOptions={{
          headerShown: false,
          navigationBarHidden: true
        }}
      />
    </AllergiesProvider>
  );
}
